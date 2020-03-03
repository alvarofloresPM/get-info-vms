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
def updateinfoserver(data, master_ip):
    server_name = data
    server_state = ""
    server_ram = ""
    server_uptime = ""
    Huser = os.getenv('HVuser')
    Hpass = os.getenv('HVpass')
    s = winrm.Session(master_ip, auth=(Huser, Hpass))

    # server_state
    response = ""
    response = s.run_ps("get-vm -Name " + server_name + " | select state | Format-List")
    response = response.std_out
    response = response.rstrip()
    response = re.findall("State : ([a-zA-Z]{1,10})", response)
    if len(response) != 0:
        server_state = str(response[0])
        print (server_state)
    # server_ram
    response = ""
    if server_state != "Off":
        response = s.run_ps("get-vm -Name " + server_name + " |  select MemoryAssigned | Format-List")
        response = response.std_out
        response = response.rstrip()
        response = re.findall("[0-9]{1,20}", response)
        if len(response) != 0:
            server_ram = str(response[0])
            server_ram = int(server_ram)/1000000
            server_ram = str(server_ram) + " MB"
            print (server_ram)
    else:
        server_ram = ""

    # server_uptime
    response = ""
    if server_state != "Off":
        response = s.run_ps("get-vm -Name " + server_name + " | select Uptime | Format-List")
        response = response.std_out
        response1 = re.findall("([0-9]{1,4})\.([0-9]{2}):([0-9]{1,2}):([0-9]{1,2})", response)
        response2 = re.findall(" ([0-9]{1,2}):([0-9]{1,2}):([0-9]{1,2})", response)
        if len(response2) != 0:
            server_uptime_d = ""
            server_uptime_h = str(response2[0][0])
            server_uptime_m = str(response2[0][1])
        if len(response1) != 0:
            server_uptime_d = str(response1[0][0])
            server_uptime_h = str(response1[0][1])
            server_uptime_m = str(response1[0][2])
        server_uptime = server_uptime_d + " dias " + server_uptime_h + " horas " + server_uptime_m +" minutos "
        print (server_uptime_d + " dias " + server_uptime_h + " horas " + server_uptime_m +" minutos ")
    else:
        server_uptime = ""
    # Insert data to the database
    mycursor = mydb.cursor()
    sql = "UPDATE server SET server_state = %s , server_ram = %s , server_uptime = %s WHERE server_name = %s "
    val = (server_state, server_ram, server_uptime, server_name)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record updated.")
    mycursor.close()


