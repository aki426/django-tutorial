# Windows WSL + Python + Django Webサービス開発チュートリアル

## 1. WSL (Windows Subsystem for Linux) のセットアップ

### 1.1 WSLの有効化
1. **管理者権限でPowerShellを開く**
2. **WSL機能を有効化**
   ```powershell
   dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
   dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
   ```
3. **PCを再起動**

なお、コマンドの代わりにGUGIからWindowsの機能「仮想マシンプラットフォーム」（又はHyper-V）と「Linux用Windowsサブシステム」を有効化してもよい。

### 1.2 WSL2のインストール
1. **WSL2をデフォルトバージョンに設定**
   ```powershell
   wsl --set-default-version 2
   ```
2. **Ubuntu 22.04 LTSをインストール**
   ```powershell
   wsl --install -d Ubuntu-22.04
   ```
3. **初回セットアップ（ユーザー名とパスワードを設定）**

### 1.3 WSLの動作確認
```bash
# WSLのバージョン確認
wsl --list --verbose

# Ubuntu起動
wsl -d Ubuntu-22.04
```

## 2. Python環境のセットアップ

### 2.1 システムの更新 - ★
```bash
# パッケージリストの更新
sudo apt update && sudo apt upgrade -y

# 必要なパッケージのインストール
sudo apt install -y curl git build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget llvm libncurses5-dev \
libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python3-openssl
```

### 2.2 pyenvのインストール（Python バージョン管理）
```bash
# pyenvのインストール
curl https://pyenv.run | bash

# .bashrcに設定を追加
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# 設定を反映
source ~/.bashrc
```

### 2.3 Pythonのインストール
```bash
# 利用可能なPythonバージョンを確認
pyenv install --list | grep "3.11"

# Python 3.11.x（最新）をインストール
pyenv install 3.11.7

# グローバルで使用するPythonバージョンを設定
pyenv global 3.11.7

# インストール確認
python --version
python3 --version
pip --version
```

※場合によってはpythonではなくpython3コマンドが割り当たっているのでその場合python3コマンドを使う。

※自分のWSLではpython3が正だったので以降python3コマンドで解説する。

```bash
$ python --version
Command 'python' not found, did you mean:
  command 'python3' from deb python3
  command 'python' from deb python-is-python3
$ python3 --version
Python 3.12.3
```

### 2.4 venvによる仮想環境構築 - ★

venvインストール、環境構築、環境にインする

```bash
$ sudo apt install python3.12-venv
$ python3 -m venv venv
$ source venv/bin/activate
(venv)$ 
```

仮想環境内でインストールするには。

```bash
(venv)$ pip install black
(venv)$ black <dir>
```


## 3. Djangoプロジェクトの開発環境構築

### 3.1 プロジェクトディレクトリの作成
```bash
# ホームディレクトリに移動
cd ~

# プロジェクト用ディレクトリを作成
mkdir django-projects
cd django-projects

# 具体的なプロジェクト名でディレクトリ作成
mkdir mywebapp
cd mywebapp
```

### 3.2 Python仮想環境の作成 - ★
```bash
# 仮想環境を作成
python3 -m venv venv

# 仮想環境を有効化
source venv/bin/activate

# pip を最新版にアップデート
pip install --upgrade pip
```

### 3.3 Djangoとその他必要パッケージのインストール - ★
```bash
# Djangoのインストール
pip install django
# バージョン指定する場合
pip install django==5.1.2

# その他よく使用されるパッケージのインストール
pip install djangorestframework  # REST API用
pip install python-dotenv        # 環境変数管理
pip install pillow              # 画像処理
pip install psycopg2-binary     # PostgreSQL接続用

# インストール済みパッケージの確認
pip list

# requirements.txtファイルの生成
pip freeze > requirements.txt
```

## 4. Djangoプロジェクトの作成とScaffolding

### 4.1 Djangoプロジェクトの作成 - ★
```bash
# Djangoプロジェクトを作成（現在のディレクトリに作成）
django-admin startproject config .
# Djangoプロジェクトを作成（1階層掘る場合）
django-admin startproject config .
django-admin startproject mywebapp

# プロジェクト構造の確認
tree . -L 2
```

**期待される構造:**
```
mywebapp/
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
└── venv/
```

