"""
RealEstateAI - AI Marketing Assistant for Realtors
Main Streamlit Application
"""

import os
import sys

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="RealEstateAI - AI Marketing for Realtors",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://realestateai.app/help',
        'Report a bug': 'https://realestateai.app/bug',
        'About': '# RealEstateAI - AI Marketing Assistant for Realtors'
    }
)

# Custom CSS for styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root {
        --primary: #1E3A5F;
        --secondary: #2ECC71;
        --accent: #F39C12;
        --background: #0F1419;
        --surface: #192734;
        --surface-hover: #22303C;
        --text-primary: #FFFFFF;
        --text-secondary: #8899A6;
        --error: #E74C3C;
        --success: #2ECC71;
        --border: #38444D;
    }
    
    .stApp {
        background: var(--background);
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        color: var(--text-primary);
    }
    
    h1 {
        font-size: 2.5rem;
        background: linear-gradient(135deg, var(--primary) 0%, #3498DB 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .feature-card {
        background: var(--surface);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid var(--border);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(30, 58, 95, 0.3);
        border-color: var(--primary);
    }
    
    [data-testid="stSidebar"] {
        background: var(--surface);
        border-right: 1px solid var(--border);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, #2980B9 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(30, 58, 95, 0.4);
    }
    
    .header-container {
        background: linear-gradient(135deg, rgba(30, 58, 95, 0.9) 0%, rgba(41, 128, 185, 0.9) 100%);
        padding: 40px;
        border-radius: 20px;
        margin-bottom: 30px;
        text-align: center;
    }
    
    .header-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 10px;
        color: white;
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.8);
    }
    
    .pricing-card {
        background: var(--surface);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        border: 2px solid var(--border);
        transition: all 0.3s ease;
    }
    
    .pricing-card:hover {
        transform: scale(1.02);
        border-color: var(--primary);
    }
    
    .pricing-card.featured {
        border-color: var(--secondary);
        background: linear-gradient(135deg, rgba(46, 204, 113, 0.1) 0%, rgba(46, 204, 113, 0.05) 100%);
    }
    
    .price {
        font-size: 3rem;
        font-weight: 800;
        color: var(--secondary);
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize Streamlit session state variables"""
    if 'generated_content' not in st.session_state:
        st.session_state.generated_content = {}
    if 'api_keys_configured' not in st.session_state:
        st.session_state.api_keys_configured = False
    if 'user_tier' not in st.session_state:
        st.session_state.user_tier = 'free'
    if 'credits' not in st.session_state:
        st.session_state.credits = 3


def check_api_keys():
    """Check if required API keys are configured"""
    openai_key = os.getenv('OPENAI_API_KEY')
    return bool(openai_key and openai_key != 'sk-your-openai-api-key-here')


def show_home():
    """Home page with overview and features"""
    
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🏠 RealEstateAI</h1>
        <p class="header-subtitle">
            🤖 AI Marketing Automation for Real Estate Agents<br>
            Generate reels, listings, virtual staging, and more in seconds
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🚀 Reels Generated", "12,450+")
    with col2:
        st.metric("📝 Listings Written", "8,230+")
    with col3:
        st.metric("🏠 Virtual Stagings", "5,670+")
    with col4:
        st.metric("⭐ Agent Rating", "4.9/5")
    
    st.markdown("---")
    
    # Features Overview
    st.markdown("## ✨ AI Features")
    
    features = [
        {"icon": "🎬", "title": "AI Reel Generator", "description": "Transform property photos into stunning Instagram Reels, YouTube Shorts, and TikToks with AI voiceover, captions, and trending music."},
        {"icon": "📝", "title": "AI Listing Generator", "description": "Generate SEO-optimized MLS listings, social media captions, and email campaigns from property details in seconds."},
        {"icon": "🪑", "title": "AI Virtual Staging", "description": "Transform empty rooms into beautifully furnished spaces with AI-powered virtual staging in multiple styles."},
        {"icon": "💬", "title": "AI Lead Follow-Up Bot", "description": "Never lose a lead again. AI-powered chatbot responds instantly across SMS, WhatsApp, and website."},
        {"icon": "📊", "title": "AI Market Reports", "description": "Generate professional neighborhood market reports with price trends and insights automatically."},
        {"icon": "🎨", "title": "AI Content Engine", "description": "Complete social media content strategy with daily posts, scripts, and brand building tools."}
    ]
    
    # Display features in grid
    for i in range(0, len(features), 2):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="feature-card">
                <h3 style="font-size: 2rem; margin-bottom: 10px;">{features[i]['icon']}</h3>
                <h3>{features[i]['title']}</h3>
                <p style="color: var(--text-secondary);">{features[i]['description']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if i + 1 < len(features):
                st.markdown(f"""
                <div class="feature-card">
                    <h3 style="font-size: 2rem; margin-bottom: 10px;">{features[i+1]['icon']}</h3>
                    <h3>{features[i+1]['title']}</h3>
                    <p style="color: var(--text-secondary);">{features[i+1]['description']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Pricing Section
    st.markdown("## 💰 Pricing Plans")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="pricing-card">
            <h3>🚀 Starter</h3>
            <div class="price">$49<span style="font-size: 1rem; color: var(--text-secondary);">/mo</span></div>
            <p style="color: var(--text-secondary);">Perfect for individual agents</p>
            <hr>
            <ul style="text-align: left; color: var(--text-secondary);">
                <li>✅ 20 AI Reels/month</li>
                <li>✅ 50 Listing Generations</li>
                <li>✅ Basic Virtual Staging</li>
                <li>✅ Email Support</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="pricing-card featured">
            <h3>⭐ Pro</h3>
            <div class="price">$99<span style="font-size: 1rem; color: var(--text-secondary);">/mo</span></div>
            <p style="color: var(--text-secondary);">Most popular choice</p>
            <hr>
            <ul style="text-align: left; color: var(--text-secondary);">
                <li>✅ 100 AI Reels/month</li>
                <li>✅ 200 Listing Generations</li>
                <li>✅ Advanced Virtual Staging</li>
                <li>✅ Lead Follow-Up Bot</li>
                <li>✅ Priority Support</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="pricing-card">
            <h3>🏢 Enterprise</h3>
            <div class="price">$199<span style="font-size: 1rem; color: var(--text-secondary);">/mo</span></div>
            <p style="color: var(--text-secondary);">For teams & brokerages</p>
            <hr>
            <ul style="text-align: left; color: var(--text-secondary);">
                <li>✅ Unlimited AI Reels</li>
                <li>✅ Unlimited Listings</li>
                <li>✅ Unlimited Virtual Staging</li>
                <li>✅ Full Lead Bot Suite</li>
                <li>✅ CRM Integration</li>
                <li>✅ Dedicated Support</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # CTA Section
    st.markdown("""
    <div style="text-align: center; padding: 40px;">
        <h2>🚀 Ready to Transform Your Real Estate Business?</h2>
        <p style="color: var(--text-secondary); font-size: 1.2rem;">
            Join thousands of agents using AI to save time and close more deals.
        </p>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main application entry point"""
    init_session_state()
    
    # Check API keys
    st.session_state.api_keys_configured = check_api_keys()
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="display: flex; align-items: center; justify-content: center; gap: 12px; margin-bottom: 20px;">
            <span style="font-size: 32px;">🏠</span>
            <h2 style="margin:0; color: white;">RealEstateAI</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation
        st.markdown("### 📋 Menu")
        page = st.radio(
            "Go to",
            ["🏠 Home", "🎬 Reel Generator", "📝 Listing Generator", 
             "🪑 Virtual Staging", "💬 Lead Bot", "📊 Market Report"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Credits/Usage
        st.markdown("### 💳 Your Plan")
        tier = st.session_state.user_tier
        credits = st.session_state.credits
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Plan", tier.title())
        with col2:
            st.metric("Credits", credits)
        
        if credits < 5:
            st.warning("⚠️ Low credits! Consider upgrading.")
        
        st.markdown("---")
        
        # API Status
        st.markdown("### 🔌 API Status")
        if st.session_state.api_keys_configured:
            st.success("✅ OpenAI Connected")
        else:
            st.warning("⚠️ Configure API keys in .env file")
    
    # Route to selected page
    if page == "🏠 Home":
        show_home()
    elif page == "🎬 Reel Generator":
        from app.pages import reel_generator
        reel_generator.show()
    elif page == "📝 Listing Generator":
        from app.pages import listing_generator
        listing_generator.show()
    elif page == "🪑 Virtual Staging":
        from app.pages import virtual_staging
        virtual_staging.show()
    elif page == "💬 Lead Bot":
        from app.pages import lead_bot
        lead_bot.show()
    elif page == "📊 Market Report":
        from app.pages import market_report
        market_report.show()


if __name__ == "__main__":
    main()

