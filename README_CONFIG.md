# ChessSudoku 서버 설정 가이드

## 🔧 설정 방법

서버 주소를 안전하게 관리하기 위해 다음 3가지 방법을 사용할 수 있습니다:

### 1. 환경 변수 사용 (권장)

```bash
# Windows (PowerShell)
$env:CHESSUDOKU_SERVER_URL="https://your-server.com"

# Windows (CMD)
set CHESSUDOKU_SERVER_URL=https://your-server.com

# Linux/Mac
export CHESSUDOKU_SERVER_URL=https://your-server.com
```

### 2. config.json 파일 사용

`config.json.example`을 `config.json`으로 복사하고 실제 서버 주소를 입력:

```json
{
  "server_url": "https://your-actual-server.com",
  "api_timeout": 30
}
```

### 3. 코드에서 직접 설정

```python
from puzzle_api_client import PuzzleAPIClient

# 방법 1: 생성자에서 직접 지정
client = PuzzleAPIClient("https://your-server.com")

# 방법 2: 함수 호출 시 지정
create_normal_puzzle(server_url="https://your-server.com")
```

## 🔒 보안 주의사항

- ✅ `config.json`은 `.gitignore`에 포함되어 Git에 커밋되지 않습니다
- ✅ 실제 서버 주소는 환경 변수나 로컬 설정 파일에만 저장하세요
- ❌ 코드에 서버 주소를 하드코딩하지 마세요
- ❌ `config.json` 파일을 Git에 커밋하지 마세요

## 📋 설정 우선순위

1. 코드에서 직접 지정한 `server_url` 매개변수
2. 환경 변수 `CHESSUDOKU_SERVER_URL`
3. `config.json` 파일의 `server_url`
4. 기본값: `http://localhost:3000`

## 🧪 설정 확인

현재 설정을 확인하려면:

```bash
python config.py
```

## 📁 파일 구조

```
chessudoku_puzzle/
├── config.py              # 설정 관리 모듈
├── config.json.example     # 설정 파일 예시
├── config.json            # 실제 설정 파일 (Git에 포함되지 않음)
├── .gitignore             # config.json 등 민감한 파일 제외
└── ...
```
