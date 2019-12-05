from core.SshHost import SshHost

def disk_usage_pct(ec2_instance):
    disk_usage_pct='df --output=pcent /data | awk "NR > 1 {print $1}" | sed "s/%//"'
    sh = SshHost()
    disk_usage = sh.ssh_instance(ec2_instance, disk_usage_pct)
    return disk_usage
