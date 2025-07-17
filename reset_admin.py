from database.database_manager import DatabaseManager
from models.user import User, UserRole, UserStatus

with DatabaseManager() as db:
    # Xóa tài khoản admin cũ nếu có
    db.execute("DELETE FROM users WHERE username = 'admin'")
    db.commit()
    # Tạo tài khoản admin mới
    admin_user = User(
        username="admin",
        email="admin@example.com",
        full_name="Administrator",
        role=UserRole.ADMIN,
        status=UserStatus.ACTIVE
    )
    admin_user.set_password("admin123")
    db.create_user(admin_user)
    print("Đã tạo lại tài khoản admin với mật khẩu: admin123") 