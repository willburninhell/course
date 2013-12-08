from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen = cmdgen.CommandGenerator()

errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(cmdgen.CommunityData('WGS_RO'),cmdgen.UdpTransportTarget(('10.254.5.3', 161)),'1.3.6.1.2.1.2.2.1.5.43')
if errorIndication:
    print(errorIndication)
else:
    if errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex)-1] or '?'))
    else:
        for name, val in varBinds:
            print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))