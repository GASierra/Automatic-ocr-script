
#!/usr/bin/python3
# coding=utf-8
#
# Author: Gabriel Alexis Sierra Rodriguez
#
# Python version: 3

import os
import sys
import glob

#obtener lista de susbscripciones/webspaces
def listSubscription():
    output = os.popen('sudo plesk bin subscription -l').read()
    subscription = output.strip().split("\n")
    return subscription

def listMainUser():
    subscription = listSubscription()
    output = os.popen("sudo  ls -l /var/www/vhosts/"+subscription+"/httpdocs/occ | awk '{ print $3 }'").read()
    mainUser = output.strip().split("\n")
    print (mainUser)
    return mainUser
    
# obtener lista de usuarios
def listUsers():
    subscription =listSubscription()
    for subscription in listSubscription():
        output = os.popen("sudo -u diversificaadmin /opt/plesk/php/7.4/bin/php /var/www/vhosts/"+subscription+"/httpdocs/occ user:list | awk '{print $2}\' | sed -e 's/://g'").read()
        users = output.strip().split("\n")
    return users

# indexar archivos para que no queden archivos sin convertir
def indexFiles():
    users = listUsers()
    subscription =listSubscription()
    for users in listUsers():
        directory = os.popen("sudo -u diversificaadmin /opt/plesk/php/7.4/bin/php /var/www/vhosts/"+subscription+"/httpdocs/occ files:scan --path "+users+"/files/scan/").read()
        print(os.system(directory))


# paso a ocr
def ocr():
    # users = listUsers()
    subscription =listSubscription()
    for subscription in listSubscription():
        
        # cogemos el Id de la instalacion de nextcloud
        output = os.popen('sudo -u ls /var/wwww/vhosts/'+subscription+'/.nextcloud/data/').read()
        installation = output.strip().split("\n")
        
        # cogemos la lista de usuarios relaccionada con la instalacion
        outputTwo = os.popen("sudo -u diversificaadmin /opt/plesk/php/7.4/bin/php /var/www/vhosts/"+subscription+"/httpdocs/occ user:list | awk '{print $2}\' | sed -e 's/://g'").read()
        users = outputTwo.strip().split("\n")
        
        for users in len(users):
            for files in glob.glob('/var/www/vhosts/'+subscription+'/.nextcloud/data/'+installation+'/'+users+'/files/scan/*.pdf'): 
                nameFiles = os.path.split(files)
                print(os.system('ocrmypdf '+files+' /var/www/vhosts/'+subscription+'/.nextcloud/data/'+installation+'/'+users+'/files/scan/ocr/'+nameFiles[1]+' --skip-text'))
                print('trabajo '+nameFiles[1]+' hecho')

indexFiles()
ocr()
indexFiles()
sys.exit("trabajo completado")



