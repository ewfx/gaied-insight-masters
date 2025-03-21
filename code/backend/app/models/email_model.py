from pydantic import BaseModel
from typing import List, Optional

class EmailData(BaseModel):
    sender: str
    subject: str
    date: str
    body: str
    attachments: List[str]
    request_type: Optional[str] = None
    priority: Optional[str] = None
    confidence_score: Optional[float] = None
    duplicate_flag: bool = False
    duplicate_reason: Optional[str] = None
