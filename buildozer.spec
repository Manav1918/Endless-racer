[app]

# (str) Title of your application
title = Endless Racer

# (str) Package name
package.name = endlessracer

# (str) Package domain (needed for android packaging)
package.domain = org.manav1918.racer

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let's be explicit)
source.include_exts = py,png,jpg,mp3,json,wav,ttf
source.include_patterns = assets/*,assets/images/*,assets/audio/*

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
# pygame-ce is the community edition we are using
requirements = python3,pygame-ce

# (str) Custom source folders for requirements
# p4a.local_recipes = ./recipes

# (str) Presplash of the application
presplash.filename = %(source.dir)s/assets/images/logo.png

# (str) Icon of the application
icon.filename = %(source.dir)s/assets/images/logo.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
# android.ndk = 25b

# (str) Android SDK directory to use (if empty, it will be installed automatically)
# android.sdk_path = 

# (str) Android NDK directory to use (if empty, it will be installed automatically)
# android.ndk_path = 

# (list) The Android architectures to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (bool) enable Android auto backup
android.allow_backup = True

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT_TO_PY

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
