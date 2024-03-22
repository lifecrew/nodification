# 내장
import os

# 서드파티
import dotenv
import notion_client

# 환경 변수 로드
dotenv.load_dotenv()

# 환경 변수에서 값을 가져옴
NOTION_API_KEY = os.getenv("NOTION_API_KEY")

# 노션 클라이언트 초기화
notion = notion_client.Client(auth=NOTION_API_KEY)
