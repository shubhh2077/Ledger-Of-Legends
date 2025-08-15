import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import re
import plotly.express as px

# App config
st.set_page_config(page_title="Ledger of Legends", layout="wide")
st.title("Ledger of Legends")

# File upload
uploaded_file = st.file_uploader("📂 Upload your Ledger Activity HTML", type=["html"])

if uploaded_file is not None:
    # Parse HTML
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

    if transactions:
        df = pd.DataFrame(transactions)
        df["type"] = df["description"].apply(lambda x: "Credit" if "received" in x.lower() else "Debit")

        # Sidebar Filters - minimal style
        st.sidebar.header("🔍 Smart Filters")
        min_date, max_date = df["date"].min(), df["date"].max()
        start_date, end_date = st.sidebar.date_input(
            "📅 Date Range",
            value=[min_date, max_date],
            min_value=min_date,
            max_value=max_date
        )

        type_filter = st.sidebar.multiselect("💳 Transaction Type", options=df["type"].unique(), default=df["type"].unique())
        name_filter = st.sidebar.text_input("🔍 Search by Name / Keyword")

        # Apply filters
        filtered_df = df[
            (df["date"].dt.date >= start_date) &
            (df["date"].dt.date <= end_date) &
            (df["type"].isin(type_filter))
        ]
        if name_filter:
            filtered_df = filtered_df[filtered_df["description"].str.contains(name_filter, case=False, na=False)]

        # Calculate average monthly spending (only for Debits)
        if not filtered_df.empty:
            monthly_spending = filtered_df[filtered_df['type'] == 'Debit'].groupby(filtered_df['date'].dt.to_period('M'))['amount'].sum()
            avg_monthly_spending = monthly_spending.mean()
        else:
            avg_monthly_spending = 0

        # Insights Section
        st.subheader("📊 Quick Insights")
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("💸 Total Spent", f"₹{filtered_df[filtered_df['type'] == 'Debit']['amount'].sum():,.2f}")
        col2.metric("💰 Total Received", f"₹{filtered_df[filtered_df['type'] == 'Credit']['amount'].sum():,.2f}")
        col3.metric("📈 Highest Transaction", f"₹{filtered_df['amount'].max():,.2f}")
        col4.metric("🛍️ Avg Transaction", f"₹{filtered_df['amount'].mean():,.2f}")
        col5.metric("📆 Avg Monthly Spending", f"₹{avg_monthly_spending:,.2f}")

        # Transactions Table
        st.subheader("📄 Transactions")
        st.dataframe(filtered_df, use_container_width=True)

        # Daily spending trend
        daily_sum = filtered_df.groupby("date")["amount"].sum().reset_index()
        fig_daily = px.line(daily_sum, x="date", y="amount", title="📅 Daily Transactions", markers=True)
        fig_daily.update_xaxes(rangeslider_visible=True)
        st.plotly_chart(fig_daily, use_container_width=True)

        # Pie chart
        pie_data = filtered_df.groupby("type")["amount"].sum().reset_index()
        fig_pie = px.pie(pie_data, names="type", values="amount", title="💳 Credit vs Debit Distribution")
        fig_pie.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

        # Monthly breakdown chart
        monthly_sum = filtered_df.groupby(filtered_df["date"].dt.to_period("M"))["amount"].sum().reset_index()
        monthly_sum["date"] = monthly_sum["date"].astype(str)
        fig_monthly = px.bar(monthly_sum, x="date", y="amount", title="📆 Monthly Spending Overview")
        st.plotly_chart(fig_monthly, use_container_width=True)

    else:
        st.error("⚠️ No transactions found in the HTML file. Please check file format.")
