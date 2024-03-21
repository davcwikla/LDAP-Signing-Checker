from ldap3 import Server, Connection, ALL

print("""\
                                                      
  _      _____          _____     _____ _             _                _____ _               _             
 | |    |  __ \   /\   |  __ \   / ____(_)           (_)              / ____| |             | |            
 | |    | |  | | /  \  | |__) | | (___  _  __ _ _ __  _ _ __   __ _  | |    | |__   ___  ___| | _____ _ __ 
 | |    | |  | |/ /\ \ |  ___/   \___ \| |/ _` | '_ \| | '_ \ / _` | | |    | '_ \ / _ \/ __| |/ / _ \ '__|
 | |____| |__| / ____ \| |       ____) | | (_| | | | | | | | | (_| | | |____| | | |  __/ (__|   <  __/ |   
 |______|_____/_/    \_\_|      |_____/|_|\__, |_| |_|_|_| |_|\__, |  \_____|_| |_|\___|\___|_|\_\___|_|   
                                           __/ |               __/ |                                       
                                          |___/               |___/                                           

Author: Dawid Ćwikła
Version: 1.0 (and final)
-------------------------------------------------------------
""")

ldap_server = input('Podaj adres serwera LDAP (np. ad.example.com): ')
ldap_user = input('Podaj nazwę użytkownika do uwierzytelnienia: ')
ldap_password = input('Podaj hasło użytkownika: ')

server = Server(ldap_server, get_info=ALL)
conn = Connection(server, user=ldap_user, password=ldap_password, authentication='SIMPLE')

if not conn.bind():
    print('Nie udało się połączyć z serwerem LDAP: ', conn.result)
else:
    print('Połączono z serwerem LDAP')

    conn.search('cn=Configuration,dc=example,dc=com',
                '(objectClass=msDS-Other-Settings)',
                attributes=['msDS-Other-Settings'])

    if conn.entries:
        ldap_signing_config = str(conn.entries[0]['msDS-Other-Settings'])
        if 'LDAPServerIntegrity' in ldap_signing_config:
            print('LDAP Signing jest włączony.')
        else:
            print('LDAP Signing nie jest włączony.')
    else:
        print('Nie znaleziono konfiguracji LDAP Signing.')

    conn.unbind()
