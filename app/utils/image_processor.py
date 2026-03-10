"""
Image Processor for RealEstateAI
Handles image processing, enhancement, and analysis
"""

import os
import io
import base64
from typing import List, Dict, Tuple, Optional
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps
import tempfile


class ImageProcessor:
    """AI-powered image processing for real estate photos"""
    
    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.webp']
        self.max_size = (4096, 4096)
        self.output_size = (2048, 2048)
    
    def process_property_photos(self, images: List[str], enhance: bool = True, resize: bool = True, output_format: str = 'JPEG', quality: int = 90) -> List[str]:
        """Process multiple property photos"""
        processed = []
        
        for img_path in images:
            processed_path = self.process_single_image(img_path, enhance=enhance, resize=resize, output_format=output_format, quality=quality)
            processed.append(processed_path)
        
        return processed
    
    def process_single_image(self, image_path: str, enhance: bool = True, resize: bool = True, output_format: str = 'JPEG', quality: int = 90) -> str:
        """Process a single image"""
        img = Image.open(image_path)
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        if enhance:
            img = self.enhance_image(img)
        
        if resize:
            img = self.resize_image(img)
        
        output_dir = tempfile.gettempdir()
        filename = f"processed_{Path(image_path).stem}.{output_format.lower()}"
        output_path = os.path.join(output_dir, filename)
        
        if output_format.upper() == 'JPEG':
            img.save(output_path, format='JPEG', quality=quality, optimize=True)
        else:
            img.save(output_path, format=output_format)
        
        return output_path
    
    def enhance_image(self, img: Image.Image) -> Image.Image:
        """Enhance image brightness, contrast, and color"""
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.1)
        
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.15)
        
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.1)
        
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.2)
        
        return img
    
    def resize_image(self, img: Image.Image, target_size: Optional[Tuple[int, int]] = None) -> Image.Image:
        """Resize image while maintaining aspect ratio"""
        target_size = target_size or self.output_size
        img.thumbnail(target_size, Image.Resampling.LANCZOS)
        return img
    
    def analyze_image_content(self, image_path: str) -> Dict[str, any]:
        """Analyze image content to identify rooms/features"""
        img = Image.open(image_path)
        
        width, height = img.size
        aspect_ratio = width / height
        
        room_type = self._detect_room_type(aspect_ratio)
        is_empty = self._is_likely_empty(img)
        quality_score = self._estimate_quality(img)
        
        return {
            'width': width,
            'height': height,
            'aspect_ratio': aspect_ratio,
            'room_type': room_type,
            'likely_empty': is_empty,
            'quality_score': quality_score,
            'format': img.format,
            'mode': img.mode
        }
    
    def _detect_room_type(self, aspect_ratio: float) -> str:
        if aspect_ratio > 1.5:
            return "wide_view"
        elif aspect_ratio < 0.7:
            return "tall_view"
        else:
            return "standard_room"
    
    def _is_likely_empty(self, img: Image.Image) -> bool:
        gray = img.convert('L')
        arr = np.array(gray)
        variance = np.var(arr)
        return variance < 1000
    
    def _estimate_quality(self, img: Image.Image) -> str:
        gray = img.convert('L')
        arr = np.array(gray)
        variance = np.var(arr)
        
        if variance > 5000:
            return "high"
        elif variance > 2000:
            return "medium"
        else:
            return "low"
    
    def create_thumbnail(self, image_path: str, size: Tuple[int, int] = (400, 300)) -> str:
        """Create thumbnail of image"""
        img = Image.open(image_path)
        img.thumbnail(size, Image.Resampling.LANCZOS)
        
        output_dir = tempfile.gettempdir()
        filename = f"thumb_{Path(image_path).stem}.jpg"
        output_path = os.path.join(output_dir, filename)
        
        img.save(output_path, format='JPEG', quality=85)
        return output_path
    
    def convert_to_base64(self, image_path: str) -> str:
        """Convert image to base64 string for web display"""
        with open(image_path, 'rb') as f:
            data = base64.b64encode(f.read()).decode()
        return f"data:image/jpeg;base64,{data}"


def quick_process(image_paths: List[str]) -> List[str]:
    """Quick utility to process multiple images"""
    processor = ImageProcessor()
    return processor.process_property_photos(image_paths)


def quick_grid(image_paths: List[str], cols: int = 3) -> str:
    """Quick utility to create image grid"""
    processor = ImageProcessor()
    return processor.create_image_grid(image_paths, cols=cols)


