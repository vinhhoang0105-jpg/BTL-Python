# 🔬 SciRes — Hệ thống Quản lý Nghiên cứu Khoa học

Hệ thống quản lý vòng đời đề tài NCKH cấp trường: từ đăng ký, phản biện, phê duyệt, thực hiện đến nghiệm thu.

## Cấu trúc dự án

```
BTL-PY/
├── docs/               # Tài liệu kiến trúc & nghiệp vụ
├── backend/            # FastAPI + SQLAlchemy + PostgreSQL
│   ├── app/
│   │   ├── api/        # Routers: auth, users, catalog, periods, proposals, councils, workflow
│   │   ├── core/       # Security, dependencies, exceptions
│   │   ├── models/     # SQLAlchemy ORM models (18 tables)
│   │   ├── seed/       # Seed data mẫu
│   │   ├── schemas.py  # Tất cả Pydantic schemas
│   │   └── main.py     # FastAPI app entry point
│   └── alembic/        # Database migrations
└── frontend/           # HTML thuần + Vanilla JS (nginx)
    ├── index.html      # Trang đăng nhập
    ├── app.html        # Ứng dụng chính
    ├── js/             # api.js + app.js
    └── css/            # style.css
```

---

## Khởi động

```bash
docker-compose up --build -d
```

Chờ 30–60 giây. Kiểm tra log:

```bash
docker-compose logs backend --tail=30
```

> Tìm dòng `Application startup complete` và `Seed data inserted successfully!`

---

## Các URL

| Dịch vụ | URL |
|---|---|
| **Frontend** | http://localhost:3000 |
| **Swagger API Docs** | http://localhost:8000/docs |
| **Health Check** | http://localhost:8000/api/health |

---

## Tài khoản demo (password: `password123`)

| Role | Email |
|---|---|
| Admin | admin@university.edu.vn |
| Staff (P.KHCN) | staff@university.edu.vn |
| Lãnh đạo | leader@university.edu.vn |
| Giảng viên (PI) | faculty1@university.edu.vn |
| Giảng viên | faculty2@university.edu.vn |
| Phản biện | reviewer1@university.edu.vn |
| Phản biện | reviewer2@university.edu.vn |

---

## Luồng test chính (full lifecycle)

```
DRAFT → SUBMITTED → VALIDATED → UNDER_REVIEW → REVIEWED
     → IN_PROGRESS → ACCEPTANCE_SUBMITTED → UNDER_ACCEPTANCE_REVIEW → ACCEPTED
```

### Bước 1 — Mở đợt đăng ký (Staff)
> Seed data đã có sẵn 1 đợt OPEN, có thể bỏ qua bước này.

Login `staff@university.edu.vn` → **Đợt đăng ký** → Tạo hoặc bấm **Mở**.

---

### Bước 2 — Giảng viên tạo và nộp đề tài

Login `faculty1@university.edu.vn` → **Tạo đề tài**:
- Điền đầy đủ tất cả các trường
- Chọn đợt đăng ký đang OPEN
- Bấm **Nộp ngay** (hoặc Lưu → vào "Đề tài của tôi" → bấm **Nộp**)

✅ Đề tài chuyển sang `SUBMITTED`

---

### Bước 3 — Staff kiểm tra hồ sơ

Login `staff@university.edu.vn` → **Kiểm tra hồ sơ**:
- Bấm **✓ Hợp lệ** → `VALIDATED`
- Hoặc **↩ Trả về** (nhập lý do ≥10 ký tự) → `REVISION_REQUESTED`

---

### Bước 4 — Staff tạo hội đồng phản biện

Login `staff@university.edu.vn` → **Hội đồng** → Tạo hội đồng (chọn loại `Phản biện đề tài`).

Sau đó dùng **Swagger UI** tại `http://localhost:8000/docs`:
1. Login lấy token: `POST /api/auth/login` → copy `access_token`
2. Bấm 🔒 **Authorize** → dán `Bearer <token>`
3. Lấy `council_id` từ response vừa tạo
4. `POST /api/councils/{council_id}/members` — thêm `reviewer1` (role: `CHAIR`)
5. `POST /api/councils/{council_id}/members` — thêm `reviewer2` (role: `REVIEWER`)
6. `POST /api/councils/{council_id}/activate` → đề tài chuyển `UNDER_REVIEW`

---

### Bước 5 — Phản biện nộp đánh giá

Login `reviewer1@university.edu.vn` → **Phản biện** → **Nộp đánh giá**:
- Điểm: 0–100
- Kết luận: PASS / FAIL / NEEDS_REVISION
- Nhận xét: ≥50 ký tự

Lặp lại với `reviewer2`. Khi cả 2 xong → đề tài tự động chuyển `REVIEWED`.

---

### Bước 6 — Lãnh đạo phê duyệt

Login `leader@university.edu.vn` → **Phê duyệt**:
- Xem kết quả phản biện → **✓ Phê duyệt** → `APPROVED` → tự động vào `IN_PROGRESS`

---

### Bước 7 — Giảng viên nộp báo cáo tiến độ

Login `faculty1@university.edu.vn` → **Báo cáo tiến độ** → Chọn đề tài → Điền và nộp.

---

### Bước 8 — Giảng viên nộp hồ sơ nghiệm thu

Login `faculty1@university.edu.vn` → **Nghiệm thu** → Điền báo cáo tổng kết → **Nộp** → `ACCEPTANCE_SUBMITTED`

---

### Bước 9 — Staff tạo hội đồng nghiệm thu & Phản biện đánh giá

Lặp lại Bước 4–5 nhưng chọn loại `Nghiệm thu` khi tạo hội đồng.

---

### Bước 10 — Lãnh đạo xác nhận kết quả

Login `leader@university.edu.vn` → **Xác nhận NThu** → **✓ Đạt** → `ACCEPTED`

---

## Lệnh hữu ích

```bash
# Xem log realtime
docker-compose logs -f backend

# Khởi động lại backend
docker-compose restart backend

# Reset toàn bộ dữ liệu (xóa DB)
docker-compose down -v
docker-compose up -d

# Dừng tất cả
docker-compose down
```

---

## Biến môi trường (`.env`)

| Biến | Mặc định |
|---|---|
| `POSTGRES_USER` | scires |
| `POSTGRES_PASSWORD` | scires_secret |
| `DATABASE_URL` | postgresql://scires:scires_secret@db:5432/scires_db |
| `SECRET_KEY` | dev-secret-key-change-in-production |
| `AUTO_SEED` | true |
| `BACKEND_PORT` | 8000 |
