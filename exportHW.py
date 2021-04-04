from jnpr.junos import *
import sys, os
from pathlib import Path
from datetime import datetime
from getpass import getpass
from jnpr.junos.exception import ConnectError

from jnpr.junos.utils.start_shell import StartShell

#from lxml import etree

#set time variables for txt naming
timenow = str(datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
date = str(datetime.now().strftime("%Y-%m-%d"))
#opening input file
input_file=open(sys.argv[1], 'r')
lines = input_file.readlines()
#user:password to log in
user = input("Username: ")
password = getpass("Password: ")
#creating folder in desktop if not existent
desktop_folder=os.path.expanduser("~/Desktop")
Path(desktop_folder + "/report Juniper " + date + "/").mkdir(parents=True, exist_ok=True)
#creating set for unreachable IPs
unreachable_ip_set= set()

for line in lines:
    ip=line.strip() #strips CR/LF
    device = Device(host=ip, user=user, password=password, port=22)
    try:
        device.open(normalize=True)
        hostname=device.facts['hostname']
        print("Connected to device ", hostname , "(", ip, ")")
        completeName = os.path.join(os.path.expanduser("~/Desktop/report Juniper " + date + "/"), timenow + "_" + device.facts['hostname'] + "_Hdw_dtl.txt")
        output_file = open(completeName, "w", newline='')
        """ via device.rpc. command remove_ns doesn't work, so the command was run via shell 
        # >show chassis hardware detail | no-more | display xml
        command_result = device.rpc.get_chassis_inventory(remove_ns=False, verbosity="detail")
        #print (etree.dump(command_result))
        command_result_string = etree.tostring(command_result, pretty_print=True)
        output_file.write(command_result_string)
        """
        ####alternative mode, bad implementation since uses shell and cli output but the only available
        ss = StartShell(device)
        ss.open()
        res=ss.run('cli -c "show chassis hardware detail | display xml | no-more"')
        ss.close()
        #strip cli command from string, taking only the second element of the tuple res (splitted by \n)
        clioutput = (res[1]).split("\n",1)[1]
        #strip the last line from string, to delete the trailing character "%"
        clioutput=clioutput[:clioutput.rfind('\n')]
        output_file.write(clioutput)
        ####
        output_file.close()
        device.close()
        print("Disconnected from device ", hostname, "(", ip, ")")
    except ConnectError as err:
        print("Connection Error: {0}".format(err))
        unreachable_ip_set.add(ip)

if not len(unreachable_ip_set) == 0:
    print("\n\nYou had connection errors on these devices: {0}".format(unreachable_ip_set))

input_file.close()

