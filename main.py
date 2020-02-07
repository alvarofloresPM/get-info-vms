import winrm
import os
import string
Huser = os.getenv('HVuser')
Hpass = os.getenv('HVpass')
s = winrm.Session('192.168.100.200', auth=(Huser, Hpass))
m = s.run_ps('(Get-Counter -Counter "\Memory\Available MBytes").CounterSamples[0].CookedValue')
d = s.run_ps('Get-WMIObject -Class Win32_LogicalDisk | Where-Object {$_.DriveType -eq 3} | Select-Object @{n="Unidad";e={($_.Name)}}, @{n="Libre (GB)";e={"{0:n2}" -f ($_.freespace/1gb)}}, @{n="% Libre";e={"{0:n2}" -f ($_.freespace/$_.size*100)}}')
ht = s.run_ps('(Get-VM).count')
hr = s.run_ps('(Get-VM | where {$_.State -eq "Running"}).count')
ho = s.run_ps('(Get-VM | where {$_.State -eq "Off"}).count')
hs = s.run_ps('(Get-VM | where {$_.State -eq "Saved"}).count')
mns = ("\n" 
"--------------------------------------" + "\n" 
"- HYPNOS - 192.168.100.200 -" + "\n"
"--------------------------------------" + "\n"
"Total	 	 Virtual Machines :	" + ht.std_out +
"Saved		Virtual Machines :	" + hs.std_out +
"Running	Virtual Machines :	" + hr.std_out +
"Off		    Virtual Machines :	" + ho.std_out + "\n" + "Free RAM (MB) :  " + m.std_out + d.std_out)

mns = string.replace( mns, '\r', '' )

file = open("/tmp/environment.txt", "w")
file.write("MY_DATA=" + mns)
file.close()

prefix = ' '
suffix = '\\n \\'

with open('/tmp/environment.txt', 'r') as src:
    with open('/tmp/environment2.txt', 'w') as dest:
       for line in src:
           dest.write('%s%s%s\n' % (prefix, line.rstrip('\n'), suffix))