from rest_framework.routers import SimpleRouter

from .views import IncidentReportView

app_name = 'report'

router = SimpleRouter()
router.register('incident-reports', IncidentReportView, basename='incident-reports')
urls = []
urlpatterns = urls + router.urls
