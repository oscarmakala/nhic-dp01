from pydantic import BaseModel
from typing import Dict, List, Any, Optional

class DataProductInfo(BaseModel):
    """Information about the data product."""
    name: str
    domain: str
    version: str
    description: str
    owner: str
    update_frequency: str
    last_updated: str

class ProcessingResult(BaseModel):
    """Result of a data processing operation."""
    success: bool
    message: str
    results: Optional[Dict[str, Any]] = None
    errors: Optional[List[str]] = None