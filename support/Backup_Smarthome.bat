net use S: \\192.168.1.50\PiShare /persistent:no /user:pi raspberry

robocopy S:\ C:\Users\stanman\Desktop\Unterlagen\Smarthome_Backup /E /MIR /R:3 /W:2 /TEE /FFT /NP /LOG:C:\Skripte\Logs\%DATE%_Smarthome.log

net use S: /delete 