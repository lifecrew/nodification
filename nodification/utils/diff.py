# 내장
from pprint import pprint
from datetime import datetime, timedelta

# 서드파티
import pytz

# 프로젝트
from nodification.notion import notion


def get_notion_pages(
    notion_database_id: str,
    verbose: bool = True,
) -> list:
    """
    현재 시간 기준으로 10분~20분 전에 수정된 노션 데이터베이스 페이지를 가져옴.
    """
    now = datetime.now(pytz.timezone("Asia/Seoul"))
    start_time = now - timedelta(minutes=20)
    end_time = now - timedelta(minutes=10)
    response = notion.databases.query(
        notion_database_id, **{
            "filter":
                {
                    "and":
                        [
                            {
                                "timestamp": "last_edited_time",
                                "last_edited_time": {
                                    "after": start_time.isoformat()
                                },
                            },
                            {
                                "timestamp": "last_edited_time",
                                "last_edited_time": {
                                    "before": end_time.isoformat()
                                },
                            },
                        ]
                },
        }
    )
    pages = response.get('results', [])
    print(f'{start_time} 와 {end_time} 사이 {len(pages)}개의 레코드를 찾았습니다.')

    if pages and verbose:
        print('샘플 페이지를 보여줍니다.')
        pprint(pages[0])

    return pages
