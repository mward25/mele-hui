build-pyside-project:
    uv run pyside6-project build

run: build-pyside-project
    cd ./app/src/ && python ./melehui_app.py

lint:
    uv run pyside6-project qmllint
    prek run --all-files

build-flatpak:
    flatpak-builder --force-clean build-dir com.trumpetrespas.melehui.json

deploy-flatpak: build-flatpak
    flatpak build-bundle build-dir melehui.flatpak com.trumpetrespas.melehui
