# 내장
import os

# 서드파티
import dotenv
from discord_webhook import DiscordWebhook  #, DiscordEmbed

# 프로젝트
from nodification.utils.diff import get_notion_pages
from nodification.core.notifier import NotionToDiscordWebhookNotifier

# 환경 변수 로드
dotenv.load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
NOTION_DB_ID = os.getenv('NOTION_KANBANBOARD_DB_ID')


class KanbanboardDiscordWebhookNotifier(NotionToDiscordWebhookNotifier):

    @classmethod
    def get_avartar_url(cls, page):
        url = page['properties']['봇연동용-마이크로비즈니스-로고URL']['rollup']['array'][0]['url']
        print(f'아바타 URL로 `{url}`을 사용합니다.')
        return url

    @classmethod
    def get_ticket_end(cls, page) -> str:
        end = page['properties']['진행기간']['date']['end']
        if end is None:
            end = ''
        return end

    @classmethod
    def get_dri_name(cls, page) -> str:
        try:
            title_type = page['properties']['봇연동용-DRI이름']['rollup']['array'][0]
        except IndexError:
            print('이름을 찾지 못했습니다. 릴레이션이 등록되어 있나요?')
            name = ''
        else:
            name = title_type['title'][0]['plain_text']
        return name

    @classmethod
    def get_business_name(cls, page: dict) -> str:
        try:
            title_type = page['properties']['봇연동용-마이크로비즈니스-이름']['rollup']['array'][0]
        except IndexError:
            print('`봇연동용-마이크로비즈니스-이름`을 찾지 못했습니다. 릴레이션이 등록되어 있나요?')
            name = '미궁의 마이크로비즈니스'
        else:
            name = title_type['title'][0]['plain_text']
        return name

    def duedate_text(self, page: dict):
        if date := self.get_ticket_end(page):
            return f'"{date}" 까지 이 태스크를 끝마쳐요.'
        else:
            return '진행기간이 설정되지 않았어요!'

    def ownership_text(self, page: dict):
        s = f'[티켓 변경사항]({self.get_page_url(page)})을 한번 확인해보세요!'
        if name := self.get_dri_name(page):
            return f'오너쉽을 가진 **{name}**님은 ' + s
        else:
            return '담당자가 지정되어 있지 않아요. ' + s

    def parse(self, page: dict) -> DiscordWebhook:
        return DiscordWebhook(
            self.discord_webhook_url,
            avartar_url=self.get_avartar_url(page),
            content=(
                f'칸반보드의 "{self.get_icon(page)} [{self.get_title(page)}]({self.get_page_url(page)})" 티켓이 수정됐어요.\n\n'
                f'- {self.duedate_text(page)}\n'
                f'- {self.ownership_text(page)}\n'
            ),
            username=self.get_business_name(page),
            timeout=2,
        )


if __name__ == '__main__':
    discord = KanbanboardDiscordWebhookNotifier(DISCORD_WEBHOOK_URL)
    pages = get_notion_pages(NOTION_DB_ID)
    for page in pages:
        discord.send(page)
