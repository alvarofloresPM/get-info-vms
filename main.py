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
def windowsinfo(PM_ip):
    Huser = os.getenv('HVuser')
    Hpass = os.getenv('HVpass')
    PM_ip = '192.168.100.201'
    s = winrm.Session(PM_ip, auth=(Huser, Hpass))
    ht = s.run_ps('(Get-VM).count')
    print(ht)
    print("hola esto es un ejemplo")
    # vm_count = int(vm_count)-1
    # vm_name = s.run_ps('Get-VM | Select -ExpandProperty Name | Select-Object -Index ('+ vm_count + ')' )
    # print (vm_name)
    return;

windowsinfo()