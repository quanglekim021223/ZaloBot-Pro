"""Zalo webhook router - receives messages from Zalo OA"""
from fastapi import APIRouter, Request, HTTPException
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/zalo", tags=["zalo"])


@router.post("/webhook")
async def zalo_webhook(request: Request):
    """
    Webhook endpoint for Zalo Official Account
    
    Zalo will POST JSON data to this endpoint when user sends a message.
    Currently returns 200 OK to allow Zalo to test connection.
    """
    try:
        # Get request body
        body = await request.json()
        logger.info(f"Received webhook from Zalo: {body}")
        
        # TODO: Parse user_id, text, and handle "mua" keyword
        # TODO: Create order and send payment link
        
        # Return 200 OK for now (allows Zalo to test connection)
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

