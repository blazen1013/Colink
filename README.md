# Colink

직원의 기본 정보와 개인 상태를 관리하기 위한 FastAPI + React 예시 프로젝트입니다.

## 폴더 구조

- `backend/` – FastAPI 애플리케이션과 SQLite 데이터베이스 초기화 코드
- `frontend/` – Vite 기반 React 클라이언트
- `db/schema.sql` – 전체 시스템을 위한 참고용 데이터베이스 스키마

## 개발 환경 실행 방법

### 1. FastAPI 서버

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

서버는 기본적으로 `http://localhost:8000`에서 실행되며 초기 더미 데이터(직원, 계정, 개인 상태)를 자동으로 생성합니다.

### 2. React 클라이언트

```bash
cd frontend
npm install
npm run dev
```

개발 서버는 `http://localhost:5173`에서 실행되며, FastAPI 서버의 API(`VITE_API_URL` 환경 변수로 변경 가능)에 연결하여 직원의 이름, 이메일, 휴대전화, 비밀번호 해시 그리고 개인 상태를 수정할 수 있습니다.

## 기능 요약

- 직원 목록 및 현재 개인 상태 조회
- 이름, 이메일, 휴대전화, 패스워드 해시 수정
- 자리 비움/외근/퇴근 등 개인 상태 변경 및 메모 저장
- 멤버 개인 설정 화면에서 로그인 ID를 입력하고 자신의 기본 정보·상태를 바로 수정

## 테스트

- 백엔드: `python -m compileall backend`
- 프론트엔드: `npm run build`

두 명령 모두 프로젝트 루트에서 실행하여 코드가 정상적으로 빌드되는지 확인할 수 있습니다.
