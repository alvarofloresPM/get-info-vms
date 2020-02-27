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
        mycursor.execute("SELECT server_name FROM server WHERE server_name='Alpha-568PM332-507'")
        myresult = mycursor.fetchone()
        myresult = myresult[0]
        vm_names = vm_name.std_out
        print (myresult)
        print (vm_names)
        if ( myresult == vm_names ):
            print ("Igual --------")
        else:
            print ("NAda -------- ")
    mycursor.close()
    mydb.close()
    # vm_count = int(vm_count)-1
    # vm_name = s.run_ps('Get-VM | Select -ExpandProperty Name | Select-Object -Index ('+ vm_count + ')' )
    # print (vm_name)
windowsinfo("192.168.100.205")