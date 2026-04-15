/**
 * Top header bar — user info, role badge, logout.
 */

import { HiOutlineLogout, HiOutlineUserCircle } from 'react-icons/hi';
import { useAuth } from '../../contexts/AuthContext';
import { ROLE_LABELS } from '../../utils/constants';
import './Header.css';

export default function Header() {
  const { user, logout } = useAuth();

  return (
    <header className="app-header">
      <div className="header-left">
        <h2 className="header-greeting">
          Xin chào, <span className="header-username">{user?.full_name}</span>
        </h2>
      </div>

      <div className="header-right">
        <div className="header-role-badge">
          <HiOutlineUserCircle />
          <span>{ROLE_LABELS[user?.role] || user?.role}</span>
        </div>
        <button className="btn btn-ghost btn-sm" onClick={logout} title="Đăng xuất">
          <HiOutlineLogout />
          <span>Đăng xuất</span>
        </button>
      </div>
    </header>
  );
}
