import json
import requests
import re
from urllib import parse
from FuzzTools import PayloadOperation

Code = {
    # Informational.
    100: ('continue',),
    101: ('switching_protocols',),
    102: ('processing',),
    103: ('checkpoint',),
    122: ('uri_too_long', 'request_uri_too_long'),
    200: ('ok', 'okay', 'all_ok', 'all_okay', 'all_good', '\\o/', '✓'),
    201: ('created',),
    202: ('accepted',),
    203: ('non_authoritative_info', 'non_authoritative_information'),
    204: ('no_content',),
    205: ('reset_content', 'reset'),
    206: ('partial_content', 'partial'),
    207: ('multi_status', 'multiple_status', 'multi_stati', 'multiple_stati'),
    208: ('already_reported',),
    226: ('im_used',),

    # Redirection.
    300: ('multiple_choices',),
    301: ('moved_permanently', 'moved', '\\o-'),
    302: ('found',),
    303: ('see_other', 'other'),
    304: ('not_modified',),
    305: ('use_proxy',),
    306: ('switch_proxy',),
    307: ('temporary_redirect', 'temporary_moved', 'temporary'),
    308: ('permanent_redirect',
          'resume_incomplete', 'resume',),  # These 2 to be removed in 3.0

    # Client Error.
    400: ('bad_request', 'bad'),
    401: ('unauthorized',),
    402: ('payment_required', 'payment'),
    403: ('forbidden',),
    404: ('not_found', '-o-'),
    405: ('method_not_allowed', 'not_allowed'),
    406: ('not_acceptable',),
    407: ('proxy_authentication_required', 'proxy_auth', 'proxy_authentication'),
    408: ('request_timeout', 'timeout'),
    409: ('conflict',),
    410: ('gone',),
    411: ('length_required',),
    412: ('precondition_failed', 'precondition'),
    413: ('request_entity_too_large',),
    414: ('request_uri_too_large',),
    415: ('unsupported_media_type', 'unsupported_media', 'media_type'),
    416: ('requested_range_not_satisfiable', 'requested_range', 'range_not_satisfiable'),
    417: ('expectation_failed',),
    418: ('im_a_teapot', 'teapot', 'i_am_a_teapot'),
    421: ('misdirected_request',),
    422: ('unprocessable_entity', 'unprocessable'),
    423: ('locked',),
    424: ('failed_dependency', 'dependency'),
    425: ('unordered_collection', 'unordered'),
    426: ('upgrade_required', 'upgrade'),
    428: ('precondition_required', 'precondition'),
    429: ('too_many_requests', 'too_many'),
    431: ('header_fields_too_large', 'fields_too_large'),
    444: ('no_response', 'none'),
    449: ('retry_with', 'retry'),
    450: ('blocked_by_windows_parental_controls', 'parental_controls'),
    451: ('unavailable_for_legal_reasons', 'legal_reasons'),
    499: ('client_closed_request',),

    # Server Error.
    500: ('internal_server_error', 'server_error', '/o\\', '✗'),
    501: ('not_implemented',),
    502: ('bad_gateway',),
    503: ('service_unavailable', 'unavailable'),
    504: ('gateway_timeout',),
    505: ('http_version_not_supported', 'http_version'),
    506: ('variant_also_negotiates',),
    507: ('insufficient_storage',),
    509: ('bandwidth_limit_exceeded', 'bandwidth'),
    510: ('not_extended',),
    511: ('network_authentication_required', 'network_auth', 'network_authentication'),
}


