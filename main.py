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
    for x in range(int(ht)):
        vm_name = s.run_ps("Get-VM | Select -ExpandProperty Name | Select-Object -Index " + str(x) )
        print (vm_name.std_out) 
        mycursor.execute("SELECT server_name FROM server WHERE server_name='" + vm_name.std_out + "'" )
        myresult = mycursor.fetchone()
        print (myresult)
        print (vm_name.std_out)
        if myresult == vm_name.std_out:
            print ("Igual --------")
        else:
            print ("NAda -------- ")
    mycursor.close()
    mydb.close()
    # vm_count = int(vm_count)-1
    # vm_name = s.run_ps('Get-VM | Select -ExpandProperty Name | Select-Object -Index ('+ vm_count + ')' )
    # print (vm_name)
windowsinfo("192.168.100.205")