#!/bin/env python

import os
import glob
import subprocess
import argparse
import sys
import fileinput
import shutil

__author__ = 'Thiago dos Santos'

"""Global Variables"""
repo_os_path = '/path/projectName/'
tomcat_projectName_path = '/path/tomcat-projectName/'
war_loc = tomcat_projectName_path+'webapps'

#artifactory base conf
artifacts_url = 'artifacts_content_url'
group_id = 'group_id'
extension = 'extension'
classifier = 'classifier'
extension_war = 'extension_war'
content_api = 'content_api'

list_comp = []
FNULL = open(os.devnull, 'w')

def getargs():
    """This function parses and return arguments"""
    parser = argparse.ArgumentParser(description='Build and Deploy projectName based on component version')
    parser.add_argument('--project1', type=str, help='projectName-project1 component version', required=True, nargs='+')
    args = parser.parse_args()
    project1_version = args.project1

    return project1_version

# Match return values from getargs()
project1_version = getargs()

"""Process management Func"""
def manage_process(action, process_name):
    subprocess.call([action, process_name], stdout=FNULL)
    subprocess.call(['sleep', '20'])

"""Remove war files"""
def rm_files(file_path):
    subprocess.call(['rm', '-rf', file_path])

def remove_wars():
    os.chdir(war_loc)
    files=glob.glob('*')
    for line in files:
        if line == 'host-manager' or line == 'manager' or line == 'ROOT':
            pass
        else:
            rm_files(line)

def download_war(comp_name, comp_version):
    if 'SNAPSHOT' in comp_version:
        repository_id = 'type1-s'
    else:
        repository_id = 'type2-r'

    artifacts_content_url = mount_url_here
    subprocess.call(['wget', artifacts_content_url, '-O', war_loc + '/' + comp_name  + '.' + extension_war], stdout=FNULL)
    subprocess.call(['sleep', '15'])

def deploy_projectName():
    if not os.path.isdir(war_loc):
        os.makedirs(war_loc)
    subprocess.call(['chown', '-R', 'tomcat:tomcat', war_loc])
    download_war('project1', project1_version[0])

manage_process('bash', tomcat_projectName_path+'bin/shutdown.sh')
remove_wars()
manage_process('bash', tomcat_projectName_path+'bin/startup.sh')

deploy_projectName()
