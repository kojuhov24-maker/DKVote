[app]
title = DK Vote
package.name = dkvote
package.domain = org.culture.vote

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0.0

# Необходимые зависимости
requirements = python3,kivy==2.2.1

# Разрешения Android
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# Ориентация экрана
orientation = portrait

# Архитектуры процессоров современных смартфонов
android.archs = arm64-v8a, armeabi-v7a

# Минимальная версия Android (Android 7.0+)
android.minapi = 24
android.api = 33

# (str) Android NDK version to use
android.ndk = 25b

# Настройки сборки
android.accept_sdk_license = True
