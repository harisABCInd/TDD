from django.urls import path, include
from rest_framework.routers import DefaultRouter

from TODO.views import TaskViewSet

app_name = 'TODO'

router = DefaultRouter()
router.register('tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
