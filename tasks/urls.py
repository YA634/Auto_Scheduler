from rest_framework.routers import DefaultRouter
from .views import TaskView

router = DefaultRouter()
router.register(r'tasks', TaskView)

urlpatterns = router.urls