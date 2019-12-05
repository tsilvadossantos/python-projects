import subprocess

def ssh_instance(command, host):
        ssh_stdout = {}
        ssh = subprocess.Popen(['ssh', '-q', '-o', 'StrictHostKeyChecking=no', '%s' % host, command],
                               shell=False,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        stdout, stderr = ssh.communicate()
        ssh_stdout[host] = stdout.decode('utf-8'), stderr.decode('utf-8')
        return ssh_stdout


def scp_instance(src, dst, host):
        scp_stdout = {}
        scp = subprocess.Popen(["scp", src, "%s:%s" % (host, dst)],
                               shell=False,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        stdout, stderr = scp.communicate()
        scp_stdout[host] = src, dst
        return scp_stdout
