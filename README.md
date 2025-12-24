# ZaloBot Pro

> Hệ thống tự động bán sản phẩm số trên Zalo - Chat → Pay → Deliver NGAY LẬP TỨC

## 🎯 Dự án này là gì?

**ZaloBot Pro** là một hệ thống tự động bán sản phẩm số trên Zalo, cho phép khách hàng:
- Chat với bot trên Zalo
- Thanh toán qua MoMo
- Nhận hàng (link tải) **NGAY LẬP TỨC** - không cần người trực

👉 **Không phải chatbot AI phức tạp**  
👉 **Là một "máy thu tiền + giao hàng tự động" chạy 24/7**

## 💡 Bài toán thực tế

### Trước khi có ZaloBot Pro
- Khách nhắn Zalo lúc **11-12h đêm** → Chủ shop đang ngủ/bận
- Sáng hôm sau mới trả lời → **Khách hết hứng → không mua nữa**
- 💸 **Mất tiền vì chậm**

### Sau khi có ZaloBot Pro
- Khách nhắn: `mua ebook`
- Bot tự động:
  1. Giới thiệu sản phẩm
  2. Gửi **link thanh toán MoMo**
- Khách trả tiền → **Bot tự gửi link ebook ngay**
- Chủ shop **không cần làm gì** → Bán được hàng **24/7**

## 🏗️ Kiến trúc tổng thể

```
Khách hàng
   |
   |  (1) Chat "mua ebook"
   v
Zalo OA (Official Account)
   |
   |  (2) Webhook
   v
FastAPI Server (ZaloBot Pro)
   |
   |  (3) Tạo Order + Gọi MoMo API
   v
MoMo Payment Gateway
   |
   |  (4) IPN Callback
   v
FastAPI Server
   |
   |  (5) Gửi link sản phẩm qua Zalo API
   v
Khách hàng 🎉
```

## 📁 Cấu trúc Code

### 1. **Webhook nhận tin từ Zalo**
📍 `routers/webhook.py`
- Nhận JSON từ Zalo OA
- Parse `user_id`, `text`
- Detect keyword "mua" → Tạo đơn hàng
- Gửi phản hồi với link thanh toán

### 2. **Database lưu đơn hàng**
📍 `models.py`
```python
Order:
- id
- user_id (Zalo user ID)
- product_code (vd: "ebook_python")
- amount (vd: 99000)
- status (PENDING / PAID)
- created_at
```

### 3. **Gọi API MoMo (Tạo thanh toán)**
📍 `services/momo.py`
- Tạo HMAC signature
- Gửi request tạo payment
- Nhận `payUrl` → Gửi cho khách

### 4. **Nhận Callback MoMo (Xác nhận thanh toán)**
📍 `routers/payment.py`
- Endpoint: `/momo/ipn`
- Verify HMAC signature
- Update DB: `PENDING → PAID`
- Trigger giao hàng tự động

### 5. **Gửi hàng tự động (Fulfillment)**
📍 `services/zalo.py`
- Gọi Zalo API gửi tin nhắn
- Nội dung: "Thanh toán thành công! Link tải: ..."

## 🔄 Flow hoạt động chi tiết

1. **Khách chat**: "mua ebook python"
2. **Webhook** nhận tin → Parse text
3. **Bot** tạo Order (status: PENDING)
4. **Bot** gọi MoMo API → Tạo payment link
5. **Bot** gửi link thanh toán cho khách
6. **Khách** thanh toán trên MoMo
7. **MoMo** gọi IPN callback → `/momo/ipn`
8. **Server** verify signature → Update Order (status: PAID)
9. **Server** gọi Zalo API → Gửi link sản phẩm
10. **Khách** nhận link → Tải sản phẩm ✅

## 🛠️ Tech Stack (Dự kiến)

- **Backend**: FastAPI (Python)
- **Database**: SQLite / PostgreSQL
- **Payment**: MoMo Payment Gateway
- **Platform**: Zalo Official Account API
- **Deployment**: (TBD)

## 📝 Lưu ý quan trọng

### Dự án này KHÔNG phải:
- ❌ Shopee / E-commerce platform
- ❌ Chatbot AI nói chuyện thông minh
- ❌ CRM phức tạp
- ❌ Hệ thống kho / ship / COD

### Dự án này TẬP TRUNG:
- ✅ **Chat → Pay → Deliver** (3 bước đơn giản)
- ✅ Tự động hóa 100% quy trình bán hàng
- ✅ Hoạt động 24/7 không cần người trực

## 🚀 Getting Started

_(Sẽ được cập nhật khi có code)_

## 📄 License

_(TBD)_

---

**Mục tiêu**: Giúp người bán kiếm tiền ngay cả khi họ đang ngủ 😴💰
