import winrm
import os
import string
import mysql.connector

## Mysql connection ##
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="OHS&4p%6zH",
  database="servers"
)
## Get info of the servers ##
def windowsinfo(ip):
    Huser = os.getenv('HVuser')
    Hpass = os.getenv('HVpass')
    s = winrm.Session( ip , auth=(Huser, Hpass))
    vm_count = s.run_ps('(Get-VM).count')
    print (vm_count)
    # vm_count = int(vm_count)-1
    # vm_name = s.run_ps('Get-VM | Select -ExpandProperty Name | Select-Object -Index ('+ vm_count + ')' )
    # print (vm_name)
    return 0

windowsinfo("192.168.100.200")
