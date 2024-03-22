# 내장
import time
from requests.exceptions import Timeout

# 서드파티
from discord_webhook import DiscordWebhook  #, DiscordEmbed

# 프로젝트
from nodification.notion.core.schema import NotionPageSchemaTool


class DiscordWebhookNotifier:

    def __init__(
        self,
        discord_webhook_url: str,
    ) -> None:
        self.discord_webhook_url = discord_webhook_url

    def parse(self, *args, **kwargs):
        return DiscordWebhook(
            self.discord_webhook_url,
            content='hello world',
            username='default username',
            timeout=2,
        )

    def send(self, *args, **kwargs):
        webhook = self.parse(*args, **kwargs)
        try:
            _ = webhook.execute()
        except Timeout as err:
            print(f"Oops! Connection to Discord timed out: {err}")
        time.sleep(0.5)


class NotionToDiscordWebhookNotifier(DiscordWebhookNotifier, NotionPageSchemaTool):

    def parse(self, page: dict) -> DiscordWebhook:
        return super().parse()
