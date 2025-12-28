# Quick Start - Day 1 Setup

### Terminal 1: Start Server
```bash
uvicorn main:app --reload --port 8000
```

### Terminal 2: Start Ngrok
```bash
ngrok http 8000
```

Copy HTTPS URL từ Ngrok → Config vào Zalo OA.


👉 Quy trình bạn phải làm mỗi khi tắt Ngrok:

Bật lại Ngrok: Lấy link mới.

Vào Zalo Developers -> Webhook: Dán link mới vào, bấm Update.

Vào Zalo Developers -> Domain Verification:

Nó sẽ báo link mới chưa xác thực.

Bạn nhập domain mới vào, bấm Verify.
