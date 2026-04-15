/**
 * Vietnamese status/role label constants used across all UI components.
 */

export const PROPOSAL_STATUS = {
  DRAFT: 'DRAFT',
  SUBMITTED: 'SUBMITTED',
  REVISION_REQUESTED: 'REVISION_REQUESTED',
  VALIDATED: 'VALIDATED',
  UNDER_REVIEW: 'UNDER_REVIEW',
  REVIEWED: 'REVIEWED',
  APPROVED: 'APPROVED',
  REJECTED: 'REJECTED',
  IN_PROGRESS: 'IN_PROGRESS',
  ACCEPTANCE_SUBMITTED: 'ACCEPTANCE_SUBMITTED',
  UNDER_ACCEPTANCE_REVIEW: 'UNDER_ACCEPTANCE_REVIEW',
  ACCEPTANCE_REVISION_REQUESTED: 'ACCEPTANCE_REVISION_REQUESTED',
  ACCEPTED: 'ACCEPTED',
  ACCEPTANCE_FAILED: 'ACCEPTANCE_FAILED',
};

export const PROPOSAL_STATUS_LABELS = {
  DRAFT: 'Bản nháp',
  SUBMITTED: 'Đã nộp',
  REVISION_REQUESTED: 'Yêu cầu chỉnh sửa',
  VALIDATED: 'Đã kiểm tra',
  UNDER_REVIEW: 'Đang phản biện',
  REVIEWED: 'Đã phản biện',
  APPROVED: 'Đã phê duyệt',
  REJECTED: 'Từ chối',
  IN_PROGRESS: 'Đang thực hiện',
  ACCEPTANCE_SUBMITTED: 'Đã nộp nghiệm thu',
  UNDER_ACCEPTANCE_REVIEW: 'Đang nghiệm thu',
  ACCEPTANCE_REVISION_REQUESTED: 'Yêu cầu bổ sung',
  ACCEPTED: 'Nghiệm thu thành công',
  ACCEPTANCE_FAILED: 'Nghiệm thu không đạt',
};

export const PROPOSAL_STATUS_BADGE = {
  DRAFT: 'badge-gray',
  SUBMITTED: 'badge-blue',
  REVISION_REQUESTED: 'badge-amber',
  VALIDATED: 'badge-purple',
  UNDER_REVIEW: 'badge-purple',
  REVIEWED: 'badge-blue',
  APPROVED: 'badge-green',
  REJECTED: 'badge-red',
  IN_PROGRESS: 'badge-green',
  ACCEPTANCE_SUBMITTED: 'badge-blue',
  UNDER_ACCEPTANCE_REVIEW: 'badge-purple',
  ACCEPTANCE_REVISION_REQUESTED: 'badge-amber',
  ACCEPTED: 'badge-green',
  ACCEPTANCE_FAILED: 'badge-red',
};

export const ROLE_LABELS = {
  FACULTY: 'Giảng viên',
  STAFF: 'Phòng KHCN',
  LEADERSHIP: 'Lãnh đạo',
  REVIEWER: 'Phản biện',
  ADMIN: 'Quản trị viên',
};

export const PERIOD_STATUS_LABELS = {
  DRAFT: 'Bản nháp',
  OPEN: 'Đang mở',
  CLOSED: 'Đã đóng',
};

export const PERIOD_STATUS_BADGE = {
  DRAFT: 'badge-gray',
  OPEN: 'badge-green',
  CLOSED: 'badge-red',
};
