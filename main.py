
from wifi_tools import Wifi_Tools

wt = Wifi_Tools()

num_networks = wt.scan_network()
print("num_networks=" + str(num_networks))

ssid_list = wt.get_ssid_list
for ssid in ssid_list:
    print("ssid=" + ssid)

connected = wt.connect("ogsplosh", "7526250244")
print("connected=" + str(connected))

address = wt.ip_address

print("ip_address=" + str(address))


#import ili9488_pitft_simpletest_parallel
