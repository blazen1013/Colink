import React, { useEffect, useMemo, useState } from 'react';

import { STATUS_LABELS } from '../constants.js';
import { formatDateTime } from '../utils/format.js';
import {
  fetchMemberProfile,
  updateMemberProfile,
  updateMemberStatus
} from '../api.js';

const defaultProfileForm = {
  name: '',
  email: '',
  mobile: '',
  password_hash: ''
};

const defaultStatusForm = (initialStatus) => ({
  status: initialStatus,
  note: ''
});

const PersonalSettings = ({ statusOptions }) => {
  const [loginId, setLoginId] = useState('');
  const [profile, setProfile] = useState(null);
  const [profileForm, setProfileForm] = useState(defaultProfileForm);
  const [statusForm, setStatusForm] = useState(defaultStatusForm(statusOptions[0] || 'WORKING'));
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [statusSaving, setStatusSaving] = useState(false);
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);

  const currentStatusLabel = useMemo(() => {
    if (!profile?.employee?.current_status?.status) return '상태 정보 없음';
    const code = profile.employee.current_status.status;
    return STATUS_LABELS[code] || code;
  }, [profile]);

  useEffect(() => {
    if (!profile?.employee) {
      setProfileForm(defaultProfileForm);
      setStatusForm(defaultStatusForm(statusOptions[0] || 'WORKING'));
      return;
    }

    setProfileForm({
      name: profile.employee.name || '',
      email: profile.employee.email || '',
      mobile: profile.employee.mobile || '',
      password_hash: profile.employee.password_hash || ''
    });
    setStatusForm({
      status:
        profile.employee.current_status?.status || statusOptions[0] || 'WORKING',
      note: profile.employee.current_status?.note || ''
    });
  }, [profile, statusOptions]);

  useEffect(() => {
    if (!message && !error) {
      return undefined;
    }
    const timeout = setTimeout(() => {
      setMessage(null);
      setError(null);
    }, 2500);
    return () => clearTimeout(timeout);
  }, [message, error]);

  const handleLoadProfile = async (event) => {
    event.preventDefault();
    const trimmedId = loginId.trim();
    if (!trimmedId) {
      setError('로그인 ID를 입력해주세요.');
      return;
    }

    setLoading(true);
    setError(null);
    setMessage(null);
    try {
      const data = await fetchMemberProfile(trimmedId);
      setProfile(data);
      setMessage('내 정보를 불러왔습니다.');
    } catch (err) {
      setProfile(null);
      setError(err.response?.data?.detail || '프로필을 불러오지 못했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const handleProfileChange = (event) => {
    const { name, value } = event.target;
    setProfileForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleStatusChange = (event) => {
    const { name, value } = event.target;
    setStatusForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleProfileSubmit = async (event) => {
    event.preventDefault();
    if (!profile?.employee) {
      setError('직원 정보가 연결되지 않았습니다.');
      return;
    }

    setSaving(true);
    setError(null);
    try {
      const updated = await updateMemberProfile(profile.login_id, profileForm);
      setProfile(updated);
      setMessage('내 정보가 저장되었습니다.');
    } catch (err) {
      setError(err.response?.data?.detail || '저장 중 오류가 발생했습니다.');
    } finally {
      setSaving(false);
    }
  };

  const handleStatusSubmit = async (event) => {
    event.preventDefault();
    if (!profile?.employee) {
      setError('직원 정보가 연결되지 않았습니다.');
      return;
    }

    setStatusSaving(true);
    setError(null);
    try {
      const updatedStatus = await updateMemberStatus(profile.login_id, statusForm);
      setProfile((prev) =>
        prev
          ? {
              ...prev,
              employee: {
                ...prev.employee,
                current_status: updatedStatus
              }
            }
          : prev
      );
      setStatusForm((prev) => ({ ...prev, status: updatedStatus.status }));
      setMessage('개인 상태가 갱신되었습니다.');
    } catch (err) {
      setError(err.response?.data?.detail || '상태 변경 중 오류가 발생했습니다.');
    } finally {
      setStatusSaving(false);
    }
  };

  return (
    <section className="employee-card personal-settings-card">
      <form className="profile-loader" onSubmit={handleLoadProfile}>
        <label>
          로그인 ID
          <div className="loader-row">
            <input
              name="loginId"
              placeholder="예: D001001"
              value={loginId}
              onChange={(event) => setLoginId(event.target.value)}
            />
            <button className="secondary" type="submit" disabled={loading}>
              {loading ? '불러오는 중...' : '내 정보 불러오기'}
            </button>
          </div>
        </label>
      </form>

      {profile && profile.employee ? (
        <>
          <div className="profile-summary">
            <h3>{profile.employee.name}</h3>
            <p>
              {profile.employee.emp_no} · {profile.employee.department_name || '부서 미지정'} ·{' '}
              {profile.employee.role_name || '직책 미지정'}
            </p>
            {profile.employee.current_status && (
              <div className="status-pill">
                <span>{currentStatusLabel}</span>
                <span>{formatDateTime(profile.employee.current_status.status_start)}</span>
              </div>
            )}
          </div>

          <form className="form-grid" onSubmit={handleProfileSubmit}>
            <label>
              이름
              <input name="name" value={profileForm.name} onChange={handleProfileChange} />
            </label>
            <label>
              이메일
              <input
                name="email"
                type="email"
                value={profileForm.email}
                onChange={handleProfileChange}
              />
            </label>
            <label>
              휴대전화
              <input name="mobile" value={profileForm.mobile} onChange={handleProfileChange} />
            </label>
            <label>
              패스워드 해시
              <input
                name="password_hash"
                value={profileForm.password_hash}
                onChange={handleProfileChange}
              />
            </label>
            <div className="form-actions">
              <button className="primary" type="submit" disabled={saving}>
                {saving ? '저장 중...' : '내 정보 저장'}
              </button>
            </div>
          </form>

          <form className="form-grid" onSubmit={handleStatusSubmit}>
            <label>
              개인 상태
              <select
                name="status"
                value={statusForm.status}
                onChange={handleStatusChange}
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
                value={statusForm.note}
                onChange={handleStatusChange}
              />
            </label>
            <div className="form-actions">
              <button className="secondary" type="submit" disabled={statusSaving}>
                {statusSaving ? '갱신 중...' : '상태 변경'}
              </button>
            </div>
          </form>

          <div className="status-history">
            <div>
              시작:{' '}
              {formatDateTime(profile.employee.current_status?.status_start)}
            </div>
            {profile.employee.current_status?.status_end && (
              <div>종료: {formatDateTime(profile.employee.current_status.status_end)}</div>
            )}
            {profile.employee.current_status?.note && (
              <div>메모: {profile.employee.current_status.note}</div>
            )}
          </div>
        </>
      ) : (
        <p className="profile-placeholder">
          {loading
            ? '내 정보를 불러오고 있습니다...'
            : '로그인 ID를 입력한 뒤 "내 정보 불러오기" 버튼을 눌러주세요.'}
        </p>
      )}

      {message && <p className="feedback success">{message}</p>}
      {error && <p className="feedback error">{error}</p>}
    </section>
  );
};

export default PersonalSettings;
