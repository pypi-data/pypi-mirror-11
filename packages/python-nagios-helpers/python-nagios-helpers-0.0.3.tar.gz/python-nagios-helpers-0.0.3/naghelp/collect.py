# -*- coding: utf-8 -*-
'''
Création : July 7th, 2015

@author: Eric Lapouyade
'''

import telnetlib
import re
import socket

__all__ = ['search_invalid_port', 'telnet_cmd', 'ssh_cmd']

def search_invalid_port(ip,ports):
    """Returns the first invalid port encountered or None if all are reachable"""
    if isinstance(ports, basestring):
        ports = [ int(n) for n in ports.split(',') ]
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ip, port))
            s.close()
        except:
            return port
    return None

def telnet_cmd(cmd, host,user,password,port=0,timeout=10):
    try:
        is_connected = False
        tn = telnetlib.Telnet(host,port,timeout)
        is_connected = True
        tn.expect([re.compile(r'login\s*:\s+',re.I),])
        tn.write(user + "\n")
        tn.expect([re.compile(r'Password\s*:\s+',re.I),])
        tn.write(password + "\n")
        tn.expect([re.compile(r'[\$#>\]:]'),])
        tn.write("echo; echo '____BEGIN_TELNETLIB____'; %s; echo '____END_TELNETLIB____'\n" % cmd)
        tn.write("exit\n")
        buffer = tn.read_all()

        out = ''
        flag = False
        for l in buffer.splitlines():
            ls = l.strip()
            if ls == '____BEGIN_TELNETLIB____':
                flag = True
            elif ls == '____END_TELNETLIB____':
                flag = False
            elif flag:
                out += l + '\n'

        out = out[:-1]
    except Exception,e:
        if not is_connected:
            raise Exception('Unable to connect to host')
        raise Exception('Bad login/password')
    return out

def ssh_cmd(cmd, host, user, timeout=10, **kwargs):
    import spur
    if isinstance(cmd, basestring):
        cmd = cmd.split(' ')
    shell = spur.SshShell(hostname=host, username=user, connect_timeout=timeout, **kwargs)
    with shell:
        result = shell.run(cmd)
    return result.output