def createnewserver(data, master_ip, master_name):
    server_master = master_name + "(" + master_ip + ")"
    server_name = data
    server_ip = ""
    server_vlan = ""
    server_domain = ""
    server_state = ""
    server_ram = ""
    server_uptime = ""
    Huser = os.getenv('HVuser')
    Hpass = os.getenv('HVpass')
    s = winrm.Session(master_ip, auth=(Huser, Hpass))
    nmScan = nmap.PortScanner()

    # server_state
    response = ""
    response = s.run_ps("get-vm -Name " + server_name + " | select state | Format-List")
    response = response.std_out
    response = response.rstrip()
    response = re.findall("State : ([a-zA-Z]{1,10})", response)
    if len(response) != 0:
        server_state = str(response[0])
        print (server_state)

    # server_ip
    response = ""
    if server_state != "Off":
        response = s.run_ps("get-vm -Name " + server_name + " | ?{$_.State -eq \"Running\"} | select -ExpandProperty networkadapters | select ipaddresses | Format-List")
        response = response.std_out
        response = response.rstrip()
        response = re.findall("(10\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})", response)
        if len(response) != 0:
            server_ip = str(response[0])
            print (server_ip)
    # server_vlan
    response = ""
    if server_state != "Off":
        response = s.run_ps("get-vm -Name " + server_name + " | select -ExpandProperty networkadapters | select SwitchName | Format-List")
        response = response.std_out
        response = response.rstrip()
        response = re.findall("[0-9]{2,4}", response)
        if len(response) != 0:
            if str(response[0]) == "501":
                server_vlan = str(response[0])
                server_vlan = "Devops (" + server_vlan + ")"
            if str(response[0]) == "502":
                server_vlan = str(response[0])
                server_vlan = "PS01 (" + server_vlan + ")"
            if str(response[0]) == "503":
                server_vlan = str(response[0])
                server_vlan = "PS02 (" + server_vlan + ")"
            if str(response[0]) == "504":
                server_vlan = str(response[0])
                server_vlan = "PS03-04 (" + server_vlan + ")"
            if str(response[0]) == "505":
                server_vlan = str(response[0])
                server_vlan = "TrDoc (" + server_vlan + ")"
            if str(response[0]) == "506":
                server_vlan = str(response[0])
                server_vlan = "Support (" + server_vlan + ")"
            if str(response[0]) == "507":
                server_vlan = str(response[0])
                server_vlan = "Alpha (" + server_vlan + ")"
            if str(response[0]) == "508":
                server_vlan = str(response[0])
                server_vlan = "Devleopment (" + server_vlan + ")"
            if str(response[0]) == "509":
                server_vlan = str(response[0])
                server_vlan = "QA (" + server_vlan + ")"
            if str(response[0]) == "510":
                server_vlan = str(response[0])
                server_vlan = "Sales (" + server_vlan + ")"
            if str(response[0]) == "500":
                server_vlan = str(response[0])
                server_vlan = "IT (" + server_vlan + ")"
            print (server_vlan)
    # server_domain
    response = ""
    if server_state != "Off":
        if server_ip != "":
            nmScan.scan(server_ip, '21-443')
            try:
                response = str(nmScan[server_ip].hostname())
                response = response.rstrip()
            except KeyError as exkey:
                print("[!] Cannot scan host!: " + server_ip)
            print(type(response))
            print (str(response))
            if len(response) != 0:
                server_domain = str(response)
                print (server_domain)
    
    # server_ram
    response = ""
    if server_state != "Off":
        response = s.run_ps("get-vm -Name " + server_name + " |  select MemoryAssigned | Format-List")
        response = response.std_out
        response = response.rstrip()
        response = re.findall("[0-9]{1,20}", response)
        if len(response) != 0:
            server_ram = str(response[0])
            server_ram = int(server_ram)/1000000
            server_ram = str(server_ram) + " MB"
            print (server_ram)
    # server_uptime
    response = ""
    if server_state != "Off":
        response = s.run_ps("get-vm -Name " + server_name + " | select Uptime | Format-List")
        response = response.std_out
        response1 = re.findall("([0-9]{1,4})\.([0-9]{2}):([0-9]{1,2}):([0-9]{1,2})", response)
        response2 = re.findall(" ([0-9]{1,2}):([0-9]{1,2}):([0-9]{1,2})", response)
        if len(response2) != 0:
            server_uptime_d = ""
            server_uptime_h = str(response2[0][0])
            server_uptime_m = str(response2[0][1])
        if len(response1) != 0:
            server_uptime_d = str(response1[0][0])
            server_uptime_h = str(response1[0][1])
            server_uptime_m = str(response1[0][2])
        server_uptime = server_uptime_d + " dias " + server_uptime_h + " horas " + server_uptime_m +" minutos "
        print (server_uptime_d + " dias " + server_uptime_h + " horas " + server_uptime_m +" minutos ")
    
    # Insert data to the database
    mycursor = mydb.cursor()
    sql = "INSERT INTO server (server_master, server_name, server_ip, server_vlan, server_domain, server_state, server_ram, server_uptime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (server_master, server_name, server_ip, server_vlan, server_domain, server_state, server_ram, server_uptime)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    mycursor.close()

def itwasdeleted(master_ip, master_name):
    Huser = os.getenv('HVuser')
    Hpass = os.getenv('HVpass')
    s = winrm.Session(master_ip, auth=(Huser, Hpass))
    mycursor = mydb.cursor()
    master_name = master_name + "(" + master_ip + ")"
    sql = "SELECT server_name FROM server WHERE server_master = '" + master_name + "'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x[0])
        try:
            vm_name = s.run_ps("Get-VM -Name " + str(x) )
            vm_names = vm_name.std_out
            vm_names = vm_names.rstrip()
            print (vm_names)
        except:
            print("Posiblemente borrado: " + str(x))

    mycursor.close()

# Get info of the servers ##
def windowsinfo(master_ip, master_name):
    Huser = os.getenv('HVuser')
    Hpass = os.getenv('HVpass')
    s = winrm.Session(master_ip, auth=(Huser, Hpass))
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
            updateinfoserver(vm_names, master_ip)
        else:
            print ("Create new Data -------- " + vm_names)
            createnewserver(vm_names, master_ip, master_name)
    mycursor.close()

# MAIN section
#windowsinfo("192.168.100.205","PHOBOS")

itwasdeleted("192.168.100.205","PHOBOS")