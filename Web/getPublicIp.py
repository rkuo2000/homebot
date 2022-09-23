from urllib.request import urlopen
import re
def getPublicIp():
    data = str(urlopen('http://checkip.dyndns.com/').read())
    return re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)

ipaddr = getPublicIp()
print(ipaddr)
