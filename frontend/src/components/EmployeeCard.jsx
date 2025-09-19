import React, { useEffect, useMemo, useState } from 'react';

import { STATUS_LABELS } from '../constants.js';
import { formatDateTime } from '../utils/format.js';

function useEmployeeForm(employee) {
  const [formState, setFormState] = useState({
    name: employee.name,
    email: employee.email,
    mobile: employee.mobile,
    password_hash: employee.password_hash || ''
  });

  useEffect(() => {
    setFormState({
      name: employee.name,
      email: employee.email,
      mobile: employee.mobile,
      password_hash: employee.password_hash || ''
    });
  }, [employee]);

  return [formState, setFormState];
}

function useStatusForm(employee, statusOptions) {
  const initialStatus = employee.current_status?.status || statusOptions[0] || 'WORKING';
  const [statusState, setStatusState] = useState({
    status: initialStatus,
    note: employee.current_status?.note || ''
  });

  useEffect(() => {
    setStatusState({
      status: employee.current_status?.status || statusOptions[0] || 'WORKING',
      note: employee.current_status?.note || ''
    });
  }, [employee, statusOptions]);

  return [statusState, setStatusState];
}

const EmployeeCard = ({ employee, statusOptions, onUpdateEmployee, onUpdateStatus }) => {
  const [formState, setFormState] = useEmployeeForm(employee);
  const [statusState, setStatusState] = useStatusForm(employee, statusOptions);
  const [saving, setSaving] = useState(false);
  const [statusSaving, setStatusSaving] = useState(false);
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (message || error) {
      const timeout = setTimeout(() => {
        setMessage(null);
        setError(null);
      }, 2500);
      return () => clearTimeout(timeout);
    }
    return undefined;
  }, [message, error]);

  const statusLabel = useMemo(() => {
    const code = employee.current_status?.status;
    if (!code) return '상태 정보 없음';
    return STATUS_LABELS[code] || code;
  }, [employee.current_status]);

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFormState((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSaving(true);
    setError(null);
    try {
      await onUpdateEmployee(employee.emp_id, formState);
      setMessage('직원 정보가 저장되었습니다.');
    } catch (err) {
      setError(err.response?.data?.detail || '저장 중 오류가 발생했습니다.');
    } finally {
      setSaving(false);
    }
  };

  const handleStatusSubmit = async (event) => {
    event.preventDefault();
    setStatusSaving(true);
    setError(null);
    try {
      await onUpdateStatus(employee.emp_id, statusState);
      setMessage('개인 상태가 갱신되었습니다.');
    } catch (err) {
      setError(err.response?.data?.detail || '상태 변경 중 오류가 발생했습니다.');
    } finally {
      setStatusSaving(false);
    }
  };

  return (
    <section className="employee-card">
      <div className="employee-header">
        <h2>{employee.name}</h2>
        <p className="employee-meta">
          {employee.emp_no} · {employee.department_name || '부서 미지정'} · {employee.role_name || '직책 미지정'}
        </p>
        {employee.current_status && (
          <div className="status-pill">
            <span>{statusLabel}</span>
            <span>{formatDateTime(employee.current_status.status_start)}</span>
          </div>
        )}
      </div>

      <form className="form-grid" onSubmit={handleSubmit}>
        <label>
          이름
          <input name="name" value={formState.name} onChange={handleInputChange} />
        </label>
        <label>
          이메일
          <input name="email" type="email" value={formState.email} onChange={handleInputChange} />
        </label>
        <label>
          휴대전화
          <input name="mobile" value={formState.mobile} onChange={handleInputChange} />
        </label>
        <label>
          패스워드 해시
          <input name="password_hash" value={formState.password_hash} onChange={handleInputChange} />
        </label>
        <div className="form-actions">
          <button className="primary" type="submit" disabled={saving}>
            {saving ? '저장 중...' : '기본 정보 저장'}
          </button>
        </div>
      </form>

      <form className="form-grid" onSubmit={handleStatusSubmit}>
        <label>
          개인 상태
          <select
            name="status"
            value={statusState.status}
            onChange={(event) =>
              setStatusState((prev) => ({ ...prev, status: event.target.value }))
            }
          >
            {statusOptions.map((option) => (
              <option key={option} value={option}>
                {STATUS_LABELS[option] || option}
              </option>
            ))}
          </select>
        </label>
        <label>
          메모
          <textarea
            rows={2}
            name="note"
            value={statusState.note}
            onChange={(event) =>
              setStatusState((prev) => ({ ...prev, note: event.target.value }))
            }
          />
        </label>
        <div className="form-actions">
          <button className="secondary" type="submit" disabled={statusSaving}>
            {statusSaving ? '갱신 중...' : '상태 변경'}
          </button>
        </div>
      </form>

      {message && <p style={{ color: '#047857' }}>{message}</p>}
      {error && <p style={{ color: '#dc2626' }}>{error}</p>}

      {employee.current_status && (
        <div className="status-history">
          <div>시작: {formatDateTime(employee.current_status.status_start)}</div>
          {employee.current_status.status_end && (
            <div>종료: {formatDateTime(employee.current_status.status_end)}</div>
          )}
          {employee.current_status.note && <div>메모: {employee.current_status.note}</div>}
        </div>
      )}
    </section>
  );
};

export default EmployeeCard;
