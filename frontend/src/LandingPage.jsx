import React from 'react';
import { useNavigate } from 'react-router-dom';
import { BookOpen, Shield, Users, ArrowRight } from 'lucide-react';

function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="landing-container">
      <nav className="landing-nav">
        <div className="landing-logo">
          <BookOpen className="logo-icon" size={28} />
          <span>Khoa ATTT - NCKH</span>
        </div>
        <button className="btn-nav-login" onClick={() => navigate('/login')}>
          Đăng Nhập <ArrowRight size={16} style={{ marginLeft: '6px' }} />
        </button>
      </nav>

      <main className="landing-hero">
        <div className="hero-content">
          <div className="badge">Nền tảng Mới 2026</div>
          <h1>Hệ thống Quản lý <br/><span className="text-gradient">Nghiên cứu Khoa học</span></h1>
          <p>Nền tảng số hóa quy trình quản lý dự án, theo dõi tiến độ và lưu trữ thành quả nghiên cứu dành cho sinh viên và giảng viên khoa An toàn Thông tin.</p>
          <button className="btn-hero-primary" onClick={() => navigate('/login')}>
            Khám phá hệ thống <ArrowRight size={20} style={{ marginLeft: '8px' }} />
          </button>
        </div>
        <div className="hero-graphics">
          <div className="glass-card mockup-card">
            <div className="mockup-header">
              <span className="dot red"></span>
              <span className="dot yellow"></span>
              <span className="dot green"></span>
            </div>
            <div className="mockup-body">
              <div className="skeleton-line" style={{ width: '60%' }}></div>
              <div className="skeleton-line" style={{ width: '80%' }}></div>
              <div className="skeleton-line" style={{ width: '40%' }}></div>
              <div className="skeleton-box"></div>
            </div>
          </div>
        </div>
      </main>

      <section className="landing-features">
        <div className="feature-card">
          <Shield size={36} className="feature-icon" />
          <h3>Bảo mật & Phân quyền</h3>
          <p>Tự động phân biệt vai trò Admin, Sinh viên và Giảng viên với các quyền hạn riêng biệt bảo vệ dữ liệu nền tảng.</p>
        </div>
        <div className="feature-card">
          <Users size={36} className="feature-icon" />
          <h3>Quy trình Liên thông</h3>
          <p>Đăng ký, duyệt đề tài và theo dõi tiến độ báo cáo một cách linh hoạt, trực tiếp trên nền tảng trực tuyến.</p>
        </div>
        <div className="feature-card">
          <BookOpen size={36} className="feature-icon" />
          <h3>Kho lưu trữ Số</h3>
          <p>Lưu trữ tài liệu, bài báo khoa học và thành viên nhóm trên một hệ thống tập trung thuận tiện tìm kiếm.</p>
        </div>
      </section>
    </div>
  );
}

export default LandingPage;
