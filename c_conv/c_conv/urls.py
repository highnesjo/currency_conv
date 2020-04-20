from django.conf.urls import url,include
from django.contrib import admin
from cc import views
from django.conf.urls.static import static
from django.conf import settings


from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url

urlpatterns = [
    url(r'^$',views.index,name='index'),
    path('admin/', admin.site.urls),
    path("register/", views.register, name="register"),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^user_login/$',views.user_login,name='user_login'),
]