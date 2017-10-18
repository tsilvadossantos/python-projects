#!/bin/env python

import argparse
import subprocess
import os

__author__ = "Thiago Santos"

class GetArgs:
    def getargs(self):
        """This function parses and return arguments"""
        parser = argparse.ArgumentParser(description='Manage image and containers')
        parser.add_argument('--remove_containers', type=str, help='remove containers < specify TYPE>', required=True, nargs='+')
        parser.add_argument('--remove_images', type=str, help='remove images <specify TYPE>', required=True, nargs='+')
        parser.add_argument('--branch', type=str, help='checkout branch', required=True, nargs='+')
        self.args = parser.parse_args()
        self.remove_image_ret = self.args.remove_images
        self.remove_containers_ret = self.args.remove_containers
        self.branch_version = self.args.branch
        return self.remove_image_ret, self.remove_containers_ret, self.branch_version

class Git:
    """Git clone"""
    def __init__(self, git_par, branch, repo_os_path):
        self.branch = branch
        self.FNULL = open(os.devnull, 'w')
        self.git_command = '/usr/bin/git'
        self.repo_os_path = repo_os_path
        self.repo_credential = '<repo_credential>'
        self.repo_url = '<repo_url>'
        self.repo_full_url = 'https://' + self.repo_credential + self.repo_url

    def git_clone(self):
        subprocess.call(['rm', '-rf', self.repo_os_path])
        if not os.path.exists(self.repo_os_path):
            os.makedirs(self.repo_os_path)
        os.chdir(self.repo_os_path)
        subprocess.call([self.git_command, 'clone', self.repo_full_url], stdout=self.FNULL)
        os.chdir(self.repo_os_path)
        subprocess.call([self.git_command, 'checkout', '-f', self.branch], stdout=self.FNULL)

class Image:
    """ Read the file with the image names """
    def __init__(self, parameter, images_list_path):
        self.parameter = parameter
        self.imageid_list = []
        self.images_list_path = images_list_path

    def fetch_images(self):
        with open(self.images_list_path, 'r') as f:
            for line in f:
                app_type, image_name = line.strip().split(' ')
                if self.parameter == 'all':
                    self.get_image_name(image_name)
                elif self.parameter == app_type:
                    self.get_image_name(image_name)

    def get_image_name(self, target):
        """ Obtain docker image name """
        try:
            output = subprocess.Popen(['docker', 'images', '--format', '{{.Repository}}', target], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output.wait()
            for line in output.stdout.readlines():
                self.get_image_id(line.strip())
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)

    def get_image_id(self, imageid):
        """ Obtain docker image ID """
        output = subprocess.Popen(['docker', 'images', '--format', '{{.ID}}', imageid], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output.wait()
        for line in output.stdout.readlines():
            self.imageid_list.append(line.strip())
        return self.imageid_list

    def docker_remove_images(self):
        for line in self.imageid_list:
            subprocess.call(['docker', 'rmi', '-f', line])

class Container(object):
    def __init__(self, parameter, container_list_path):
        self.parameter = parameter
        self.container_dict = {}
        self.container_list_path = container_list_path

    def fetch_containers(self):
        """ Read the file with the container names """
        with open(self.container_list_path, 'r') as f:
            for line in f:
                app_type, container_name = line.strip().split(' ')
                if self.parameter == 'all':
                    self.container_dict[self.get_container_id(container_name)] = container_name
                elif self.parameter == app_type:
                    self.container_dict[self.get_container_id(container_name)] = container_name
            return self.container_dict

    def get_container_id(self, container_name):
        """ Obtain docker container ID """
        try:
            output = subprocess.Popen(['docker', 'ps', '-a', '--format', '{{.ID}}', '--filter', 'name='+container_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output.wait()
            for line in output.stdout.readlines():
                return line.strip()
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)

    def docker_remove_containers(self):
        #Inspect volumes while running
        vol = Volume()
        vol.docker_inspect_volumes(self.container_dict)

        for k in self.container_dict.keys():
            if k:
                subprocess.call(['docker', 'stop', k])
                subprocess.call(['docker', 'rm', k])

        #Remove volumes after removing containers
        vol.docker_remove_volumes()

class Volume(Container):
    def __init__(self):
        self.volume_dict = {}

    def docker_inspect_volumes(self, container_dict):
        for container_id in container_dict.keys():
            if container_id is not None:
                output = subprocess.Popen(['docker', 'inspect', '--format', '{{range .Mounts}} {{.Name}}{{end}}', container_id], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output.wait()
                for volume_name in output.stdout.readlines():
                    volume_name = volume_name.strip()
                    self.volume_dict[container_id] = volume_name
        return self.volume_dict

    def docker_remove_volumes(self):
        temp_list = []
        for container_id, volume_name in self.volume_dict.iteritems():
            if volume_name:
                temp_list = volume_name.split(' ')
                for item in temp_list:
                    subprocess.call(['docker', 'volume', 'rm', item])
