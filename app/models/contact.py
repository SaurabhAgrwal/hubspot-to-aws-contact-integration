from pydantic import BaseModel
from typing import List, Dict, Optional

class ContactResponse(BaseModel):
    """Model for individual contact processing result"""
    email: str
    status: str
    operation: Optional[str] = None
    error: Optional[str] = None

class SyncResponse(BaseModel):
    """Model for sync operation response"""
    total_processed: int
    successful: int
    failed: int
    results: List[Dict]