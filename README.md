# 🏛️ Phần Mềm Quản Lý Đối Tượng Thi Hành Án

## 📋 Tổng Quan

Phần mềm quản lý đối tượng thi hành án được phát triển bằng PyQt6 với giao diện hiện đại, tích hợp AI và các tính năng thông minh để hỗ trợ công tác quản lý đối tượng thi hành án.

## ✨ Tính Năng Chính

### 🔐 Bảo Mật & Đăng Nhập
- ✅ Hệ thống đăng nhập an toàn
- ✅ Phân quyền người dùng
- ✅ Ghi log hoạt động
- ✅ Quản lý phiên làm việc

### 👥 Quản Lý Đối Tượng
- ✅ Thêm, sửa, xóa đối tượng
- ✅ Thông tin chi tiết đầy đủ
- ✅ Tự động tính toán ngày hoàn thành
- ✅ Cảnh báo sắp hết hạn
- ✅ Xét điều kiện giảm án

### 🔍 Tìm Kiếm & Lọc
- ✅ Tìm kiếm thông minh
- ✅ Lọc theo địa bàn, trạng thái, loại án
- ✅ Sắp xếp theo nhiều tiêu chí
- ✅ Thao tác hàng loạt

### 📊 Báo Cáo & Thống Kê
- ✅ Báo cáo tháng/quý/năm
- ✅ Thống kê trạng thái
- ✅ Phân tích xu hướng
- ✅ Xuất Excel/PDF

### 🤖 AI & Thông Minh
- ✅ Dự đoán nguy cơ vi phạm
- ✅ Chatbot hỗ trợ pháp lý
- ✅ Phân tích xu hướng
- ✅ Cảnh báo thông minh

### 📈 Dashboard
- ✅ Tổng quan hệ thống
- ✅ Biểu đồ thống kê
- ✅ Cảnh báo real-time
- ✅ AI insights

## 🛠️ Cài Đặt & Chạy

### Yêu Cầu Hệ Thống
- Python 3.8+
- PyQt6
- SQLite3

### Cài Đặt Dependencies
```bash
pip install -r requirements.txt
```

### Chạy Ứng Dụng
```bash
python main.py
```

## 🏗️ Kiến Trúc Hệ Thống

### 📁 Cấu Trúc Thư Mục
```
KIEN TRUC/
├── main.py                 # Entry point
├── constants.py            # Constants & config
├── requirements.txt        # Dependencies
├── assets/                 # Resources
│   ├── styles/
│   │   └── style.py       # Global styles
│   ├── templates/          # Report templates
│   └── *.png              # Icons & images
├── database/              # Database layer
│   ├── database_manager.py
│   └── migrations/
├── models/                # Data models
│   ├── offender.py
│   ├── user.py
│   └── case.py
├── services/              # Business logic
│   ├── offender_service.py
│   ├── user_service.py
│   ├── ai_service.py
│   └── report_service.py
└── ui/                    # User interface
    ├── login_dialog.py
    ├── main_window.py
    ├── dashboard.py
    ├── offender_form.py
    ├── offender_list.py
    ├── reports.py
    ├── settings.py
    └── ai_tools.py
```

### 🔧 Các Thành Phần Chính

#### 1. Database Layer
- **DatabaseManager**: Quản lý kết nối SQLite
- **Migrations**: Tạo và cập nhật schema
- **Models**: Định nghĩa cấu trúc dữ liệu

#### 2. Services Layer
- **OffenderService**: CRUD đối tượng
- **UserService**: Quản lý người dùng
- **AIService**: Tính năng AI
- **ReportService**: Tạo báo cáo

#### 3. UI Layer
- **LoginDialog**: Đăng nhập
- **MainWindow**: Cửa sổ chính
- **Dashboard**: Tổng quan
- **OffenderForm**: Form nhập liệu
- **OffenderList**: Danh sách đối tượng
- **Reports**: Báo cáo
- **Settings**: Cài đặt
- **AITools**: Công cụ AI

## 🎨 Giao Diện & UX

### 🎯 Thiết Kế UI/UX
- **Framework**: PyQt6 với Modern Design
- **Theme**: Material Design / Fluent Design
- **Color Scheme**: Professional Blue & Gray
- **Responsive**: Tương thích nhiều độ phân giải
- **Accessibility**: Hỗ trợ keyboard navigation

### 🎨 Style Guidelines
- **Font**: Segoe UI, 13px
- **Primary Color**: #1976D2
- **Layout**: QVBoxLayout, QHBoxLayout, QGridLayout
- **Margins**: 12px, Spacing: 10px
- **Buttons**: Padding 6px 12px, min-height 32px
- **Inputs**: Border-radius 6px, border #ccc

### ⌨️ Keyboard Shortcuts
- **Ctrl+N**: Thêm mới đối tượng
- **Ctrl+S**: Lưu
- **Ctrl+F**: Tìm kiếm
- **Ctrl+E**: Xuất Excel
- **Ctrl+P**: In báo cáo
- **F1**: Trợ giúp
- **F5**: Refresh
- **Esc**: Hủy/Thoát

