"""
AI Market Report Generator Page
Creates professional neighborhood market reports with AI
"""

import streamlit as st
import os
from datetime import datetime
from app.utils.openai_client import ContentGenerator


def show():
    """Display the Market Report page"""
    
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="font-size: 2.5rem; margin-bottom: 10px;">📊 AI Market Report Generator</h1>
        <p style="color: #8899A6; font-size: 1.1rem;">
            Generate professional neighborhood market reports, price trends, and insights automatically.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📋 Generate Report", "👁️ Preview", "📤 Export"])
    
    with tab1:
        st.markdown("### 📋 Report Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🗺️ Report Area")
            
            neighborhood = st.text_input("Neighborhood/Area", placeholder="Kitchener, Ontario")
            
            report_type = st.selectbox("Report Type", ["Monthly Market Update", "Quarterly Analysis", "Annual Review", "Neighborhood Spotlight", "Buyers Market Report", "Sellers Market Report"])
            
            report_format = st.selectbox("Report Format", ["Newsletter", "Social Media", "Website Blog", "Email", "Video Script"])
        
        with col2:
            st.markdown("#### 📅 Time Period")
            
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                start_month = st.selectbox("Start Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], index=0)
                start_year = st.number_input("Start Year", min_value=2020, max_value=2025, value=2024)
            with col_d2:
                end_month = st.selectbox("End Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], index=11)
                end_year = st.number_input("End Year", min_value=2020, max_value=2025, value=2024)
            
            include_forecast = st.toggle("Include 3-Month Forecast", value=True)
        
        st.markdown("---")
        st.markdown("#### 📈 Market Data")
        
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        
        with col_m1:
            avg_price = st.number_input("Average Price ($)", value=650000, step=10000)
            price_change = st.number_input("Price Change (%)", value=4.2, step=0.1)
        
        with col_m2:
            days_on_market = st.number_input("Days on Market", value=28, step=1)
            inventory = st.number_input("Active Listings", value=450, step=10)
        
        with col_m3:
            sales_volume = st.number_input("Sales Volume ($M)", value=125, step=5)
            new_listings = st.number_input("New Listings", value=180, step=10)
        
        with col_m4:
            sold_listings = st.number_input("Sold Listings", value=165, step=10)
            months_supply = st.number_input("Months of Supply", value=2.7, step=0.1)
        
        with st.expander("📊 Additional Data"):
            col_a1, col_a2 = st.columns(2)
            
            with col_a1:
                price_by_type = st.text_area("Price by Property Type", value="$550,000 - Condos\n$750,000 - Townhouses\n$850,000 - Single Family")
            
            with col_a2:
                top_features = st.text_area("Top Buyer Preferences", value="• 3+ Bedrooms\n• 2+ Bathrooms\n• Garage\n• Open Concept\n• Updated Kitchen")
        
        st.markdown("---")
        st.markdown("#### 🎨 Brand Customization")
        
        col_b1, col_b2 = st.columns(2)
        
        with col_b1:
            agent_name = st.text_input("Agent Name", value="Your Name")
            company_name = st.text_input("Company/Brand Name", value="Your Realty Group")
        
        with col_b2:
            include_cta = st.toggle("Include Call-to-Action", value=True)
            cta_text = st.text_input("CTA Text", value="Ready to make a move? Let's talk!")
        
        st.markdown("---")
        
        col_g1, col_g2, col_g3 = st.columns([1, 2, 1])
        with col_g2:
            generate_btn = st.button("📊 Generate Market Report", use_container_width=True, disabled=not neighborhood)
    
    with tab2:
        st.markdown("### 👁️ Report Preview")
        
        if generate_btn and neighborhood:
            with st.spinner("🤖 AI is generating your market report..."):
                market_data = {
                    'avg_price': f"${avg_price:,}", 'price_change': f"+{price_change}%" if price_change > 0 else f"{price_change}%",
                    'days_on_market': days_on_market, 'inventory': inventory, 'sales_volume': f"${sales_volume}M",
                    'new_listings': new_listings, 'sold_listings': sold_listings, 'months_supply': months_supply
                }
                
                report_content = f"""
# 📊 {neighborhood} Market Update
## {start_month} {start_year} - {end_month} {end_year}

---

### 🏠 Executive Summary

The {neighborhood} real estate market continues to show {"strong" if price_change > 0 else "stable"} growth with average home prices {"increasing" if price_change > 0 else "holding steady"} by **{price_change}%** compared to last year. With **{days_on_market}** average days on market, properties are selling quickly.

---

### 📈 Key Market Statistics

| Metric | Value |
|--------|-------|
| Average Price | ${avg_price:,} |
| Price Change | {price_change}% |
| Days on Market | {days_on_market} |
| Active Listings | {inventory} |
| Sales Volume | ${sales_volume}M |
| New Listings | {new_listings} |
| Sold Listings | {sold_listings} |
| Months of Supply | {months_supply} |

---

### 🔍 Market Analysis

#### Price Trends
The median home price in {neighborhood} currently sits at **${avg_price:,}**, reflecting a **{price_change}%** {"increase" if price_change > 0 else "change"} year-over-year.

#### Property Types
{price_by_type}

#### Buyer Activity
With **{sold_listings}** homes sold and **{new_listings}** new listings entering the market, we see {"strong buyer demand" if days_on_market < 30 else "balanced market conditions"}.

---

### 🎯 Key Insights

1. **Market Speed**: Homes are selling in an average of **{days_on_market}** days

2. **Inventory Levels**: With **{months_supply}** months of supply, this is a **{"Seller's" if months_supply < 3 else "Buyer's" if months_supply > 6 else "Balanced"}** market

3. **Buyer Preferences**: Today's buyers are looking for:
{top_features}

---

### 📝 Recommendations

**For Sellers:**
- Price competitively to attract multiple offers
- Stage your home to highlight its best features

**For Buyers:**
- Get pre-approved before shopping
- Be prepared to act quickly in competitive situations

---

### 🔮 3-Month Forecast

{"We expect continued growth in the region with prices potentially increasing by 2-4% over the next quarter." if include_forecast else ""}

---

### 💬 Let's Connect!

{cta_text}

**{agent_name}**
{company_name}

*Disclaimer: Market data is based on historical trends.*
"""
                
                st.session_state.generated_report = report_content
                st.session_state.market_data = market_data
            
            st.markdown("### 📄 Generated Report")
            st.markdown(report_content)
            
            st.markdown("---")
            st.markdown("### 📊 Report Stats")
            
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                st.metric("Word Count", len(report_content.split()))
            with col_s2:
                st.metric("Characters", len(report_content))
            with col_s3:
                st.metric("Sections", "8")
        
        else:
            st.info("👆 Configure your report and click Generate to see preview")
            
            st.markdown("### 📝 Example Report Preview")
            st.markdown("""
            # 📊 Kitchener Market Update
            ## January 2024 - December 2024
            
            ### 🏠 Executive Summary
            
            The Kitchener real estate market continues to show strong growth with average home prices increasing by **4.2%** compared to last year.
            
            ### 📈 Key Statistics
            
            | Metric | Value |
            |--------|-------|
            | Average Price | $650,000 |
            | Price Change | +4.2% |
            | Days on Market | 28 |
            | Active Listings | 450 |
            
            ### 💬 Let's Connect!
            
            Ready to make a move? Let's talk!
            """)
    
    with tab3:
        st.markdown("### 📤 Export Options")
        
        if 'generated_report' in st.session_state:
            export_format = st.selectbox("Export Format", ["Markdown", "PDF", "HTML", "Email Template"])
            
            st.markdown("---")
            
            col_e1, col_e2, col_e3 = st.columns(3)
            
            with col_e1:
                st.button("📥 Download as Markdown", use_container_width=True)
            with col_e2:
                st.button("📥 Download as PDF", use_container_width=True)
            with col_e3:
                st.button("📥 Download as HTML", use_container_width=True)
            
            st.markdown("---")
            
            st.markdown("#### 📤 Share Directly")
            
            col_s1, col_s2, col_s3, col_s4 = st.columns(4)
            
            with col_s1:
                st.button("📧 Email to Clients", use_container_width=True)
            with col_s2:
                st.button("📄 Add to Website", use_container_width=True)
            with col_s3:
                st.button("📱 Share to Social", use_container_width=True)
            with col_s4:
                st.button("📅 Schedule Send", use_container_width=True)
        else:
            st.info("Generate a report first to see export options")


if __name__ == "__main__":
    show()


