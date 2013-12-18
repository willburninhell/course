from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902
from .ping import do_one


def get_ports_links(ip, ports):
    cmdGen = cmdgen.CommandGenerator()
    port = {}
    links = {}
    ping = False
    if do_one(ip) > 0:
        print ip, 'ping'
        ping = True
        eInd, eS, eI, vB = cmdGen.getCmd(cmdgen.CommunityData('WGS_RO'),
                                         cmdgen.UdpTransportTarget((ip, 161)),
                                         '1.3.6.1.2.1.1.5.0')
    else:
        print ip, 'do not ping'
        eInd = "No SNMP response received before timeout"

    for p in range(ports):
        if ping and (eInd != "No SNMP response received before timeout"):
            print 'port status checked'
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
            print 'port status not checked'
            port[ip+':'+str(p+1)] = '2'

    for p in range(ports):
        if ping and (eInd != "No SNMP response received before timeout"):
            print 'link status checked'
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
            print 'link status not checked'
            links[ip+':'+str(p+1)] = '2'
    return port, links


def get_one_ports_links(ip, ports):
    print ip
    print ports
    cmdGen = cmdgen.CommandGenerator()
    port = {}
    links = {}
    ping = do_one(ip)
    if not ping:
        errorIndication = "No SNMP response received before timeout"
    else:
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
            cmdgen.CommunityData('WGS_RO'),
            cmdgen.UdpTransportTarget((ip, 161)),
            '1.3.6.1.2.1.2.2.1.7.'+str(ports)
        )
    if not (errorIndication == "No SNMP response received before timeout"):
        for n, v in varBinds:
            port[ip+':'+str(ports)] = v.prettyPrint()
    else:
        port[ip+':'+str(ports)] = '2'

    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.CommunityData('WGS_RO'),
        cmdgen.UdpTransportTarget((ip, 161)),
        '1.3.6.1.2.1.2.2.1.8.'+str(ports)
    )
    if not (errorIndication == "No SNMP response received before timeout"):
        for n, v in varBinds:
            links[ip+':'+str(ports)] = v.prettyPrint()
    else:
        links[ip+':'+str(ports)] = '2'
    return port, links


def get_query_port_link(query):
    cmdGen = cmdgen.CommandGenerator()
    port = {}
    links = {}
    ping = {}
    eInd = {}
    eS = {}
    eI = {}
    # k = 0
    for entry in query:
        # print k
        # k+=1
        # if k == 10:
            # return
        switch, sw_port = str(entry).split(':')
        if switch not in ping:
            ping[switch] = do_one(switch)
        if ping[switch] > 0:
            print switch, sw_port
            if switch not in eInd:
                print switch
                print eInd
                eInd[switch], eS[switch], eI, vB = cmdGen.getCmd(
                    cmdgen.CommunityData('WGS_RO'),
                    cmdgen.UdpTransportTarget((switch, 161)),
                    '1.3.6.1.2.1.1.5.0')
            if not (eInd[switch] or eS[switch]):
                eIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
                    cmdgen.CommunityData('WGS_RO'),
                    cmdgen.UdpTransportTarget((switch, 161)),
                    '1.3.6.1.2.1.2.2.1.7.'+str(sw_port)
                )
                if not (eIndication or errorStatus) :
                    for n, v in varBinds:
                        port[entry] = v.prettyPrint()
                else:
                    port[entry] = '2'

                eIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
                    cmdgen.CommunityData('WGS_RO'),
                    cmdgen.UdpTransportTarget((switch, 161)),
                    '1.3.6.1.2.1.2.2.1.8.'+str(sw_port)
                )
                if not (eIndication or errorStatus):
                    for n, v in varBinds:
                        links[entry] = v.prettyPrint()
                else:
                    links[entry] = '2'
            else:
                port[entry] = '2'
                links[entry] = '2'
        else:
            port[entry] = '2'
            links[entry] = '2'
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