#import Library
import paramiko
import time
import sys

try:
#variabel ip (untuk ip yang diremote), username (untuk masuk ssh), password (password ssh)
    ip_address = ["192.168.122.65","192.168.122.190","192.168.122.152","192.168.122.4"]
    username = "admin"
    password = ""
    i = 0

#perintah untuk melakukan koneksi ssh client ke mikrotik
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for ip in ip_address :
        i += 1
        ssh_client.connect(hostname=ip,username=username,password=password)
        print (f"sukses login to {ip}")
        config_list = [ 'ip dhcp-client add dhcp-options=hostname,clientid disabled=no interface=ether1',
                        'ip dns set servers=8.8.8.8',
                        'ip address add address=192.168.1.1/24 interface=ether2',
                        'ip pool add name=dhcp-server ranges=192.168.1.2-192.168.1.254',
                        'ip dhcp-server add name=dhcp-server interface=ether2 address-pool=dhcp-server disabled=no',
                        'ip dhcp-server network add address=192.168.1.0/24 gateway=192.168.1.1 dns-server=8.8.8.8',
                        'ip service disable telnet,ftp,www,api-ssl',
                        'ip firewall nat add chain=srcnat out-interface=ether1 action=masquerade',
                        'ip firewall address-list add address=192.168.1.2-192.168.1.10 list=allowed_to_router',
                        'ip firewall address-list add address=10.10.10.1 list=allowed_to_router',
                        'ip firewall filter add action=accept chain=input src-address-list=allowed_to_router',
                        'ip firewall filter add action=accept chain=input protocol=icmp',
                        'ip firewall filter add action=drop chain=input',
                        'ip firewall filter add action=drop chain=forward comment="Drop new connections from internet which are not dst-natted" connection-nat-state=!dstnat connection-state=new in-interface=ether1',
                        'tool bandwidth-server set enabled=no',
                        'system clock set time-zone-name=Asia/Jakarta',
                        'system ntp client set enabled=yes primary-ntp=202.162.32.12',
                        'tool mac-server set allowed-interface-list=none',
                        'tool mac-server mac-winbox set allowed-interface-list=none',
                        'tool mac-server ping set enabled=no',
                        'ip neighbor discovery-settings set discover-interface-list=none',
                        'tool romon set enabled=yes secrets=very',
                        f'system identity set name=R{i}',
                        'password old-password="" new-password="kangphery" confirm-new-password="kangphery"',
                        'user add name=very password="very123" disabled=no group=read',
                        ]
        for command in config_list:
            ssh_client.exec_command(command)
            print (command)
        print (f"Konfigurasi Router dengan identity : {i} dan IP Address : {ip} Berhasil")
        time.sleep(0.5)
    sys.exit()

except KeyboardInterrupt:
    print ("\n Exit \n")
    sys.exit()
