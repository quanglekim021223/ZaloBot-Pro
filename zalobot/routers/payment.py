"""MoMo payment router - receives IPN callbacks from MoMo"""
from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
import logging
import json

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/momo", tags=["momo"])


async def process_momo_ipn_background(body: dict):
    """
    Handle logic IPN in background to avoid blocking request
    
    CRITICAL: This function runs after responding 200 OK to MoMo.
    If there is an error here, MoMo will not retry because it has received 200 OK.
    """
    try:
        logger.info(f"📩 Background Task: Handling IPN from MoMo: {body}")
        
        # TODO: Verify HMAC signature (will implement in Day 2-3)
        # TODO: Update order status from PENDING to PAID
        # TODO: Trigger fulfillment (send product link via Zalo API)
        
    except Exception as e:
        logger.error(f"❌ Error in background task: {e}", exc_info=True)


@router.post("/ipn")
async def momo_ipn(
    request: Request,
    background_tasks: BackgroundTasks
):
    """
    IPN (Instant Payment Notification) endpoint for MoMo Payment
    
    MoMo will POST payment result to this endpoint after customer pays.
    Currently returns 200 OK.
    
    CRITICAL: Must respond 200 OK quickly to avoid MoMo retry.
    Logic processing is pushed into background task.
    """
    # 1. Read Raw Bytes (to verify signature later)
    # Must read body_bytes before parsing JSON
    body_bytes = await request.body()
    
    # 2. Parse JSON to process logic
    try:
        body = json.loads(body_bytes)
        logger.info(f"Received IPN from MoMo: {body}")
    except json.JSONDecodeError as e:
        logger.error(f"❌ Invalid JSON in IPN body: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    # 3. Push into Background Task (Fire and Forget)
    # Logic processing will run after responding 200 OK
    background_tasks.add_task(process_momo_ipn_background, body)
    
    # 4. Return 200 OK immediately
    # MoMo will receive response quickly, without timeout
    return {"status": "ok"}

