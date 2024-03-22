class NotionPageSchemaTool:
    """ 노션 페이지를 현명하게 핸들링할 수 있는 도구를 들고 있는 클래스.
    """

    @classmethod
    def extract_plain_text_from(self, title_type: dict):
        # NOTE: 무결함
        return title_type[0]['plain_text']

    @classmethod
    def get_icon(self, page: dict):
        # NOTE: 무결함
        if page['icon']['type'] != 'emoji':
            emoji = '😇'
            print(f'아이콘이 이모지가 아닙니다. 기본값 `{emoji}`으로 대체합니다.')
        emoji = page['icon']['emoji']
        return emoji

    @classmethod
    def get_title(self, page: dict):
        # NOTE: 무결함
        return page['properties']['Name']['title'][0]['plain_text']

    @classmethod
    def get_page_url(self, page: dict):
        # NOTE: 무결함
        return page['url']
