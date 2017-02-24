from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^createuser$', views.createuser),
    url(r'^login$', views.login),
    url(r'^user_dashboard$', views.user_dashboard),
    url(r'^add_appointment$', views.add_appointment),
    url(r'^destroy/(?P<id>\d+)$', views.task_delete),
    url(r'^show_app/(?P<id>\d+)$', views.show_app),
    url(r'^edit_app/(?P<id>\d+)$', views.edit_app),
    url(r'^logout$', views.logout),




]
