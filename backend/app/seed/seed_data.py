"""Seed realistic Vietnamese university data for demo purposes.

Run standalone: python -m app.seed.seed_data
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.catalog import Department, ResearchField
from app.models.period import RegistrationPeriod
from app.core.security import hash_password
from datetime import date


def seed():
    """Insert seed data into the database."""
    # Create all tables if they don't exist
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Skip if data already exists
        if db.query(User).first():
            print("⚠️  Database already has data, skipping seed.")
            return

        print("🌱 Seeding database...")

        # ── Departments ──────────────────────────────────────────
        departments = [
            Department(name="Khoa Công nghệ Thông tin", code="CNTT"),
            Department(name="Khoa Điện - Điện tử", code="DDE"),
            Department(name="Khoa Cơ khí", code="CK"),
            Department(name="Khoa Kinh tế", code="KT"),
            Department(name="Khoa Ngoại ngữ", code="NN"),
            Department(name="Khoa Khoa học Cơ bản", code="KHCB"),
            Department(name="Khoa Xây dựng", code="XD"),
            Department(name="Khoa Môi trường", code="MT"),
        ]
        db.add_all(departments)
        db.flush()
        print(f"  ✅ {len(departments)} departments")

        # ── Research Fields ──────────────────────────────────────
        fields = [
            ResearchField(name="Trí tuệ nhân tạo", code="AI"),
            ResearchField(name="Internet vạn vật", code="IOT"),
            ResearchField(name="An toàn thông tin", code="ATTT"),
            ResearchField(name="Khoa học dữ liệu", code="DS"),
            ResearchField(name="Năng lượng tái tạo", code="NLTT"),
            ResearchField(name="Vật liệu tiên tiến", code="VLTT"),
            ResearchField(name="Kinh tế số", code="KTS"),
            ResearchField(name="Phát triển bền vững", code="PTBV"),
            ResearchField(name="Công nghệ sinh học", code="CNSH"),
            ResearchField(name="Tự động hóa", code="TDH"),
        ]
        db.add_all(fields)
        db.flush()
        print(f"  ✅ {len(fields)} research fields")

        # ── Users ────────────────────────────────────────────────
        default_pw = hash_password("password123")

        users = [
            # Admin
            User(
                email="admin@university.edu.vn",
                hashed_password=default_pw,
                full_name="Nguyễn Quản Trị",
                role="ADMIN",
                department_id=departments[0].id,
            ),
            # S&T Staff
            User(
                email="staff@university.edu.vn",
                hashed_password=default_pw,
                full_name="Trần Thị Phòng KHCN",
                role="STAFF",
                department_id=departments[0].id,
                phone="0901234567",
            ),
            # Leadership
            User(
                email="leader@university.edu.vn",
                hashed_password=default_pw,
                full_name="Phạm Văn Lãnh Đạo",
                role="LEADERSHIP",
                academic_rank="Giáo sư",
                academic_title="Tiến sĩ",
                department_id=departments[0].id,
                phone="0912345678",
            ),
            # Faculty members
            User(
                email="faculty1@university.edu.vn",
                hashed_password=default_pw,
                full_name="Lê Văn Nghiên Cứu",
                role="FACULTY",
                academic_rank="Phó Giáo sư",
                academic_title="Tiến sĩ",
                department_id=departments[0].id,
                phone="0923456789",
            ),
            User(
                email="faculty2@university.edu.vn",
                hashed_password=default_pw,
                full_name="Hoàng Thị Khoa Học",
                role="FACULTY",
                academic_rank="Giảng viên",
                academic_title="Thạc sĩ",
                department_id=departments[1].id,
                phone="0934567890",
            ),
            User(
                email="faculty3@university.edu.vn",
                hashed_password=default_pw,
                full_name="Ngô Minh Dữ Liệu",
                role="FACULTY",
                academic_rank="Giảng viên chính",
                academic_title="Tiến sĩ",
                department_id=departments[0].id,
                phone="0945678901",
            ),
            # Reviewers
            User(
                email="reviewer1@university.edu.vn",
                hashed_password=default_pw,
                full_name="Đặng Phản Biện",
                role="REVIEWER",
                academic_rank="Phó Giáo sư",
                academic_title="Tiến sĩ",
                department_id=departments[1].id,
                phone="0956789012",
            ),
            User(
                email="reviewer2@university.edu.vn",
                hashed_password=default_pw,
                full_name="Vũ Thị Đánh Giá",
                role="REVIEWER",
                academic_rank="Giáo sư",
                academic_title="Tiến sĩ",
                department_id=departments[2].id,
                phone="0967890123",
            ),
        ]
        db.add_all(users)
        db.flush()
        print(f"  ✅ {len(users)} users")

        # ── Registration Periods ─────────────────────────────────
        periods = [
            RegistrationPeriod(
                title="Đợt đăng ký NCKH Học kỳ 1 - 2026",
                description="Đợt đăng ký đề tài nghiên cứu khoa học cấp trường, học kỳ 1 năm học 2025-2026",
                start_date=date(2026, 1, 15),
                end_date=date(2026, 6, 30),
                status="OPEN",
            ),
            RegistrationPeriod(
                title="Đợt đăng ký NCKH Học kỳ 2 - 2026",
                description="Đợt đăng ký đề tài nghiên cứu khoa học cấp trường, học kỳ 2 năm học 2025-2026",
                start_date=date(2026, 7, 1),
                end_date=date(2026, 12, 31),
                status="DRAFT",
            ),
        ]
        db.add_all(periods)
        db.flush()
        print(f"  ✅ {len(periods)} registration periods")

        db.commit()
        print("🎉 Seed data inserted successfully!")
        print()
        print("📋 Demo accounts (password: password123):")
        print("   Admin:      admin@university.edu.vn")
        print("   Staff:      staff@university.edu.vn")
        print("   Leadership: leader@university.edu.vn")
        print("   Faculty:    faculty1@university.edu.vn")
        print("   Reviewer:   reviewer1@university.edu.vn")

    except Exception as e:
        db.rollback()
        print(f"❌ Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
