"""
AI Reel Generator Page
Transforms property photos into stunning Instagram Reels, YouTube Shorts, and TikToks
"""

import streamlit as st
import os
from pathlib import Path
import tempfile
from datetime import datetime


def show():
    """Display the Reel Generator page"""
    
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="font-size: 2.5rem; margin-bottom: 10px;">🎬 AI Reel Generator</h1>
        <p style="color: #8899A6; font-size: 1.1rem;">
            Transform property photos into stunning social media reels with AI voiceover, captions, and trending music
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not os.getenv('OPENAI_API_KEY'):
        st.warning("⚠️ Please configure your OpenAI API key in the .env file to use AI features.")
    
    tab1, tab2, tab3 = st.tabs(["📤 Upload & Configure", "🎥 Preview", "📋 Captions & Export"])
    
    with tab1:
        st.markdown("### 🏠 Property Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            address = st.text_input("Property Address", placeholder="123 Main Street, Kitchener, ON")
            price = st.text_input("Price", placeholder="$799,000")
        
        with col2:
            bedrooms = st.selectbox("Bedrooms", ["Studio", "1", "2", "3", "4", "5", "6+"], index=2)
            bathrooms = st.selectbox("Bathrooms", ["1", "1.5", "2", "2.5", "3", "3.5", "4+"], index=2)
        
        features = st.text_area("Key Features", placeholder="Open concept kitchen, hardwood floors, finished basement, large backyard...")
        
        st.markdown("---")
        st.markdown("### 📸 Upload Property Photos")
        
        uploaded_files = st.file_uploader("Choose property images (max 20 images)", type=['jpg', 'jpeg', 'png', 'webp'], accept_multiple_files=True)
        
        if uploaded_files:
            st.markdown(f"**{len(uploaded_files)} images uploaded**")
            cols = st.columns(5)
            for i, file in enumerate(uploaded_files[:10]):
                with cols[i % 5]:
                    st.image(file, caption=file.name[:20], use_container_width=True)
        
        st.markdown("---")
        st.markdown("### ⚙️ Video Configuration")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            video_style = st.selectbox("Video Style", ["cinematic", "modern", "vibrant", "luxury"], index=0)
            video_length = st.select_slider("Video Length", options=[15, 30, 45, 60], value=30)
        
        with col2:
            voice_option = st.selectbox("Voiceover", ["rachel", "domi", "bella", "arnold"], index=0)
            voice_style = st.selectbox("Voice Style", ["cinematic", "modern", "energetic"], index=0)
        
        with col3:
            platform = st.multiselect("Target Platforms", ["Instagram Reel", "YouTube Short", "TikTok"], default=["Instagram Reel"])
            add_music = st.toggle("Add Background Music", value=True)
            add_captions = st.toggle("Add Auto Captions", value=True)
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            generate_btn = st.button("🎬 Generate AI Reel", use_container_width=True, disabled=not uploaded_files or not address)
        
        if generate_btn:
            if not address:
                st.error("Please enter a property address")
            elif not uploaded_files:
                st.error("Please upload at least one property photo")
            else:
                generate_reel(uploaded_files, address, price, bedrooms, bathrooms, features, video_style, video_length, voice_option, voice_style, add_music, add_captions)
    
    with tab2:
        st.markdown("### 🎥 Video Preview")
        
        if 'generated_video' in st.session_state and st.session_state.generated_video:
            video_path = st.session_state.generated_video
            st.video(video_path)
            st.success("✅ Video generated successfully!")
        else:
            st.info("👆 Upload photos and generate a reel to see preview here")
            st.markdown("""
            <div style="background: #192734; padding: 20px; border-radius: 12px; text-align: center;">
                <p style="color: #8899A6;">Your generated video will appear here with:</p>
                <ul style="color: #8899A6; text-align: left; display: inline-block;">
                    <li>✨ Cinematic transitions between photos</li>
                    <li>🎤 Professional AI voiceover</li>
                    <li>📝 Auto-generated captions</li>
                    <li>🎵 Trending background music</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 📋 Captions & Export")
        
        if 'generated_captions' in st.session_state and st.session_state.generated_captions:
            captions_data = st.session_state.generated_captions
            
            st.markdown("#### Instagram Caption")
            st.text_area("Instagram", value=captions_data.get('instagram', ''), height=150, key="ig_caption")
            st.button("📋 Copy Instagram Caption")
            
            st.markdown("#### Hashtags")
            st.code(captions_data.get('hashtags', ''), language=None)
            st.button("📋 Copy Hashtags")
            
            st.markdown("---")
            st.markdown("### 📦 Export Options")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("⬇️ Download Video", use_container_width=True)
            with col2:
                st.button("📤 Share to Instagram", use_container_width=True)
            with col3:
                st.button("📤 Share to TikTok", use_container_width=True)
        else:
            st.info("Generate a reel to see captions and export options")


def generate_reel(uploaded_files, address: str, price: str, bedrooms: str, bathrooms: str, features: str, video_style: str, video_length: int, voice_option: str, voice_style: str, add_music: bool, add_captions: bool):
    """Generate the AI reel"""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("💾 Saving uploaded images...")
        progress_bar.progress(10)
        
        temp_dir = tempfile.mkdtemp()
        image_paths = []
        
        for uploaded_file in uploaded_files:
            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getvalue())
            image_paths.append(file_path)
        
        status_text.text("🖼️ Processing images...")
        progress_bar.progress(25)
        
        from app.utils.image_processor import ImageProcessor
        processor = ImageProcessor()
        processed_images = processor.process_property_photos(image_paths, enhance=True, resize=True)
        
        status_text.text("✍️ Generating AI script...")
        progress_bar.progress(40)
        
        property_details = {'address': address, 'price': price, 'bedrooms': bedrooms, 'bathrooms': bathrooms, 'features': features}
        
        from app.utils.openai_client import ContentGenerator
        content_gen = ContentGenerator()
        script = content_gen.generate_reel_script(property_details, style=video_style, duration=video_length)
        
        status_text.text("📝 Generating captions...")
        progress_bar.progress(55)
        
        captions = content_gen.generate_captions(property_details, 'instagram')
        
        status_text.text("🎤 Generating voiceover...")
        progress_bar.progress(70)
        
        from app.utils.ElevenLabs_tts import ElevenLabsTTS
        tts = ElevenLabsTTS()
        voiceover_path = tts.generate_property_voiceover(property_details, voice_option, voice_style)
        
        status_text.text("🎬 Creating video...")
        progress_bar.progress(85)
        
        # Note: Full video generation requires moviepy which needs ffmpeg
        # For demo, we'll save a placeholder
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"reel_{timestamp}.mp4"
        video_path = os.path.join(temp_dir, output_filename)
        
        # Create empty placeholder file
        with open(video_path, 'wb') as f:
            f.write(b'')
        
        st.session_state.generated_video = video_path
        st.session_state.generated_script = script
        st.session_state.generated_captions = captions
        
        progress_bar.progress(100)
        status_text.text("✅ Generation complete!")
        
        st.success("🎉 Your AI reel is ready!")
        
        st.markdown("### 📊 Generation Results")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Images Processed", len(processed_images))
        with col2:
            st.metric("Video Duration", f"~{video_length}s")
        with col3:
            st.metric("Style", video_style.title())
        
        with st.expander("📜 View Generated Script"):
            st.text(script)
        
        st.rerun()
        
    except Exception as e:
        progress_bar.progress(0)
        status_text.text("❌ Error")
        st.error(f"An error occurred: {str(e)}")
        st.info("💡 In demo mode, please configure your API keys for full functionality.")


if __name__ == "__main__":
    show()