### 4.2 Djangoアプリケーションの作成
```bash
# メインアプリケーションを作成
python3 manage.py startapp main

# API用アプリケーション作成（必要に応じて）
python3 manage.py startapp api
```

### 4.3 基本設定の構成

#### settings.pyの編集
```bash
# エディタでsettings.pyを開く
nano config/settings.py
```

**settings.pyに以下を追加/修正:**
```python
import os
from pathlib import Path

# 作成したアプリをINSTALLED_APPSに追加
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',  # 追加
    'api',   # 追加（作成した場合）
    'rest_framework',  # 追加（DRFを使用する場合）
]

# 日本語・タイムゾーン設定
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_TZ = True

# 静的ファイル設定
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# メディアファイル設定
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### 4.4 初期データベースマイグレーション
```bash
# データベースマイグレーションファイルの作成
python3 manage.py makemigrations

# マイグレーションの実行
python3 manage.py migrate

# スーパーユーザーの作成
python3 manage.py createsuperuser
```

### 4.5 開発サーバーの起動確認 - ★
```bash
# 開発サーバーを起動
python3 manage.py runserver 0.0.0.0:8000
# 特にIP指定しなくてもよい。
python3 manage.py runserver
```

**ブラウザで確認:**
- `http://localhost:8000` - Djangoウェルカムページ
- `http://localhost:8000/admin` - 管理画面

### 4.6 基本的なView作成

#### main/views.py
```python
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, Django World!")

def about(request):
    context = {
        'title': 'About Page',
        'message': 'Welcome to our web application!'
    }
    return render(request, 'main/about.html', context)
```

#### main/urls.py を作成
```python
from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
]
```

#### config/urls.py を編集
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
]

# 開発環境でのメディアファイル配信
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

### 4.7 テンプレートの作成

#### ディレクトリ構造作成
```bash
# テンプレート用ディレクトリを作成
mkdir -p main/templates/main
mkdir -p static/css static/js static/images
```

#### base.html テンプレート作成
```bash
nano main/templates/main/base.html
```

```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My Web App{% endblock %}</title>
    {% load static %}
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'main:home' %}">My Web App</a>
            <div class="navbar-nav">
                <a class="nav-link" href="{% url 'main:home' %}">Home</a>
                <a class="nav-link" href="{% url 'main:about' %}">About</a>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% block content %}
        {% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{% static 'js/script.js' %}"></script>
</body>
</html>
```

#### about.html テンプレート作成
```bash
nano main/templates/main/about.html
```

```html
{% extends 'main/base.html' %}

{% block title %}{{ title }} - {{ block.super }}{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-8">
        <h1>{{ title }}</h1>
        <p class="lead">{{ message }}</p>
        <p>This is a Django web application running on WSL!</p>
    </div>
</div>
{% endblock %}
```

## 5. 開発環境の最終確認

### 5.1 プロジェクト構造の確認
```bash
# 最終的なプロジェクト構造
tree . -I 'venv|__pycache__|*.pyc'
```

### 5.2 サーバー起動と動作確認
```bash
# 開発サーバーを起動
python3 manage.py runserver 0.0.0.0:8000
```

### 5.3 Gitリポジトリの初期化
```bash
# Gitリポジトリを初期化
git init

# .gitignoreファイルを作成
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Django
*.log
local_settings.py
db.sqlite3
media/

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOF

# 初回コミット
git add .
git commit -m "Initial Django project setup"
```

## 6. 開発のベストプラクティス

### 6.1 環境変数の管理
```bash
# .envファイルを作成
cat > .env << 'EOF'
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
EOF

# .envを.gitignoreに追加
echo ".env" >> .gitignore
```

### 6.2 VS Code設定（WSL用）
1. **VS Code で WSL拡張機能をインストール**
2. **WSL内でプロジェクトを開く**
   ```bash
   code .
   ```

## 7. 次のステップ

? **完了したこと:**
- WSL2 + Ubuntu環境の構築
- Python仮想環境の作成
- Djangoプロジェクトの作成
- 基本的なView、Template、URLの設定
- Bootstrap導入による基本的なUI

d?? **今後の開発で追加できる機能:**
- ユーザー認証システム
- データベースモデルの作成
- REST API の構築
- フロントエンドフレームワーク（React/Vue.js）との連携
- Docker化
- CI/CD パイプラインの構築

これでDjangoを使ったWebサービス開発の基盤が完成しました！