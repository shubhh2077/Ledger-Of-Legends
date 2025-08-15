import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import re
from datetime import datetime, timedelta

class FinanceAIAgent:
    def __init__(self):
        self.categories = {
            'Food & Dining': ['restaurant', 'food', 'meal', 'dining', 'cafe', 'pizza', 'burger', 'swiggy', 'zomato'],
            'Transportation': ['uber', 'ola', 'metro', 'bus', 'fuel', 'petrol', 'diesel', 'parking', 'toll'],
            'Shopping': ['amazon', 'flipkart', 'myntra', 'shop', 'store', 'mall', 'clothing', 'electronics'],
            'Entertainment': ['movie', 'netflix', 'prime', 'hotstar', 'game', 'concert', 'theatre'],
            'Healthcare': ['medical', 'pharmacy', 'doctor', 'hospital', 'medicine', 'health'],
            'Utilities': ['electricity', 'water', 'gas', 'internet', 'mobile', 'recharge'],
            'Education': ['course', 'book', 'tuition', 'college', 'university', 'education'],
            'Investment': ['mutual', 'fund', 'stock', 'investment', 'sip', 'equity'],
            'Travel': ['hotel', 'flight', 'booking', 'travel', 'vacation', 'trip'],
            'Personal Care': ['salon', 'spa', 'beauty', 'gym', 'fitness', 'wellness']
        }
    
    def categorize_transactions(self, df):
        def get_category(description):
            description_lower = description.lower()
            for category, keywords in self.categories.items():
                if any(keyword in description_lower for keyword in keywords):
                    return category
            return 'Other'
        
        df['category'] = df['description'].apply(get_category)
        return df
    
    def analyze_spending_patterns(self, df):
        insights = {}
        insights['total_transactions'] = len(df)
        insights['total_spent'] = df[df['type'] == 'Debit']['amount'].sum()
        insights['total_received'] = df[df['type'] == 'Credit']['amount'].sum()
        insights['net_flow'] = insights['total_received'] - insights['total_spent']
        
        if 'category' in df.columns:
            category_spending = df[df['type'] == 'Debit'].groupby('category')['amount'].sum().sort_values(ascending=False)
            insights['top_categories'] = category_spending.head(5).to_dict()
        
        df['month'] = df['date'].dt.to_period('M')
        monthly_spending = df[df['type'] == 'Debit'].groupby('month')['amount'].sum()
        insights['avg_monthly_spending'] = monthly_spending.mean()
        
        return insights
    
    def generate_recommendations(self, insights):
        recommendations = []

        total_spent = float(insights.get('total_spent', 0) or 0)
        total_received = float(insights.get('total_received', 0) or 0)
        net_flow = float(insights.get('net_flow', total_received - total_spent) or 0)
        avg_monthly_spending = float(insights.get('avg_monthly_spending', 0) or 0)

        # Use small epsilon to avoid float noise
        EPS = 1e-9

        if net_flow < -EPS:
            # Negative net flow → warning only
            recommendations.append({
                'type': 'warning',
                'title': 'High Spending Alert',
                'message': f"You're spending ₹{abs(net_flow):,.2f} more than you're receiving. Consider cutting discretionary categories and setting a weekly cap."
            })
        elif net_flow > EPS:
            # Positive net flow → positive message only
            recommendations.append({
                'type': 'info',
                'title': 'Healthy Net Flow',
                'message': f"Great job! You have a surplus of ₹{net_flow:,.2f}. Consider allocating 20–30% to savings/investments to compound your gains."
            })
        else:
            # Balanced case → neutral suggestion
            recommendations.append({
                'type': 'info',
                'title': 'Balanced Cash Flow',
                'message': "Your income matches your spending. Set a small monthly savings target (e.g., 10%) to build a consistent surplus."
            })

        # High monthly spending nudge (applies in all cases)
        if avg_monthly_spending > 50000:
            recommendations.append({
                'type': 'info',
                'title': 'High Monthly Spending',
                'message': f"Your average monthly spending is ₹{avg_monthly_spending:,.2f}. Consider a category-level budget and weekly checkpoints."
            })

        # Note: intentionally not adding 'Spending Focus Areas' recommendation

        return recommendations
