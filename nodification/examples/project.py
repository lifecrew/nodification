# 내장
import os

# 서드파티
import dotenv
from discord_webhook import DiscordWebhook  #, DiscordEmbed

# 프로젝트
from nodification.utils.diff import get_notion_pages
from nodification.core.notifier import DiscordWebhookNotifier

# 환경 변수 로드
dotenv.load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
NOTION_DB_ID = os.getenv('NOTION_PROJECTNOTE_DB_ID')


class ProjectNoteDiscordWebhookNotifier(DiscordWebhookNotifier):

    def parse(self, page: dict) -> DiscordWebhook:
        return DiscordWebhook(
            self.discord_webhook_url,
            content='hello ProjectNoteDiscordWebhookNotifier',
            username='default username',
            timeout=2,
        )


if __name__ == '__main__':
    discord = ProjectNoteDiscordWebhookNotifier(DISCORD_WEBHOOK_URL)
    pages = get_notion_pages(NOTION_DB_ID)
    for page in pages:
        discord.send(page)
