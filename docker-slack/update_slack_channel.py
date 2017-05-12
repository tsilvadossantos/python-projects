#!/bin/env python

from slacker import Slacker
import os.path
import docker
import socket

def send_post_message():
    HOST_NAME= socket.gethostname()
    client = docker.from_env()
    slack = Slacker('TOKEN')

    for container in client.containers.list():
        #Obtain containers status
        slackMessage = '[{}] *{:40}* `{}` *{}*'.format(HOST_NAME, container.attrs['Config']['Image'], 'Status:', container.status)
        #Post the message to slack
        slack.chat.post_message('#CHANNEL-NAME', slackMessage)

if __name__ == "__main__":
    send_post_message()
