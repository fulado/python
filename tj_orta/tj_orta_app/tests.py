from django.test import TestCase
import urllib
import base64
import json


class ViolationException(Exception):
    def __str__(self):
        return 'violation research error'


def get_token():
    data = '{"username":"ceshihttp","password":"ceshihttp"}'
    url = 'http://192.168.100.234:7000/login'
    data = get_json(get_response_encoded_data(url, data))
    # print(data)
    return data['token']


def get_violation(car_list):
    url = 'http://192.168.100.234:7000/illgledata/vehicle'

    token = get_token()
    data = str({"token": token, "cars": car_list})
    data = get_response_encoded_data(url, data)
    # print(data)
    if b'\xef\xbf\xbd' in data:
        raise ViolationException()

    return get_json(data)


def get_response_encoded_data(url, data):
    # base64加密
    data = base64.b64encode(data.encode('utf-8'))
    data = 'param=%s' % data.decode('utf-8')

    request = urllib.request.Request(url, data.encode('utf-8'))

    response = urllib.request.urlopen(request)

    return base64.b64decode(response.read())


def get_json(data):
    data = data.decode('utf-8')
    return json.loads(data)


def get_violation_count(cars):
    try:
        data = get_violation(cars)['result']
        # print(data)
        violation_dict = {}
        for violation_data in data:
            print(violation_data)
            if violation_data['status'] == 0:
                number = violation_data['platNumber']
                violation_count = len(violation_data['punishs'])
                violation_dict[number] = violation_count
        return violation_dict
    except Exception as violation_error:
        raise violation_error
        return None


if __name__ == '__main__':
    cars = [{"engineNumber": "121111", "platNumber": "冀JD7697", "carType": "01"},
            {"engineNumber": "15E51A", "platNumber": "津CA9257", "carType": "01"},
            {"engineNumber": "15E51A", "platNumber": "津CA9257", "carType": "01"}]

    try:
        violation_count = get_violation_count(cars)
        print(violation_count)
    except Exception as e:
        print(e)
