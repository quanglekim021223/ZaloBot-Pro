"""Order service - handles order creation and management"""
from typing import Optional
import logging
from sqlmodel import Session

from zalobot.database.models import Order
from zalobot.database.connection import engine

logger = logging.getLogger(__name__)


def create_order(
    user_id: str,
    amount: int = 99000,
    product_code: Optional[str] = None
) -> Order:
    """
    Create a new order in the database
    
    Args:
        user_id: Zalo user ID
        amount: Order amount in VND (default: 99000)
        product_code: Product code (optional)
    
    Returns:
        Order object with id populated
    
    Raises:
        Exception: If database operation fails
    """
    try:
        with Session(engine) as session:
            # Create new order
            order = Order(
                user_id=user_id,
                amount=amount,
                product_code=product_code,
                status="PENDING"
            )
            
            # Add to session and commit
            session.add(order)
            session.commit()
            session.refresh(order)  # Refresh to get the ID
            
            logger.info(f"✅ Created order #{order.id} for user {user_id}, amount: {amount:,}đ")
            
            return order
            
    except Exception as e:
        logger.error(f"❌ Error creating order for user {user_id}: {e}", exc_info=True)
        raise

