run:
    cd ./app/src/ && python ./melehui_app.py

build-flatpak:
    flatpak-builder --user --force-clean --install-deps-from=flathub build-dir com.trumpetrespas.melehui.json

run-flatpak:
    flatpak run com.trumpetrespas.melehui
