import winrm
import os
import string
import mysql.connector
import re

# Mysql connection ##
pass_db = os.getenv('db_pass')
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd=pass_db,
  database="servers"
)
# functions to update data
def updateram(data):
    server_ram = ""
    return 0
def updatestatus(data):
    server_state = ""
    return 0
def updatetime(data):
    server_uptime = ""
    return 0
def createnewserver(data, master):
    server_master = master
    server_name = data
    server_ip = ""
    server_vlan = ""
    server_domain = ""
    server_state = ""
    server_ram = ""
    server_uptime = ""
    server_ssh = ""
    server_web = ""
    server_mysql = ""
    server_os = ""
    server_service = ""
    Huser = os.getenv('HVuser')
    Hpass = os.getenv('HVpass')
    s = winrm.Session(server_master, auth=(Huser, Hpass))
    
    response = s.run_ps("get-vm -Name " + server_name + " | ?{$_.State -eq \"Running\"} | select -ExpandProperty networkadapters | select ipaddresses | Format-List")
    response = response.std_out
    response = response.rstrip()
    response = re.findall("(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)", response)
    response = str(response[0])
    print (type(response))
    print (response)

    return 0

# Get info of the servers ##
def windowsinfo(server_ip):
    Huser = os.getenv('HVuser')
    Hpass = os.getenv('HVpass')
    s = winrm.Session(server_ip, auth=(Huser, Hpass))
    ht = s.run_ps('(Get-VM).count')
    ht = ht.std_out
    mycursor = mydb.cursor()
    #for x in range(int(ht)):
    for x in range(1):
        vm_name = s.run_ps("Get-VM | Select -ExpandProperty Name | Select-Object -Index " + str(x) )
        vm_names = vm_name.std_out
        vm_names = vm_names.rstrip()
        mycursor.execute("SELECT server_name FROM server WHERE server_name='" + vm_names + "' LIMIT 1")
        myresult = mycursor.fetchone()
        if myresult is not None:
            myresult = str(myresult[0])
        if ( myresult == vm_names ):
            print ("Update data --------" + myresult )
            updateram(myresult)
            updatestatus(myresult)
            updatetime(myresult)
        else:
            print ("Create new Data -------- " + vm_names)
            createnewserver(vm_names,server_ip)
    mycursor.close()
    mydb.close()
    # vm_count = int(vm_count)-1
    # vm_name = s.run_ps('Get-VM | Select -ExpandProperty Name | Select-Object -Index ('+ vm_count + ')' )
    # print (vm_name)
windowsinfo("192.168.100.205")