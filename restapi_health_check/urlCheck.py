from requests.exceptions import ConnectionError
import sys
import requests
import os
import socket
import re
from slacker import Slacker
import os.path
import time

__author__ = "Thiago Santos"

class File:
    def __init__(self):
        self.hostname = socket.gethostname()
        self.origFile = 'urls.txt'
        self.pattern = 'localhost'

    def read_file(self):
        file_line = []
        with open(self.origFile, "r") as r:
            for line in r:
                file_line.append(str(line.strip()))
        return file_line

    def get_api_url(self):
        new_list = []
        for line in self.read_file():
            if self.pattern in line:
                new_list.append(re.sub(r'\b{}\b'.format(self.pattern), self.hostname, line))
            else:
                new_list.append(line)
        return new_list

    def verify_list_size(self):
        if len(self.read_file()) == len(self.get_api_url()):
            return len(self.read_file())
        else:
            return '{}'.format('List of Urls does not match all lines in urls.txt file')

class RestApi(File):
    def __init__(self):
        pass

    def get_api_response(self):
        f = File()
        api_response_datastruct = {}
        for line in f.get_api_url():
            line = str(line.strip())
            url, comp = line.split(' ')
            try:
                r = requests.get(url)
                slack_msg_format = '{},{},{}'.format(comp, url, r.status_code)
                api_response_datastruct[comp] = slack_msg_format
            except ConnectionError as err:
                print '{}'.format(100*'=')
                print 'Waiting for {}'.format(url)
        return api_response_datastruct

    def validate_api_response(self):
        f = File()
        total_response = len(self.get_api_response())
        while f.verify_list_size() is not total_response:
            self.get_api_response()
            total_response = len(self.get_api_response())
            time.sleep(15)

class Jenkins:
    def __init__(self):
        pass

    def print_to_console(self):
        p = RestApi()
        for v in p.get_api_response().values():
            #value format: admin1,http://qa06.xcl.ie:19701/admin/metrics/index.html,200
            comp, url, status_code = v.split(',')
            if status_code == "200" or status_code == "401":
                print '{} {} ==> {}'.format('Check Succeeds', url, status_code)
            elif status_code == "503":
                #Get api response code
                r = RestApi()
                r.validate_api_response()
            else:
                print '{} {} ==> {}'.format('Check failed', url, status_code)

class Slack:
    def __init__(self):
        pass

    def slack_token(self):
        return Slacker('xoxp-23051919203-28858890404-28863758500-4891c1b716')

    def post_to_slack(self):
        p = RestApi()
        channel_name = sys.argv[1]
        for v in p.get_api_response().values():
            #value format: admin1,http://qa06.xcl.ie:19701/admin/metrics/index.html,200
            comp, url, status_code = v.split(',')
            slack_msg_format = '*[{}]* {} *{}* ==> `{}`'.format(comp, url, 'Status Code', status_code)
            slack = self.slack_token()
            slack.chat.post_message('#' + channel_name, slack_msg_format)

if __name__ == "__main__":
    #Get api response code
    r = RestApi()
    r.validate_api_response()

    #print output to Jenkins
    j = Jenkins()
    j.print_to_console()

    #Post to slack
    p = Slack()
    p.post_to_slack()
