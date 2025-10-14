import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import altair as alt
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import calendar
from ai_agent import FinanceAIAgent
import warnings
import os
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="FinAlyze",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    /* Ensure AI insight content is readable */
    .ai-insight {
        background: #ffffff;
        color: #111111;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid rgba(0,0,0,0.08);
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .ai-insight * { color: inherit; }
    .recommendation {
        background: #ffffff;
        color: #111111;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .recommendation strong { color: inherit; }
    .warning { border-left-color: #dc3545; }
    .info { border-left-color: #17a2b8; }
</style>
""", unsafe_allow_html=True)

# Initialize AI Agent
@st.cache_resource
def get_ai_agent():
    return FinanceAIAgent()

ai_agent = get_ai_agent()

# Main header
st.markdown("""
<div class="main-header">
    <h1>FinAlyze</h1>
    <p>Improvised and Complete Financial Data Analysis and Insights</p>
</div>
""", unsafe_allow_html=True)

# Sidebar configuration
st.sidebar.markdown("## 🎛️ Control Panel")

# File upload with multiple format support
uploaded_file = st.sidebar.file_uploader(
    "📂 Upload your Ledger Data",
    type=["html", "csv"],
    help="Upload an activity HTML file or CSV export"
)

# Data processing function
@st.cache_data
def process_data(uploaded_file):
    if uploaded_file is None:
        return None
    
    if uploaded_file.name.endswith('.html'):
        # Parse HTML file
        soup = BeautifulSoup(uploaded_file, "html.parser")
        transactions = []
        
        for entry in soup.find_all("div", class_="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1"):
            text = entry.get_text(separator=" ").strip()
            
            date_match = re.search(r"\w+\s\d{1,2},\s\d{4}", text)
            amount_match = re.search(r"₹[\d,]+(\.\d{1,2})?", text)
            
            if date_match and amount_match:
                transactions.append({
                    "date": pd.to_datetime(date_match.group(), format='mixed'),
                    "amount": float(amount_match.group().replace("₹", "").replace(",", "")),
                    "description": text
                })
        
        df = pd.DataFrame(transactions)
        df["type"] = df["description"].apply(lambda x: "Credit" if "received" in x.lower() else "Debit")
        
    else:  # CSV file
        df = pd.read_csv(uploaded_file)
        # Standardize common column names
        if 'Date' in df.columns and 'date' not in df.columns:
            df['date'] = df['Date']
        if 'Amount' in df.columns and 'amount' not in df.columns:
            df['amount'] = df['Amount']
        if 'Description' in df.columns and 'description' not in df.columns:
            df['description'] = df['Description']
        if 'Type' in df.columns and 'type' not in df.columns:
            df['type'] = df['Type']

        # Create description column if it doesn't exist
        if 'description' not in df.columns:
            # Try to build a description from available columns
            desc_parts = []
            if 'Name' in df.columns:
                desc_parts.append(df['Name'].astype(str))
            if 'Payment Method' in df.columns:
                desc_parts.append('via ' + df['Payment Method'].astype(str))
            if 'Status' in df.columns:
                desc_parts.append('(' + df['Status'].astype(str) + ')')
            
            if desc_parts:
                # Properly concatenate all parts
                df['description'] = desc_parts[0]
                for i in range(1, len(desc_parts)):
                    df['description'] = df['description'] + ' ' + desc_parts[i]
            else:
                df['description'] = 'Transaction'

        # Coerce types
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
        if 'amount' in df.columns:
            df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        
        # Infer type if still missing
        if 'type' not in df.columns:
            if 'Status' in df.columns:
                # Use Status to determine type: Success = Credit, others = Debit
                df['type'] = df['Status'].apply(lambda x: 'Credit' if str(x).lower() == 'success' else 'Debit')
            elif 'description' in df.columns:
                df['type'] = df['description'].apply(lambda x: 'Credit' if 'received' in str(x).lower() else 'Debit')
            else:
                # Default heuristic: mark every 3rd transaction as Credit
                df = df.reset_index(drop=False)
                df['type'] = df['index'].apply(lambda i: 'Credit' if (i % 3 == 0) else 'Debit')
                df = df.drop(columns=['index'])
    
    return df

# Process uploaded data
df = process_data(uploaded_file)

# Use sample data if present in session and no file uploaded
if df is None and 'sample_df' in st.session_state:
    df = st.session_state.sample_df

if df is not None and not df.empty:
    # Enhanced sidebar filters
    st.sidebar.markdown("### 🔍 Advanced Filters")
    
    # Date range filter
    min_date, max_date = df["date"].min(), df["date"].max()
    date_range = st.sidebar.date_input(
        "📅 Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
    # Transaction type filter
    transaction_types = df["type"].unique()
    selected_types = st.sidebar.multiselect(
        "💳 Transaction Types",
        options=transaction_types,
        default=transaction_types
    )
    
    # Amount range filter
    min_amount, max_amount = df["amount"].min(), df["amount"].max()
    amount_range = st.sidebar.slider(
        "💰 Amount Range (₹)",
        min_value=float(min_amount),
        max_value=float(max_amount),
        value=(float(min_amount), float(max_amount)),
        step=100.0
    )
    
    # Search filter
    search_term = st.sidebar.text_input("🔍 Search Transactions", placeholder="Enter keywords...")
    
    # Category filter (if available)
    if 'category' in df.columns:
        categories = df['category'].unique()
        selected_categories = st.sidebar.multiselect(
            "📂 Categories",
            options=categories,
            default=categories
        )
    
    # Apply filters
    filtered_df = df[
        (df["date"].dt.date >= date_range[0]) &
        (df["date"].dt.date <= date_range[1]) &
        (df["type"].isin(selected_types)) &
        (df["amount"] >= amount_range[0]) &
        (df["amount"] <= amount_range[1])
    ]
    
    if search_term:
        if 'description' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["description"].str.contains(search_term, case=False, na=False)]
        else:
            st.sidebar.warning("Search not available - no description column found")
    
    if 'category' in df.columns and selected_categories:
        filtered_df = filtered_df[filtered_df['category'].isin(selected_categories)]
    
    # AI Analysis
    if st.sidebar.button("🤖 Run AI Analysis"):
        with st.spinner("AI is analyzing your financial data..."):
            # Categorize transactions
            categorized_df = ai_agent.categorize_transactions(filtered_df.copy())
            
            # Get insights
            insights = ai_agent.analyze_spending_patterns(categorized_df)
            recommendations = ai_agent.generate_recommendations(insights)
            
            # Store in session state
            st.session_state.ai_insights = insights
            st.session_state.ai_recommendations = recommendations
            st.session_state.categorized_df = categorized_df
    
    # Main content area
    if not filtered_df.empty:
        # Enhanced metrics dashboard
        st.markdown("## 📊 Financial Dashboard")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_spent = filtered_df[filtered_df['type'] == 'Debit']['amount'].sum()
            st.metric("💸 Total Spent", f"₹{total_spent:,.2f}")
        
        with col2:
            total_received = filtered_df[filtered_df['type'] == 'Credit']['amount'].sum()
            st.metric("💰 Total Received", f"₹{total_received:,.2f}")
        
        with col3:
            net_flow = total_received - total_spent
            st.metric("📈 Net Flow", f"₹{net_flow:,.2f}")
        
        with col4:
            avg_transaction = filtered_df['amount'].mean()
            st.metric("📊 Avg Transaction", f"₹{avg_transaction:,.2f}")
        
        # AI Insights Section
        if hasattr(st.session_state, 'ai_insights'):
            st.markdown("## 🤖 AI Insights & Recommendations")
            
            # Display recommendations
            for rec in st.session_state.ai_recommendations:
                rec_class = "warning" if rec['type'] == 'warning' else "info"
                st.markdown(f"""
                <div class="recommendation {rec_class}">
                    <strong>{rec['title']}</strong><br>
                    {rec['message']}
                </div>
                """, unsafe_allow_html=True)
            
            # Category breakdown if available
            if 'top_categories' in st.session_state.ai_insights:
                st.markdown("### 📂 Spending by Category")
                category_data = pd.DataFrame(
                    list(st.session_state.ai_insights['top_categories'].items()),
                    columns=['Category', 'Amount']
                )
                
                fig_category = px.pie(
                    category_data,
                    values='Amount',
                    names='Category',
                    title="Top Spending Categories"
                )
                st.plotly_chart(fig_category, use_container_width=True)
        
        # Enhanced Charts Section
        st.markdown("## 📈 Advanced Analytics")
        
        # Create tabs for different chart types
        tab1, tab2, tab3, tab4 = st.tabs(["📅 Timeline", "📊 Patterns", "🎯 Insights", "📋 Details"])
        
        with tab1:
            # Enhanced timeline chart
            daily_data = filtered_df.groupby("date")["amount"].sum().reset_index()
            
            fig_timeline = go.Figure()
            fig_timeline.add_trace(go.Scatter(
                x=daily_data['date'],
                y=daily_data['amount'],
                mode='lines+markers',
                name='Daily Spending',
                line=dict(color='#667eea', width=2),
                marker=dict(size=6)
            ))
            
            fig_timeline.update_layout(
                title="Daily Transaction Timeline",
                xaxis_title="Date",
                yaxis_title="Amount (₹)",
                hovermode='x unified',
                showlegend=True
            )
            
            st.plotly_chart(fig_timeline, use_container_width=True)
        
        with tab2:
            # Spending patterns analysis
            col1, col2 = st.columns(2)
            
            with col1:
                # Monthly spending pattern
                monthly_data = filtered_df.groupby(filtered_df["date"].dt.to_period("M"))["amount"].sum().reset_index()
                monthly_data["date"] = monthly_data["date"].astype(str)
                
                fig_monthly = px.bar(
                    monthly_data,
                    x="date",
                    y="amount",
                    title="Monthly Spending Pattern",
                    color="amount",
                    color_continuous_scale="viridis"
                )
                st.plotly_chart(fig_monthly, use_container_width=True)
            
            with col2:
                # Transaction type distribution
                type_data = filtered_df.groupby("type")["amount"].sum().reset_index()
                fig_type = px.pie(
                    type_data,
                    values="amount",
                    names="type",
                    title="Credit vs Debit Distribution"
                )
                st.plotly_chart(fig_type, use_container_width=True)
        
        with tab3:
            # Advanced insights
            col1, col2 = st.columns(2)
            
            with col1:
                # Spending heatmap by day of week
                filtered_df['day_of_week'] = filtered_df['date'].dt.day_name()
                filtered_df['hour'] = filtered_df['date'].dt.hour
                
                day_hour_data = filtered_df.groupby(['day_of_week', 'hour'])['amount'].sum().reset_index()
                
                # Create heatmap
                heatmap_data = day_hour_data.pivot(index='day_of_week', columns='hour', values='amount')
                
                fig_heatmap = px.imshow(
                    heatmap_data,
                    title="Spending Heatmap (Day vs Hour)",
                    color_continuous_scale="viridis"
                )
                st.plotly_chart(fig_heatmap, use_container_width=True)
            
            with col2:
                # Top transactions
                st.markdown("### 🏆 Top Transactions")
                # Build column list based on what's available
                top_cols = ['date', 'amount', 'type']
                if 'description' in filtered_df.columns:
                    top_cols.insert(1, 'description')
                top_transactions = filtered_df.nlargest(10, 'amount')[top_cols]
                st.dataframe(top_transactions, use_container_width=True)
        
        with tab4:
            # Detailed transaction table with enhanced features
            st.markdown("### 📋 Transaction Details")
            
            # Add download button
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Filtered Data",
                data=csv,
                file_name="filtered_transactions.csv",
                mime="text/csv"
            )
            
            # Enhanced dataframe display
            st.dataframe(
                filtered_df,
                use_container_width=True,
                column_config={
                    "date": st.column_config.DatetimeColumn("Date", format="DD/MM/YYYY"),
                    "amount": st.column_config.NumberColumn("Amount (₹)", format="₹%.2f"),
                    "type": st.column_config.SelectboxColumn("Type", options=["Credit", "Debit"])
                }
            )
        
        # Budget tracking section
        st.markdown("## 💰 Budget Tracking")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Set budget
            monthly_budget = st.number_input(
                "Set Monthly Budget (₹)",
                min_value=0,
                value=50000,
                step=1000
            )
            
            # Calculate budget status
            current_month = datetime.now().replace(day=1)
            current_month_spending = filtered_df[
                (filtered_df['date'] >= current_month) &
                (filtered_df['type'] == 'Debit')
            ]['amount'].sum()
            
            budget_remaining = monthly_budget - current_month_spending
            budget_percentage = (current_month_spending / monthly_budget) * 100 if monthly_budget > 0 else 0
            
            st.metric("Current Month Spending", f"₹{current_month_spending:,.2f}")
            st.metric("Budget Remaining", f"₹{budget_remaining:,.2f}")
            
            # Budget progress bar
            st.progress(min(budget_percentage / 100, 1.0))
            st.caption(f"{budget_percentage:.1f}% of budget used")
        
        with col2:
            # Budget alerts
            if budget_percentage > 80:
                st.error("⚠️ Warning: You've used over 80% of your monthly budget!")
            elif budget_percentage > 60:
                st.warning("⚠️ Caution: You've used over 60% of your monthly budget.")
            else:
                st.success("✅ Good job! You're well within your budget.")
    
    else:
        st.warning("⚠️ No transactions found with the current filters. Try adjusting your filter criteria.")

else:
    # Welcome screen
    st.markdown("""
    ## 🚀 Welcome to FinAlyze!
    
    ### Features:
    - 🤖 **AI-Powered Insights**: Get intelligent recommendations and spending analysis
    - 📊 **Advanced Analytics**: Comprehensive charts and visualizations
    - 🔍 **Smart Filtering**: Multiple filter options for detailed analysis
    - 💰 **Budget Tracking**: Set and monitor your monthly budget
    - 📈 **Trend Analysis**: Understand your spending patterns over time
    
    ### How to get started:
    1. Upload your ledger data (HTML or CSV), which you can download from: https://takeout.google.com/
    2. Use the filters in the sidebar to analyze specific data
    3. Click "Run AI Analysis" for intelligent insights
    4. Explore different chart types in the Analytics section
    5. Set up budget tracking to monitor your spending
    
    ### Supported file formats:
    - Ledger Activity HTML files
    - CSV exports
    """)
    
    # Sample data option
    if st.button("📊 Load Sample Data (transactions.csv)"):
        try:
            sample_path = os.path.join('data', 'transactions.csv')
            if not os.path.exists(sample_path):
                st.error("Sample file not found at 'data/transactions.csv'.")
            else:
                df_raw = pd.read_csv(sample_path)
                # Map to expected columns
                df_sample = pd.DataFrame()
                # Date
                date_col = 'Date' if 'Date' in df_raw.columns else 'date'
                amount_col = 'Amount' if 'Amount' in df_raw.columns else 'amount'
                df_sample['date'] = pd.to_datetime(df_raw[date_col], errors='coerce')
                df_sample['amount'] = pd.to_numeric(df_raw[amount_col], errors='coerce')
                # Use Description from CSV when available; otherwise build a basic one
                if 'Description' in df_raw.columns:
                    df_sample['description'] = df_raw['Description'].astype(str)
                else:
                    def build_description(row):
                        name = row.get('Name', 'Unknown')
                        method = row.get('Payment Method', row.get('payment_method', 'NA'))
                        status = row.get('Status', row.get('status', ''))
                        return f"{name} via {method} ({status})"
                    df_sample['description'] = df_raw.apply(build_description, axis=1)
                # Derive type
                if 'Type' in df_raw.columns:
                    df_sample['type'] = df_raw['Type'].astype(str).str.title().map(lambda x: 'Credit' if x.startswith('C') else 'Debit')
                elif 'type' in df_raw.columns:
                    df_sample['type'] = df_raw['type'].astype(str).str.title().map(lambda x: 'Credit' if x.startswith('C') else 'Debit')
                else:
                    # Deterministic heuristic to ensure both types exist
                    df_sample = df_sample.reset_index(drop=False)
                    df_sample['type'] = df_sample['index'].apply(lambda i: 'Credit' if (i % 3 == 0) else 'Debit')
                    df_sample = df_sample.drop(columns=['index'])
                # Drop rows with invalid date/amount
                df_sample = df_sample.dropna(subset=['date', 'amount'])
                st.session_state.sample_df = df_sample
                st.success("Sample data loaded from 'data/transactions.csv'!")
                st.rerun()
        except Exception as e:
            st.error(f"Failed to load sample data: {e}")
