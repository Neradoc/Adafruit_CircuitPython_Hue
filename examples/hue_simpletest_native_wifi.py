import board
import socketpool
import ssl
import time
import wifi

from adafruit_hue import Bridge
import adafruit_requests

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

wifi.radio.connect(ssid=secrets["ssid"], password=secrets["password"])
socket_pool = socketpool.SocketPool(wifi.radio)

requests = adafruit_requests.Session(socket_pool, ssl.create_default_context())

# Attempt to load bridge username and IP address from secrets.py
try:
    username = secrets["hue_username"]
    bridge_ip = secrets["bridge_ip"]
    my_bridge = Bridge(requests, bridge_ip, username)
except:
    # Perform first-time bridge setup
    my_bridge = Bridge(requests)
    ip = my_bridge.discover_bridge()
    username = my_bridge.register_username()
    print(
        'ADD THESE VALUES TO SECRETS.PY: \
                            \n\t"bridge_ip":"{0}", \
                            \n\t"hue_username":"{1}"'.format(
            ip, username
        )
    )
    raise

# Enumerate all lights on the bridge
my_bridge.get_lights()

# Turn on the light
my_bridge.set_light(1, on=True)

# RGB colors to Hue-Compatible HSL colors
hsl_y = my_bridge.rgb_to_hsb([255, 255, 0])
hsl_b = my_bridge.rgb_to_hsb([0, 0, 255])
hsl_w = my_bridge.rgb_to_hsb([255, 255, 255])
hsl_colors = [hsl_y, hsl_b, hsl_w]

# Set the light to Python colors!
for color in hsl_colors:
    my_bridge.set_light(1, hue=int(color[0]), sat=int(color[1]), bri=int(color[2]))
    time.sleep(5)

# Set a predefinedscene
# my_bridge.set_group(1, scene='AB34EF5')

# Turn off the light
my_bridge.set_light(1, on=False)
