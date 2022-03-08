from unittest import mock

from django.test import TestCase

from ..Factories import MonitoringSystemFactory
from ..mocks import MockPullIncidentReportsSuccessfully
from ...models import IncidentReport, MonitoringSystem
from ...tasks import pull_results, pull_incident_report


class TaskPullIncidentReportUnitTest(TestCase):
    """Test celery beat task"""

    @classmethod
    def setUpTestData(cls):
        cls.monitoring_system_1 = MonitoringSystemFactory(start_page=1, is_active=True)
        cls.monitoring_system_2 = MonitoringSystemFactory(start_page=2, is_active=True)
        cls.monitoring_system_3 = MonitoringSystemFactory(start_page=10, is_active=True)
        cls.monitoring_system_4 = MonitoringSystemFactory(start_page=20, is_active=True)

        cls.monitoring_system_5 = MonitoringSystemFactory(start_page=1, is_active=False)
        cls.monitoring_system_6 = MonitoringSystemFactory(start_page=1, is_active=False)

    def test_pull_results_with_length_zero(self):
        pull_results(1, 1)
        self.assertEqual(IncidentReport.objects.count(), 0)

    @mock.patch('requests.get', return_value=MockPullIncidentReportsSuccessfully())
    def test_pull_results_with_length_one(self, mocked):
        pull_results(0, 1)
        self.assertEqual(IncidentReport.objects.count(), MockPullIncidentReportsSuccessfully().number_of_results)

        monitoring_system = MonitoringSystem.objects.get(id=IncidentReport.objects.first().monitoring_system.id)
        self.assertEqual(monitoring_system.reports.all().count(), MockPullIncidentReportsSuccessfully().number_of_results)

    @mock.patch('requests.get', return_value=MockPullIncidentReportsSuccessfully())
    def test_pull_results_with_length_four(self, mocked):
        pull_results(0, 4)
        self.assertEqual(IncidentReport.objects.count(), MockPullIncidentReportsSuccessfully().number_of_results * 4)

    @mock.patch('requests.get', return_value=MockPullIncidentReportsSuccessfully())
    def test_pull_incident_reports_with_four_monitoring_system(self, mocked):
        pull_incident_report()
        self.assertEqual(IncidentReport.objects.count(), MockPullIncidentReportsSuccessfully().number_of_results * 4)

        for system in MonitoringSystem.active_objects.all():
            self.assertEqual(system.reports.count(), MockPullIncidentReportsSuccessfully().number_of_results)
            self.assertEqual(system.current_page, system.start_page + 1)

    @mock.patch('requests.get', return_value=MockPullIncidentReportsSuccessfully())
    def test_pull_results_with_length_more_than_four_system(self, mocked):
        MonitoringSystemFactory(start_page=20, is_active=True)
        MonitoringSystemFactory(start_page=0, is_active=True)
        pull_incident_report()

        self.assertEqual(IncidentReport.objects.count(), MockPullIncidentReportsSuccessfully().number_of_results * 6)
