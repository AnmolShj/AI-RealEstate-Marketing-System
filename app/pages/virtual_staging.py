"""
AI Virtual Staging Page
Transforms empty rooms into beautifully furnished spaces using AI
"""

import streamlit as st
import os
import tempfile
from app.utils.image_processor import ImageProcessor


def show():
    """Display the Virtual Staging page"""
    
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="font-size: 2.5rem; margin-bottom: 10px;">🪑 AI Virtual Staging</h1>
        <p style="color: #8899A6; font-size: 1.1rem;">
            Transform empty rooms into beautifully furnished spaces. Sell homes faster with AI-powered virtual staging.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💰 Pricing: $10-30 per room. Free for first 3 rooms!")
    
    tab1, tab2, tab3 = st.tabs(["📤 Upload", "🎨 Configure", "📸 Results"])
    
    with tab1:
        st.markdown("### 📤 Upload Room Photos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            uploaded_file = st.file_uploader("Choose a room photo", type=['jpg', 'jpeg', 'png', 'webp'])
            
            if uploaded_file:
                st.image(uploaded_file, caption="Original Room", use_container_width=True)
                
                processor = ImageProcessor()
                
                temp_dir = tempfile.mkdtemp()
                temp_path = os.path.join(temp_dir, uploaded_file.name)
                with open(temp_path, 'wb') as f:
                    f.write(uploaded_file.getvalue())
                
                analysis = processor.analyze_image_content(temp_path)
                
                st.markdown("#### 📊 Image Analysis")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Detected Type", analysis.get('room_type', 'Unknown'))
                    st.metric("Quality Score", analysis.get('quality_score', 'Unknown'))
                with col_b:
                    st.metric("Dimensions", f"{analysis.get('width', 0)}x{analysis.get('height', 0)}")
                    likely_empty = "Yes - Perfect for staging!" if analysis.get('likely_empty') else "No - May already be furnished"
                    st.metric("Likely Empty", likely_empty)
        
        with col2:
            st.markdown("### 💡 Tips for Best Results")
            st.markdown("""
            - **Use horizontal photos** - Works better than vertical
            - **Good lighting** - Natural light produces best results
            - **Empty rooms** - Should have minimal furniture
            - **Show the space** - Capture the full room
            """)
            
            st.markdown("### 📐 Supported Room Types")
            st.markdown("""
            - Living Room
            - Bedroom
            - Kitchen
            - Dining Room
            - Bathroom
            - Home Office
            """)
    
    with tab2:
        st.markdown("### 🎨 Staging Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            room_type = st.selectbox("Room Type", ["Living Room", "Bedroom", "Kitchen", "Dining Room", "Bathroom", "Home Office", "Nursery", "Basement"], index=0)
            style = st.selectbox("Furniture Style", ["Modern", "Traditional", "Minimalist", "Scandinavian", "Industrial", "Farmhouse", "Luxury"], index=0)
        
        with col2:
            color_scheme = st.selectbox("Color Scheme", ["Neutral (Beige/Gray)", "Warm (Earth Tones)", "Cool (Blue/Green)", "Bold (Dark Colors)", "Bright (White/Light)"], index=0)
            mood = st.selectbox("Mood/Ambiance", ["Cozy & Inviting", "Bright & Airy", "Elegant & Sophisticated", "Modern & Sleek", "Family-Friendly"], index=0)
        
        with st.expander("⚙️ Advanced Options"):
            quality = st.select_slider("Output Quality", options=["Standard", "High", "Ultra"], value="High")
            include_artwork = st.toggle("Include Wall Art", value=True)
            include_accessories = st.toggle("Include Accessories", value=True)
        
        st.markdown("---")
        
        col_g1, col_g2, col_g3 = st.columns([1, 2, 1])
        with col_g2:
            stage_btn = st.button("🎨 Stage This Room", use_container_width=True, disabled=not uploaded_file)
    
    with tab3:
        st.markdown("### 📸 Staging Results")
        
        if stage_btn and uploaded_file:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.text("🎨 Analyzing room...")
                progress_bar.progress(25)
                
                status_text.text("🏠 Generating furniture...")
                progress_bar.progress(50)
                
                status_text.text("✨ Applying AI enhancements...")
                progress_bar.progress(75)
                
                status_text.text("💾 Finalizing images...")
                progress_bar.progress(100)
                
                st.success("✅ Virtual staging complete!")
                
                st.markdown("#### Before & After")
                
                col_before, col_after = st.columns(2)
                with col_before:
                    st.markdown("**Original (Empty)**")
                    st.image(uploaded_file, use_container_width=True)
                with col_after:
                    st.markdown("**Staged Result**")
                    st.info("🎨 In production, this would show the AI-staged image using Stable Diffusion + ControlNet")
                    st.image(uploaded_file, caption="Staged Preview", use_container_width=True)
                
                st.markdown("---")
                st.markdown("### ⬇️ Download Options")
                
                col_d1, col_d2, col_d3 = st.columns(3)
                with col_d1:
                    st.button("📥 Download Staged Image", use_container_width=True)
                with col_d2:
                    st.button("📥 Download High-Res", use_container_width=True)
                with col_d3:
                    st.button("📥 Download All Styles", use_container_width=True)
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.info("👆 Upload a room photo and click Stage This Room to see results")
            
            st.markdown("### 🎨 Available Styles")
            
            styles = [
                ("Modern", "Sleek, contemporary furniture with clean lines"),
                ("Traditional", "Classic furniture with warm, rich colors"),
                ("Minimalist", "Clean, uncluttered spaces with essential furniture"),
                ("Scandinavian", "Light wood, white accents, cozy textures"),
                ("Industrial", "Exposed elements, metal, concrete textures")
            ]
            
            for style_name, desc in styles:
                st.markdown(f"**{style_name}**: {desc}")


if __name__ == "__main__":
    show()


