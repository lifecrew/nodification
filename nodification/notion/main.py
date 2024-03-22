# 내장
import os
import time
from datetime import datetime, timedelta
from requests.exceptions import Timeout

# 서드파티
import pytz
from dotenv import load_dotenv
from notion_client import Client
from discord_webhook import DiscordWebhook, DiscordEmbed

# 환경 변수 로드
load_dotenv()

# 환경 변수에서 값을 가져옴
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# 노션 클라이언트 초기화
notion = Client(auth=NOTION_API_KEY)


def get_notion_pages(last_edited_time_property_name) -> list:
    """
    현재 시간 기준으로 10분~20분 전에 수정된 노션 데이터베이스 페이지를 가져옴.
    """
    now = datetime.now(pytz.timezone("Asia/Seoul"))
    start_time = now - timedelta(minutes=20)
    end_time = now - timedelta(minutes=10)

    response = notion.databases.query(
        **{
            "database_id": NOTION_DATABASE_ID,
            "filter":
                {
                    "and":
                        [
                            {
                                "property": last_edited_time_property_name,
                                "last_edited_time":
                                    {
                                        "after": start_time.isoformat(),
                                        "before": end_time.isoformat()
                                    },
                            },
                        ]
                },
        }
    )
    return response.get("results", [])


def send_discord_notification(pages: list):
    """
    디스코드 웹훅을 사용해 알림을 보냄.
    """
    print(f'got {len(pages)} pages')
    for page in pages:
        print(page["properties"]["Name"])
        title = page["properties"]["Name"]["title"][0]["text"]["content"]
        content = f"**temp:** {title}"
        embed = DiscordEmbed(
            color="03b2f8",
            title="Your Title",
            description="Lorem ipsum dolor sit",
        )
        print(title)
        print(DISCORD_WEBHOOK_URL)
        webhook = DiscordWebhook(
            url=DISCORD_WEBHOOK_URL,
            content=content,
            username='temp',
            timeout=0.1,
        )
        webhook.add_embed(embed)
        try:
            response = webhook.execute()
            if response.status_code != 204:
                print(f"Error sending message to Discord: {response.status_code}, {response.text}")
        except Timeout as err:
            print(f"Oops! Connection to Discord timed out: {err}")
        time.sleep(1)


if __name__ == "__main__":
    pages = get_notion_pages("__최종수정일")
    if pages:
        send_discord_notification(pages)
    else:
        print("No updates in the specified time frame.")
