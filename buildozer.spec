[app]

# (str) Title of your application
title = WeatherApp

# (str) Package name
package.name = weatherapp

# (str) Package domain (needed for Android)
package.domain = org.mycompany

# (str) Source code where the main.py is located
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 1.0

# (str) The name of the entry point to the program
entrypoint = main.py

# (str) Icon of the application
icon.filename = %(source.dir)s/assets/icon.png

# (list) Permissions
android.permissions = INTERNET

# (int) Android API to target
android.api = 31

# (int) Minimum API required (you can set this to lower API if backward compatibility is required)
android.minapi = 21

# (bool) Indicate if the application should be fullscreen
fullscreen = 1

# (str) Supported orientation (one of: landscape, portrait, sensorLandscape, sensorPortrait)
orientation = portrait

# (list) Requirements
requirements = python3,kivy,requests

# (bool) Enable/Disable the compilation of the Cython sources
cython.compile_time_env = 1

# (str) Presplash of the application
presplash.filename = %(source.dir)s/assets/splash.png

# (str) Presplash background color (for example #FFFFFF)
presplash.color = #FFFFFF
