PROJECT = myproject

all: install lint test format

install:
	python3 -m pip install --upgrade pip
	python3 -m pip install --require-virtualenv -e .[dev]

install-without-venv:
	python3 -m pip install --upgrade pip
	python3 -m pip install -e .[dev]

uninstall:
	python3 -m pip install --upgrade pip
	python3 -m pip uninstall ${PROJECT}
	# NOTE: 이 패키지로 인해 설치된 의존성은 가상환경을 삭제하는 방식으로 제거되어야 합니다.

lint:
	python3 -m pylint --rcfile=pylintrc ./${PROJECT}

format:
	python3 -m yapf -ir .

test:
	python3 -m unittest discover -s ./${PROJECT} -p "*_test.py" -v
	python3 -m unittest discover -s ./${PROJECT} -p "test_*.py" -v

publish:
	python3 -m flit publish
