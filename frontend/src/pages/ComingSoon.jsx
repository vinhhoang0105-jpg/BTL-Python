/**
 * Placeholder page — shows "Coming Soon" for routes not yet implemented.
 */

import { useLocation } from 'react-router-dom';
import { HiOutlineCog } from 'react-icons/hi';

export default function ComingSoon() {
  const location = useLocation();

  return (
    <div className="empty-state" style={{ minHeight: '60vh' }}>
      <HiOutlineCog style={{ fontSize: 64 }} />
      <h2 style={{ fontSize: 'var(--font-size-xl)', color: 'var(--color-text-secondary)' }}>
        Đang phát triển
      </h2>
      <p style={{ color: 'var(--color-text-muted)', fontSize: 'var(--font-size-sm)' }}>
        Chức năng tại <code style={{ color: 'var(--color-accent)' }}>{location.pathname}</code> sẽ sớm được hoàn thiện.
      </p>
    </div>
  );
}
