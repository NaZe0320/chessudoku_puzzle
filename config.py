"""
ChessSudoku 설정 관리 모듈

환경 변수 또는 설정 파일에서 서버 URL과 기타 설정을 읽어옵니다.
"""
import os
import json

class Config:
    """애플리케이션 설정 관리 클래스"""
    
    # 기본 설정값
    DEFAULT_SERVER_URL = "http://localhost:3000"
    DEFAULT_API_TIMEOUT = 30
    
    def __init__(self):
        self.server_url = self._get_server_url()
        self.api_timeout = self._get_api_timeout()
    
    def _get_server_url(self):
        """서버 URL 가져오기 (우선순위: 환경변수 > 설정파일 > 기본값)"""
        # 1. 환경 변수 확인
        env_url = os.environ.get('CHESSUDOKU_SERVER_URL')
        if env_url:
            return env_url
        
        # 2. 설정 파일 확인
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                file_url = config_data.get('server_url')
                if file_url:
                    return file_url
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            pass
        
        # 3. 기본값 반환
        return self.DEFAULT_SERVER_URL
    
    def _get_api_timeout(self):
        """API 타임아웃 값 가져오기"""
        # 1. 환경 변수 확인
        env_timeout = os.environ.get('API_TIMEOUT')
        if env_timeout:
            try:
                return int(env_timeout)
            except ValueError:
                pass
        
        # 2. 설정 파일 확인
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                file_timeout = config_data.get('api_timeout')
                if file_timeout:
                    return int(file_timeout)
        except (FileNotFoundError, json.JSONDecodeError, KeyError, ValueError):
            pass
        
        # 3. 기본값 반환
        return self.DEFAULT_API_TIMEOUT
    
    def set_server_url(self, url):
        """서버 URL 동적 변경"""
        self.server_url = url
        print(f"서버 URL 변경됨: {url}")
    
    def get_server_url(self):
        """현재 서버 URL 반환"""
        return self.server_url
    
    def get_api_timeout(self):
        """현재 API 타임아웃 반환"""
        return self.api_timeout
    
    def print_config(self):
        """현재 설정 출력"""
        print("=" * 50)
        print("현재 ChessSudoku 설정")
        print("=" * 50)
        print(f"서버 URL: {self.server_url}")
        print(f"API 타임아웃: {self.api_timeout}초")
        print()
        print("설정 변경 방법:")
        print("1. 환경 변수: CHESSUDOKU_SERVER_URL=https://your-server.com")
        print("2. config.json 파일 생성")
        print("3. 코드에서 config.set_server_url() 호출")

# 전역 설정 인스턴스
config = Config()

if __name__ == "__main__":
    # 설정 테스트
    config.print_config()
