# Docker Garbage Collector

This project was developed to meet the following criteria:

Clean up docker images, containers and volumes, given a specific git branch.

The project was develop using the following:

1. Python 2.7.12

## Usage:

1. Create a folder inside your project named docker-clean
2. Inside the docker-clean folder, create two files: containers.docker and images.docker
3. In the containers.docker file, edit the template by providing container type and container name
4. In the images.docker file, edit the template by providing image type and image repository/name
5. Create a file named docker-gc.py and Instantiate the classes as needed, here an example:

```
#!/bin/env python

import dockergc

if __name__ == "__main__":
    #Instantiate the GetArgs() class
    cli_args = dockergc.GetArgs()
    remove_image_ret, remove_containers_ret, branch_version = cli_args.getargs()

    #Instantiate Git
    if branch_version[0] != 'None':
        gitc = dockergc.Git(branch_version[0], 'ABSOLUTE_PATH_TO_REPO')
        gitc.git_clone()

    #Manage containers
    if remove_containers_ret[0] != 'None':
        container = dockergc.Container(remove_containers_ret[0], 'ABSOLUTE_PATH_TO/containers.docker')
        container.fetch_containers()
        container.docker_remove_containers()

    #Manage images
    if remove_image_ret[0] != 'None':
        image = dockergc.Image(remove_image_ret[0], 'ABSOLUTE_PATH_TO/images.docker')
        image.fetch_images()
        image.docker_remove_images()
```

6. Get help menu:
```
python docker-gc.py --help
```

7. Run script passing arguments:
```
python docker-gc.py --remove_containers=<type> --remove_images=<type> --branch=option

type: The types you created at steps 3 and 4 or 'None' for no action.
```
