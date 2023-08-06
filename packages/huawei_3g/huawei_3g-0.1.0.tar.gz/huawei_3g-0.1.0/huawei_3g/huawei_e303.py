import requests
import xmltodict
from huawei_3g.datastructures import SMSMessage


class TokenError(Exception):
    pass


class HuaweiE303Modem:
    token = ""

    _error_codes = {
        "100002": "No support",  # Huawei branded 404
        "100003": "Access denied",  # Huawei branded 403
        "100004": "Busy",
        "108001": "Wrong username",
        "108002": "Wrong password",
        "108003": "Already logged in",
        "120001": "Voice busy",
        "125001": "Wrong __RequestVerificationToken header"
    }
    _network_type = {
        0: "No service",
        1: "GSM",
        2: "GPRS",
        3: "EDGE",
        4: "WCDMA",
        5: "HSDPA",
        6: "HSUPA",
        7: "HSPA",
        8: "TDSCDMA",
        9: "HSPA+",
        10: "EVDO rev 0",
        11: "EVDO rev A",
        12: "EVDO rev B",
        13: "1xRTT",
        14: "UMB",
        15: "1xEVDV",
        16: "3xRTT",
        17: "HSPA+ 64QAM",
        18: "HSPA+ MIMO",
        19: "LTE",
        41: "3G"
    }
    _network_status = {
        2: "Connection failed, the profile is invalid",
        3: "Connection failed, the profile is invalid",
        5: "Connection failed, the profile is invalid",
        7: "Network access not allowed",
        8: "Connection failed, the profile is invalid",
        11: "Network access not allowed",
        12: "Connection failed, roaming not allowed",
        13: "Connection failed, roaming not allowed",
        14: "Network access not allowed",
        20: "Connection failed, the profile is invalid",
        21: "Connection failed, the profile is invalid",
        23: "Connection failed, the profile is invalid",
        27: "Connection failed, the profile is invalid",
        28: "Connection failed, the profile is invalid",
        29: "Connection failed, the profile is invalid",
        30: "Connection failed, the profile is invalid",
        31: "Connection failed, the profile is invalid",
        32: "Connection failed, the profile is invalid",
        33: "Connection failed, the profile is invalid",
        37: "Network access not allowed",
        201: "Connection failed, bandwidth exceeded",
        900: "Connecting",
        901: "Connected",
        902: "Disconnected",
        903: "Disconnecting",
        905: "Connection failed, signal poor",
    }

    def __init__(self, interface, sysfs_path):
        self.interface = interface
        self.path = sysfs_path
        self.ip = "192.168.8.1"
        self.base_url = "http://{}/api".format(self.ip)
        self.token = ""
        # self._get_token()

    def get_status(self):
        status_raw = self._api_get("/monitoring/status")
        signal = int(int(status_raw['SignalIcon']) / 5.0 * 100.0)
        network_type = "Unknown"
        if int(status_raw['CurrentNetworkType']) in self._network_type:
            network_type = self._network_type[int(status_raw['CurrentNetworkType'])]
        return {
            'status': self._network_status[int(status_raw['ConnectionStatus'])],
            'signal': signal,
            'network_type': network_type
        }

    def get_message_count(self):
        messages_raw = self._api_get("/sms/sms-count")
        return {
            'count': int(messages_raw['LocalInbox']),
            'unread': int(messages_raw['LocalUnread'])
        }

    def get_messages(self, delete=False):
        raw = self._api_post("/sms/sms-list",
                             "<?xml version=\"1.0\" encoding=\"UTF-8\"?><request>"
                             "<PageIndex>1</PageIndex>"
                             "<ReadCount>50</ReadCount>"
                             "<BoxType>1</BoxType>"
                             "<SortType>0</SortType>"
                             "<Ascending>0</Ascending>"
                             "<UnreadPreferred>0</UnreadPreferred>"
                             "</request>")
        messages = []
        if raw['Count'] == '0':
            return []

        if raw['Count'] == '1':
            # why? WHY HUAWEI?
            message_list = [raw['Messages']['Message']]
        else:
            message_list = raw['Messages']['Message']

        for message in message_list:
            sms = SMSMessage()
            sms.message_id = message['Index']
            sms.message = message['Content']
            sms.sender = message['Phone']
            sms.receive_time = message['Date']
            messages.append(sms)
        if delete:
            ids = []
            for message in messages:
                ids.append(message.message_id)
            self.delete_messages(ids)
        return messages

    def delete_message(self, message_id):
        return self.delete_messages([message_id])

    def delete_messages(self, ids):
        xml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><request>"
        for message_id in ids:
            xml += "<Index>{}</Index>".format(message_id)
        xml += "</request>"
        self._api_post("/sms/delete-sms", xml)

    def __repr__(self):
        return "<HuaweiE303Modem {} ({})>".format(self.interface, self.path)

    def _get_token(self):
        token_response = self._api_get("/webserver/token")
        self.token = token_response['token']

    def _api_get(self, url):
        full_url = self.base_url + url
        response = requests.get(full_url)
        try:
            return self._parse_api_response(response)
        except TokenError:
            self._get_token()
            return self._api_get(url)

    def _api_post(self, url, parameters):
        full_url = self.base_url + url
        parameters_bytes = parameters.encode('UTF-8')

        response = requests.post(full_url, parameters_bytes, headers={
            "__RequestVerificationToken": self.token
        })

        try:
            return self._parse_api_response(response)
        except TokenError:
            self._get_token()
            return self._api_post(url, parameters)

    def _parse_api_response(self, response):
        if response.status_code == 200:
            payload = response.content
            parsed = xmltodict.parse(payload)

            # HAHA! HTTP response codes are for the weak!
            if 'response' in parsed:
                return parsed['response']
            else:
                code = parsed['error']['code']
                if str(code) == "125001":
                    raise TokenError()
                if code in self._error_codes:
                    raise Exception(self._error_codes[str(code)])
                else:
                    raise Exception("Unknown error occurred")
        return {}
