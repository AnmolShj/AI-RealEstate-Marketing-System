"""
ElevenLabs TTS for RealEstateAI
Handles voice generation for video voiceovers
"""

import os
import io
from typing import Optional, Dict, List
from pathlib import Path
import tempfile
import requests


class ElevenLabsTTS:
    """Text-to-Speech using ElevenLabs API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('ELEVENLABS_API_KEY')
        self.base_url = "https://api.elevenlabs.io/v1"
        self.default_voice_id = "21m00Tcm4TlvDq8ikWAM"
        
        self.voice_options = {
            "rachel": {"id": "21m00Tcm4TlvDq8ikWAM", "name": "Rachel", "description": "Professional, clear voice"},
            "domi": {"id": "9TB06NFCi1IGKhh3dake", "name": "Domi", "description": "Strong, confident voice"},
            "bella": {"id": "EXAVITQ4l9Jri6aw3aF3", "name": "Bella", "description": "Warm, friendly voice"},
            "arnold": {"id": "pNInz6obpgDQGcFmaJgB", "name": "Arnold", "description": "Deep, authoritative voice"}
        }
    
    def generate_speech(self, text: str, voice_id: Optional[str] = None, output_filename: str = "voiceover.mp3", stability: float = 0.5, similarity_boost: float = 0.75) -> str:
        """Generate speech from text"""
        
        if not self.api_key:
            return self._generate_placeholder_audio(text, output_filename)
        
        voice_key = voice_id or "rachel"
        voice = self.voice_options.get(voice_key, self.voice_options["rachel"])
        
        url = f"{self.base_url}/text-to-speech/{voice['id']}"
        
        headers = {"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": self.api_key}
        
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {"stability": stability, "similarity_boost": similarity_boost}
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                output_dir = tempfile.gettempdir()
                output_path = os.path.join(output_dir, output_filename)
                
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                
                return output_path
        except Exception as e:
            print(f"Error: {e}")
        
        return self._generate_placeholder_audio(text, output_filename)
    
    def generate_property_voiceover(self, property_details: Dict, voice_id: str = "rachel", style: str = "cinematic") -> str:
        """Generate voiceover for property reel"""
        
        if style == "cinematic":
            script = f"Welcome to {property_details.get('address', 'this property')}. This stunning home features {property_details.get('bedrooms', '3')} bedrooms and {property_details.get('bathrooms', '2')} bathrooms. {property_details.get('features', 'Beautiful property, must see!')} Priced at {property_details.get('price', '')}. Don't miss this opportunity. Schedule your showing today."
        elif style == "modern":
            script = f"Check out {property_details.get('address', 'this property')}. Asking {property_details.get('price', '')}. Beautiful property. Must see!"
        else:
            script = f"Just listed! {property_details.get('address', 'this amazing property')}. {property_details.get('bedrooms', '3')} bed, {property_details.get('bathrooms', '2')} bath! Priced at {property_details.get('price', '')}. This one won't last! Call now!"
        
        return self.generate_speech(text=script, voice_id=voice_id, output_filename="property_voiceover.mp3")
    
    def _generate_placeholder_audio(self, text: str, filename: str) -> str:
        """Generate placeholder when API is not available"""
        output_dir = tempfile.gettempdir()
        output_path = os.path.join(output_dir, filename)
        
        with open(output_path, 'wb') as f:
            f.write(b'')
        
        return output_path
    
    def list_available_voices(self) -> List[Dict]:
        """List all available voices"""
        return [
            {"key": k, "name": v["name"], "description": v["description"]}
            for k, v in self.voice_options.items()
        ]


def generate_property_voiceover(property_details: Dict, voice: str = "rachel", style: str = "cinematic") -> str:
    """Quick utility to generate property voiceover"""
    tts = ElevenLabsTTS()
    return tts.generate_property_voiceover(property_details, voice, style)


def generate_speech_from_text(text: str, voice: str = "rachel") -> str:
    """Quick utility to generate speech from text"""
    tts = ElevenLabsTTS()
    return tts.generate_speech(text, voice)


