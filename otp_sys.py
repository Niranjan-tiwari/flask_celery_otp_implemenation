import requests
import json


class TwoFactor:

    API_KEY = "<API_KEY>"

    def __init__(self,
                 mobile_num):
        self.mobile_num = mobile_num

    def send_opt(self):
        api_end_point = 'https://2factor.in/API/V1/' + self.API_KEY + '/SMS/+91' + self.mobile_num + '/AUTOGEN'
        status = None
        result = requests.get(api_end_point)
        response = json.loads(result.text)
        if response["Status"] == "Success":
            status = True
        return response, status

    def verify_otp(self, session_id, otp):
        api_end_point = 'https://2factor.in/API/V1/' + self.API_KEY + '/SMS/VERIFY/' + session_id + '/' + otp
        status = False
        response = None
        result = requests.get(api_end_point)
        response = json.loads(result.text)
        if response["Status"] == "Success":
            status = True
        return response, status
