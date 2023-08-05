#-*- coding: utf-8 -*-

from subprocess32 import call

# Script para los logs
import logging

import pexpect

from instaladorapt import instalador

def crearRol2(rol, password):
    """
    Función alternativa a la mierda de popen, threads y la hostia en verso de subprocess32
    """
    print("Creando rol %s ...", % rol)
    hijo = pexpect.spawn("su - postgres -c 'createuser --createdb --username postgres --no-createrole --no-superuser --pwprompt "+rol+"'")
    hijo.expect('Enter password for new role:')
    hijo.sendline(password)
    hijo.expect('Enter it again:')
    hijo.sendline(password)
    


def instalaPostgres(log_file):
    """
    Instala postgresql. 
    """

    print("""       Instalando postgresql
            ----------------------------------------""")

    instalador('postgresql')
    # call(['apt-get', 'install', 'postgresql', '-y'],  stderr=log_file)


def main():
    pass_del_rol_postgres = 'ubuntu'
    path, archivo = logging.logSettings(filename="test_postgres.txt")
    # instalaPostgres(archivo)
    crearRol2(password='ubuntu')

if __name__ == '__main__':
    main()
