from pydantic import BaseModel
from typing import List, Optional

class PredictionResponse(BaseModel):
    predictedClass: str
    confidence: float
    classProbabilities: Optional[List[float]] = None
    predictedClassIndex: int
    heatmapUrl: str
    explanation: str
    imageType: Optional[str] = None # used for jackfruit phase A output
