from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^accounts/login/$', views.login_view),
    url(r'^logout/$', views.logout_view),
    url(r'^register/$', views.register),
    url(r'^changepassword/$', views.changepassword),
    url(r'^forgot/$', views.forgot),
    url(r'^recover/$',views.recover)
]
