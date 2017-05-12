#!/bin/env python

import argparse
import subprocess
import os

"""Global Variables"""
dockeruser = 'DOCKERHUB USERNAME'
dockerpassword = 'DOCKERHUB PASSWORD'
registryurl = 'https://index.docker.io/v1/'
FNULL = open(os.devnull, 'w')
git_command = '/usr/bin/git'
repo_os_path = 'PATH'
repo_credential = 'REPO_CREDENTIAL'
repo_url = 'REPO_URL'
repo_full_url = 'https://' + repo_credential + repo_url
comp_env_list = ['NODE1', 'NODE2']

def getargs():
    """This function parses and return arguments"""
    parser = argparse.ArgumentParser(description='Build and Deploy EDDIE based on component version')
    parser.add_argument('--node1', type=str, help='node1 version', required=True, nargs='+')
    parser.add_argument('--node2', type=str, help='node2 version', required=True, nargs='+')

    args = parser.parse_args()
    node1_version = args.node1
    node2_version = args.node2

    return node1_version, node2_version

"""Git clone"""
def git_func(git_par, repo_os_path):
    if not os.path.exists(repo_os_path):
        os.makedirs(repo_os_path)
    os.chdir(repo_os_path)
    subprocess.call([git_command, git_par, repo_full_url], stdout=FNULL)

def get_comp_version():
    """create a dict from comp_env_list and getargs() list and update key, value in .env file"""
    os.chdir('PROJECT-PATH')
    env_path = '.env'
    env_path_temp = 'env_temp'
    node1_version, node2_version = getargs()
    with open(env_path, 'r') as r:
         with open(env_path_temp, 'w') as a:
             for line in r:
                 for k, v in dict(zip(comp_env_list, getargs())).iteritems():
                     if k in line:
                         a.write(str(k)+'='+str(v)[1:-1].split("'")[1] + '\n')
                         break
                 else:
                     a.write(line)
    os.rename('env_path', '.env')

def docker_login():
    subprocess.call(['docker', 'login', '--username='+dockeruser, '--password='+dockerpassword, registryurl])

def docker_compose_up():
    docker_login()
    os.chdir('PROJECT-PATH')
    subprocess.call(['docker-compose', '-f', 'docker-compose-nodes.yml', 'down', '-v', '--remove-orphans', '--rmi', 'local'])
    subprocess.call(['docker-compose', '-f', 'docker-compose-nodes.yml', 'pull'])
    subprocess.call(['docker-compose', '-f', 'docker-compose-nodes.yml', 'up', '-d'])

if __name__ == '__main__':
    git_func('clone', repo_os_path)
    get_comp_version()
    docker_compose_up()
