from pydantic import BaseModel
from typing import Any, Dict, List, Optional

class EmailData(BaseModel):
    sender: str
    subject: str
    request_type: Optional[str] = None
    sub_request_type: Optional[str] = None
    confidence_score: Optional[float] = None
    duplicate_flag: bool = False
    all_extracted_numbers: Optional[List[Dict[str, Any]]] = None
