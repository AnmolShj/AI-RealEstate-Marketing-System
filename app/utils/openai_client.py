"""
OpenAI Client for RealEstateAI
Handles script generation, captions, and content creation
"""

import os
import openai
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')


class ContentGenerator:
    """AI-powered content generation for real estate"""
    
    def __init__(self):
        self.model = "gpt-4-turbo-preview"
    
    def generate_reel_script(self, property_details: Dict, style: str = "cinematic", duration: int = 30) -> str:
        """Generate a script for real estate reel from property details"""
        
        prompt = f"""Create a {duration}-second engaging real estate video script for a property with the following details:

Property Address: {property_details.get('address', 'N/A')}
Price: {property_details.get('price', 'N/A')}
Bedrooms: {property_details.get('bedrooms', 'N/A')}
Bathrooms: {property_details.get('bathrooms', 'N/A')}
Key Features: {property_details.get('features', 'N/A')}

Style: {style}

Create a compelling, concise script that:
1. Opens with an attention-grabbing hook
2. Highlights key property features
3. Ends with a call to action
4. Is conversational and enthusiastic
5. Can be spoken in approximately {duration} seconds

Script:"""

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert real estate content creator. Create engaging, sales-driven scripts for property videos."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Welcome to this beautiful property! This stunning home features {property_details.get('bedrooms', '3')} bedrooms and {property_details.get('bathrooms', '2')} bathrooms. Don't miss this incredible opportunity!"
    
    def generate_listing_description(self, property_details: Dict, listing_type: str = "mls") -> str:
        """Generate property listing description"""
        
        listing_types = {
            "mls": "Professional MLS listing description (300-500 words, SEO-optimized, factual)",
            "instagram": "Engaging Instagram caption (2200 char max, with emojis, hashtags)",
            "facebook": "Facebook ad copy (short and compelling)",
            "email": "Email newsletter format (warm, inviting)",
            "website": "Website listing page (detailed, SEO-optimized)"
        }
        
        prompt = f"""Generate a {listing_types.get(listing_type, listing_type)} listing description for:

Address: {property_details.get('address', 'N/A')}
Price: {property_details.get('price', 'N/A')}
Bedrooms: {property_details.get('bedrooms', 'N/A')}
Bathrooms: {property_details.get('bathrooms', 'N/A')}
Square Feet: {property_details.get('sqft', 'N/A')}
Features: {property_details.get('features', 'N/A')}
Neighborhood: {property_details.get('neighborhood', 'N/A')}

Make it compelling, accurate, and tailored to the specified format."""

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert real estate copywriter. Create compelling property descriptions that sell."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Beautiful property located at {property_details.get('address', 'N/A')}. This stunning home features {property_details.get('bedrooms', '3')} bedrooms and {property_details.get('bathrooms', '2')} bathrooms. {property_details.get('features', 'Must see!')}"
    
    def generate_captions(self, property_details: Dict, platform: str = "instagram") -> Dict[str, str]:
        """Generate social media captions for multiple platforms"""
        
        prompt = f"""Generate engaging social media captions for a property listing:

Property: {property_details.get('address', 'N/A')}
Price: {property_details.get('price', 'N/A')}
Features: {property_details.get('features', 'N/A')}

Create:
1. A catchy headline (max 10 words)
2. Main caption (compelling, {platform}-appropriate)
3. 10-15 relevant hashtags
4. Call to action"""

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a social media expert for real estate. Create viral-worthy content."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=500
            )
            return {
                "headline": "Amazing Property!",
                "caption": response.choices[0].message.content.strip(),
                "hashtags": "#realestate #homesweethome #property #realestateagent #luxuryhomes",
                "call_to_action": "Schedule a viewing today!"
            }
        except Exception as e:
            return {
                "headline": "Stunning Property!",
                "caption": f"Check out this amazing property at {property_details.get('address', 'N/A')}!",
                "hashtags": "#realestate #property #homesweethome",
                "call_to_action": "DM for more info!"
            }
    
    def generate_lead_response(self, lead_message: str, property_details: Optional[Dict] = None, context: str = "initial_inquiry") -> str:
        """Generate AI response to lead inquiry"""
        
        property_info = ""
        if property_details:
            property_info = f"""
Property Details:
- Address: {property_details.get('address', 'N/A')}
- Price: {property_details.get('price', 'N/A')}
- Status: {property_details.get('status', 'Available')}
"""
        
        prompt = f"""Generate a professional, friendly response to this lead inquiry:

Lead Message: {lead_message}
Context: {context}
{property_info}

The response should:
1. Be warm and professional
2. Answer the question asked
3. Qualify the lead if needed
4. Include a clear call to action
5. Be concise (under 150 words)"""

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional real estate assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return "Thank you for your interest! I'd be happy to help. Could you tell me more about what you're looking for?"


def quick_script(address: str, price: str, features: str) -> str:
    """Quick utility function to generate a reel script"""
    generator = ContentGenerator()
    details = {'address': address, 'price': price, 'features': features, 'bedrooms': '', 'bathrooms': ''}
    return generator.generate_reel_script(details)


def quick_listing(address: str, price: str, bedrooms: str, bathrooms: str, features: str) -> Dict[str, str]:
    """Quick utility function to generate listings for all formats"""
    generator = ContentGenerator()
    details = {'address': address, 'price': price, 'bedrooms': bedrooms, 'bathrooms': bathrooms, 'features': features}
    
    return {
        'mls': generator.generate_listing_description(details, 'mls'),
        'instagram': generator.generate_listing_description(details, 'instagram'),
        'facebook': generator.generate_listing_description(details, 'facebook'),
        'email': generator.generate_listing_description(details, 'email'),
        'website': generator.generate_listing_description(details, 'website')
    }


