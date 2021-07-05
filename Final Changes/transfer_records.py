import json
import requests

headers = {
    'Content-Type': 'Application/json',
}


def connect(external_access_host=None, tenant_id=None, user_name=None, password=None, json_to_push=None,
            single_record=None, multi_record=None):
    external_access_host = external_access_host
    url = 'https://' + str(external_access_host) + '/auth/authentication-endpoint/authenticate/login?TENANTID=' + str(
        tenant_id)

    payload = {"Login": user_name, "password": password}

    response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
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
        if single_record and multi_record is None:
            resp = requests.post(url, headers=headers, verify=False, json=json_to_push)
            if not resp.status_code == 200:
                raise Exception('POST {}'.format(resp.status_code))
            else:
                ticket_count = 1
            return ticket_count, resp.status_code
        if multi_record and single_record is None:
            for x in json_to_push:
                resp = requests.post(url, headers=headers, verify=False, json=x)
                if not resp.status_code == 200:
                    return ticket_count, resp.status_code
                    # raise Exception('POST {}'.format(resp.status_code))
                else:
                    ticket_count += 1
            return ticket_count, None

    except Exception as e:
        raise
