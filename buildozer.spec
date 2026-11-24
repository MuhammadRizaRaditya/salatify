[app]

title = SALATIFY
package.name = salatify
package.domain = com.hlrw
source.dir = .
source.include_exts = py,kv,png,jpg,json,ttf,otf,mp3,ogg,txt
source.exclude_dirs = web,tests,docs,.git,.github,bin,.buildozer,__pycache__,.venv,venv
version = 1.0.0
requirements = python3,kivy==2.3.0,pillow,sqlalchemy,requests,urllib3,idna,certifi,charset-normalizer,passlib,plyer,pyjnius,exceptiongroup,materialyoucolor,asynckivy,asyncgui,kivymd @ https://github.com/kivymd/KivyMD/archive/master.zip
orientation = portrait
fullscreen = 0

osx.python_version = 3
osx.kivy_version = 2.3.0

android.fullscreen = 0
android.archs = arm64-v8a
android.min_sdk = 24
android.target_sdk = 33
android.archs = arm64-v8a,armeabi-v7a
android.accept_sdk_license = True
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,POST_NOTIFICATIONS,VIBRATE,ACCESS_NETWORK_STATE
android.meta_data = 
android.dependencies = 
android.add_aar = 
android.add_jar = 
android.add_src = 
android.gradle_dependencies = 
android.gradle_repositories = 
android.gradle_repositories_priority = 
android.manifest_template = android/AndroidManifest.xml
android.add_manifest_uses_permission = false
android.api = 33
android.ndk = 25b
android.ndk_api = 24
android.sdk = 24
android.sdk_version = 33

buildozer = 1.5.0

[buildozer]

[buildozer:log_level] = 2
[buildozer:warning] = 0

[buildozer:target]
name = android

[buildozer:target:arch]
arm64-v8a = 

[buildozer:target:arm64-v8a]
arch = arm64-v8a
ndk_api = 24

[buildozer:target:x86_64]
arch = x86_64

[buildozer:target:x86_64]
arch = x86_64

[buildozer:sqlite]
url = https://www.sqlite.org/2024/sqlite-amalgamation-3450100.zip
md5 = 

[buildozer:python_compile]
optimize_level = 0

[buildozer:webview]
enabled = false
