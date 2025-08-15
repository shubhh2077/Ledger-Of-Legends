# 🤖 Ledger of Legends

A comprehensive, intelligent financial analysis tool for your transaction data with AI-powered insights, advanced visualizations, and personalized recommendations.

## ✨ Features

### 🤖 AI-Powered Analysis
- **Intelligent Categorization**: Automatically categorizes transactions using AI
- **Smart Recommendations**: Get personalized financial advice and spending insights
- **Anomaly Detection**: Identify unusual spending patterns and transactions
- **Trend Analysis**: Predict future spending based on historical data

### 📊 Advanced Analytics
- **Interactive Dashboards**: Comprehensive financial overview with real-time metrics
- **Multiple Chart Types**: Timeline, heatmaps, pie charts, bar charts, and more
- **Customizable Filters**: Date range, amount range, transaction types, categories
- **Export Capabilities**: Download filtered data in multiple formats

### 💰 Budget Management
- **Monthly Budget Tracking**: Set and monitor your spending limits
- **Smart Alerts**: Get notified when approaching budget limits
- **Progress Visualization**: Visual budget progress indicators
- **Spending Insights**: Understand where your money goes

### 🔍 Enhanced Filtering
- **Date Range Selection**: Filter by specific time periods
- **Amount Range Filter**: Focus on transactions within specific amounts
- **Category Filtering**: Analyze spending by categories
- **Keyword Search**: Find specific transactions quickly
- **Transaction Type Filter**: Separate credits and debits

### 📈 Advanced Visualizations
- **Timeline Charts**: Daily, weekly, and monthly transaction trends
- **Spending Heatmaps**: Visualize spending patterns by day and hour
- **Category Breakdowns**: Pie charts, bar charts, and treemaps
- **Anomaly Detection**: Highlight unusual transactions
- **Rolling Averages**: Track spending trends over time

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Ledger data (HTML or CSV format)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/shubhh2077/Ledger-Of-Legends.git
   cd Ledger-Of-Legends
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   run run_app.batch file
   ```

### How to Use

1. **Upload Your Data**
   - Upload your ledger HTML file or CSV export
   - The app supports multiple file formats

2. **Explore the Dashboard**
   - View key financial metrics at a glance
   - Use the sidebar filters to analyze specific data

3. **Run AI Analysis**
   - Click "Run AI Analysis" for intelligent insights
   - Get personalized recommendations and spending patterns

4. **Customize Your View**
   - Use the advanced filters to focus on specific data
   - Explore different chart types in the Analytics section

5. **Set Up Budget Tracking**
   - Set your monthly budget
   - Monitor your spending progress

## 📁 File Structure

```
ledger-of-legends/
├── enhanced_app.py          # Main Streamlit application
├── ai_agent.py             # AI analysis and insights
├── data_processor.py       # Data processing and validation
├── visualizations.py       # Advanced chart generation
├── config.py              # Application configuration
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── data/                 # Sample data directory
    └── transactions.csv
```

## 🔧 Configuration

The application can be customized through the `config.py` file:

- **AI Categories**: Customize transaction categorization
- **Budget Settings**: Set default budget thresholds
- **Visualization Colors**: Customize chart appearance
- **Export Formats**: Configure supported export options

## 📊 Supported Data Formats

### HTML Format (Legacy Google Pay Activity)
- Legacy support for Google Pay exports
- Automatic parsing of transaction data
- Extracts date, amount, and description

### CSV Format
- Flexible column mapping
- Supports various CSV structures
- Automatic data type detection

## 🎯 Key Features Explained

### AI-Powered Insights
The AI agent analyzes your spending patterns and provides:
- **Spending Recommendations**: Tips to optimize your budget
- **Category Analysis**: Understanding of spending distribution
- **Anomaly Detection**: Identification of unusual transactions
- **Trend Predictions**: Future spending forecasts

### Advanced Filtering
- **Date Range**: Filter transactions by specific time periods
- **Amount Range**: Focus on transactions within budget ranges
- **Category Filter**: Analyze spending by merchant categories
- **Keyword Search**: Find specific transactions or merchants
- **Transaction Type**: Separate incoming and outgoing money

### Budget Tracking
- **Monthly Budget Setting**: Define your spending limits
- **Progress Monitoring**: Visual indicators of budget usage
- **Smart Alerts**: Warnings when approaching limits
- **Historical Comparison**: Compare spending across months

### Export and Sharing
- **Multiple Formats**: CSV, JSON, Excel export options
- **Filtered Data**: Export only the data you're analyzing
- **Custom Reports**: Generate specific financial reports

## 🛠️ Technical Details

### Dependencies
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **Scikit-learn**: Machine learning for AI analysis
- **BeautifulSoup**: HTML parsing
- **NumPy**: Numerical computations

### Performance
- **Caching**: Optimized data processing with caching
- **Lazy Loading**: Efficient handling of large datasets
- **Memory Management**: Optimized for large transaction files

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:
1. Check the documentation
2. Review the configuration settings
3. Ensure your data format is supported
4. Create an issue in the repository

## 🔮 Future Enhancements

- **Machine Learning Models**: More sophisticated spending predictions
- **Mobile App**: Native mobile application
- **Cloud Integration**: Store data securely in the cloud
- **Multi-Currency Support**: Support for different currencies
- **Bank Integration**: Direct bank account integration
- **Receipt Scanning**: OCR for receipt processing

---

**Made with ❤️ for better financial management**

