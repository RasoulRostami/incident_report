from django.contrib.auth import get_user_model
from factory import django, Faker
from factory import fuzzy, SubFactory

from ..models import MonitoringSystem, IncidentReport

User = get_user_model()


class MonitoringSystemFactory(django.DjangoModelFactory):
    class Meta:
        model = MonitoringSystem

    url = Faker('url')
    title = Faker('name')
    start_page = Faker('random_number', digits=1)
    current_page = Faker('random_number', digits=1)
    is_active = Faker('boolean')


class IncidentReportFactory(django.DjangoModelFactory):
    class Meta:
        model = IncidentReport

    monitoring_system = SubFactory(MonitoringSystemFactory)
    incident = Faker('text')
    position = Faker('random_number', digits=1)
    report_type = fuzzy.FuzzyChoice([value for value in IncidentReport.IncidentReportType.values])
