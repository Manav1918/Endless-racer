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

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
# Using 'pygame' as the requirement (p4a will use its stable recipe)
requirements = python3,pygame

# (str) Presplash of the application
presplash.filename = assets/images/logo.png

# (str) Icon of the application
icon.filename = assets/images/logo.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API
android.api = 31

# (int) Minimum API
android.minapi = 21

# (list) The Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) enable Android auto backup
android.allow_backup = True

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT_TO_PY

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0
