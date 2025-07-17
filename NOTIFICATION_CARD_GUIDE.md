# 🎯 Notification Card - Hướng Dẫn Sử Dụng

## 📋 Tổng Quan

Notification Card là component hiện đại để hiển thị thông báo, cảnh báo và thông tin quan trọng trong ứng dụng. Component này được thiết kế theo Material Design với giao diện đẹp, responsive và dễ sử dụng.

## 🎨 Thiết Kế

### **Các Loại Thông Báo:**

1. **✅ Success (Thành công)**
   - Màu nền: Xanh lá nhạt (#f1f8e9)
   - Viền: Xanh lá (#c8e6c9)
   - Icon: ✅
   - Dùng cho: Lưu thành công, hoàn thành tác vụ

2. **⚠️ Warning (Cảnh báo)**
   - Màu nền: Vàng nhạt (#fff8e1)
   - Viền: Vàng (#ffcc80)
   - Icon: ⚠️
   - Dùng cho: Cảnh báo, sắp hết hạn

3. **❌ Error (Lỗi)**
   - Màu nền: Đỏ nhạt (#ffebee)
   - Viền: Đỏ (#ffcdd2)
   - Icon: ❌
   - Dùng cho: Lỗi hệ thống, thất bại

4. **ℹ️ Info (Thông tin)**
   - Màu nền: Xanh dương nhạt (#e3f2fd)
   - Viền: Xanh dương (#bbdefb)
   - Icon: ℹ️
   - Dùng cho: Thông tin chung, cập nhật

## 🚀 Cách Sử Dụng

### **1. Import Component:**

```python
from ui.notification_card import (
    NotificationContainer, NotificationType,
    show_success_notification, show_warning_notification,
    show_error_notification, show_info_notification
)
```

### **2. Tạo Container:**

```python
# Trong MainWindow hoặc Widget chính
self.notification_container = NotificationContainer()
self.notification_container.setObjectName("notificationContainer")
# Thêm vào layout
layout.addWidget(self.notification_container)
```

### **3. Hiển Thị Thông Báo:**

#### **Cách 1: Sử dụng hàm tiện ích**

```python
# Thông báo thành công
show_success_notification(
    self.notification_container,
    "Thành công!",
    "Dữ liệu đã được lưu thành công."
)

# Thông báo cảnh báo
show_warning_notification(
    self.notification_container,
    "Cảnh báo!",
    "Có 3 đối tượng sắp hết hạn."
)

# Thông báo lỗi
show_error_notification(
    self.notification_container,
    "Lỗi!",
    "Không thể kết nối database."
)

# Thông báo thông tin
show_info_notification(
    self.notification_container,
    "Thông tin",
    "Hệ thống đã được cập nhật."
)
```

#### **Cách 2: Tạo notification tùy chỉnh**

```python
notification = self.notification_container.add_notification(
    title="Cập nhật có sẵn",
    message="Phiên bản 2.1.0 đã có sẵn.",
    notification_type=NotificationType.INFO,
    auto_dismiss=False,  # Không tự động đóng
    dismiss_timeout=10000,  # 10 giây
    show_action=True,  # Hiển thị nút action
    action_text="Cập nhật ngay"
)

# Kết nối signal action
notification.action_clicked.connect(self.on_update_clicked)
```

## ⚙️ Tùy Chọn

### **NotificationCard Parameters:**

- `title`: Tiêu đề thông báo
- `message`: Nội dung thông báo
- `notification_type`: Loại thông báo (SUCCESS, WARNING, ERROR, INFO)
- `auto_dismiss`: Tự động đóng sau timeout (mặc định: True)
- `dismiss_timeout`: Thời gian tự động đóng (ms, mặc định: 5000)
- `show_action`: Hiển thị nút action (mặc định: False)
- `action_text`: Text nút action (mặc định: "Xem chi tiết")

### **Signals:**

- `dismissed`: Emit khi notification bị đóng
- `action_clicked`: Emit khi click nút action

## 🎯 Best Practices

### **1. Sử Dụng Đúng Loại Thông Báo:**

```python
# ✅ Đúng - Success cho lưu thành công
show_success_notification(container, "Lưu thành công", "Dữ liệu đã được lưu.")

# ❌ Sai - Dùng Error cho thông tin
show_error_notification(container, "Thông tin", "Hệ thống cập nhật.")
```

### **2. Thông Báo Ngắn Gọn:**

```python
# ✅ Đúng - Ngắn gọn, rõ ràng
show_warning_notification(container, "Cảnh báo", "3 đối tượng sắp hết hạn.")

# ❌ Sai - Quá dài, khó đọc
show_warning_notification(container, "Cảnh báo quan trọng", 
    "Có 3 đối tượng thi hành án sắp hết hạn trong vòng 5 ngày tới, cần kiểm tra ngay.")
```

### **3. Sử Dụng Action Button Cho Tác Vụ Quan Trọng:**

```python
notification = container.add_notification(
    title="Cập nhật có sẵn",
    message="Phiên bản mới với nhiều tính năng.",
    notification_type=NotificationType.INFO,
    auto_dismiss=False,
    show_action=True,
    action_text="Cập nhật ngay"
)
```

### **4. Xử Lý Lỗi:**

```python
try:
    # Thực hiện tác vụ
    save_data()
    show_success_notification(container, "Thành công", "Dữ liệu đã được lưu.")
except Exception as e:
    show_error_notification(container, "Lỗi", f"Không thể lưu: {str(e)}")
```

## 🎨 Tùy Chỉnh Style

### **Thêm vào style.qss:**

```css
/* Tùy chỉnh màu sắc */
QFrame#notificationCardSuccess {
    background: #your-color;
    border: 1px solid #your-border;
}

/* Tùy chỉnh animation */
@keyframes slideIn {
    from { opacity: 0; transform: translateX(100%); }
    to { opacity: 1; transform: translateX(0%); }
}
```

## 📱 Responsive Design

- **Desktop**: Hiển thị đầy đủ với action button
- **Tablet**: Tự động điều chỉnh kích thước
- **Mobile**: Tối ưu cho màn hình nhỏ

## 🔧 Tích Hợp Vào Ứng Dụng

### **Trong MainWindow:**

```python
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        # ... existing code ...
        
        # Thêm notification container
        self.notification_container = NotificationContainer()
        self.notification_container.setObjectName("notificationContainer")
        
        # Thêm vào layout (góc phải trên)
        layout.addWidget(self.notification_container, 0, 1)
        
    def show_success_message(self, message):
        """Hiển thị thông báo thành công."""
        show_success_notification(
            self.notification_container,
            "Thành công!",
            message
        )
```

## 🧪 Test & Demo

Chạy file demo để xem các loại notification:

```bash
python test_notification_card.py
```

## 📋 Checklist

- [ ] Import component đúng cách
- [ ] Tạo NotificationContainer trong layout
- [ ] Sử dụng đúng loại notification
- [ ] Thông báo ngắn gọn, rõ ràng
- [ ] Xử lý lỗi với try/catch
- [ ] Test trên các kích thước màn hình
- [ ] Tùy chỉnh style nếu cần

---

**🎯 Notification Card đã sẵn sàng sử dụng trong ứng dụng của bạn!** 