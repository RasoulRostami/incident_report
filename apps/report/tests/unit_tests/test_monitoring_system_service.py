from unittest import mock

from django.test import TestCase
from rest_framework import status

from ..Factories import MonitoringSystemFactory
from ..mocks import MockPullIncidentReportsSuccessfully, MockPullIncidentReportsNotFound
from ...models import IncidentReport
from ...services import MonitoringSystemService


class MonitoringSystemServiceUnitTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.monitoring_system = MonitoringSystemFactory(start_page=0)

    def setUp(self) -> None:
        self.assertIsNone(self.monitoring_system.last_status)
        self.assertIsNone(self.monitoring_system.last_update)
        self.assertEqual(IncidentReport.objects.count(), 0)

    def test_current_url(self):
        monitoring_system_service = MonitoringSystemService(self.monitoring_system)
        url = monitoring_system_service._current_url()
        self.assertEqual(url.rsplit('?')[-1], f'start={self.monitoring_system.current_page}')

        _current_page = 10
        self.monitoring_system.current_page = _current_page
        self.monitoring_system.save()
        self.monitoring_system.refresh_from_db()

        monitoring_system_service = MonitoringSystemService(self.monitoring_system)
        url = monitoring_system_service._current_url()
        self.assertEqual(url.rsplit('?')[-1], f'start={_current_page}')
        self.assertIn('http', url)

    def test_update_request_data_after_field_request(self):
        _status = status.HTTP_400_BAD_REQUEST
        monitoring_system_service = MonitoringSystemService(self.monitoring_system)
        monitoring_system_service._update_request_data(_status)
        self.monitoring_system.refresh_from_db()

        self.assertIsNotNone(self.monitoring_system.last_update)
        self.assertEqual(self.monitoring_system.last_status, _status)
        self.assertEqual(self.monitoring_system.current_page, 0)

    def test_update_request_data_after_success_request(self):
        _status = status.HTTP_200_OK
        monitoring_system_service = MonitoringSystemService(self.monitoring_system)
        monitoring_system_service._update_request_data(_status, self.monitoring_system.current_page + 1)
        self.monitoring_system.refresh_from_db()

        self.assertIsNotNone(self.monitoring_system.last_update)
        self.assertEqual(self.monitoring_system.last_status, _status)
        self.assertEqual(self.monitoring_system.current_page, 1)

    def test_save_new_incident_report(self):
        _results = [
            {'incident': 'create', 'position': 1},
            {'incident': 'update', 'position': 2},
        ]
        monitoring_system_service = MonitoringSystemService(self.monitoring_system)
        monitoring_system_service._save_new_incident_report(_results)

        self.assertEqual(IncidentReport.objects.count(), len(_results))
        self.assertTrue(IncidentReport.objects.filter(position=_results[0]['position']))
        self.assertTrue(IncidentReport.objects.filter(incident=_results[1]['incident']))

    def test_incident_type_is_pull(self):
        _results = [
            {'incident': 'create', 'position': 1},
            {'incident': 'update', 'position': 2},
        ]
        monitoring_system_service = MonitoringSystemService(self.monitoring_system)
        monitoring_system_service._save_new_incident_report(_results)

        self.assertEqual(
            IncidentReport.objects.filter(report_type=IncidentReport.IncidentReportType.PULL).count(), len(_results))

    @mock.patch('requests.get', return_value=MockPullIncidentReportsSuccessfully())
    def test_pull_incident_reports(self, mocked):
        monitoring_system_service = MonitoringSystemService(self.monitoring_system)
        monitoring_system_service.pull_incident_report()
        self.monitoring_system.refresh_from_db()

        self.assertEqual(self.monitoring_system.last_status, status.HTTP_200_OK)
        self.assertEqual(self.monitoring_system.current_page, 1)
        self.assertIsNotNone(self.monitoring_system.last_update)
        self.assertEqual(IncidentReport.objects.count(), len(MockPullIncidentReportsSuccessfully().json()))
        self.assertEqual(IncidentReport.objects.exclude(monitoring_system=self.monitoring_system).count(), 0)

    @mock.patch('requests.get', return_value=MockPullIncidentReportsNotFound())
    def test_pull_incident_reports_not_found_response(self, mocked):
        monitoring_system_service = MonitoringSystemService(self.monitoring_system)
        monitoring_system_service.pull_incident_report()
        self.monitoring_system.refresh_from_db()

        self.assertIsNotNone(self.monitoring_system.last_update)
        self.assertEqual(self.monitoring_system.last_status, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.monitoring_system.current_page, 0)
