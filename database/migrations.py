"""
Database migrations for creating tables.
"""

import sqlite3
from pathlib import Path


def create_tables(db_path: str = "data/database.db"):
    """Create all database tables."""
    db_file = Path(db_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create offenders table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS offenders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_number TEXT NOT NULL UNIQUE,
        full_name TEXT NOT NULL,
        gender TEXT NOT NULL,
        birth_date DATE,
        address TEXT,
        occupation TEXT,
        crime TEXT,
        case_type TEXT NOT NULL,
        sentence_number TEXT,
        decision_number TEXT,
        start_date DATE,
        duration_months INTEGER DEFAULT 0,
        reduced_months INTEGER DEFAULT 0,
        reduction_date DATE,
        reduction_count INTEGER DEFAULT 0,
        completion_date DATE,
        status TEXT NOT NULL,
        days_remaining INTEGER DEFAULT 0,
        risk_level TEXT NOT NULL,
        risk_percentage REAL DEFAULT 0.0,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL,
        created_by INTEGER,
        notes TEXT
    )
    """)
    
    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL,
        status TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL,
        last_login DATETIME,
        login_attempts INTEGER DEFAULT 0,
        locked_until DATETIME
    )
    """)
    
    # Create cases table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_number TEXT NOT NULL UNIQUE,
        case_name TEXT,
        offender_id INTEGER,
        court_name TEXT,
        judge_name TEXT,
        prosecutor_name TEXT,
        crime_description TEXT,
        sentence_details TEXT,
        decision_details TEXT,
        case_date DATE,
        decision_date DATE,
        effective_date DATE,
        status TEXT NOT NULL,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL,
        created_by INTEGER,
        notes TEXT,
        FOREIGN KEY (offender_id) REFERENCES offenders (id)
    )
    """)
    
    # Create violations table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS violations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        offender_id INTEGER NOT NULL,
        violation_type TEXT NOT NULL,
        description TEXT,
        location TEXT,
        violation_date DATE,
        report_date DATE,
        penalty TEXT,
        additional_months INTEGER DEFAULT 0,
        warning_level INTEGER DEFAULT 0,
        status TEXT NOT NULL,
        resolution_notes TEXT,
        resolved_by INTEGER,
        resolved_date DATE,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL,
        created_by INTEGER,
        FOREIGN KEY (offender_id) REFERENCES offenders (id),
        FOREIGN KEY (resolved_by) REFERENCES users (id)
    )
    """)
    
    # Create reductions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reductions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        offender_id INTEGER NOT NULL,
        reduction_type TEXT NOT NULL,
        months_reduced INTEGER DEFAULT 0,
        reason TEXT,
        evidence TEXT,
        application_date DATE,
        decision_date DATE,
        effective_date DATE,
        status TEXT NOT NULL,
        decision_notes TEXT,
        decided_by INTEGER,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL,
        created_by INTEGER,
        FOREIGN KEY (offender_id) REFERENCES offenders (id),
        FOREIGN KEY (decided_by) REFERENCES users (id)
    )
    """)
    
    # Create indexes for better performance
    try:
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_offenders_case_number ON offenders(case_number)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_offenders_full_name ON offenders(full_name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_offenders_status ON offenders(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_offenders_completion_date ON offenders(completion_date)")
        
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_role ON users(role)")
        
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_violations_offender_id ON violations(offender_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_violations_status ON violations(status)")
        
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_reductions_offender_id ON reductions(offender_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_reductions_status ON reductions(status)")
    except sqlite3.OperationalError as e:
        print(f"Warning: Could not create some indexes: {e}")
    
    conn.commit()
    conn.close()
    
    print("Database tables created successfully!")


def create_default_admin():
    """Create default admin user."""
    from database.database_manager import DatabaseManager
    from models.user import User, UserRole, UserStatus
    
    with DatabaseManager() as db:
        # Check if admin user already exists
        admin = db.get_user_by_username("admin")
        if admin:
            print("Admin user already exists!")
            return
        
        # Create default admin user
        admin_user = User(
            username="admin",
            email="admin@example.com",
            full_name="Administrator",
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE
        )
        admin_user.set_password("admin123")
        
        admin_id = db.create_user(admin_user)
        print(f"Default admin user created with ID: {admin_id}")
        print("Username: admin")
        print("Password: admin123")


if __name__ == "__main__":
    create_tables()
    create_default_admin() 