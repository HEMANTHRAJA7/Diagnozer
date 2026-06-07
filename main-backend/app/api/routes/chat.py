from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.core.config import settings
from app.api.dependencies import get_current_user
from app.db.mongodb import get_database
import traceback

try:
    from google import genai
    client = genai.Client(api_key=settings.GEMINI_API_KEY) if settings.GEMINI_API_KEY else None
except (ImportError, Exception):
    genai = None
    client = None

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

class ChatHistoryItem(BaseModel):
    user_msg: str
    bot_reply: str
    created_at: Optional[datetime] = None

@router.get("/history", response_model=List[ChatHistoryItem])
async def get_chat_history(current_user: dict = Depends(get_current_user), db=Depends(get_database)):
    try:
        # Load user's chat history sorted by creation time
        cursor = db["chats"].find({"user_id": str(current_user["_id"])}).sort("created_at", 1)
        chats = await cursor.to_list(length=100)
        
        history = []
        for chat in chats:
            history.append(ChatHistoryItem(
                user_msg=chat.get("user_msg", ""),
                bot_reply=chat.get("bot_reply", ""),
                created_at=chat.get("created_at")
            ))
        return history
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=ChatResponse)
async def chat_with_bot(request: ChatRequest, current_user: dict = Depends(get_current_user), db=Depends(get_database)):
    if not settings.GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Gemini API Key missing!")
        
    try:
        # Load user's latest diagnosis
        latest_history = await db["history"].find_one(
            {"user_id": str(current_user["_id"])},
            sort=[("created_at", -1)]
        )
        
        system_context = ""
        if latest_history:
            system_context = f"The user recently scanned a {latest_history['crop_type']} crop. The AI detected '{latest_history['predicted_class']}' with {(latest_history['confidence'] * 100):.1f}% confidence. Frame your answers around treating this diagnosis."
        else:
            system_context = "The user has not ran an AI diagnosis yet. Be helpful regarding Mango and Jackfruit farming."
            
        system_context += " IMPORTANT: Return your response in clean, plain text ONLY. Do NOT use markdown formatting (no bold asterisks like **, no headers like #, no markdown list bullet symbols like *). Use standard newlines and numbers/hyphens for lists."
            
        # Build prompt
        prompt = f"System Context: {system_context}\n\nUser Question: {request.message}"
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        # Post-process to strip any accidental markdown tags
        import re
        reply_text = response.text
        reply_text = reply_text.replace("**", "")  # Strip bolding
        reply_text = re.sub(r'(?m)^#+\s+', '', reply_text)  # Strip headers
        
        # Save to chat history db
        await db["chats"].insert_one({
            "user_id": str(current_user["_id"]),
            "user_msg": request.message,
            "bot_reply": reply_text,
            "created_at": datetime.utcnow()
        })

        return {"reply": reply_text}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


