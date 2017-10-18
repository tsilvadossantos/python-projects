# Docker Garbage Collector

This project was developed to meet the following criteria:

Clean up docker images, containers, given a specific git branch.

The project was develop using the following:

1. Python 2.7.12

## Usage:

1. Create a folder inside your project named docker-clean
2. Inside the docker-clean folder, create two files: containers.docker and images.docker
3. In the containers.docker file, edit the template by providing container type and container name
4. In the images.docker file, edit the template by providing image type and image repository/name
5. Get help menu:
```
python docker-gc.py --help
```
6. Run script passing arguments:
```
python docker-gc.py --remove_containers=<type> --remove_images=<type> --branch=option

type: The types you created at steps 3 and 4 or 'None' for no action.
```
