import winrm
import os
import string
import mysql.connector

## Mysql connection ##
# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   passwd="OHS&4p%6zH",
#   database="servers"
# )
## Get info of the servers ##
def windowsinfo(server_ip):
    Huser = os.getenv('HVuser')
    Hpass = os.getenv('HVpass')
    s = winrm.Session(server_ip, auth=(Huser, Hpass))
    ht = s.run_ps('(Get-VM).count')
    ht = ht.std_out
    for x in range(ht):
        vm_name = s.run_ps("Get-VM | Select -ExpandProperty Name | Select-Object -Index " + x )
        print (vm_name.std_out)        
    # vm_count = int(vm_count)-1
    # vm_name = s.run_ps('Get-VM | Select -ExpandProperty Name | Select-Object -Index ('+ vm_count + ')' )
    # print (vm_name)
windowsinfo("192.168.100.205")