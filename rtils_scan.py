import blescan
import sys

import bluetooth._bluetooth as bluez

sock = bluez.hci_open_dev(0)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

returnedList = blescan.parse_events(sock, 10)
print "----------"
for list in returnedList:
    print list
