#!/usr/bin/env python
"""
RealEstateAI - Startup Script
Run this to launch the AI Real Estate Marketing System

Copyright (c) 2024 Anmol Sharma. All Rights Reserved.
"""

import os
import sys
import subprocess

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def check_requirements():
    """Check if required packages are installed"""
    try:
        import streamlit
        import openai
        print("✅ Core dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("\n📦 Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True

def setup_environment():
    """Setup environment variables"""
    if not os.path.exists('.env'):
        print("⚠️ .env file not found. Creating from template...")
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("✅ Created .env file. Please add your API keys!")
        else:
            print("❌ .env.example not found")
            return False
    return True

def main():
    """Main entry point"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║   🏠  RealEstateAI - AI Marketing for Realtors         ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    if not check_requirements():
        sys.exit(1)
    
    if not setup_environment():
        print("⚠️ Continuing anyway...")
    
    print("\n🚀 Starting RealEstateAI...")
    print("📍 Open http://localhost:8501 in your browser\n")
    
    os.system("streamlit run app/main.py")

if __name__ == "__main__":
    main()

