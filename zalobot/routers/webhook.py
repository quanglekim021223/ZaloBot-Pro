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
    Xử lý logic nghiệp vụ ở background để không block request
    
    CRITICAL: Function này chạy sau khi đã trả lời 200 OK cho Zalo.
    Nếu có lỗi ở đây, Zalo sẽ không retry vì đã nhận được 200 OK.
    """
    try:
        # Parse user_id và text từ body (cấu trúc Zalo webhook)
        sender = body.get("sender", {})
        user_id = sender.get("id")
        message = body.get("message", {})
        text = message.get("text", "")
        
        if not user_id:
            logger.warning("⚠️ No user_id found in webhook body")
            return
        
        logger.info(f"📩 Background Task: Xử lý tin nhắn từ user_id={user_id}, text='{text}'")
        
        # TODO: Logic bán hàng sẽ viết ở đây
        if "mua" in text.lower():
            logger.info("👉 Phát hiện nhu cầu mua hàng -> Tạo Order...")
            # create_order(user_id=user_id, text=text)
            # Gọi MoMo API tạo payment link
            # Gửi payment link cho khách qua Zalo API
            
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
    Webhook nhận tin từ Zalo OA.
    
    CRITICAL: Phải phản hồi 200 OK trong vòng 3 giây.
    Logic xử lý được đẩy vào background task để đảm bảo response nhanh.
    
    Security: Verify signature từ Zalo để tránh fake requests.
    """
    # 1. Đọc Raw Bytes để verify signature (QUAN TRỌNG)
    # Phải đọc body_bytes trước khi parse JSON
    body_bytes = await request.body()
    
    # 2. Check Security - Verify signature
    if x_zalo_signature:
        if not verify_zalo_signature(body_bytes, x_zalo_signature):
            logger.warning("⛔ Invalid Zalo Signature! Request rejected.")
            # Trả về 403 để chặn hẳn (Zalo sẽ không retry với 403)
            raise HTTPException(status_code=403, detail="Invalid Signature")
    else:
        # Trong dev/test mode, có thể cho qua nhưng log warning
        # Trong production, nên reject nếu không có signature
        logger.warning("⚠️ No X-Zalo-Signature header found. Allowing in dev mode.")
        # Nếu muốn strict, uncomment dòng dưới:
        # raise HTTPException(status_code=403, detail="Missing Signature")
    
    # 3. Parse JSON để xử lý logic
    try:
        body = json.loads(body_bytes)
    except json.JSONDecodeError as e:
        logger.error(f"❌ Invalid JSON in webhook body: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    # Log để debug (chỉ log một phần để tránh spam)
    logger.info(f"✅ Verified webhook from Zalo: user_id={body.get('sender', {}).get('id', 'unknown')}")
    
    # 4. Đẩy vào Background Task (Fire and Forget)
    # Logic xử lý sẽ chạy sau khi đã trả lời 200 OK
    background_tasks.add_task(process_webhook_background, body)
    
    # 5. Return 200 OK ngay lập tức (< 100ms)
    # Zalo sẽ nhận được response nhanh, không timeout
    return {"status": "success"}

