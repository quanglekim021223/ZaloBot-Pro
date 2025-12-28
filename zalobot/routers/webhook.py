"""Zalo webhook router - receives messages from Zalo OA"""
from fastapi import APIRouter, Request, HTTPException, BackgroundTasks, Header
import logging
import json

from zalobot.utils import verify_zalo_signature
# from zalobot.services.order import process_order  # Sẽ import ở Day 3

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/zalo", tags=["zalo"])


async def process_webhook_background(body: dict):
    """
    Handle business logic in background to avoid blocking request
    
    CRITICAL: This function runs after responding 200 OK to Zalo.
    If there is an error here, Zalo will not retry because it has received 200 OK.
    """
    try:
        # Parse user_id and text from body (Zalo webhook structure)
        sender = body.get("sender", {})
        user_id = sender.get("id")
        message = body.get("message", {})
        text = message.get("text", "")
        
        if not user_id:
            logger.warning("⚠️ No user_id found in webhook body")
            return
        
        logger.info(f"📩 Background Task: Handling message from user_id={user_id}, text='{text}'")
        
        # TODO: Logic bán hàng sẽ viết ở đây
        if "mua" in text.lower():
            logger.info("👉 Detected purchase intent -> Create Order...")
            # create_order(user_id=user_id, text=text)
            # Call MoMo API to create payment link
            # Send payment link to customer via Zalo API
            
    except KeyError as e:
        logger.error(f"❌ Missing key in webhook body: {e}")
    except Exception as e:
        logger.error(f"❌ Error in background task: {e}", exc_info=True)


@router.post("/webhook")
async def zalo_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_zalo_signature: str = Header(None, alias="X-Zalo-Signature")
):
    """
    Webhook endpoint for receiving messages from Zalo OA.
    
    CRITICAL: Must respond 200 OK within 3 seconds.
    Logic processing is pushed into background task to ensure quick response.
    
    Security: Verify signature from Zalo to prevent fake requests.
    """
    # 1. Read Raw Bytes to verify signature (CRITICAL)
    # Must read body_bytes before parsing JSON
    body_bytes = await request.body()
    
    # 2. Check Security - Verify signature
    if x_zalo_signature:
        if not verify_zalo_signature(body_bytes, x_zalo_signature):
            logger.warning("⛔ Invalid Zalo Signature! Request rejected.")
            # Return 403 to block (Zalo will not retry with 403)
            raise HTTPException(status_code=403, detail="Invalid Signature")
    else:
        # In dev/test mode, it can be allowed but log warning
        # In production, it should be rejected if there is no signature
        logger.warning("⚠️ No X-Zalo-Signature header found. Allowing in dev mode.")
        # If you want to be strict, uncomment the line below:
        # raise HTTPException(status_code=403, detail="Missing Signature")
    
    # 3. Parse JSON to process logic
    try:
        body = json.loads(body_bytes)
    except json.JSONDecodeError as e:
        logger.error(f"❌ Invalid JSON in webhook body: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    # Log for debugging (only log a part to avoid spam)
    logger.info(f"✅ Verified webhook from Zalo: user_id={body.get('sender', {}).get('id', 'unknown')}")
    
    # 4. Push into Background Task (Fire and Forget)
    # Logic processing will run after responding 200 OK
    background_tasks.add_task(process_webhook_background, body)
    
    # 5. Return 200 OK immediately (< 100ms)
    # Zalo will receive response quickly, without timeout
    return {"status": "success"}

