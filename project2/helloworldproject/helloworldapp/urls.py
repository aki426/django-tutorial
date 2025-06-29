from django.urls import path
from .views import helloworldfunc

urlpatterns = [
    path('helloworldapp/', helloworldfunc), # projectのurlsに記載のURLは除外したサブディレクトリを指定する。
]