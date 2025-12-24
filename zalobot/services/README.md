# Services Package

Business logic layer - xử lý các nghiệp vụ chính của hệ thống.

## Các service sẽ có:

- **zalo.py**: Tích hợp với Zalo Official Account API
  - Gửi tin nhắn cho user
  - Lấy thông tin user
  - Xử lý các tương tác với Zalo

- **momo.py**: Tích hợp với MoMo Payment Gateway
  - Tạo payment link
  - Verify payment signature
  - Xử lý payment callbacks

- **order.py**: Xử lý logic đơn hàng
  - Tạo order
  - Update order status
  - Fulfillment (giao hàng tự động)

