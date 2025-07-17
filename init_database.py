#!/usr/bin/env python3
"""
Initialize database and create sample data.
"""

import sys
import os
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.migrations import create_tables, create_default_admin
from database.database_manager import DatabaseManager
from models.offender import Offender, Gender, CaseType, Status, RiskLevel


def create_sample_data():
    """Create sample offender data."""
    try:
        with DatabaseManager() as db:
            # Create sample offenders
            sample_offenders = [
                {
                    'case_number': '40CE0625/405LF',
                    'full_name': 'Nguyễn Văn An',
                    'gender': Gender.MALE,
                    'birth_date': date(1990, 5, 15),
                    'address': 'TDP 1, P. Bắc Hồng, TX. Hồng Lĩnh, Hà Tĩnh',
                    'occupation': 'Nông dân',
                    'crime': 'Trộm cắp tài sản',
                    'case_type': CaseType.SUSPENDED_SENTENCE,
                    'sentence_number': 'Số 15/2025/HS-ST, ngày 15/5/2025',
                    'decision_number': 'Số 15/2025/QĐ-CA, ngày 29/5/2025',
                    'start_date': date(2025, 6, 1),
                    'duration_months': 6,
                    'reduced_months': 1,
                    'reduction_date': date(2025, 9, 2),
                    'reduction_count': 1,
                    'notes': 'Đối tượng có tiến bộ tốt'
                },
                {
                    'case_number': '41CG0626/406LF',
                    'full_name': 'Trần Thị Bình',
                    'gender': Gender.FEMALE,
                    'birth_date': date(1985, 8, 20),
                    'address': 'TDP 2, P. Nam Hồng, TX. Hồng Lĩnh, Hà Tĩnh',
                    'occupation': 'Thất nghiệp',
                    'crime': 'Gây thương tích',
                    'case_type': CaseType.PROBATION,
                    'sentence_number': 'Số 20/2025/HS-ST, ngày 20/6/2025',
                    'decision_number': 'Số 20/2025/QĐ-CA, ngày 5/7/2025',
                    'start_date': date(2025, 7, 10),
                    'duration_months': 12,
                    'reduced_months': 0,
                    'reduction_count': 0,
                    'notes': 'Cần giám sát đặc biệt'
                },
                {
                    'case_number': '40CE0627/407LF',
                    'full_name': 'Lê Văn Cường',
                    'gender': Gender.MALE,
                    'birth_date': date(1995, 3, 10),
                    'address': 'TDP 3, P. Đậu Liêu, TX. Hồng Lĩnh, Hà Tĩnh',
                    'occupation': 'Công nhân',
                    'crime': 'Lừa đảo chiếm đoạt tài sản',
                    'case_type': CaseType.SUSPENDED_SENTENCE,
                    'sentence_number': 'Số 25/2025/HS-ST, ngày 25/7/2025',
                    'decision_number': 'Số 25/2025/QĐ-CA, ngày 10/8/2025',
                    'start_date': date(2025, 8, 15),
                    'duration_months': 18,
                    'reduced_months': 0,
                    'reduction_count': 0,
                    'notes': 'Đối tượng mới'
                }
            ]
            
            for offender_data in sample_offenders:
                try:
                    offender = Offender(**offender_data)
                    offender_id = db.create_offender(offender)
                    print(f"✓ Created offender: {offender.full_name} (ID: {offender_id})")
                except Exception as e:
                    print(f"✗ Error creating offender {offender_data['full_name']}: {e}")
            
            print(f"✓ Created {len(sample_offenders)} sample offenders")
            
    except Exception as e:
        print(f"✗ Error creating sample data: {e}")


def main():
    """Main function."""
    print("Initializing database...")
    
    try:
        # Create tables
        create_tables()
        print("✓ Database tables created")
        
        # Create default admin user
        create_default_admin()
        print("✓ Default admin user created")
        
        # Create sample data
        create_sample_data()
        print("✓ Sample data created")
        
        print("\nDatabase initialization completed successfully!")
        print("\nDefault login credentials:")
        print("Username: admin")
        print("Password: admin123")
        
    except Exception as e:
        print(f"✗ Error during database initialization: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 