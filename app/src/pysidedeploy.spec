[app]

# title of your application
title = pyside_app_demo

# project root directory. default = The parent directory of input_file
project_dir = .

# source file entry point path. default = main.py
input_file = main.py

# directory where the executable output is generated
exec_directory = .

# path to the project file relative to project_dir
project_file = 

# application icon
icon = /home/miles/projects/melehui/.venv/lib/python3.12/site-packages/PySide6/scripts/deploy_lib/pyside_icon.jpg

[python]

# python packages to install
packages = Nuitka==4.1.1

# buildozer = for deploying Android application
android_packages = buildozer==1.6.0,cython==0.29.33

[qt]

# paths to required qml files. comma separated
# normally all the qml files required by the project are added automatically
# design studio projects include the qml files using qt resources
qml_files = qml/DrawingOverlay.qml,qml/camera.qml,qml/main.qml,qml/new_setlist.qml,qml/new_song.qml,qml/setlist_gallery.qml,qml/setlist_viewer.qml,qml/song_gallery.qml,qml/song_selector.qml,qml/song_viewer.qml

# excluded qml plugin binaries
excluded_qml_plugins = QtCharts,QtQuick3D,QtSensors,QtTest,QtWebEngine

# qt modules used. comma separated
modules = Qml,OpenGL,Gui,Network,Quick,QuickControls2,Core

# qt plugins used by the application. only relevant for desktop deployment
# for qt plugins used in android application see [android][plugins]
plugins = 

[android]

# path to pyside wheel
wheel_pyside = /home/miles/projects/melehui/android/pyside6-6.12.0-6.12.0-cp310-abi3-android_aarch64.whl

# path to shiboken wheel
wheel_shiboken = /home/miles/projects/melehui/android/shiboken6-6.12.0-6.12.0-cp310-abi3-android_aarch64.whl

# plugins to be copied to libs folder of the packaged application. comma separated
plugins = platforms_qtforandroid

[ios]

# path to pyside wheel
wheel_pyside = 

# path to shiboken wheel
wheel_shiboken = 

# path to python.xcframework
xcframework_path = 

# reverse-dns bundle identifier, eg = com.example.myapp
# default (like xcode's own placeholder) = com.example.<app name, alphanumeric only>
bundle_id = 

# apple developer team id, used for code signing. only required for device builds
team_id = 

# app version (cfbundleshortversionstring)
version = 1.0

# minimum ios deployment target. default = read from the PySide6 wheel's embedded
# qt-for-ios kit
deployment_target = 

# path to an .entitlements file, relative to project_dir
entitlements = 

# code signing style. possible values = [Automatic, Manual]
signing_style = Automatic

# extra header search paths, relative to project_dir. comma separated
header_search_paths = 

[nuitka]

# usage description for permissions requested by the app as found in the info.plist file
# of the app bundle. comma separated
# eg = extra_args = --show-modules --follow-stdlib
macos.permissions = 

# mode of using nuitka. accepts standalone or onefile. default = standalone
# standalone creates a folder with the executable and its dependencies.
# onefile creates a single executable that unpacks itself at every start.
mode = standalone

# specify any extra nuitka arguments
extra_args = --quiet --noinclude-qt-translations

[buildozer]

# build mode
# possible values = ["aarch64", "x86_64"]
# release creates a .aab, while debug creates a .apk
mode = debug

# path to pyside6 and shiboken6 recipe dir
recipe_dir = /home/miles/projects/melehui/app/src/deployment/recipes

# path to extra qt android .jar files to be loaded by the application
jars_dir = /home/miles/projects/melehui/app/src/deployment/jar/PySide6/jar

# if empty, uses default ndk path downloaded by buildozer
ndk_path = /home/miles/.pyside6_android_deploy/android-ndk/android-ndk-r28c

# if empty, uses default sdk path downloaded by buildozer
sdk_path = 

# other libraries to be loaded at app startup. comma separated.
local_libs = plugins_platforms_qtforandroid

# architecture of deployed platform
arch = aarch64

