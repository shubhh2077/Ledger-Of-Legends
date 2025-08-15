#!/usr/bin/env python3
"""
Launcher script for Ledger of Legends
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'streamlit',
        'pandas',
        'plotly',
        'beautifulsoup4',
        'scikit-learn',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Installing missing packages...")
        
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
            ])
            print("✅ Dependencies installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies. Please run:")
            print("   pip install -r requirements.txt")
            return False
    
    return True

def main():
    """Main launcher function"""
    print("🚀 Starting Ledger of Legends...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path('enhanced_app.py').exists():
        print("❌ Error: enhanced_app.py not found!")
        print("   Please run this script from the project directory.")
        return
    
    # Check dependencies
    if not check_dependencies():
        return
    
    print("✅ All dependencies are installed!")
    print("🌐 Starting the Ledger of Legends web application...")
    print("📱 The app will open in your default browser")
    print("🔗 If it doesn't open automatically, go to: http://localhost:8501")
    print("=" * 50)
    
    try:
        # Run the Streamlit app
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'enhanced_app.py',
            '--server.port', '8501',
            '--server.address', 'localhost'
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

if __name__ == "__main__":
    main()
