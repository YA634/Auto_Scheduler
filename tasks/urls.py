from rest_framework.routers import DefaultRouter

from django.urls import path
from .import views

router = DefaultRouter()
router.register(r'tasks', views.TaskView)

urlpatterns = [
    path('oauth/login/',views.oauth_login),
    path('oauth/callback/',views.oauth_callback),
    path('free-slots/',views.FreeSlotsView.as_view()),
    path('')
]
urlpatterns += router.urls