run:
    cd ./app/src/ && python ./melehui_app.py

deploy-android:
    cd app/src && uv run pyside6-android-deploy \
        --name melehui\
        --wheel-pyside=../../android/pyside6-6.12.0-6.12.0-cp310-abi3-android_aarch64.whl \
        --wheel-shiboken=../../android/shiboken6-6.12.0-6.12.0-cp310-abi3-android_aarch64.whl \
