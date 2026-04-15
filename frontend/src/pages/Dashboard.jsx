/**
 * Generic dashboard — placeholder shown after login.
 * Each role will get a specialized dashboard in Milestone 5.
 */

import { useAuth } from '../contexts/AuthContext';
import { ROLE_LABELS } from '../utils/constants';
import {
  HiOutlineDocumentText,
  HiOutlineClipboardCheck,
  HiOutlineClock,
  HiOutlineChartBar,
} from 'react-icons/hi';

export default function Dashboard() {
  const { user } = useAuth();

  const stats = [
    { label: 'Đề tài', value: '—', icon: HiOutlineDocumentText, color: 'var(--color-accent)' },
    { label: 'Đang thực hiện', value: '—', icon: HiOutlineClock, color: 'var(--color-success)' },
    { label: 'Chờ duyệt', value: '—', icon: HiOutlineClipboardCheck, color: 'var(--color-warning)' },
    { label: 'Hoàn thành', value: '—', icon: HiOutlineChartBar, color: 'var(--color-info)' },
  ];

  return (
    <div className="animate-fade-in">
      <div className="page-header">
        <div>
          <h1 className="page-title">Tổng quan</h1>
          <p className="page-subtitle">
            {ROLE_LABELS[user?.role]} — {user?.department_name || 'Chưa gán khoa'}
          </p>
        </div>
      </div>

      <div className="stats-grid">
        {stats.map((s) => (
          <div key={s.label} className="stat-card">
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <span className="stat-label">{s.label}</span>
              <s.icon style={{ fontSize: 24, color: s.color, opacity: 0.7 }} />
            </div>
            <span className="stat-value">{s.value}</span>
          </div>
        ))}
      </div>

      <div className="card" style={{ marginTop: 'var(--space-8)', textAlign: 'center', padding: 'var(--space-12)' }}>
        <p style={{ color: 'var(--color-text-muted)', fontSize: 'var(--font-size-md)' }}>
          🚀 Dashboard chi tiết sẽ được phát triển theo từng module nghiệp vụ.
        </p>
        <p style={{ color: 'var(--color-text-muted)', fontSize: 'var(--font-size-sm)', marginTop: 'var(--space-2)' }}>
          Sử dụng menu bên trái để điều hướng.
        </p>
      </div>
    </div>
  );
}
