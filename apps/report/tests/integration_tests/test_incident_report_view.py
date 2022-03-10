import copy
import json

from cerberus import Validator
from rest_framework import status
from rest_framework.test import APITestCase

from apps.account.tests.factories import UserFactory
from apps.report.models import IncidentReport
from apps.report.tests.Factories import MonitoringSystemFactory, IncidentReportFactory
from apps.report.tests.schemas import incident_report_list_schema, incident_report_schema


class IncidentReportListTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.monitoring_system = MonitoringSystemFactory(is_active=True)
        cls.incident_report_1 = IncidentReportFactory(monitoring_system=cls.monitoring_system,
                                                      report_type=IncidentReport.IncidentReportType.PULL)
        cls.incident_report_2 = IncidentReportFactory(monitoring_system=cls.monitoring_system,
                                                      report_type=IncidentReport.IncidentReportType.PULL)
        cls.incident_report_3 = IncidentReportFactory(monitoring_system=None,
                                                      report_type=IncidentReport.IncidentReportType.PULL)

        cls.user = UserFactory(is_staff=False)

        cls.url = '/api/v1/report/incident-reports/'

    def setUp(self) -> None:
        self.assertIsNone(self.incident_report_3.monitoring_system)

    def test_is_authenticated_401(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_incident_report_permission_and_count(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], IncidentReport.objects.count())

    def test_incident_report_schema(self):
        schema_validator = Validator(incident_report_list_schema)
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertTrue(schema_validator.validate(json.loads(response.content)), msg=schema_validator.errors)

    def test_monitoring_system_id_filter(self):
        new_monitoring_system = MonitoringSystemFactory(is_active=True)
        new_incident_report = IncidentReportFactory(monitoring_system=new_monitoring_system)
        self.client.force_login(self.user)
        response = self.client.get(f'{self.url}?monitoring_system_id={new_monitoring_system.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['id'], str(new_incident_report.id))

    def test_report_type_filter(self):
        new_monitoring_system = MonitoringSystemFactory(is_active=True)
        new_incident_report = IncidentReportFactory(monitoring_system=new_monitoring_system,
                                                    report_type=IncidentReport.IncidentReportType.CUSTOM)
        self.client.force_login(self.user)
        response = self.client.get(f'{self.url}?report_type={IncidentReport.IncidentReportType.CUSTOM.value}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['id'], str(new_incident_report.id))


class IncidentReportCreateTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.monitoring_system = MonitoringSystemFactory(is_active=True)

        cls.staff = UserFactory(is_staff=True)
        cls.user = UserFactory(is_staff=False)

        cls.valid_data_1 = {'incident': 'text', 'position': 1}
        cls.valid_data_2 = {'incident': 'text', 'position': 1, 'monitoring_system_id': str(cls.monitoring_system.id)}

        cls.url = '/api/v1/report/incident-reports/'

    def test_permission_denied(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.valid_data_1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permission_access(self):
        self.client.force_login(self.staff)
        response = self.client.post(self.url, self.valid_data_1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.content)

    def test_required_field(self):
        self.client.force_login(self.staff)

        for key in self.valid_data_1.keys():
            data = copy.deepcopy(self.valid_data_1)
            del data[key]
            response = self.client.post(self.url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.content)

    def test_monitoring_system_is_null(self):
        self.client.force_login(self.staff)
        response = self.client.post(self.url, self.valid_data_1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.content)
        self.assertIsNone(response.data['monitoring_system'])

    def test_monitoring_system_is_not_null(self):
        self.client.force_login(self.staff)
        response = self.client.post(self.url, self.valid_data_2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.content)
        self.assertIsNotNone(response.data['monitoring_system'])
        self.assertEqual(response.data['monitoring_system']['id'], str(self.monitoring_system.id))

    def test_schema(self):
        self.client.force_login(self.staff)
        response = self.client.post(self.url, self.valid_data_2)
        schema_validator = Validator(incident_report_schema)
        self.assertTrue(schema_validator.validate(json.loads(response.content)), msg=schema_validator.errors)

    def test_invalid_data(self):
        self.client.force_login(self.staff)
        data = copy.copy(self.valid_data_1)
        data['report_type'] = IncidentReport.IncidentReportType.PULL
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.content)
