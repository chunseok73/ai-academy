# AI 아카데미 학습지원 포털

교육과정 조회, 수강신청, 학습 질문과 자료 공유를 지원하는
Django 기반 학습지원 포털입니다.

HTML 기획 시안을 바탕으로 실제 로그인과 데이터 저장 기능을 구현하고,
PythonAnywhere에 배포했습니다.

## 서비스 주소

- 실제 서비스: https://cslim.pythonanywhere.com/
- HTML 기획 시안: https://chunseok73.github.io/ai-academy/
- 소스 코드: https://github.com/chunseok73/ai-academy

HTML 시안과 실제 Django 서비스는 별도로 운영됩니다.
무료 호스팅의 운영 상태에 따라 실제 서비스 접속이 제한될 수 있습니다.

## 주요 기능

| 구분 | 기능 |
|---|---|
| 회원 | 회원가입, 로그인, 로그아웃 |
| 교육과정 | 과정 목록과 상세 정보 조회 |
| 수강신청 | 신청, 취소, 재신청, 본인 수강 내역 조회 |
| 신청 검증 | 중복 신청, 정원 초과, 모집 종료 강좌 신청 차단 |
| 게시판 | 공지·자료·질문 목록, 제목 검색, 페이지 이동 |
| 질문 | 로그인 회원의 질문 작성 및 본인 질문 수정·삭제 |
| 관리자 | 공지·자료 작성, 게시글 관리, 답변 등록·삭제 |
| 첨부파일 | 업로드, 다운로드, 삭제 |

공통 게시글은 누구나 열람할 수 있습니다.
강좌 게시글과 첨부파일은 해당 강좌의 수강 중인 회원과 관리자만 열람합니다.

일반 회원은 질문만 작성하며, 관리자 답변 수정은 삭제 후 재등록 방식입니다.
첨부파일은 작성·수정 시 한 번에 하나씩 추가할 수 있습니다.

## 사용 기술

- Python
- Django 6.1.1
- SQLite
- HTML / CSS
- Git / GitHub
- PythonAnywhere

세부 패키지 버전은 requirements.txt에 기록되어 있습니다.

## 프로젝트 구성

- academy/: 교육과정, 개설강좌, 수강신청, 학습 홈, 회원 화면
- board/: 게시글, 관리자 답변, 첨부파일
- config/: Django 설정과 URL 연결
- manage.py: Django 관리 명령 실행
- requirements.txt: 설치할 패키지 목록
- index.html: 기존 HTML 기획 시안

## 로컬 실행 방법

아래는 Windows PowerShell 기준입니다.
Python 3.13 또는 3.14가 설치된 환경에서 진행합니다.

### 1. 저장소 복제 및 패키지 설치

```powershell
git clone https://github.com/chunseok73/ai-academy.git
cd ai-academy
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 2. 개발용 비밀키 설정

현재 PowerShell 세션에서 사용할 비밀키를 생성합니다.

```powershell
$env:DJANGO_SECRET_KEY = & ".\.venv\Scripts\python.exe" -c "import secrets; print(secrets.token_urlsafe(64))"
```

새 터미널에서는 환경변수를 다시 설정해야 합니다.
키를 새로 생성하면 기존 로그인 세션이 무효화될 수 있습니다.
운영 서버에서는 고정된 비밀키를 별도로 안전하게 관리합니다.

### 3. DB 생성 및 관리자 계정 생성

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
```

### 4. 검사 및 실행

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py runserver
```

- 학습 홈: http://127.0.0.1:8000/
- 관리자: http://127.0.0.1:8000/admin/

새로 복제한 프로젝트에는 시연용 회원과 데이터가 없습니다.
관리자 화면에서 교육과정을 먼저 등록하고 개설강좌를 추가합니다.
일반 회원으로 가입한 뒤 모집 중인 강좌에 수강신청할 수 있습니다.

## 데이터와 배포 관리

- DB, 업로드 파일, 가상환경, 비밀키는 GitHub에 포함하지 않습니다.
- 소스 코드와 별도로 DB 및 첨부파일을 백업합니다.
- 로컬 DB와 운영 서버 DB는 자동 동기화되지 않습니다.
- GitHub에 push해도 PythonAnywhere 서비스가 자동 갱신되지 않습니다.
- 현재 운영 서버 전용 설정과 WSGI 설정은 서버에서 별도로 관리합니다.
- 운영 배포에는 DEBUG=False, 호스트 설정, 비밀키,
  정적 파일 수집 및 HTTPS 설정이 필요합니다.
- 첨부파일은 Django의 권한 검사 후 다운로드합니다.
  업로드 폴더를 정적 파일 매핑으로 직접 공개하지 않습니다.

## 시연 순서

1. 일반 회원 로그인
2. 교육과정 목록과 상세 정보 확인
3. 수강신청 및 내 수강 정보 확인
4. 질문 작성과 첨부파일 등록
5. 관리자 계정에서 답변 등록
6. 일반 회원 계정에서 답변과 첨부파일 확인

## 향후 개선

- 자동화 테스트 확대
- 관리자 답변 수정 기능
- 첨부파일 교체 화면 개선
- 배포 자동화 및 정기 백업