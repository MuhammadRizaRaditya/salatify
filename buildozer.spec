[app]

title = SALATIFY
package.name = salatify
package.domain = com.hlrw
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json
version = 1.0.0
requirements = python3,kivy==2.3.0,kivymd==1.2.0,sqlalchemy,requests,pytz,passlib,plyer
orientation = portrait
fullscreen = 0

osx.python_version = 3
osx.kivy_version = 2.3.0

android.fullscreen = 0
android.archs = arm64-v8a
android.min_sdk = 24
android.target_sdk = 33
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
android.entrypoint = main.py

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
