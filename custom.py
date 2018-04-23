from flask import Flask, request, Response, make_response
import socket
from zeroconf import ServiceInfo, Zeroconf
import json
import fcntl
import struct
t1 = "Hello1"
t2 = "Hello2"

'''
==================  zeroconf  ====================
'''

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

desc = {'path': '/~paulsm/'}
info = ServiceInfo("_http._tcp.local.",
                       "Custom._http._tcp.local.",
                       get_ip_address('wlan'), 8081, 0, 0,
                       desc, "ash-2.local.")

zeroconf = Zeroconf()
print("Registration of a service")
zeroconf.register_service(info)

app = Flask(__name__)

@app.route('/t1_update', strict_slashes=True, methods=['POST'])
def update_t1():
    text1 = request.get_data()
    global t1
    t1 = text1
    return "update success!"

@app.route('/t2_update', strict_slashes=True, methods=['POST'])
def update_t2():
    text2 = request.get_data()
    global t2
    t2 = text2
    return "update success!"

@app.route('/t1', strict_slashes=True, methods=['GET'])
def get_t1():
    return t1

@app.route('/t2', strict_slashes=True, methods=['GET'])
def get_t2():
    return t2

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8082, debug=True)

print("Unregistering...")
zeroconf.unregister_service(info)
zeroconf.close()
