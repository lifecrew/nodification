# vscode-py-template

환경은 MacOS, Linux 를 기준으로 합니다.

## 셋업

1. 프로젝트의 이름을 정해 `myproject`(가명) 디렉토리의 이름을 변경합니다
    - 이때 `myproject` 는 파이썬에서 임포트가능한 이름이어야 합니다. (e.g. `tensorflow`, `torch`, `Flask`)
    - 소문자만으로 이루어진 단일단어로 구성하세요.  *'_' 같은 것이 덕지덕지 붙으면 멋이 없어요.*
    - `Makefile`의 `PROJECT` 변수값을 동일하게 변경합니다.
    - `pyproject.yaml` 의 `name` 변수값을 동일하게 변경합니다.
2. 가상환경을 준비하고 활성화한 다음 `make install` 명령을 실행합니다.
    - `make install` 은 개발 모드로 패키지를 설치합니다.
    - 개발 모드로 설치하는 것이기 때문에, 가상환경의 `site-package` 디렉토리에 소프트 링크를 거는 방식으로 작동합니다.
    - 동일한 가상환경을 사용하는 프로젝트에서 이 `myproject`(가명) 을 임포트해 사용할 수 있습니다. 이때, 현재 프로젝트 폴더 내에서 파일을 수정하면, 링크가 걸려 있기 때문에 `myproject` 를 사용하는 다른 프로젝트에서도 별도의 업데이트 없이 곧바로 수정내용이 반영됩니다. 물론, 이미 특정 모듈을 불러왔다면 파이썬을 닫았다가 다시 켜야 합니다.
3. 디스코드를 사용하는 경우, 깃허브 액션 secret 변수 `DISCORD_WEBHOOK_URL` 을 지정합니다.
    - 알림을 보내고 싶은 디스코드 채널의 웹훅 URL을 값으로 등록합니다.
    - 관련 액션은 [notification.yml](.github/workflows/notification.yml) 입니다.

## `Makefile`

`Makefile`은 다음과 같은 기능들을 가지고 있습니다.

### `make lint`

- `.vscode` 설정을 사용하려면 `pylint` 익스텐션을 설치하세요.
- 린터의 기본 세팅에 `pyproject.toml` 파일에 명시된 옵션을 오버라이딩해 코드를 린팅합니다.

### `make format`

- 포매터는 google의 `yapf`를 사용합니다.
- `yapf` 포매터의 기본 세팅에 `pyproject.toml` 파일에 명시된 옵션을 오버라이딩해 코드를 포매팅합니다.
- `.vscode` 설정을 사용하려면 `yapf` 익스텐션을 설치하세요.

### `make test`

- 테스트는 `unittest`를 사용합니다.
- `test_*.py` 와 `*_test.py` 패턴을 모두 지원합니다.
- 테스트 파일이 존재하는 위치까지 `__init__.py` 로 연결되어 있어야 합니다.

### `make publish`

- `~/.pypirc` 파일을 아래와 같이 작성하세요.
    ```
    [pypi]
    username = __token__
    password = pypi-어쩌고저쩌고 # 개인 API 토큰을 발급받아 작성하세요.
    ```
- 이 명령을 실행하면 `flit` 을 사용하여 PyPI 공개 레지스트리에 패키지를 푸시합니다.
- 앞서 이름으로 지정한 `myproject`(가명)이 업로드되어, 전세계 누구나 `python3 -m pip install myproject`로 패키지를 설치해 사용할 수 있게 됩니다.
