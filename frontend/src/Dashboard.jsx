import React, { useState, useEffect } from 'react';
import { LayoutDashboard, BookOpen, List, LogOut, Activity, FileText, CheckCircle, Clock } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import ProjectList from './ProjectList';
import MyProjects from './MyProjects';
import api from './api';

function Dashboard() {
  const [activeMenu, setActiveMenu] = useState('Tổng quan');
  const [user, setUser] = useState(null);
  const [stats, setStats] = useState({ total: 0, submitted: 0, approved: 0, completed: 0 });
  const navigate = useNavigate();

  // Kiểm tra quyền truy cập lúc component vừa load và fetch thông tin user
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
    } else {
      fetchUser();
      fetchStats();
    }
  }, [navigate]);

  const fetchUser = async () => {
    try {
      const response = await api.get('/api/auth/me');
      setUser(response.data);
    } catch (err) {
      console.error('Không thể lấy thông tin user. Token lỗi?', err);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await api.get('/api/projects/');
      const projs = response.data;
      setStats({
        total: projs.length,
        submitted: projs.filter(p => p.status === 'SUBMITTED').length,
        approved: projs.filter(p => p.status === 'APPROVED').length,
        completed: projs.filter(p => p.status === 'COMPLETED').length
      });
    } catch (err) {
      console.error('Không thể lấy danh sách đề tài để đếm', err);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  let menuItems = [
    { name: 'Tổng quan', icon: <LayoutDashboard size={20} /> },
    { name: 'Tất cả Đề tài', icon: <List size={20} /> }
  ];

  if (user && user.role === 'TEACHER') {
    // Chèn vào giữa để thứ tự tự nhiên hơn
    menuItems.splice(1, 0, { name: 'Đề tài của tôi', icon: <BookOpen size={20} /> });
  }

  return (
    <div className="app-container">
      {/* Sidebar Navigation */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <div className="avatar" style={{ width: 32, height: 32, fontSize: 14 }}>AT</div>
          <h2>Khoa ATTT</h2>
        </div>
        <nav className="nav-menu">
          {menuItems.map((item) => (
            <div
              key={item.name}
              className={`nav-item ${activeMenu === item.name ? 'active' : ''}`}
              onClick={() => setActiveMenu(item.name)}
            >
              {item.icon}
              <span>{item.name}</span>
            </div>
          ))}
        </nav>
      </aside>

      {/* Main Content Area */}
      <main className="main-content">
        <header className="topbar">
          <div className="page-title">{activeMenu}</div>
          <div className="user-profile">
            <div className="user-info">
              <div className="user-name">{user ? user.username : 'GUEST'}</div>
              <div className="user-role">{user ? user.role : 'Đang tải...'}</div>
            </div>
            <div className="avatar">{user ? user.username.charAt(0).toUpperCase() : 'U'}</div>
            <button className="btn-logout" title="Đăng xuất" onClick={handleLogout}>
              Logout
            </button>
          </div>
        </header>

        <div className="content-area">
          {activeMenu === 'Tất cả Đề tài' ? (
            <ProjectList user={user} />
          ) : activeMenu === 'Đề tài của tôi' ? (
            <MyProjects user={user} />
          ) : (
            <div className="overview-container" key={activeMenu}>
              <div className="overview-header">
                <h3>Tổng Quan Hệ Thống</h3>
                <p>Xin chào, <strong className="text-primary">{user ? user.username : 'GUEST'}</strong>! Cấp quyền hiện tại của bạn là: <span className="status-badge status-approved">{user?.role}</span></p>
              </div>
              
              <div className="stats-grid">
                <div className="stat-card">
                  <div className="stat-icon" style={{backgroundColor: '#e0f2fe', color: '#0284c7'}}><FileText size={28}/></div>
                  <div className="stat-info">
                    <h4>Tổng số đề tài</h4>
                    <h2>{stats.total}</h2>
                  </div>
                </div>
                <div className="stat-card">
                  <div className="stat-icon" style={{backgroundColor: '#fef3c7', color: '#d97706'}}><Clock size={28}/></div>
                  <div className="stat-info">
                    <h4>Chờ duyệt</h4>
                    <h2>{stats.submitted}</h2>
                  </div>
                </div>
                <div className="stat-card">
                  <div className="stat-icon" style={{backgroundColor: '#dcfce7', color: '#16a34a'}}><Activity size={28}/></div>
                  <div className="stat-info">
                    <h4>Đang thực hiện</h4>
                    <h2>{stats.approved}</h2>
                  </div>
                </div>
                <div className="stat-card">
                  <div className="stat-icon" style={{backgroundColor: '#f3e8ff', color: '#9333ea'}}><CheckCircle size={28}/></div>
                  <div className="stat-info">
                    <h4>Hoàn thành</h4>
                    <h2>{stats.completed}</h2>
                  </div>
                </div>
              </div>
              
              <div className="overview-content">
                <div className="dashboard-card" style={{ marginTop: '20px' }}>
                  <h3>Giới thiệu nhanh</h3>
                  <p>Hệ thống Quản lý NCKH hỗ trợ sinh viên và giảng viên khoa ATTT thực hiện đăng ký, xét duyệt và lưu trữ các đề tài nghiên cứu khoa học. Sử dụng thanh công cụ bên trái để bắt đầu.</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default Dashboard;