def CreateDataPackge(url, method, header, data, cookie):
    cookies = dict(cookies_are=cookie)
    if method == "GET":
        r = requests.get(url, headers=header, params=data, cookies=cookies)
    elif method == "POST":
        r = requests.post(url=url, headers=header, data=data, cookies=cookies)
    result = {'request': [], 'response': [], 'body': []}
    result['request'].append(r.request.method + ' ' + r.request.path_url + " HTTP/1.1")
    for key in r.request.headers.keys():
        result['request'].append(key + ':' + r.request.headers[key])
    result['request'].append('')
    if (r.request.method == "POST"):
        result['request'].append(r.request.body)
    result['response'].append("HTTP/1.1 " + str(r.status_code) + ' ' + Code[r.status_code][0])
    for key in r.headers.keys():
        result['response'].append(key + ':' + r.headers[key])
    result['body'].append(r.text)
    if len(r.history) > 0:
        r = r.history[0]
    json_data = {}
    json_data['host'] = re.findall('(\.[^/]*)*', '.' + re.sub('http://|https://', '', r.url))[0][1:]
    json_data['path'] = r.request.path_url
    json_data['method'] = r.request.method
    json_data['headers'] = dict(r.headers)
    json_data['data'] = {}
    try:
        json_data['cookies'] = r.request.headers['Cookie']
    except Exception as e:
        print(e)
    if r.request.body == "":
        pass
    else:
        data1 = {}
        if r.request.body == None:
            pass
        else:
            temp = r.request.body.split('&')
            for t in temp:
                i = t.split('=')
                data1[i[0]] = i[1]
        json_data['data'] = data1
    result['json_data'] = json.dumps(json_data)
    return result


def Fuzz(data_json):
    # {"host":"baidu.com","path":"","method":"GET","headers":{"User-Agent":"python36/requests"},"data":{},"cookies":""}
    temp = data_json
    host = temp['host']
    path = temp['path']
    method = temp['method']
    try:
        headers = temp['headers']
    except Exception as e:
        headers = None
    try:
        cookies = temp['cookies']
        cookies = dict(cookies_are=cookies)
    except Exception as e:
        cookies = ""
    try:
        data = temp['data']
    except KeyError as e:
        data = None
    url = "http://" + host + path
    result = {}
    result['host'] = host
    result['path'] = path
    try:
        if (method == 'GET'):
            r = requests.get(url, headers=headers, params=data, cookies=cookies)
            result['statusco'] = str(r.status_code)
            try:
                result['codelenth'] = str(r.headers['Content-Length'])
            except Exception as e:
                result['codelenth'] = "-"
            result['status'] = "1"
            result['r'] = r
        elif (method == 'POST'):
            r = requests.post(url, data=data, headers=headers, cookies=cookies)
            result['statusco'] = str(r.status_code)
            try:
                result['codelenth'] = str(r.headers['Content-Length'])
            except Exception as e:
                result['codelenth'] = "-"
            result['r'] = r
        else:
            result['statusco'] = "-"
            result['codelenth'] = "-"
            result['status'] = "-1"
    except Exception as e:
        result['status'] = "0"
        print(e)
        # {"host": "www.baidu.com", "path": "/", "statusco": "200", "codelenth": "555", "status": "1"}
    return result


def FuzzTest(TestType, strategy, data_json):
    strategy = strategy.replace('\n', '').replace('\r','')
    strategy = strategy.split(';')
    resentop = 0
    updateop = []
    judgeop = []
    errorOp = []

    for i in range(len(strategy)):
        if (strategy[i] == "resent()"):
            resentop = resentop + 1
        elif len(re.findall('judge\[.*?\]', strategy[i], re.S)) == 1:
            judgeop.append(re.findall('judge\[(.*?)\]', strategy[i], re.S)[0].split(',')[0])
        elif len(re.findall('update\[.*?\]', strategy[i], re.S)) == 1:
            updateop.append(re.findall('update\[(.*?)\]', strategy[i], re.S)[0].split(','))
        else:
            errorOp.append(strategy[i])
    result = []

    for i in range(resentop):
        result.append(Fuzz(json.loads(data_json)))
    temp = data_json
    str1 = ""
    for item in updateop:
        t = item[0]
        method = item[3]
        payload = PayloadOperation.getPayload(item[1])

        for i in range(min(int(item[2]),len(payload['BODY']))):
            if str1 != "":
                str1 += ','
            if method == 'a':
                str1 += temp.replace(t, t + payload['BODY'][i])
            elif method == 'w':
                str1 += temp.replace(t, payload['BODY'][i])
        temp = str1
        str1 = ""
    temp = '[' + temp + ']'
    for i in json.loads(temp):
        result.append(Fuzz(i))
    test = []
    for i in range(len(result)):
        test.append(result[i]['r'])
        result[i].pop('r')
    tem = {'results': result, 'hitCount': 0, "200_ok": 0, 'loop': len(result), 'HitMap': "", 'tiaojian': ""}
    for item in judgeop:
        tem['tiaojian']=tem['tiaojian']+str(item).replace('《','').replace('》','')
        if tem['tiaojian'] !="":
            tem['tiaojian'] = tem['tiaojian']+','
        for i in range(len(test)):
            result[i]['status'] = judge(test[i], item)


    dic = {}
    for i in result:
        for j in i['status']['ResultMap']:
            dic[j]=0
    for i in result:

        try:
            if i['status']['result'] == '1':
                tem['hitCount'] += 1

        except Exception as e:
            pass
        if i['statusco'] == '200':
            tem['200_ok'] += 1
        for j in i['status']['ResultMap']:
            if i['status']['ResultMap'][j] == 1:
                dic[j]+=1
    for i in dic:
        tem['HitMap'] = tem['HitMap']+str(i)+":"+str(dic[i])+"次;"

    return tem


