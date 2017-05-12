#!/usr/bin/python
import sys
import os
import salt.client
import requests
import re


"""
This piece of code updates the /etc/hosts of each minion (no-DNS scenario) + run salt mine-update
"""

"""
global Variables
"""
local = salt.client.LocalClient()
base_dir = '/domain/base-root-dir/'
base_file = 'hosts.generated'
target = '/etc/hosts'

"""
Get minions list sorted a-z by name
"""
def get_list_minions(minion):
   minions = []
   try:
       hosts = local.cmd(minion, 'test.ping', timeout=4)
       for i in hosts:
           minions.append(i)
           minions.sort()
       return minions
   except requests.ConnectionError, err:
       print err

"""
Get minions ip_addr
"""
def get_network_info(minion):
   try:
       returns = local.cmd_iter(minion, ['network.interface_ip','network.get_hostname',],[['eth0'],[],])
       return returns
   except requests.ConnectionError, err:
       print err

"""
write to file function
"""
def write_to_file(hosts_info, file_object):
    with open(file_object, 'a') as f:
        f.write(hosts_info + '\n')


"""
Loop through minion list extracting ip and hostname and writing to a file
"""
def generate_data():
    if os.path.isfile(base_dir + base_file):
        os.remove(base_dir + base_file)

    write_to_file("127.0.0.1 localhost", base_dir + base_file)
    net_info = {}
    hosts = get_list_minions('*')
    for i in hosts:
        net_info = get_network_info(i)
        for j in net_info:
            ip_addr =  j[i]['ret']['network.interface_ip']
            hname = j[i]['ret']['network.get_hostname']
        hosts_info = ip_addr + ' ' + hname
        write_to_file(hosts_info, base_dir + base_file)

"""
Send host file to /etc/hosts on minions
"""
def send_hosts_file():
    source = 'salt://' + base_file
    try:
        returns = local.cmd('*', 'cp.get_file', [source,target],verbose=False)
        return returns
    except requests.ConnectionError, err:
       print err

"""
Salt mine update to fix the ui bug - not getting upstream file from salt-master
"""
def salt_mine_func():
    try:
        returns = local.cmd_iter('*', ['mine.flush',],[[],])
        returns1 = local.cmd_iter('*', ['network.get_hostname',],[,[],])
        returns2 = local.cmd_iter('*', ['mine.send','network.get_hostname',],[[],[],])
        returns3 = local.cmd_iter('*', ['mine.update',],[[],])
        return returns, returns1, returns2, returns2, returns3
    except requests.ConnectionError, err:
        print err

"""
main_func defined
"""
def main():
    get_network_info('None')
    generate_data()
    send_hosts_file()
    salt_mine_func()

if __name__ == '__main__':
    main()
