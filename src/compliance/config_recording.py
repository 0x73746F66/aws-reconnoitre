import libs
import logging
from copy import deepcopy
from compliance import Reconnoitre, BaseScan, Finding


def config_recording(rule: BaseScan):
    aws_config = libs.get_client('config')
    data = aws_config.describe_configuration_recorder_status()['ConfigurationRecordersStatus']
    for recorder in data:
        finding_base = {
            'account_id': str(rule.account_id),
            'name': f"{rule.__class__.__name__.lower().replace('scan', '')}",
            'region': rule.region,
            'title': rule.name.replace('_', ' '),
            'description': rule.purpose,
            'compliance_status': Finding.STATUS_NOT_AVAILABLE,
            'namespace': 'Software and Configuration Checks',
            'category': 'Industry and Regulatory Standards',
            'classifier': 'CIS AWS Foundations Benchmark',
            'recommendation_text': rule.control,
            'finding_type': 'Other',
            'finding_type_id': 'config-recording',
            'finding_type_data': Reconnoitre.fix_custom_data(recorder),
            'confidence': 100,
            'criticality': 50,
            'severity_normalized': 65
        }
        if rule.recommendation_url:
            finding_base['recommendation_url'] = rule.recommendation_url
        if rule.source_url:
            finding_base['source_url'] = rule.source_url
        if recorder['recording']:
            finding = deepcopy(finding_base)
            finding['severity_normalized'] = 0
            finding['compliance_status'] = Finding.STATUS_PASSED
            rule.setResult(Reconnoitre.COMPLIANT)
            rule.addFinding(Finding(**finding))

    if not rule.result:
        rule.setResult(Reconnoitre.NON_COMPLIANT)
        finding = deepcopy(finding_base)
        finding['confidence'] = 90
        finding['compliance_status'] = Finding.STATUS_FAILED
        rule.addFinding(Finding(**finding))

    rule.setData(data)
    return rule
