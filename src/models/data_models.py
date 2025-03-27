
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime
from decimal import Decimal

class DataProductInfo(BaseModel):
    """Information about the data product."""
    name: str = "finance-profit-margins"
    domain: str = "finance"
    version: str = "0.1.0"
    description: str = "Profit margin calculations by product category"
    owner: str = "finance-team"
    update_frequency: str = "daily"
    last_updated: str

class TransactionData(BaseModel):
    """Input transaction data structure."""
    transaction_id: str
    product_id: str
    quantity: int
    sale_price: Decimal
    transaction_date: datetime

class ProductData(BaseModel):
    """Input product master data structure."""
    product_id: str
    category: str
    cost_price: Decimal
    name: str

class ProfitMarginResult(BaseModel):
    """Output profit margin calculation result."""
    category: str
    period: str
    total_revenue: Decimal
    total_cost: Decimal
    profit_margin: Decimal
    trend: float = Field(description="Trend compared to previous period")

class ProcessingResult(BaseModel):
    """Result of a data processing operation."""
    success: bool
    message: str
    results: Optional[Dict[str, Any]] = None
    errors: Optional[List[str]] = None
