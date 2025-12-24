"""Utility functions for ZaloBot Pro"""
import hmac
import hashlib
from zalobot.config import ZALO_OA_SECRET
import logging

logger = logging.getLogger(__name__)


def verify_zalo_signature(body_bytes: bytes, x_zalo_signature: str) -> bool:
    """
    Verify Zalo webhook signature
    
    Args:
        body_bytes: Raw body bytes từ request (QUAN TRỌNG - phải là bytes gốc)
        x_zalo_signature: Header X-Zalo-Signature từ Zalo (format: "mac=<hash_value>")
    
    Returns:
        True nếu signature hợp lệ, False nếu không
    """
    # Dev mode: Nếu không có secret, cho qua (nhưng log warning)
    if not ZALO_OA_SECRET:
        logger.warning("⚠️ ZALO_OA_SECRET is missing! Skipping verification.")
        return True  # Dev mode: cho qua
    
    # Handle None hoặc empty string
    if not x_zalo_signature:
        logger.warning("⚠️ X-Zalo-Signature header is missing!")
        return False  # Reject nếu không có signature
    
    # Zalo signature format: "mac=<hash_value>"
    if not x_zalo_signature.startswith("mac="):
        logger.warning(f"⚠️ Invalid signature format: {x_zalo_signature}")
        return False
    
    # Extract hash value (bỏ phần "mac=")
    expected_mac = x_zalo_signature.split("=", 1)[1]  # Dùng maxsplit=1 để tránh lỗi nếu có "=" trong hash
    
    if not expected_mac:
        logger.warning("⚠️ Empty signature hash value")
        return False
    
    # Tính toán hash từ Raw Body + Secret Key
    calculated_mac = hmac.new(
        ZALO_OA_SECRET.encode('utf-8'),
        body_bytes,  # Dùng bytes gốc, không json.dumps
        hashlib.sha256
    ).hexdigest()
    
    # So sánh an toàn (tránh timing attack)
    is_valid = hmac.compare_digest(expected_mac, calculated_mac)
    
    if not is_valid:
        logger.warning(f"⚠️ Signature mismatch. Expected: {expected_mac[:8]}..., Calculated: {calculated_mac[:8]}...")
    
    return is_valid

