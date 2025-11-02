"""
Cloudinary service for image upload and management.

Handles uploading, deleting, and transforming images via Cloudinary API.
"""

import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary.utils import cloudinary_url

class CloudinaryService:
    """Service for interacting with Cloudinary API."""
    
    def __init__(self):
        """Initialize Cloudinary with credentials from environment."""
        cloudinary.config(
            cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
            api_key=os.getenv("CLOUDINARY_API_KEY"),
            api_secret=os.getenv("CLOUDINARY_API_SECRET"),
            secure=True
        )
    
    def upload_image(self, file, folder="portfolio", public_id=None):
        """
        Upload an image to Cloudinary.
        
        Args:
            file: File object or file path
            folder: Cloudinary folder (default: "portfolio")
            public_id: Custom public ID (optional, auto-generated if not provided)
        
        Returns:
            dict: Upload result with URL and metadata
        """
        try:
            options = {
                "folder": folder,
                "resource_type": "image",
            }
            
            if public_id:
                options["public_id"] = public_id
            
            result = cloudinary.uploader.upload(file, **options)
            
            return {
                "success": True,
                "url": result.get("secure_url"),
                "public_id": result.get("public_id"),
                "format": result.get("format"),
                "width": result.get("width"),
                "height": result.get("height"),
                "size": result.get("bytes")
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def delete_image(self, public_id):
        """
        Delete an image from Cloudinary.
        
        Args:
            public_id: Public ID of the image to delete
        
        Returns:
            dict: Deletion result
        """
        try:
            result = cloudinary.uploader.destroy(public_id)
            return {
                "success": result.get("result") == "ok",
                "result": result.get("result")
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_optimized_url(self, public_id, width=None, height=None, crop="auto", quality="auto"):
        """
        Get an optimized URL for an image with transformations.
        
        Args:
            public_id: Public ID of the image
            width: Target width (optional)
            height: Target height (optional)
            crop: Crop mode (default: "auto")
            quality: Quality setting (default: "auto")
        
        Returns:
            str: Optimized image URL
        """
        options = {
            "fetch_format": "auto",
            "quality": quality
        }
        
        if width:
            options["width"] = width
        if height:
            options["height"] = height
        if width or height:
            options["crop"] = crop
            options["gravity"] = "auto"
        
        url, _ = cloudinary_url(public_id, **options)
        return url
    
    def get_responsive_url(self, public_id, sizes=None):
        """
        Get responsive image URLs for different screen sizes.
        
        Args:
            public_id: Public ID of the image
            sizes: Dict of size names and widths (default: common breakpoints)
        
        Returns:
            dict: URLs for different sizes
        """
        if sizes is None:
            sizes = {
                "thumbnail": 300,
                "mobile": 640,
                "tablet": 1024,
                "desktop": 1920
            }
        
        urls = {}
        for name, width in sizes.items():
            urls[name] = self.get_optimized_url(public_id, width=width)
        
        return urls
    
    def extract_public_id(self, cloudinary_url):
        """
        Extract public ID from a Cloudinary URL.
        
        Args:
            cloudinary_url: Full Cloudinary URL
        
        Returns:
            str: Public ID or None
        """
        try:
            # URL format: https://res.cloudinary.com/cloud_name/image/upload/v123456/folder/image.jpg
            parts = cloudinary_url.split("/upload/")
            if len(parts) == 2:
                path = parts[1]
                # Remove version if present
                if path.startswith("v"):
                    path = "/".join(path.split("/")[1:])
                # Remove file extension
                public_id = path.rsplit(".", 1)[0]
                return public_id
        except Exception:
            pass
        return None


# Singleton instance
cloudinary_service = CloudinaryService()

