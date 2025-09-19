-- ==============================================
-- 부서 테이블
-- ==============================================
CREATE TABLE department (
    dept_id INT PRIMARY KEY AUTO_INCREMENT,
    dept_name VARCHAR(50) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ==============================================
-- 권한(Role) 테이블
-- ==============================================
CREATE TABLE role (
    role_id INT PRIMARY KEY AUTO_INCREMENT,
    role_name VARCHAR(50) UNIQUE NOT NULL,
    role_level INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ==============================================
-- 직원(Employee) 테이블
-- ==============================================
CREATE TABLE employee (
    emp_id INT PRIMARY KEY AUTO_INCREMENT,
    emp_no VARCHAR(20) UNIQUE NOT NULL,
    dept_id INT NOT NULL,
    role_id INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    mobile VARCHAR(20) UNIQUE NOT NULL,
    hire_date DATE,
    birthday DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (dept_id) REFERENCES department (dept_id),
    FOREIGN KEY (role_id) REFERENCES role (role_id)
);

-- ==============================================
-- 외부인(External) 테이블
-- ==============================================
CREATE TABLE external_person (
    ext_id INT PRIMARY KEY AUTO_INCREMENT,
    ext_no VARCHAR(20) UNIQUE NOT NULL,
    dept_id INT NOT NULL,
    role_id INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    mobile VARCHAR(20) UNIQUE NOT NULL,
    company VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (dept_id) REFERENCES department (dept_id),
    FOREIGN KEY (role_id) REFERENCES role (role_id)
);

-- ==============================================
-- 로그인 계정(Member) 테이블
-- ==============================================
CREATE TABLE member (
    member_id INT PRIMARY KEY AUTO_INCREMENT,
    login_id VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    emp_id INT,
    ext_id INT,
    user_type ENUM('EMPLOYEE', 'EXTERNAL') NOT NULL,
    last_login_at DATETIME,
    failed_attempts INT DEFAULT 0,
    locked_until DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (emp_id) REFERENCES employee (emp_id),
    FOREIGN KEY (ext_id) REFERENCES external_person (ext_id)
);

-- ==============================================
-- 부서별 권한 테이블
-- ==============================================
CREATE TABLE department_permission (
    dept_id INT,
    role_id INT,
    permission ENUM('READ', 'WRITE', 'APPROVE') NOT NULL,
    PRIMARY KEY (dept_id, role_id, permission),
    FOREIGN KEY (dept_id) REFERENCES department (dept_id),
    FOREIGN KEY (role_id) REFERENCES role (role_id)
);

-- ==============================================
-- 결재 문서(Approval Document) 테이블
-- ==============================================
CREATE TABLE approval_document (
    app_doc_id INT PRIMARY KEY AUTO_INCREMENT,
    dept_id INT NOT NULL,
    emp_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    doc_type VARCHAR(50),
    doc_pass VARCHAR(50),
    start_date DATE,
    close_date DATE,
    due_date DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (dept_id) REFERENCES department (dept_id),
    FOREIGN KEY (emp_id) REFERENCES employee (emp_id)
);

-- ==============================================
-- 결재 문서 첨부 파일
-- ==============================================
CREATE TABLE app_file (
    file_id INT PRIMARY KEY AUTO_INCREMENT,
    app_doc_id INT NOT NULL,
    file_name VARCHAR(200),
    file_path VARCHAR(1024),
    file_type VARCHAR(50),
    file_uid VARCHAR(50),
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (app_doc_id) REFERENCES approval_document (app_doc_id)
);

-- ==============================================
-- 공지사항(Notice) 테이블
-- ==============================================
CREATE TABLE notice (
    notice_id INT PRIMARY KEY AUTO_INCREMENT,
    dept_id INT NOT NULL,
    title VARCHAR(100),
    content TEXT,
    reg_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    read_count INT DEFAULT 0,
    FOREIGN KEY (dept_id) REFERENCES department (dept_id)
);

-- ==============================================
-- 출퇴근(Attendance) 테이블
-- ==============================================
CREATE TABLE attendance (
    att_id INT PRIMARY KEY AUTO_INCREMENT,
    emp_id INT NOT NULL,
    dept_id INT NOT NULL,
    work_date DATE NOT NULL,
    start_time DATETIME,
    end_time DATETIME,
    att_type ENUM('WORK', 'VACATION', 'HOLIDAY') DEFAULT 'WORK',
    late BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (emp_id) REFERENCES employee (emp_id),
    FOREIGN KEY (dept_id) REFERENCES department (dept_id)
);

-- ==============================================
-- 개인 상태(Personal Status) 테이블
-- ==============================================
CREATE TABLE personal_status (
    status_id INT PRIMARY KEY AUTO_INCREMENT,
    emp_id INT NOT NULL,
    status ENUM('WORKING', 'AWAY', 'OUT_ON_BUSINESS', 'OFF_DUTY') NOT NULL,
    status_start DATETIME DEFAULT CURRENT_TIMESTAMP,
    status_end DATETIME,
    note VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (emp_id) REFERENCES employee (emp_id)
);

-- ==============================================
-- 결재 처리(App Processing) 테이블
-- ==============================================
CREATE TABLE app_processing (
    processing_id INT PRIMARY KEY AUTO_INCREMENT,
    app_doc_id INT NOT NULL,
    emp_id INT NOT NULL,
    role_type ENUM('MANAGER', 'TEAM_LEAD', 'CEO') NOT NULL,
    status ENUM('APPROVED', 'REJECTED', 'PENDING') DEFAULT 'PENDING',
    process_type ENUM('NORMAL', 'URGENT') DEFAULT 'NORMAL',
    comment_text TEXT,
    process_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    process_order INT,
    FOREIGN KEY (app_doc_id) REFERENCES approval_document (app_doc_id),
    FOREIGN KEY (emp_id) REFERENCES employee (emp_id)
);

-- ==============================================
-- 일정(Schedule) 테이블
-- ==============================================
CREATE TABLE schedule (
    schedule_id INT PRIMARY KEY AUTO_INCREMENT,
    emp_id INT NOT NULL,
    dept_id INT NOT NULL,
    type ENUM('MEETING', 'TASK', 'REMINDER') NOT NULL,
    title VARCHAR(200),
    content TEXT,
    memo TEXT,
    checked BOOLEAN DEFAULT FALSE,
    start_datetime DATETIME,
    end_datetime DATETIME,
    FOREIGN KEY (emp_id) REFERENCES employee (emp_id),
    FOREIGN KEY (dept_id) REFERENCES department (dept_id)
);

-- ==============================================
-- 프로젝트 테이블
-- ==============================================
CREATE TABLE project (
    project_id INT PRIMARY KEY AUTO_INCREMENT,
    project_name VARCHAR(200) NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    status ENUM('PLANNED', 'IN_PROGRESS', 'ON_HOLD', 'COMPLETED') DEFAULT 'PLANNED',
    owner_emp_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_emp_id) REFERENCES employee (emp_id)
);

-- ==============================================
-- 프로젝트 멤버
-- ==============================================
CREATE TABLE project_member (
    project_id INT NOT NULL,
    emp_id INT NOT NULL,
    role ENUM('OWNER', 'MANAGER', 'MEMBER', 'VIEWER') DEFAULT 'MEMBER',
    PRIMARY KEY (project_id, emp_id),
    FOREIGN KEY (project_id) REFERENCES project (project_id),
    FOREIGN KEY (emp_id) REFERENCES employee (emp_id)
);

-- ==============================================
-- 태스크(Task) 테이블
-- ==============================================
CREATE TABLE task (
    task_id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL,
    title VARCHAR(300) NOT NULL,
    description TEXT,
    assignee_emp_id INT,
    priority ENUM('LOW', 'MEDIUM', 'HIGH', 'URGENT') DEFAULT 'MEDIUM',
    status ENUM('TODO', 'IN_PROGRESS', 'REVIEW', 'DONE') DEFAULT 'TODO',
    parent_task_id INT NULL,
    start_date DATE,
    due_date DATE,
    estimate_hours DECIMAL(6, 2) DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES project (project_id),
    FOREIGN KEY (assignee_emp_id) REFERENCES employee (emp_id),
    FOREIGN KEY (parent_task_id) REFERENCES task (task_id)
);

-- ==============================================
-- 마일스톤(Milestone) 테이블
-- ==============================================
CREATE TABLE milestone (
    milestone_id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    due_date DATE,
    status ENUM('PLANNED', 'ACHIEVED', 'MISSED') DEFAULT 'PLANNED',
    FOREIGN KEY (project_id) REFERENCES project (project_id)
);

-- ==============================================
-- 태스크 코멘트(Task Comment) 테이블
-- ==============================================
CREATE TABLE task_comment (
    comment_id INT PRIMARY KEY AUTO_INCREMENT,
    task_id INT NOT NULL,
    emp_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES task (task_id),
    FOREIGN KEY (emp_id) REFERENCES employee (emp_id)
);

-- ==============================================
-- 첨부파일(Attachment) 테이블
-- ==============================================
CREATE TABLE attachment (
    attachment_id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NULL,
    task_id INT NULL,
    filename VARCHAR(255),
    path VARCHAR(1024),
    uploaded_by INT,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES project (project_id),
    FOREIGN KEY (task_id) REFERENCES task (task_id),
    FOREIGN KEY (uploaded_by) REFERENCES employee (emp_id)
);

-- ==============================================
-- 활동 로그(Activity Log) 테이블
-- ==============================================
CREATE TABLE activity_log (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    emp_id INT,
    project_id INT,
    task_id INT,
    action VARCHAR(100),
    detail TEXT,
    ip_address VARCHAR(50),
    user_agent VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (emp_id) REFERENCES employee (emp_id),
    FOREIGN KEY (project_id) REFERENCES project (project_id),
    FOREIGN KEY (task_id) REFERENCES task (task_id)
);
