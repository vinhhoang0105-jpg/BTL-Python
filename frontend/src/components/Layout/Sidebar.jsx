/**
 * Sidebar navigation — role-based menu items.
 */

import { NavLink } from 'react-router-dom';
import {
  HiOutlineHome,
  HiOutlineDocumentText,
  HiOutlinePlusCircle,
  HiOutlineClipboardCheck,
  HiOutlineChartBar,
  HiOutlineUsers,
  HiOutlineCollection,
  HiOutlineCalendar,
  HiOutlineEye,
  HiOutlineShieldCheck,
  HiOutlineStar,
  HiOutlineClock,
} from 'react-icons/hi';
import { useAuth } from '../../contexts/AuthContext';
import './Sidebar.css';

const MENU_CONFIG = {
  FACULTY: [
    { to: '/', icon: HiOutlineHome, label: 'Tổng quan' },
    { to: '/my-proposals', icon: HiOutlineDocumentText, label: 'Đề tài của tôi' },
    { to: '/proposals/new', icon: HiOutlinePlusCircle, label: 'Tạo đề xuất' },
    { to: '/my-progress', icon: HiOutlineChartBar, label: 'Báo cáo tiến độ' },
    { to: '/my-acceptance', icon: HiOutlineClipboardCheck, label: 'Hồ sơ nghiệm thu' },
  ],
  STAFF: [
    { to: '/', icon: HiOutlineHome, label: 'Tổng quan' },
    { to: '/periods', icon: HiOutlineCalendar, label: 'Quản lý đợt đăng ký' },
    { to: '/proposals', icon: HiOutlineDocumentText, label: 'Danh sách hồ sơ' },
    { to: '/reviews', icon: HiOutlineEye, label: 'Quản lý xét duyệt' },
    { to: '/councils', icon: HiOutlineUsers, label: 'Quản lý hội đồng' },
    { to: '/progress', icon: HiOutlineClock, label: 'Theo dõi tiến độ' },
    { to: '/acceptance', icon: HiOutlineClipboardCheck, label: 'Quản lý nghiệm thu' },
    { to: '/reports', icon: HiOutlineChartBar, label: 'Báo cáo tổng hợp' },
  ],
  LEADERSHIP: [
    { to: '/', icon: HiOutlineHome, label: 'Tổng quan KPI' },
    { to: '/approvals', icon: HiOutlineShieldCheck, label: 'Chờ phê duyệt' },
    { to: '/reports', icon: HiOutlineChartBar, label: 'Báo cáo chiến lược' },
  ],
  REVIEWER: [
    { to: '/', icon: HiOutlineHome, label: 'Tổng quan' },
    { to: '/assigned', icon: HiOutlineDocumentText, label: 'Hồ sơ được phân công' },
    { to: '/councils/schedule', icon: HiOutlineCalendar, label: 'Lịch hội đồng' },
  ],
  ADMIN: [
    { to: '/', icon: HiOutlineHome, label: 'Tổng quan' },
    { to: '/users', icon: HiOutlineUsers, label: 'Quản lý người dùng' },
    { to: '/catalog', icon: HiOutlineCollection, label: 'Danh mục' },
    { to: '/periods', icon: HiOutlineCalendar, label: 'Đợt đăng ký' },
    { to: '/reports', icon: HiOutlineChartBar, label: 'Báo cáo' },
  ],
};

export default function Sidebar() {
  const { user } = useAuth();
  const menuItems = MENU_CONFIG[user?.role] || [];

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="sidebar-logo">
          <HiOutlineStar />
        </div>
        <div className="sidebar-brand-text">
          <span className="sidebar-brand-name">SciRes</span>
          <span className="sidebar-brand-sub">Quản lý NCKH</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === '/'}
            className={({ isActive }) =>
              `sidebar-link ${isActive ? 'sidebar-link-active' : ''}`
            }
          >
            <item.icon className="sidebar-link-icon" />
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div className="sidebar-version">v1.0.0 MVP</div>
      </div>
    </aside>
  );
}
