"""Configuration management - Load environment variables from .env file"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Zalo Official Account
ZALO_OA_ID = os.getenv("ZALO_OA_ID", "")
ZALO_OA_SECRET = os.getenv("ZALO_OA_SECRET", "")
ZALO_OA_ACCESS_TOKEN = os.getenv("ZALO_OA_ACCESS_TOKEN", "")

# MoMo Payment
MOMO_PARTNER_CODE = os.getenv("MOMO_PARTNER_CODE", "")
MOMO_ACCESS_KEY = os.getenv("MOMO_ACCESS_KEY", "")
MOMO_SECRET_KEY = os.getenv("MOMO_SECRET_KEY", "")

# Server
PORT = int(os.getenv("PORT", "8000"))

