import time
import ipaddress
import wifi
import socketpool
import ssl

import adafruit_requests


class Wifi_Tools:
    """
    Wifi Tools helper methods
    """

    def __init__(self):
        self._network_ssid_list = []
        self._ssid = ""
        self._password = ""
        self._connected = False
        self._socket_pool = self._init_socket_pool()

    @property
    def ssid(self):
        return self._ssid

    @staticmethod
    def _init_socket_pool() -> socketpool.SocketPool:
        return socketpool.SocketPool(wifi.radio)

    def scan_network(self) -> int:
        for network in wifi.radio.start_scanning_networks():
            self._network_ssid_list.append(network.ssid)
            # print(network, network.ssid, network.channel)
        wifi.radio.stop_scanning_networks()
        return len(self._network_ssid_list)

    @property
    def get_ssid_list(self) -> []:
        return self._network_ssid_list

    def connect(self, ssid, password) -> bool:
        try:
            print("joining network...")
            self._ssid = ssid
            self._password = password
            wifi.radio.connect(ssid=ssid, password=password)
            # the above gives "ConnectionError: Unknown failure" if ssid/passwd is wrong
            self._connected = True
            return True
        except ConnectionError:
            self._connected = False
            return False

    @property
    def ip_address(self) -> ipaddress.IPv4Address:
        if self._connected:
            return wifi.radio.ipv4_address
        else:
            return None

    def fetch_response(self, url: str, **kw) -> adafruit_requests.Response:
        request = adafruit_requests.Session(self._socket_pool, ssl.create_default_context())
        print("fetch_response:Fetching:url=" + url);
        print("fetch_response:Fetching:kw =" + str(kw));
        response = request.get(url, **kw)
        print("fetch_response:Fetching:response.status_code =" + str(response.status_code));

        return response
        # ret_val = [response.status_code, response.text]
        # print(response.status_code)
        # print(response.text)
        # return ret_val

    def get(self, url: str, **kw) -> [int, str]:
        return self.fetch_response(url, **kw)

wifi_tools = Wifi_Tools()

#
# print("my IP addr:", wifi.radio.ipv4_address)
#
# print("pinging 1.1.1.1...")
# ip1 = ipaddress.ip_address("1.1.1.1")
# print("ip1:", ip1)
# print("ping:", wifi.radio.ping(ip1))
#
# pool = socketpool.SocketPool(wifi.radio)
# request = adafruit_requests.Session(pool, ssl.create_default_context())
#
# print("Fetching wifitest.adafruit.com...");
# response = request.get("http://wifitest.adafruit.com/testwifi/index.html")
# print(response.status_code)
# print(response.text)
#
# print("Fetching https://httpbin.org/get...");
# response = request.get("https://httpbin.org/get")
# print(response.status_code)
# print(response.json())

# while True:
#     print("alive")
#     time.sleep(0.5)
