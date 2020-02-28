import winrm
import os
import string
import mysql.connector

# Mysql connection ##
pass_db = os.getenv('db_pass')
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd=pass_db,
  database="servers"
)
# Get info of the servers ##
def windowsinfo(server_ip):
    Huser = os.getenv('HVuser')
    Hpass = os.getenv('HVpass')
    s = winrm.Session(server_ip, auth=(Huser, Hpass))
    ht = s.run_ps('(Get-VM).count')
    ht = ht.std_out
    mycursor = mydb.cursor()
    #for x in range(int(ht)):
    for x in range(5):
        vm_name = s.run_ps("Get-VM | Select -ExpandProperty Name | Select-Object -Index " + str(x) )
        vm_names = vm_name.std_out
        vm_names = vm_names.rstrip()
        mycursor.execute("SELECT server_name FROM server WHERE server_name='" + vm_names + "'")
        myresult = mycursor.fetchone()
        if myresult is not None:
            myresult = str(myresult[0])
        if ( myresult == vm_names ):
            print ("Igual --------" + myresult )
        else:
            print ("NAda -------- ")
    mycursor.close()
    mydb.close()
    # vm_count = int(vm_count)-1
    # vm_name = s.run_ps('Get-VM | Select -ExpandProperty Name | Select-Object -Index ('+ vm_count + ')' )
    # print (vm_name)
windowsinfo("192.168.100.205")