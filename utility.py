#
# Utility classes
#
import socket

class IPStuff():
    '''
    Class to get hostname and IP address. Useful for IP detection when
    Note that it does no matter the kind of network connection is used: Ethernet or WiFi
    '''
    def __init__(self):
        self.host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host_name)

    def getIP(self):
        '''
        IP address getter
        :return: The currently assigne IP address
        '''
        return self.host_ip

    def getHostName(self):
        '''
        Hostname getter
        :return: The current device hotsname
        '''
        return self.host_name

######################
# For testing only
######################

# Get IP
ip_stuff = IPStuff()

print(ip_stuff.getHostName() + " : " + ip_stuff.getIP())