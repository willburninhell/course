from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902

def get_ports_links(ip, ports):
    cmdGen = cmdgen.CommandGenerator()
    port = {}
    links = {}
    eIndication, eStatus, eIndex, vBinds = cmdGen.getCmd(
            cmdgen.CommunityData('WGS_RO'),
            cmdgen.UdpTransportTarget((ip, 161)),
            '1.3.6.1.2.1.1.5.0'
            )


    for p in range(ports):
        if not (eIndication or eStatus):
            errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
                cmdgen.CommunityData('WGS_RO'),
                cmdgen.UdpTransportTarget((ip, 161)),
                '1.3.6.1.2.1.2.2.1.7.'+str(p+1)
            )
            if not (errorIndication or errorStatus):
                for n, v in varBinds:
                    port[ip+':'+str(p+1)] = v.prettyPrint()
            else:
                port[ip+':'+str(p+1)] = '2'
        else:
            port[ip+':'+str(p+1)] = '2'

    for p in range(ports):
        if not (eIndication or eStatus):
            errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
                cmdgen.CommunityData('WGS_RO'),
                cmdgen.UdpTransportTarget((ip, 161)),
                '1.3.6.1.2.1.2.2.1.8.'+str(p+1)
            )
            if not (errorIndication or errorStatus):
                for n, v in varBinds:
                    links[ip+':'+str(p+1)] = v.prettyPrint()
            else:
                links[ip+':'+str(p+1)] = '2'
        else:
            links[ip+':'+str(p+1)] = '2'
    return port, links

def get_one_ports_links(ip, ports):
    print ip
    print ports
    cmdGen = cmdgen.CommandGenerator()
    port = {}
    links = {}

    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.CommunityData('WGS_RO'),
        cmdgen.UdpTransportTarget((ip, 161)),
        '1.3.6.1.2.1.2.2.1.7.'+str(ports)
    )
    if not (errorIndication or errorStatus):
        for n, v in varBinds:
            port[ip+':'+str(ports)] = v.prettyPrint()
    else:
        port[ip+':'+str(ports)] = '2'

    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.CommunityData('WGS_RO'),
        cmdgen.UdpTransportTarget((ip, 161)),
        '1.3.6.1.2.1.2.2.1.8.'+str(ports)
    )
    if not (errorIndication or errorStatus):
        for n, v in varBinds:
            links[ip+':'+str(ports)] = v.prettyPrint()
    else:
        links[ip+':'+str(ports)] = '2'
    return port, links

def openport(ip, port):
    cmdGen = cmdgen.CommandGenerator()

    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.setCmd(
        cmdgen.CommunityData('SW_wRITE'),
        cmdgen.UdpTransportTarget((ip, 161)),
        ('1.3.6.1.2.1.2.2.1.7.'+str(port),rfc1902.Integer(1))
    )

    if errorIndication or errorStatus:
        return False
    else:
        return True

def closeport(ip, port):
    cmdGen = cmdgen.CommandGenerator()

    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.setCmd(
        cmdgen.CommunityData('SW_wRITE'),
        cmdgen.UdpTransportTarget((ip, 161)),
        ('1.3.6.1.2.1.2.2.1.7.'+str(port),rfc1902.Integer(2))
    )

    if errorIndication or errorStatus:
        return False
    else:
        return True