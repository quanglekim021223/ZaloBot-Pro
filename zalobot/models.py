"""SQLModel models for ZaloBot Pro"""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class Order(SQLModel, table=True):
    """Order model - stores customer orders"""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(description="Zalo user ID")
    product_code: Optional[str] = Field(default=None, description="Product code (e.g., 'ebook_python')")
    amount: int = Field(description="Order amount in VND")
    status: str = Field(default="PENDING", description="Order status: PENDING or PAID")
    created_at: datetime = Field(default_factory=datetime.now, description="Order creation timestamp")

