"""MoMo payment router - receives IPN callbacks from MoMo"""
from fastapi import APIRouter, Request, HTTPException
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/momo", tags=["momo"])


@router.post("/ipn")
async def momo_ipn(request: Request):
    """
    IPN (Instant Payment Notification) endpoint for MoMo Payment
    
    MoMo will POST payment result to this endpoint after customer pays.
    Currently returns 200 OK (skeleton).
    """
    try:
        # Get request body
        body = await request.json()
        logger.info(f"Received IPN from MoMo: {body}")
        
        # TODO: Verify HMAC signature
        # TODO: Update order status from PENDING to PAID
        # TODO: Trigger fulfillment (send product link via Zalo API)
        
        # Return 200 OK for now
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error processing IPN: {e}")
        raise HTTPException(status_code=500, detail=str(e))

