import subprocess

class SshHost(object):
    def ssh_instance(self, host, exec_comm):
        ssh_stdout = {}
        ssh = subprocess.Popen(["ssh", "%s" % host, exec_comm],
                               shell=False,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        stdout, stderr = ssh.communicate()
        ssh_stdout[host] = stdout.strip()
        return ssh_stdout
