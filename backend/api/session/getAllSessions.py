from fastapi import APIRouter, HTTPException
from bson import ObjectId
from db.mongo_client import sessions_collection

router = APIRouter()

@router.get("/get-all-sessions", 
            summary="Get all active sessions for a user",
            description="Returns a list of all active sessions for the authenticated user, including device, browser, OS, and last active time.")
def list_sessions(user_id: str):  # Removed 'async'
    try:
        # Validate ObjectId
        try:
            user_object_id = ObjectId(user_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid user_id format")
        
        # Synchronous find - no await needed
        sessions = list(sessions_collection.find({
            "user_id": user_object_id,
            "revoked": False
        }))
        
        # Format the data
        data = [
            {
                "id": str(s["_id"]),
                "device": s.get("device", "Unknown"),
                "browser": s.get("browser", "Unknown"),
                "os": s.get("os", "Unknown"),
                "last_active": s.get("last_active")
            }
            for s in sessions
        ]
        
        return {"status": "success", "data": data, "count": len(data)}
    
    except HTTPException:
        raise
    except Exception as e:
        return {"status": "error", "message": str(e)}