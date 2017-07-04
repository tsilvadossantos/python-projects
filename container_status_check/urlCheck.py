import requests
import os
import socket
import re
from slacker import Slacker
import os.path
import docker

__author__ = "Thiago Santos"

hostname = socket.gethostname()
origFile = '/path/to/file/urls.txt'
tempFile = '/path/to/file/url.tmp'
pattern = 'localhost'

def add_hostname_to_url():
    with open(origFile, "r") as r:
        with open(tempFile, "w") as a:
            for line in r:
                if pattern in line:
                    a.write(re.sub(r'\b{}\b'.format(pattern), hostname, line))
                else:
                    a.write(line)
    os.remove(origFile)
    os.rename(tempFile, origFile)

def check_status_code():
    with open(origFile, "r") as r:
        for line in r:
            line = str(line.strip())
            url, comp = line.split(' ')
            r = requests.get(url)
            post_to_slack('*[{}]* {} *{}* ==> `{}`'.format(comp, url, 'Status Code', r.status_code))
            if r.status_code == 200 or r.status_code == 401:
                print '{} {} ==> {}'.format('Check Succeeds', url, r.status_code)
            else:
                print '{} {} ==> {}'.format('Check failed', url, r.status_code)


def post_to_slack(slackMessage):
        slack = Slacker('SLACK-TOKEN')
        slack.chat.post_message('#channel', slackMessage)

if __name__ == "__main__":
    add_hostname_to_url()
    check_status_code()