def judge(r, tiaojian):
    dic = {}
    dic['attack.request.host'] = re.findall('(\.[^/]*)*', '.' + re.sub('http://|https://', '', r.url))[0][1:]
    dic['attack.request.url'] = r.url
    dic['attack.request.method'] = r.request.method
    dic['attack.request.length'] = len(str(r.headers))
    dic['attack.request.headers'] = str(dict(r.request.headers))
    dic['attack.response.length'] = len(str(r.headers))
    dic['attack.response.headers'] = str(dict(r.headers))
    dic['attack.response.body'] = r.text
    dic['attack.response.status'] = r.status_code
    ResultMap = {}
    isAnd = re.findall('[&,\|]', tiaojian, re.S)
    resons = re.findall('《.*?》', tiaojian, re.S)
    for i in range(len(resons)):
        resons[i] = resons[i].replace('《', '').replace('》', '')
    results = []
    for i in range(len(resons)):
        temp = resons[i]
        ResultMap[temp] = 0
        reson = []
        reson.append(re.findall('<|>|=|in|not_in', temp, re.S)[0])
        reson.append(temp.split(reson[0])[0])  # resons[i]=运算符,[运算数据1,运算数据2]
        reson.append(temp.split(reson[0])[1])
        reson[0] = reson[0].replace(' ', '')
        reson[1] = reson[1].replace(' ', '')
        reson[2] = reson[2].replace(' ', '')
        try:
            reson[1]=dic[reson[1]]
        except Exception as e:
            pass
        try:
            reson[2] = dic[reson[2]]
        except Exception as e:
            pass
        if reson[0] == '<':
            try:
                results.append(int(reson[1]) < int(reson[2]))
            except Exception as e:
                print(e)
                results.append(False)
        elif reson[0] == '>':
            try:
                results.append(int(reson[1]) > int(reson[2]))
            except Exception as e:
                print(e)
                results.append(False)
        elif reson[0] == '=':
            try:
                results.append(int(reson[1]) == int(reson[2]))
            except Exception as e:
                print(e)
                results.append(False)
        elif reson[0] == 'in':
            try:
                results.append(str(reson[1]) in str(reson[2]))
            except Exception as e:
                print(e)
                results.append(False)
        elif reson[0] == 'not_in':
            try:
                results.append(str(reson[1]) not in str(reson[2]))
            except Exception as e:
                print(e)
                results.append(False)
        if results[i] == True:
            ResultMap[temp] = 1

    if len(results) == 0:
        return {"result": '-', "ResultMap": ResultMap}
    else:
        SUM = results[0]
        for i in range(1, len(results)):
            if SUM == False and isAnd[i - 1] == '&':
                return {"result": '0', "ResultMap": ResultMap}
            elif SUM == True and isAnd[i - 1] == '|':
                return {"result": '1', "ResultMap": ResultMap}
            else:
                if isAnd[i - 1] == '&':
                    SUM = SUM and results[i]
                elif isAnd[i - 1] == '|':
                    SUM = SUM or results[i]
        if SUM == True:
            return {"result": '1', "ResultMap": ResultMap}
        else:
            return {"result": '0', "ResultMap": ResultMap}
