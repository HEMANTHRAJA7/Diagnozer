from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.db.mongodb import get_database
from app.models.user import UserCreate, UserResponse, Token
from app.core.security import get_password_hash, verify_password, create_access_token
from app.api.dependencies import get_current_user
from datetime import datetime
import traceback

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db=Depends(get_database)):
    try:
        existing_user = await db["users"].find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
            
        user_dict = user.dict()
        user_dict["password"] = get_password_hash(user_dict.pop("password"))
        user_dict["created_at"] = datetime.utcnow()
        
        result = await db["users"].insert_one(user_dict)
        user_dict["_id"] = str(result.inserted_id)
        
        return user_dict
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        print(f"REGISTRATION ERROR: {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail=f"Registration Error: {type(e).__name__}: {str(e)}")

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_database)):
    user = await db["users"].find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
