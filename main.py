import winrm
import os
import string
import mysql.connector
import re
import nmap

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
    Huser = os.getenv('HVuser')
    Hpass = os.getenv('HVpass')
    s = winrm.Session(server_master, auth=(Huser, Hpass))
    nmScan = nmap.PortScanner()

    # server_ip
    response = s.run_ps("get-vm -Name " + server_name + " | ?{$_.State -eq \"Running\"} | select -ExpandProperty networkadapters | select ipaddresses | Format-List")
    response = response.std_out
    response = response.rstrip()
    response = re.findall("(10\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})", response)
    print ("ERROR     ---   " + str(response))
    if response is not None:
        server_ip = str(response[0])
        print (server_ip)
    # server_vlan
    response = s.run_ps("get-vm -Name " + server_name + " | select -ExpandProperty networkadapters | select SwitchName | Format-List")
    response = response.std_out
    response = response.rstrip()
    response = re.findall("VLAN [0-9]{2,4}", response)
    if response is not None:
        server_vlan = str(response[0])
        print (server_vlan)
    # server_domain
    nmScan.scan(server_ip, '21-443')
    response = str(nmScan[server_ip].hostname())
    response = response.rstrip()
    if response is not None:
        server_domain = response
        print (server_domain)
    # server_state
    response = s.run_ps("get-vm -Name " + server_name + " | select state | Format-List")
    response = response.std_out
    response = response.rstrip()
    response = re.findall("State : ([a-zA-Z]{1,10})", response)
    if response is not None:
        server_state = str(response[0])
        print (server_state)
    # server_ram
    response = s.run_ps("get-vm -Name " + server_name + " |  select MemoryAssigned | Format-List")
    response = response.std_out
    response = response.rstrip()
    response = re.findall("[0-9]{1,20}", response)
    if response is not None:
        server_ram = str(response[0])
        server_ram = int(server_ram)/1000000000
        server_ram = str(server_ram) + " GB"
        print (server_ram)
    # server_uptime
    response = s.run_ps("get-vm -Name " + server_name + " | select Uptime | Format-List")
    response = response.std_out
    response = re.findall("([0-9]{1,4})\.([0-9]{2}):([0-9]{1,2}):([0-9]{1,2})", response)
    if response is None:
        response = re.findall(" ([0-9]{1,2}):([0-9]{1,2}):([0-9]{1,2})", response)
        server_ram_d = ""
        server_ram_h = str(response[0][0])
        server_ram_m = str(response[0][1])
    else:
        server_ram_d = str(response[0][0])
        server_ram_h = str(response[0][1])
        server_ram_m = str(response[0][2])
    server_uptime = server_ram_d + " dias " + server_ram_h + " horas " + server_ram_m +" minutos "
    print (server_ram_d + " dias " + server_ram_h + " horas " + server_ram_m +" minutos ")
    
    # Insert data to the database
    mycursor = mydb.cursor()
    sql = "INSERT INTO server (server_master, server_name, server_ip, server_vlan, server_domain, server_state, server_ram, server_uptime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (server_master, server_name, server_ip, server_vlan, server_domain, server_state, server_ram, server_uptime)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    mycursor.close()

# Get info of the servers ##
def windowsinfo(server_ip):
    Huser = os.getenv('HVuser')
    Hpass = os.getenv('HVpass')
    s = winrm.Session(server_ip, auth=(Huser, Hpass))
    ht = s.run_ps('(Get-VM).count')
    ht = ht.std_out
    mycursor = mydb.cursor()
    for x in range(int(ht)):
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
    # vm_count = int(vm_count)-1
    # vm_name = s.run_ps('Get-VM | Select -ExpandProperty Name | Select-Object -Index ('+ vm_count + ')' )
    # print (vm_name)
windowsinfo("192.168.100.205")