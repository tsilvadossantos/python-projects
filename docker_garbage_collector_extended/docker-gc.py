#!/bin/env python

import dockergc

if __name__ == "__main__":
    #Instantiate the GetArgs() class
    cli_args = dockergc.GetArgs()
    remove_image_ret, remove_containers_ret, branch_version = cli_args.getargs()

    #Instantiate Git
    if branch_version[0] != 'None':
        gitc = dockergc.Git(branch_version[0], '</PATH/TO/BRANCH>')
        gitc.git_clone()

    #Manage containers
    if remove_containers_ret[0] != 'None':
        container = dockergc.Container(remove_containers_ret[0], '/PATH/TO/containers.docker')
        container.fetch_containers()
        container.docker_remove_containers()

    #Manage images
    if remove_image_ret[0] != 'None':
        image = dockergc.Image(remove_image_ret[0], '/PATH/TO/images.docker')
        image.fetch_images()
        image.docker_remove_images()
