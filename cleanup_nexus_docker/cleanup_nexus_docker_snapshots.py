import subprocess
from requests.auth import HTTPBasicAuth
import json
import requests
import sys
import re

def get_images_catalog():
    """Get catalog from Nexus3: https://NEXUSURL/repository/docker/v2/_catalog"""

    img_catalog_url = 'https://NEXUSURL/repository/docker/v2/_catalog'
    r = requests.get(img_catalog_url, auth=HTTPBasicAuth('USER', 'PASSWORD'))
    catalog_data = json.loads(r.text)
    return catalog_data['repositories']

def filter_images_by_tag(repo_name):
    cached_snapshots = []
    cached_rcs = []
    try:
        output = subprocess.Popen(['/usr/bin/nexus-cli', 'image', 'tags', '-name', repo_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output.wait()
        for line in output.stdout.readlines():
            if 'There are' not in line:
                if 'SNAPSHOT' in line:
                    cached_snapshots.append(line.strip())
                else:
                    cached_rcs.append(line.strip())
        delete_snapshot_images(repo_name, cached_snapshots)
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)

def delete_snapshot_images(repo_name, cached_tag):
    repo_catalog = {}
    repo_catalog[repo_name] = cached_tag
    for img_name in repo_catalog.values():
        if len(img_name) > 0:
            for tag in img_name:
                subprocess.call(['/usr/bin/nexus-cli', 'image', 'delete', '-name', repo_name, '-tag', tag])

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filter_images_by_tag(sys.argv[1])
    else:
        for repo in get_images_catalog():
            filter_images_by_tag(repo)
