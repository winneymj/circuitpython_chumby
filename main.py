from wifi_tools import wifi_tools

num_networks = wifi_tools.scan_network()
print("num_networks=" + str(num_networks))

ssid_list = wifi_tools.get_ssid_list
for ssid in ssid_list:
    print("ssid=" + ssid)

connected = wifi_tools.connect("ogsplosh", "7526250244")
print("connected=" + str(connected))

address = wifi_tools.ip_address

print("ip_address=" + str(address))

# response = wt.fetch_response("http://wifitest.adafruit.com/testwifi/index.html")
# print("response=" + str(response[0]))
# print("response=" + response[1])

from gnewsclient import gnewsclient
# Initialize a requests object with a socket and esp32spi interface


client = gnewsclient.NewsClient(language='english', location='United States', topic='Top Stories', max_results=3)
print(client.get_config())
print(client.get_news())

# import ili9488_pitft_simpletest_parallel
