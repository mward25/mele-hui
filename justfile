run:
    cd ./app/src/ && python ./melehui_app.py

lint:
    uv run pyside6-project qmllint
