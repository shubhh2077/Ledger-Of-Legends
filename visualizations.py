import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import calendar

class FinanceVisualizations:
    def __init__(self):
        self.color_scheme = {
            'primary': '#667eea',
            'secondary': '#764ba2',
            'success': '#28a745',
            'warning': '#ffc107',
            'danger': '#dc3545',
            'info': '#17a2b8'
        }
    
    def create_dashboard_metrics(self, df):
        """Create key performance indicators"""
        metrics = {}
        
        # Basic metrics
        metrics['total_transactions'] = len(df)
        metrics['total_spent'] = df[df['type'] == 'Debit']['amount'].sum()
        metrics['total_received'] = df[df['type'] == 'Credit']['amount'].sum()
        metrics['net_flow'] = metrics['total_received'] - metrics['total_spent']
        metrics['avg_transaction'] = df['amount'].mean()
        metrics['largest_transaction'] = df['amount'].max()
        metrics['smallest_transaction'] = df['amount'].min()
        
        # Time-based metrics
        if 'month' in df.columns:
            monthly_spending = df[df['type'] == 'Debit'].groupby('month')['amount'].sum()
            metrics['avg_monthly_spending'] = monthly_spending.mean()
            metrics['highest_month'] = monthly_spending.idxmax()
            metrics['lowest_month'] = monthly_spending.idxmin()
        
        # Frequency metrics
        daily_transactions = df.groupby(df['date'].dt.date).size()
        metrics['avg_daily_transactions'] = daily_transactions.mean()
        metrics['most_active_day'] = daily_transactions.idxmax()
        
        return metrics
    
    def create_timeline_chart(self, df, chart_type='daily'):
        """Create timeline visualization"""
        if chart_type == 'daily':
            data = df.groupby('date')['amount'].sum().reset_index()
            title = "Daily Transaction Timeline"
        elif chart_type == 'monthly':
            data = df.groupby(df['date'].dt.to_period('M'))['amount'].sum().reset_index()
            data['date'] = data['date'].astype(str)
            title = "Monthly Transaction Timeline"
        elif chart_type == 'weekly':
            data = df.groupby(df['date'].dt.to_period('W'))['amount'].sum().reset_index()
            data['date'] = data['date'].astype(str)
            title = "Weekly Transaction Timeline"
        
        fig = go.Figure()
        
        # Add main line
        fig.add_trace(go.Scatter(
            x=data['date'],
            y=data['amount'],
            mode='lines+markers',
            name='Transaction Amount',
            line=dict(color=self.color_scheme['primary'], width=3),
            marker=dict(size=8, color=self.color_scheme['primary'])
        ))
        
        # Add trend line
        z = np.polyfit(range(len(data)), data['amount'], 1)
        p = np.poly1d(z)
        fig.add_trace(go.Scatter(
            x=data['date'],
            y=p(range(len(data))),
            mode='lines',
            name='Trend',
            line=dict(color=self.color_scheme['secondary'], width=2, dash='dash')
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title="Amount (₹)",
            hovermode='x unified',
            showlegend=True,
            template='plotly_white'
        )
        
        return fig
    
    def create_spending_heatmap(self, df):
        """Create spending heatmap by day of week and hour"""
        if 'day_of_week' not in df.columns or 'hour' not in df.columns:
            return None
        
        # Prepare data
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        df['day_of_week'] = pd.Categorical(df['day_of_week'], categories=day_order, ordered=True)
        
        heatmap_data = df.groupby(['day_of_week', 'hour'])['amount'].sum().reset_index()
        pivot_data = heatmap_data.pivot(index='day_of_week', columns='hour', values='amount')
        
        fig = px.imshow(
            pivot_data,
            title="Spending Heatmap (Day vs Hour)",
            color_continuous_scale="viridis",
            aspect="auto"
        )
        
        fig.update_layout(
            xaxis_title="Hour of Day",
            yaxis_title="Day of Week",
            template='plotly_white'
        )
        
        return fig
    
    def create_category_breakdown(self, df, chart_type='pie'):
        """Create category breakdown visualization"""
        if 'category' not in df.columns:
            return None
        
        category_data = df.groupby('category')['amount'].sum().sort_values(ascending=False)
        
        if chart_type == 'pie':
            fig = px.pie(
                values=category_data.values,
                names=category_data.index,
                title="Spending by Category"
            )
            fig.update_traces(textinfo='percent+label')
        
        elif chart_type == 'bar':
            fig = px.bar(
                x=category_data.index,
                y=category_data.values,
                title="Spending by Category",
                color=category_data.values,
                color_continuous_scale="viridis"
            )
            fig.update_layout(xaxis_title="Category", yaxis_title="Amount (₹)")
        
        elif chart_type == 'treemap':
            fig = px.treemap(
                names=category_data.index,
                parents=[''] * len(category_data),
                values=category_data.values,
                title="Spending Treemap by Category"
            )
        
        fig.update_layout(template='plotly_white')
        return fig
    
    def create_amount_distribution(self, df):
        """Create amount distribution histogram"""
        fig = go.Figure()
        
        # Create histogram
        fig.add_trace(go.Histogram(
            x=df['amount'],
            nbinsx=30,
            name='Transaction Amounts',
            marker_color=self.color_scheme['primary']
        ))
        
        # Add vertical line for mean
        mean_amount = df['amount'].mean()
        fig.add_vline(
            x=mean_amount,
            line_dash="dash",
            line_color=self.color_scheme['danger'],
            annotation_text=f"Mean: ₹{mean_amount:,.2f}"
        )
        
        fig.update_layout(
            title="Transaction Amount Distribution",
            xaxis_title="Amount (₹)",
            yaxis_title="Frequency",
            template='plotly_white'
        )
        
        return fig
    
    def create_comparison_chart(self, df, compare_by='type'):
        """Create comparison chart between different categories"""
        if compare_by == 'type':
            data = df.groupby('type')['amount'].sum().reset_index()
            title = "Credit vs Debit Comparison"
        elif compare_by == 'month':
            data = df.groupby('month')['amount'].sum().reset_index()
            data['month_name'] = data['month'].apply(lambda x: calendar.month_name[x])
            title = "Monthly Spending Comparison"
        elif compare_by == 'day_of_week':
            data = df.groupby('day_of_week')['amount'].sum().reset_index()
            title = "Spending by Day of Week"
        
        fig = px.bar(
            data,
            x=data.columns[0] if compare_by != 'month' else 'month_name',
            y='amount',
            title=title,
            color='amount',
            color_continuous_scale="viridis"
        )
        
        fig.update_layout(
            xaxis_title=data.columns[0].replace('_', ' ').title(),
            yaxis_title="Amount (₹)",
            template='plotly_white'
        )
        
        return fig
    
    def create_rolling_averages(self, df, window=7):
        """Create rolling average chart"""
        if 'rolling_7d_avg' not in df.columns:
            return None
        
        daily_data = df.groupby('date')['amount'].sum().reset_index()
        daily_data['rolling_avg'] = daily_data['amount'].rolling(window=window).mean()
        
        fig = go.Figure()
        
        # Actual values
        fig.add_trace(go.Scatter(
            x=daily_data['date'],
            y=daily_data['amount'],
            mode='markers',
            name='Daily Amount',
            marker=dict(size=4, color=self.color_scheme['primary'])
        ))
        
        # Rolling average
        fig.add_trace(go.Scatter(
            x=daily_data['date'],
            y=daily_data['rolling_avg'],
            mode='lines',
            name=f'{window}-Day Rolling Average',
            line=dict(color=self.color_scheme['secondary'], width=3)
        ))
        
        fig.update_layout(
            title=f"Daily Spending with {window}-Day Rolling Average",
            xaxis_title="Date",
            yaxis_title="Amount (₹)",
            template='plotly_white'
        )
        
        return fig
    
    def create_anomaly_detection(self, df):
        """Create anomaly detection visualization"""
        # Calculate z-scores for amounts
        amounts = df['amount']
        z_scores = np.abs((amounts - amounts.mean()) / amounts.std())
        anomalies = z_scores > 2  # Threshold for anomalies
        
        fig = go.Figure()
        
        # Normal transactions
        normal_data = df[~anomalies]
        fig.add_trace(go.Scatter(
            x=normal_data['date'],
            y=normal_data['amount'],
            mode='markers',
            name='Normal Transactions',
            marker=dict(size=6, color=self.color_scheme['primary'])
        ))
        
        # Anomalous transactions
        anomaly_data = df[anomalies]
        if not anomaly_data.empty:
            fig.add_trace(go.Scatter(
                x=anomaly_data['date'],
                y=anomaly_data['amount'],
                mode='markers',
                name='Anomalies',
                marker=dict(size=10, color=self.color_scheme['danger'], symbol='diamond')
            ))
        
        fig.update_layout(
            title="Transaction Anomaly Detection",
            xaxis_title="Date",
            yaxis_title="Amount (₹)",
            template='plotly_white'
        )
        
        return fig
    
    def create_summary_dashboard(self, df):
        """Create a comprehensive summary dashboard"""
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Daily Timeline', 'Category Breakdown', 'Amount Distribution', 'Monthly Comparison'),
            specs=[[{"type": "scatter"}, {"type": "pie"}],
                   [{"type": "histogram"}, {"type": "bar"}]]
        )
        
        # Daily timeline
        timeline_data = df.groupby('date')['amount'].sum().reset_index()
        fig.add_trace(
            go.Scatter(x=timeline_data['date'], y=timeline_data['amount'], mode='lines', name='Daily Amount'),
            row=1, col=1
        )
        
        # Category breakdown
        if 'category' in df.columns:
            category_data = df.groupby('category')['amount'].sum()
            fig.add_trace(
                go.Pie(values=category_data.values, labels=category_data.index, name='Categories'),
                row=1, col=2
            )
        
        # Amount distribution
        fig.add_trace(
            go.Histogram(x=df['amount'], name='Amount Distribution'),
            row=2, col=1
        )
        
        # Monthly comparison
        monthly_data = df.groupby('month')['amount'].sum().reset_index()
        fig.add_trace(
            go.Bar(x=monthly_data['month'], y=monthly_data['amount'], name='Monthly Amount'),
            row=2, col=2
        )
        
        fig.update_layout(height=800, title_text="Financial Summary Dashboard")
        return fig
