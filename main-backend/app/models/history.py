from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone

class PredictionHistory(BaseModel):
    user_id: str
    crop_type: str # 'mango' or 'jackfruit'
    image_type: Optional[str] = None # 'Leaf' or 'Fruit' for jackfruit
    predicted_class: str
    confidence: float
    heatmap_url: str
    explanation: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
