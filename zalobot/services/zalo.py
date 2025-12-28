"""Zalo API service - handles communication with Zalo Official Account API"""
import httpx
import logging
from typing import Optional

from zalobot.config import ZALO_OA_ACCESS_TOKEN, ZALO_OA_ID

logger = logging.getLogger(__name__)

# Zalo API endpoint for sending messages
ZALO_API_BASE_URL = "https://openapi.zalo.me/v2.0/oa/message"


async def send_message(user_id: str, message: str) -> bool:
    """
    Send a text message to a user via Zalo Official Account API
    
    Args:
        user_id: Zalo user ID to send message to
        message: Message text to send
    
    Returns:
        True if message sent successfully, False otherwise
    """
    if not ZALO_OA_ACCESS_TOKEN:
        logger.error("❌ ZALO_OA_ACCESS_TOKEN is not configured!")
        return False
    
    if not user_id:
        logger.error("❌ user_id is required to send message")
        return False
    
    try:
        # Prepare request
        # Zalo API uses access_token as query parameter
        url = f"{ZALO_API_BASE_URL}?access_token={ZALO_OA_ACCESS_TOKEN}"
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "recipient": {
                "user_id": user_id
            },
            "message": {
                "text": message
            }
        }
        
        # Send request to Zalo API
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            
            # Check if API returned success
            if result.get("error") == 0:
                logger.info(f"✅ Sent message to user {user_id}")
                return True
            else:
                error_msg = result.get("message", "Unknown error")
                logger.error(f"❌ Zalo API error: {error_msg}")
                return False
                
    except httpx.HTTPStatusError as e:
        logger.error(f"❌ HTTP error sending message to user {user_id}: {e.response.status_code} - {e.response.text}")
        return False
    except httpx.RequestError as e:
        logger.error(f"❌ Request error sending message to user {user_id}: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error sending message to user {user_id}: {e}", exc_info=True)
        return False

