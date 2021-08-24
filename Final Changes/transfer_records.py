from requests import post
from json import dumps

headers = {
    'Content-Type': 'Application/json',
}


def connect(external_access_host=None, tenant_id=None, user_name=None, password=None, json_to_push=None,
            single_record=None, multi_record=None):
    external_access_host = external_access_host
    url = 'https://' + str(external_access_host) + '/auth/authentication-endpoint/authenticate/login?TENANTID=' + str(
        tenant_id)

    payload = {"Login": user_name, "password": password}

    response = post(url, headers=headers, data=dumps(payload), verify=False)
    token = response.text
    headers['Cookie'] = 'LWSSO_COOKIE_KEY=' + token

    success_update_count = update_record(external_access_host=external_access_host, tenant_id=tenant_id,
                                         json_to_push=json_to_push, single_record=single_record,
                                         multi_record=multi_record)

    return success_update_count


def update_record(external_access_host=None, tenant_id=None, json_to_push=None, single_record=None, multi_record=None):
    try:
        url = 'https://' + str(external_access_host) + '/rest/' + str(tenant_id) + '/ems/bulk'
        ticket_count = 0
        error_details = None
        completion_status = None
        success_record_id = []
        failure_record_details = {}
        if single_record and multi_record is None:
            record_id = json_to_push['entities'][0]['properties']['Id']
            resp = post(url, headers=headers, verify=False, json=json_to_push)
            if not resp.status_code == 200:
                raise Exception('POST {}'.format(resp.status_code))
            else:
                data = resp.json()
                completion_status = data['meta']['completion_status']
                if str(completion_status).lower() == 'failed':
                    error_details = data['entity_result_list'][0]['errorDetails']
                if not str(completion_status).lower() == 'failed':
                    ticket_count = 1
            return ticket_count, resp.status_code, completion_status, record_id, error_details
        if multi_record and single_record is None:
            for x in json_to_push:
                record_id = x['entities'][0]['properties']['Id']
                resp = post(url, headers=headers, verify=False, json=x)
                data = resp.json()
                completion_status = data['meta']['completion_status']
                if not resp.status_code == 200 or str(completion_status).lower() == 'failed':
                    error_details = data['entity_result_list'][0]['errorDetails']
                    failure_record_details[record_id] = error_details
                else:
                    success_record_id.append(record_id)
                    ticket_count += 1
            return ticket_count, None, completion_status, success_record_id, failure_record_details

    except Exception:
        raise