## 📊 Tính Năng Chi Tiết

### 🔐 Đăng Nhập
- Username/Password validation
- Remember me functionality
- Session management
- Security logging

### 👥 Quản Lý Đối Tượng
- **Thông tin cơ bản**: Họ tên, ngày sinh, địa chỉ
- **Thông tin án**: Số bản án, quyết định, thời gian
- **Tính toán tự động**: Ngày hoàn thành, trạng thái
- **Cảnh báo**: Sắp hết hạn, vi phạm
- **Giảm án**: Điều kiện, thủ tục

### 🔍 Tìm Kiếm & Lọc
- **Tìm kiếm**: Theo tên, số hồ sơ, địa chỉ
- **Lọc**: Trạng thái, địa bàn, loại án
- **Sắp xếp**: Theo cột, tăng/giảm
- **Thao tác**: Chọn nhiều, xóa hàng loạt

### 📈 Báo Cáo
- **Báo cáo tháng/quý/năm**: Thống kê tổng quan
- **Báo cáo trạng thái**: Phân bố đối tượng
- **Báo cáo nguy cơ**: Phân tích rủi ro
- **Xuất file**: Excel, PDF, Word
- **Gửi email**: Tự động gửi báo cáo

### 🤖 AI Features
- **Dự đoán nguy cơ**: Phân tích yếu tố ảnh hưởng
- **Chatbot pháp lý**: Hỗ trợ tư vấn
- **Phân tích xu hướng**: Thống kê theo thời gian
- **Cảnh báo thông minh**: Dựa trên dữ liệu

### 📊 Dashboard
- **Tổng quan**: Số liệu tổng hợp
- **Biểu đồ**: Xu hướng, phân bố
- **Cảnh báo**: Real-time notifications
- **AI Insights**: Gợi ý từ AI

## 🔧 Cấu Hình & Tùy Chỉnh

### ⚙️ Settings
- **Chung**: Ngôn ngữ, theme, auto-save
- **Bảo mật**: Timeout, password policy
- **Backup**: Tần suất, retention
- **Giao diện**: Font size, animations

### 📁 Database
- **SQLite**: Embedded database
- **Migrations**: Schema versioning
- **Backup**: Automatic & manual
- **Optimization**: Indexes, queries

## 🚀 Tính Năng Nâng Cao

### 📱 Responsive Design
- **Desktop**: Full layout với sidebar
- **Laptop**: Compact layout
- **Tablet**: Touch-friendly interface

### 🔄 Import/Export
- **Excel**: Nhập/xuất dữ liệu
- **PDF**: Báo cáo chuyên nghiệp
- **Word**: Templates tự động
- **CSV**: Dữ liệu raw

### 🔐 Security
- **Authentication**: JWT tokens
- **Authorization**: Role-based access
- **Encryption**: Data at rest
- **Audit**: Activity logging

### 🤖 AI Integration
- **Machine Learning**: Risk prediction
- **NLP**: Legal document analysis
- **Computer Vision**: Document processing
- **Recommendation**: Smart suggestions

## 📝 Hướng Dẫn Sử Dụng

### 🚀 Khởi Động
1. Chạy `python main.py`
2. Đăng nhập với tài khoản mặc định: `admin/admin`
3. Khám phá các tính năng từ sidebar

### 👥 Thêm Đối Tượng
1. Chọn "Đối Tượng" từ sidebar
2. Click "Thêm mới"
3. Điền thông tin trong các tab
4. Lưu và xem kết quả tính toán

### 🔍 Tìm Kiếm
1. Vào "Danh sách đối tượng"
2. Sử dụng thanh tìm kiếm
3. Áp dụng bộ lọc
4. Sắp xếp theo cột

### 📊 Tạo Báo Cáo
1. Vào "Báo cáo"
2. Chọn loại báo cáo
3. Thiết lập thời gian và bộ lọc
4. Tạo và xuất báo cáo

### 🤖 Sử Dụng AI
1. Vào "AI Tools"
2. Chọn tab tính năng
3. Nhập dữ liệu cần phân tích
4. Xem kết quả AI

## 🐛 Troubleshooting

### Lỗi Thường Gặp
- **Database connection**: Kiểm tra file database
- **Import errors**: Cài đặt dependencies
- **UI issues**: Kiểm tra PyQt6 version
- **Performance**: Tối ưu queries

### 🔧 Debug Mode
```bash
python main.py --debug
```

## 📞 Hỗ Trợ

### 📧 Liên Hệ
- **Email**: support@example.com
- **Phone**: +84 123 456 789
- **Website**: https://example.com

### 📚 Tài Liệu
- **User Manual**: docs/user_manual.pdf
- **API Docs**: docs/api_reference.md
- **Developer Guide**: docs/developer_guide.md

## 📄 License

© 2024 Phần Mềm Quản Lý Đối Tượng Thi Hành Án. All rights reserved.

---

**Phiên bản**: 1.0.0  
**Cập nhật**: 2024-12-19  
**Tác giả**: Development Team 