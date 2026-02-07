from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

router = APIRouter()

class DeleteByUrl(BaseModel):
    url: str

@router.delete('/cloudinary/delete-by-url')
async def delete_by_url(data: DeleteByUrl):
    """
    Delete a file from Cloudinary using the secure_url
    Expects JSON body with:
    {
        "url": "https://res.cloudinary.com/xxx/video/upload/v123456/consultations/file.webm"
    }
    """
    try:
        url = data.url
        
        # Extract public_id from URL
        # Example URL: https://res.cloudinary.com/xxx/video/upload/v123456/consultations/file.webm
        parts = url.split('/upload/')
        if len(parts) < 2:
            raise HTTPException(status_code=400, detail="Invalid Cloudinary URL")
        
        # Get the part after /upload/
        path_parts = parts[1].split('/')
        
        # Remove version (v123456) if present
        if path_parts[0].startswith('v'):
            path_parts = path_parts[1:]
        
        # Join the remaining parts and remove file extension
        public_id = '/'.join(path_parts).rsplit('.', 1)[0]
        
        # Determine resource type from URL
        resource_type = 'video'  # default
        if '/image/' in url:
            resource_type = 'image'
        elif '/raw/' in url:
            resource_type = 'raw'
        
        # Delete from Cloudinary
        result = cloudinary.uploader.destroy(
            public_id,
            resource_type=resource_type,
            invalidate=True
        )
        
        if result.get('result') == 'ok':
            return {
                "success": True,
                "message": "File deleted successfully",
                "public_id": public_id,
                "result": result
            }
        elif result.get('result') == 'not found':
            raise HTTPException(
                status_code=404,
                detail=f"File not found: {public_id}"
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to delete file: {result}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting file by URL: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Server error while deleting file: {str(e)}"
        )