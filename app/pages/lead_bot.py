"""
AI Lead Follow-Up Bot Page
Multi-platform chatbot for instant lead response
"""

import streamlit as st
import os
from datetime import datetime
from app.utils.openai_client import ContentGenerator


def show():
    """Display the Lead Bot page"""
    
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="font-size: 2.5rem; margin-bottom: 10px;">💬 AI Lead Follow-Up Bot</h1>
        <p style="color: #8899A6; font-size: 1.1rem;">
            Never lose a lead again. AI-powered chatbot responds instantly across SMS, WhatsApp, Website, and Instagram.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["🤖 Configure Bot", "💬 Demo Chat", "📊 Settings", "📈 Analytics"])
    
    with tab1:
        st.markdown("### 🤖 Bot Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📱 Platform Settings")
            
            enable_sms = st.toggle("Enable SMS (Twilio)", value=True)
            enable_whatsapp = st.toggle("Enable WhatsApp", value=True)
            enable_website = st.toggle("Enable Website Chat", value=True)
            enable_instagram = st.toggle("Enable Instagram DM", value=False)
        
        with col2:
            st.markdown("#### ⚡ Response Settings")
            
            response_speed = st.selectbox("Response Speed", ["Instant", "Within 1 minute", "Within 5 minutes"], index=0)
            business_hours = st.selectbox("Response Mode", ["24/7 Always On", "Business Hours Only", "Agent Online Only"], index=0)
            fallback_to_agent = st.toggle("Escalate to Agent when needed", value=True)
        
        st.markdown("---")
        st.markdown("#### 📝 Auto-Response Templates")
        
        col_r1, col_r2 = st.columns(2)
        
        with col_r1:
            st.markdown("**Initial Inquiry Response**")
            initial_response = st.text_area("Response to 'Is this available?'", value="Yes, this property is still available! Would you like to schedule a showing this weekend?", height=80)
        
        with col_r2:
            st.markdown("**Quick Replies**")
            viewing_response = st.text_area("Response to showing request", value="I'd be happy to schedule a showing for you. What days/times work best?", height=80)
        
        st.markdown("---")
        save_btn = st.button("💾 Save Bot Settings", use_container_width=True)
        
        if save_btn:
            st.success("✅ Bot settings saved successfully!")
    
    with tab2:
        st.markdown("### 💬 Chat Demo")
        
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        st.markdown("#### 🏠 Property Context")
        
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            demo_address = st.text_input("Demo Property Address", value="123 Main Street, Kitchener")
            demo_price = st.text_input("Price", value="$799,000")
        with col_p2:
            demo_status = st.selectbox("Property Status", ["Available", "Under Offer", "Sold", "Coming Soon"], index=0)
            demo_bedrooms = st.selectbox("Bedrooms", ["2", "3", "4"], index=1)
        
        st.markdown("---")
        st.markdown("#### 💬 Chat Preview")
        
        chat_container = st.container()
        
        with chat_container:
            st.markdown("""
            <div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">
                <div style="background: #1E3A5F; color: white; padding: 12px 16px; border-radius: 16px 16px 16px 0; max-width: 70%;">
                    Hi! Welcome to RealEstateAI Assistant. How can I help you today?
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            for msg in st.session_state.chat_history:
                if msg['role'] == 'user':
                    st.markdown(f"""
                    <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
                        <div style="background: #2ECC71; color: white; padding: 12px 16px; border-radius: 16px 16px 0 16px; max-width: 70%;">
                            {msg['content']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">
                        <div style="background: #1E3A5F; color: white; padding: 12px 16px; border-radius: 16px 16px 16px 0; max-width: 70%;">
                            {msg['content']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("#### ⚡ Quick Responses")
        
        quick_responses = ["Is this house still available?", "Can I schedule a showing?", "What's the price?", "How many bedrooms?"]
        
        cols = st.columns(4)
        for i, resp in enumerate(quick_responses):
            with cols[i]:
                if st.button(resp, key=f"quick_{i}"):
                    st.session_state.chat_history.append({'role': 'user', 'content': resp, 'timestamp': datetime.now()})
                    
                    property_details = {'address': demo_address, 'price': demo_price, 'status': demo_status, 'bedrooms': demo_bedrooms}
                    content_gen = ContentGenerator()
                    ai_response = content_gen.generate_lead_response(resp, property_details, 'demo')
                    
                    st.session_state.chat_history.append({'role': 'assistant', 'content': ai_response, 'timestamp': datetime.now()})
                    st.rerun()
        
        custom_message = st.text_input("Type your own message...", placeholder="Ask about the property...")
        
        if st.button("Send") and custom_message:
            st.session_state.chat_history.append({'role': 'user', 'content': custom_message, 'timestamp': datetime.now()})
            
            property_details = {'address': demo_address, 'price': demo_price, 'status': demo_status, 'bedrooms': demo_bedrooms}
            content_gen = ContentGenerator()
            ai_response = content_gen.generate_lead_response(custom_message, property_details, 'demo')
            
            st.session_state.chat_history.append({'role': 'assistant', 'content': ai_response, 'timestamp': datetime.now()})
            st.rerun()
        
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
    
    with tab3:
        st.markdown("### ⚙️ Integration Settings")
        
        col_i1, col_i2 = st.columns(2)
        
        with col_i1:
            st.markdown("#### 🔗 CRM Integration")
            crm_provider = st.selectbox("CRM Provider", ["None", "Salesforce", "HubSpot", "Zoho", "Custom API"])
            if crm_provider != "None":
                api_key = st.text_input("API Key", type="password")
        
        with col_i2:
            st.markdown("#### 📧 Notification Settings")
            email_notifications = st.toggle("Email notifications for new leads", value=True)
            sms_notifications = st.toggle("SMS notifications for hot leads", value=True)
        
        st.markdown("---")
        
        st.markdown("#### 👤 Agent Profile")
        
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            agent_name = st.text_input("Agent Name", value="Your Name")
            agent_phone = st.text_input("Phone Number", value="+1 234 567 8900")
        with col_a2:
            agent_email = st.text_input("Email", value="agent@realestate.com")
        
        save_settings_btn = st.button("💾 Save All Settings", use_container_width=True)
        
        if save_settings_btn:
            st.success("✅ All settings saved!")
    
    with tab4:
        st.markdown("### 📈 Lead Bot Analytics")
        
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        
        with col_s1:
            st.metric("Total Leads", "127")
        with col_s2:
            st.metric("Replied Instantly", "98%")
        with col_s3:
            st.metric("Scheduled Showings", "34")
        with col_s4:
            st.metric("Conversion Rate", "27%")
        
        st.markdown("---")
        
        st.markdown("#### 📊 Lead Sources")
        
        sources_data = {"Website": 45, "SMS": 32, "WhatsApp": 28, "Instagram": 22}
        
        for source, count in sources_data.items():
            st.markdown(f"**{source}**: {count} leads ({count/127*100:.0f}%)")
            st.progress(count/127)
        
        st.markdown("---")
        
        st.markdown("#### 👥 Recent Leads")
        
        leads_data = [
            {"name": "John D.", "source": "Website", "time": "2 min ago", "status": "Hot"},
            {"name": "Sarah M.", "source": "WhatsApp", "time": "15 min ago", "status": "Warm"},
            {"name": "Mike R.", "source": "SMS", "time": "1 hour ago", "status": "Scheduled"}
        ]
        
        for lead in leads_data:
            col_l1, col_l2, col_l3, col_l4 = st.columns([2, 2, 2, 1])
            with col_l1:
                st.write(f"**{lead['name']}**")
            with col_l2:
                st.write(lead['source'])
            with col_l3:
                st.write(lead['time'])
            with col_l4:
                status_color = "🟢" if lead['status'] == "Hot" else "🟡" if lead['status'] == "Warm" else "🔵"
                st.write(f"{status_color} {lead['status']}")


if __name__ == "__main__":
    show()


