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
repo_os_path = '/opt/projname/'
tomcat_projname_path = '/opt/tomcat-projname/'
war_loc = tomcat_projname_path+'webapps/'
repo_url = 'REPO_PATH'
git_command = '/usr/bin/git'
projname_comp_dict = {}
dict_data = {}
FNULL = open(os.devnull, 'w')

def getargs():
    """This function parses and return arguments"""
    parser = argparse.ArgumentParser(description='Build and Deploy projname')
    parser.add_argument('-P', '--process', type=str, help='process to be restarted E.G.: java,dse', required=True)
    parser.add_argument('-BR1', '--branch1', type=str, help='first set of branches', required=True, nargs='+')
    parser.add_argument('-COMP1', '--components1', type=str, help='projname components using BR1', required=True, nargs='+')
    args = parser.parse_args()
    process = args.process
    branch1 = args.branch1
    components1 = args.components1[0].split(',')

    return process, branch1, components1

"""Process management Func"""
def manage_process(action, process_name):
    subprocess.call([action, process_name], stdout=FNULL)
    subprocess.call(['sleep', '20'])

"""Remove war files"""
def rm_files(file_path):
    subprocess.call(['rm', '-rf', file_path])

"""Git clone"""
def git_clone(git_par, git_branch):
    if not os.path.exists(repo_os_path):
        os.makedirs(repo_os_path)
    os.chdir(repo_os_path)
    subprocess.call([git_command, git_par, repo_url+git_branch], stdout=FNULL)

"""Git rebase, and checkout"""
def git_mng(git_par1, git_par2,folder_name):
    os.chdir(repo_os_path+folder_name)
    subprocess.call([git_command, git_par1, git_par2])

"""Git clone"""
def git_pull(git_par1, git_par2, folder_name):
    os.chdir(repo_os_path+folder_name)
    subprocess.call([git_command, git_par1, git_par2], stdout=FNULL)

"""Replace gradle properties file to fix url"""
def rep_file(filename, folder_name):
    os.chdir(repo_os_path+folder_name)
    for line in fileinput.input(filename, inplace = 1):
        print line.replace("artifactory.domain", "artifactory.domain1")

"""Build projname"""
def build_projname(comp_flag):
    print 'Building ' +comp_flag+ ' with gradle'
    f = open(repo_os_path+comp_flag+'/build_output', 'w+')
    if (comp_flag == 'projname-shared'):
        subprocess.call([repo_os_path+comp_flag+'/gradlew', 'clean', 'jar', 'publishToMavenLocal'], stdout=f)
        for output in f:
            if 'BUILD SUCCESSFUL' in f:
                pass
            if 'BUILD FAILED' in f:
                print comp_flag + "failed to build"
                exit(1)
    else:
        subprocess.call([repo_os_path+comp_flag+'/gradlew', 'clean', 'war', '-x', 'test'], stdout=f)
        for output in f:
            if 'BUILD SUCCESSFUL' in f:
                pass
            if 'BUILD FAILED' in f:
                print comp_flag + "failed to build"
                exit(1)

"""Locate wars"""
def find_war(comp_flag, war_loc):
    if comp_flag == 'projname-shared':
        dict_data[comp_flag] = comp_flag
    else:
        if  comp_flag == 'projname-softwarename':
            new_comp = comp_flag.split('-')
            replaced_file = new_comp[1]+'-'+new_comp[2]+'.war'

        else:
            new_comp = comp_flag.split('-')
            replaced_file = new_comp[1]+'.war'

        subprocess.Popen(('find', repo_os_path+comp_flag, '-name', '*.war', '-execdir', 'mv', '{}', replaced_file, ';'))
        subprocess.call(['sleep', '10'])
        dict_data[comp_flag] = subprocess.check_output(['find', repo_os_path+comp_flag, '-name', '*.war'])
    #update main dict
    projname_comp_dict.update(dict_data)

    return projname_comp_dict[comp_flag]

def remove_wars():
    print "Removing wars at " + war_loc
    os.chdir(war_loc)
    files=glob.glob('*')
    for line in files:
        if line == 'host-manager' or line == 'manager' or line == 'ROOT':
            pass
        else:
            rm_files(line)

    print "Removing wars at " + war_loc_bpapi
    os.chdir(war_loc_bpapi)
    files=glob.glob('b*')
    for line in files:
        rm_files(line)

def deploy_projname():
    if not os.path.isdir(war_loc):
        os.makedirs(war_loc)
    subprocess.call(['chown', '-R', 'tomcat:tomcat', war_loc])
    print 'Deploying projname ..'
    clean_dict = {key.strip(): item.strip() for key, item in projname_comp_dict.items()}
    new_dict = {key.strip(): item.split('/') for key, item in clean_dict.items()}

    if len(clean_dict) < 1:
        print "You need at least 1 components in order to deploy projname:", projname_comp_dict.keys()
    else:
        if 'projname-softwarename' in clean_dict and not os.path.isfile(new_dict['projname-softwarename'][6]):
            print 'projname-softwarename'
            subprocess.call(['sleep', '120'])
            shutil.copy(clean_dict['projname-softwarename'], war_loc)

# Match return values from getargs()
process, branch1 = getargs()

#Interact with components to build projname
for comp_list in components1:
    #remove existing repo from file system
    rm_files(repo_os_path+comp_list)

    git_clone('clone', comp_list)
    git_mng('checkout', branch1[0], comp_list)
    git_pull('pull','-f', comp_list)

    #Replace artifactory url
    rep_file('gradle.properties', comp_list)
    rep_file('build.gradle', comp_list)

    #build war/jar
    build_projname(comp_list)
    find_war(comp_list,tomcat_projname_path+'webapps/')


for comp_list in components2:
    #remove existing repo from file system
    rm_files(repo_os_path+comp_list)

    #git stuff
    git_clone('clone', comp_list)
    git_mng('checkout',branch2[0], comp_list)
    git_pull('pull','-f', comp_list)

    #Replace artifactory url
    rep_file('gradle.properties', comp_list)
    rep_file('build.gradle', comp_list)

    #build war/jar
    build_projname(comp_list)
    find_war(comp_list,tomcat_projname_path+'webapps/')

manage_process('bash', tomcat_projname_path+'bin/shutdown.sh')
manage_process('pkill', process)
remove_wars()
manage_process('bash', tomcat_projname_path+'bin/startup.sh')

deploy_projname()
