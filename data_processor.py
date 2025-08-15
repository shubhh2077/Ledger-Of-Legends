import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import json

class DataProcessor:
    def __init__(self):
        self.supported_formats = ['html', 'csv', 'json']
    
    def parse_html_file(self, file_content):
        """Parse Google Pay HTML activity file"""
        soup = BeautifulSoup(file_content, "html.parser")
        transactions = []
        
        # Look for transaction entries
        for entry in soup.find_all("div", class_="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1"):
            text = entry.get_text(separator=" ").strip()
            
            # Extract date
            date_match = re.search(r"\w+\s\d{1,2},\s\d{4}", text)
            if not date_match:
                continue
                
            # Extract amount
            amount_match = re.search(r"₹[\d,]+(\.\d{1,2})?", text)
            if not amount_match:
                continue
            
            try:
                date = pd.to_datetime(date_match.group(), format='mixed')
                amount = float(amount_match.group().replace("₹", "").replace(",", ""))
                
                transactions.append({
                    "date": date,
                    "amount": amount,
                    "description": text,
                    "raw_text": text
                })
            except (ValueError, TypeError):
                continue
        
        return pd.DataFrame(transactions)
    
    def parse_csv_file(self, file_content):
        """Parse CSV file with flexible column mapping"""
        try:
            df = pd.read_csv(file_content)
            
            # Standardize column names
            column_mapping = {
                'date': ['date', 'Date', 'DATE', 'transaction_date', 'Transaction Date'],
                'amount': ['amount', 'Amount', 'AMOUNT', 'value', 'Value', 'transaction_amount'],
                'description': ['description', 'Description', 'DESCRIPTION', 'details', 'Details', 'transaction_details'],
                'type': ['type', 'Type', 'TYPE', 'transaction_type', 'Transaction Type']
            }
            
            # Map columns
            for standard_name, possible_names in column_mapping.items():
                for col_name in possible_names:
                    if col_name in df.columns:
                        df[standard_name] = df[col_name]
                        break
            
            # Ensure required columns exist (support 'Date'/'Amount' as well)
            if 'date' not in df.columns and 'Date' in df.columns:
                df['date'] = df['Date']
            if 'amount' not in df.columns and 'Amount' in df.columns:
                df['amount'] = df['Amount']
            if 'date' not in df.columns:
                raise ValueError("Date column not found in CSV")
            if 'amount' not in df.columns:
                raise ValueError("Amount column not found in CSV")
            
            # Convert data types
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
            
            # Determine transaction type if not present
            if 'type' not in df.columns:
                # Heuristic: try to infer from description, otherwise alternate
                if 'description' in df.columns:
                    df['type'] = df['description'].apply(
                        lambda x: "Credit" if "received" in str(x).lower() or "credited" in str(x).lower() else "Debit"
                    )
                else:
                    df = df.reset_index(drop=False)
                    df['type'] = df['index'].apply(lambda i: 'Credit' if (i % 3 == 0) else 'Debit')
                    df = df.drop(columns=['index'])
            
            return df.dropna(subset=['date', 'amount'])
            
        except Exception as e:
            raise ValueError(f"Error parsing CSV file: {str(e)}")
    
    def enhance_data(self, df):
        """Add additional useful columns to the dataframe"""
        if df.empty:
            return df
        
        # Add time-based features
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['day_of_week'] = df['date'].dt.day_name()
        df['hour'] = df['date'].dt.hour
        df['quarter'] = df['date'].dt.quarter
        df['week_of_year'] = df['date'].dt.isocalendar().week
        
        # Add amount-based features
        df['amount_category'] = pd.cut(
            df['amount'],
            bins=[0, 1000, 5000, 10000, 50000, float('inf')],
            labels=['Small', 'Medium', 'Large', 'Very Large', 'Huge']
        )
        
        # Add transaction frequency
        df['transaction_count'] = df.groupby(df['date'].dt.date).cumcount() + 1
        
        # Add rolling statistics
        df['rolling_7d_avg'] = df.groupby('type')['amount'].rolling(7, min_periods=1).mean().reset_index(0, drop=True)
        df['rolling_30d_avg'] = df.groupby('type')['amount'].rolling(30, min_periods=1).mean().reset_index(0, drop=True)
        
        return df
    
    def detect_duplicates(self, df):
        """Detect and handle duplicate transactions"""
        # Create a hash for each transaction
        df['transaction_hash'] = df.apply(
            lambda row: hash(f"{row['date']}_{row['amount']}_{row['description'][:50]}"), 
            axis=1
        )
        
        duplicates = df[df.duplicated(subset=['transaction_hash'], keep=False)]
        unique_transactions = df.drop_duplicates(subset=['transaction_hash'], keep='first')
        
        return unique_transactions, duplicates
    
    def validate_data(self, df):
        """Validate data quality and return issues"""
        issues = []
        
        # Check for missing values
        missing_data = df.isnull().sum()
        if missing_data.any():
            issues.append(f"Missing data found: {missing_data[missing_data > 0].to_dict()}")
        
        # Check for invalid amounts
        invalid_amounts = df[df['amount'] <= 0]
        if not invalid_amounts.empty:
            issues.append(f"Found {len(invalid_amounts)} transactions with invalid amounts")
        
        # Check for future dates
        future_dates = df[df['date'] > datetime.now()]
        if not future_dates.empty:
            issues.append(f"Found {len(future_dates)} transactions with future dates")
        
        # Check for very old dates (more than 10 years)
        old_dates = df[df['date'] < datetime.now() - timedelta(days=3650)]
        if not old_dates.empty:
            issues.append(f"Found {len(old_dates)} transactions older than 10 years")
        
        return issues
    
    def process_file(self, file_content, file_type):
        """Main processing function"""
        if file_type == 'html':
            df = self.parse_html_file(file_content)
        elif file_type == 'csv':
            df = self.parse_csv_file(file_content)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        # Enhance data
        df = self.enhance_data(df)
        
        # Detect duplicates
        df, duplicates = self.detect_duplicates(df)
        
        # Validate data
        issues = self.validate_data(df)
        
        return {
            'data': df,
            'duplicates': duplicates,
            'issues': issues,
            'summary': {
                'total_transactions': len(df),
                'date_range': f"{df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}",
                'total_amount': df['amount'].sum(),
                'duplicate_count': len(duplicates)
            }
        }
