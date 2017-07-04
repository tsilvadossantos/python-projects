#!/bin/env python

import argparse
import subprocess
import os

FNULL = open(os.devnull, 'w')
git_command = '/usr/bin/git'
repo_os_path = '/BASEDIR'
repo_credential = 'repo_credential'
repo_url = 'repo_url'
repo_full_url = 'https://' + repo_credential + repo_url

def getargs():
    """This function parses and return arguments"""
    parser = argparse.ArgumentParser(description='Manage image and containers')
    parser.add_argument('--remove_containers', type=str, help='remove containers component/third-party/all', required=True, nargs='+')
    parser.add_argument('--remove_images', type=str, help='remove images component/third-party/all', required=True, nargs='+')
    parser.add_argument('--branch', type=str, help='checkout branch', required=True, nargs='+')
    args = parser.parse_args()
    remove_image_ret = args.remove_images
    remove_containers_ret = args.remove_containers
    branch_version = args.branch
    return remove_image_ret, remove_containers_ret, branch_version

"""Git clone"""
def git_func(git_par, repo_os_path, branch):
    subprocess.call(['rm', '-rf', repo_os_path + '/path-to-script'])
    if not os.path.exists(repo_os_path):
        os.makedirs(repo_os_path)
    os.chdir(repo_os_path)
    subprocess.call([git_command, git_par, repo_full_url], stdout=FNULL)
    os.chdir(repo_os_path+'/path-to-script')
    subprocess.call([git_command, 'checkout', '-f', branch], stdout=FNULL)

def manage_images(parameter, command):
    """ Read the file with the image names """
    with open('/BASEDIR/path-to-script/docker-clean/images.docker', 'r') as f:
        for line in f:
            app_type, image_name = line.strip().split(' ')
            if parameter == 'all':
                get_image_name(image_name, command)
            elif parameter == app_type:
                get_image_name(image_name, command)

def manage_containers(parameter, command):
    """ Read the file with the container names """
    with open('/BASEDIR/path-to-script/docker-clean/containers.docker', 'r') as f:
        for line in f:
            app_type, container_name = line.strip().split(' ')
            if parameter == 'all':
                get_container_id(container_name)
            elif parameter == app_type:
                get_container_id(container_name)

def get_container_id(container_name):
    """ Obtain docker container name """
    try:
        output = subprocess.Popen(['docker', 'ps', '-a', '--format', '{{.ID}}', '--filter', 'name='+container_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output.wait()
        for line in output.stdout.readlines():
            docker_remove_container(line.strip())
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)

def get_image_name(target, command):
    """ Obtain docker image name """
    try:
        output = subprocess.Popen(['docker', command, '--format', '{{.Repository}}', target], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output.wait()
        for line in output.stdout.readlines():
            get_docker_id(line.strip(), command)
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)

def get_docker_id(target, command):
    """ Obtain docker container/image ID """
    output = subprocess.Popen(['docker', command, '--format', '{{.ID}}', target], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output.wait()
    for line in output.stdout.readlines():
        docker_remove_image(line.strip())

def docker_remove_image(image_tag):
    subprocess.call(['docker', 'rmi', '-f', image_tag])

def docker_remove_container(container_name):
    subprocess.call(['docker', 'stop', container_name])
    subprocess.call(['docker', 'rm', container_name])

if __name__ == "__main__":
    remove_image_ret, remove_containers_ret, branch_version = getargs()

    git_func('clone', repo_os_path, branch_version[0])

    #provide parameter to manage containers
    if remove_containers_ret is not 'None':
        manage_containers(remove_containers_ret[0], 'ps')

    #provice parameter to manage images
    if remove_image_ret is not 'None':
        manage_images(remove_image_ret[0], 'images')
