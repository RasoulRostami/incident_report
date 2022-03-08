from django.contrib.auth import get_user_model
from factory import django, Faker, PostGenerationMethodCall
from factory import fuzzy, SubFactory

from ..models import MonitoringSystem, IncidentReport

User = get_user_model()


class UserFactory(django.DjangoModelFactory):
    username = Faker('user_name')
    email = Faker('email')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    password = PostGenerationMethodCall('set_password', '1sdf54sf')
    is_staff = Faker('boolean')

    class Meta:
        model = User


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
