import subprocess
from .SSH import ssh_instance, scp_instance
from .File import write_to_file

def run_command(command, host):
    ssh_stdout_dict = ssh_instance(command, host)
    for host, output in ssh_stdout_dict.items():
        stdout = output[0].strip()
        stderr = output[1].strip()
        report = ('%s, %s, %s %s' %(host, stdout, stderr, '\n'))
        print(report.strip())
        write_to_file('report.out', report, 'a')

def copy_file(src, dst, host):
    scp_stdout_dict = scp_instance(src, dst, host)
    for host, output in scp_stdout_dict.items():
        stdout = output[0].strip()
        stderr = output[1].strip()
        report = ('%s, %s, %s - %s %s' %(host, stdout, stderr, 'completed', '\n'))
        print(report.strip())
        write_to_file('report.out', report, 'a')
