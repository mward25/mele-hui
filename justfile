build-pyside-project:
    uv run pyside6-project build

run: build-pyside-project
    cd ./app/src/ && python ./melehui_app.py

lint:
    uv run pyside6-project qmllint
