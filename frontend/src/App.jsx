import React, { useEffect, useState } from 'react';
import EmployeeCard from './components/EmployeeCard.jsx';
import PersonalSettings from './components/PersonalSettings.jsx';
import {
  fetchEmployees,
  fetchStatusOptions,
  updateEmployee,
  updateEmployeeStatus
} from './api.js';

const App = () => {
  const [employees, setEmployees] = useState([]);
  const [statusOptions, setStatusOptions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadInitialData = async () => {
      try {
        setLoading(true);
        const [employeeList, statusList] = await Promise.all([
          fetchEmployees(),
          fetchStatusOptions()
        ]);
        setEmployees(employeeList);
        setStatusOptions(statusList);
      } catch (err) {
        setError('데이터를 불러오는 중 문제가 발생했습니다.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    loadInitialData();
  }, []);

  const handleUpdateEmployee = async (empId, payload) => {
    const updatedEmployee = await updateEmployee(empId, payload);
    setEmployees((prev) =>
      prev.map((employee) => (employee.emp_id === empId ? updatedEmployee : employee))
    );
  };

  const handleUpdateStatus = async (empId, payload) => {
    const updatedStatus = await updateEmployeeStatus(empId, payload);
    setEmployees((prev) =>
      prev.map((employee) =>
        employee.emp_id === empId
          ? { ...employee, current_status: updatedStatus }
          : employee
      )
    );
  };

  if (loading) {
    return (
      <main>
        <h1>직원 개인 상태 관리</h1>
        <p>불러오는 중...</p>
      </main>
    );
  }

  if (error) {
    return (
      <main>
        <h1>직원 개인 상태 관리</h1>
        <p style={{ color: '#dc2626' }}>{error}</p>
      </main>
    );
  }

  return (
    <main>
      <h1>직원 개인 상태 관리</h1>

      <section className="personal-settings-section">
        <h2>개인 설정</h2>
        <PersonalSettings statusOptions={statusOptions} />
      </section>

      <section className="employee-management-section">
        <h2>직원 관리</h2>
        {employees.map((employee) => (
          <EmployeeCard
            key={employee.emp_id}
            employee={employee}
            statusOptions={statusOptions}
            onUpdateEmployee={handleUpdateEmployee}
            onUpdateStatus={handleUpdateStatus}
          />
        ))}
        {employees.length === 0 && <p>등록된 직원이 없습니다.</p>}
      </section>
    </main>
  );
};

export default App;
