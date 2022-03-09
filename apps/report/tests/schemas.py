from helpers.test import generate_list_schema_schema

monitoring_system_schema = {
    'id': {'type': 'string', 'required': True, 'nullable': False},
    'title': {'type': 'string', 'required': True, 'nullable': False},
}

incident_report_schema = {
    'id': {'type': 'string', 'required': True, 'nullable': False},
    'monitoring_system': {'type': 'dict', 'required': True, 'schema': monitoring_system_schema, 'nullable': True},
    'incident': {'type': 'string', 'required': True, 'nullable': False},
    'position': {'type': 'integer', 'required': True, 'nullable': False},
    'report_type': {'type': 'integer', 'required': True, 'nullable': False},
    'translated_report_type': {'type': 'string', 'required': True, 'nullable': False},
}

incident_report_list_schema = generate_list_schema_schema(incident_report_schema)
