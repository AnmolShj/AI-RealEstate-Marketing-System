"""
AI Listing Generator Page
Generates professional property listings in multiple formats
"""

import streamlit as st
import os
from app.utils.openai_client import ContentGenerator


def show():
    """Display the Listing Generator page"""
    
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="font-size: 2.5rem; margin-bottom: 10px;">📝 AI Listing Generator</h1>
        <p style="color: #8899A6; font-size: 1.1rem;">
            Generate SEO-optimized MLS listings, social media captions, and marketing copy in seconds
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not os.getenv('OPENAI_API_KEY'):
        st.warning("⚠️ Please configure your OpenAI API key in the .env file to use AI features.")
    
    col1, col2 = st.columns([1, 1.5], gap="large")
    
    with col1:
        st.markdown("### 🏠 Property Information")
        
        address = st.text_input("Property Address", placeholder="123 Main Street, Kitchener, ON")
        
        col_a, col_b = st.columns(2)
        with col_a:
            price = st.text_input("Price", placeholder="$799,000")
            sqft = st.text_input("Square Feet", placeholder="2,500")
        with col_b:
            bedrooms = st.selectbox("Bedrooms", ["1", "2", "3", "4", "5", "6+"], index=2)
            bathrooms = st.selectbox("Bathrooms", ["1", "1.5", "2", "2.5", "3", "3.5", "4+"], index=2)
        
        year_built = st.text_input("Year Built", placeholder="2018")
        property_type = st.selectbox("Property Type", ["Single Family", "Condo", "Townhouse", "Multi-Family", "Land", "Commercial"])
        
        st.markdown("#### ✨ Key Features")
        features = st.text_area("Features (one per line)", placeholder="• Open concept kitchen with quartz countertops\n• Hardwood floors throughout\n• Finished basement\n• Large private backyard\n• Double attached garage")
        
        neighborhood = st.text_input("Neighborhood/Area", placeholder="Family-friendly neighborhood")
        
        generate_btn = st.button("✨ Generate Listings", use_container_width=True, disabled=not address)
    
    with col2:
        st.markdown("### 📄 Generated Listings")
        
        if generate_btn and address:
            with st.spinner("🤖 AI is generating your listings..."):
                property_details = {
                    'address': address, 'price': price, 'bedrooms': bedrooms, 'bathrooms': bathrooms,
                    'sqft': sqft, 'year_built': year_built, 'features': features, 'neighborhood': neighborhood,
                    'property_type': property_type
                }
                
                content_gen = ContentGenerator()
                
                output_tabs = st.tabs(["📋 MLS Listing", "📸 Instagram", "📘 Facebook", "📧 Email", "🌐 Website"])
                
                with output_tabs[0]:
                    mls_content = content_gen.generate_listing_description(property_details, 'mls')
                    st.text_area("MLS Description", value=mls_content, height=400, key="mls_output")
                    st.button("📋 Copy MLS Listing", key="copy_mls")
                
                with output_tabs[1]:
                    ig_content = content_gen.generate_listing_description(property_details, 'instagram')
                    st.text_area("Instagram Caption", value=ig_content, height=200, key="ig_output")
                    st.button("📋 Copy Instagram", key="copy_ig")
                    captions = content_gen.generate_captions(property_details, 'instagram')
                    if 'hashtags' in captions:
                        st.code(captions['hashtags'], language=None)
                        st.button("📋 Copy Hashtags", key="copy_hash")
                
                with output_tabs[2]:
                    fb_content = content_gen.generate_listing_description(property_details, 'facebook')
                    st.text_area("Facebook Post", value=fb_content, height=150, key="fb_output")
                    st.button("📋 Copy Facebook", key="copy_fb")
                
                with output_tabs[3]:
                    email_content = content_gen.generate_listing_description(property_details, 'email')
                    st.text_area("Email Newsletter", value=email_content, height=300, key="email_output")
                    st.button("📋 Copy Email", key="copy_email")
                
                with output_tabs[4]:
                    website_content = content_gen.generate_listing_description(property_details, 'website')
                    st.text_area("Website Listing", value=website_content, height=350, key="website_output")
                    st.button("📋 Copy Website", key="copy_website")
                
                st.markdown("---")
                st.markdown("### 📊 Quick Stats")
                
                col_s1, col_s2, col_s3 = st.columns(3)
                with col_s1:
                    st.metric("Word Count", len(mls_content.split()))
                with col_s2:
                    st.metric("Characters", len(mls_content))
                with col_s3:
                    st.metric("Formats", "5")
        
        else:
            st.info("👆 Enter property details and click Generate to create listings")
            
            st.markdown("### 📝 Example Output")
            st.markdown("""
            <div style="background: #192734; padding: 20px; border-radius: 12px;">
                <h4 style="margin-top: 0;">123 Main Street, Kitchener, ON</h4>
                <p style="color: #8899A6;">
                    Welcome to this stunning 3-bedroom, 2-bathroom home in the heart of Kitchener. 
                    Featuring an open concept layout, modern kitchen with quartz countertops, 
                    and hardwood floors throughout. The spacious backyard is perfect for entertaining.
                </p>
                <p><strong>Price:</strong> $799,000</p>
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    show()


