import subprocess

class AwsClient(object):

    def __init__(self, profile, region, output='text'):
        self.profile = profile
        self.region = region
        self.output = output

    def get_instance_fqdn(self):
        ec2_instance = []
        try:
            output = subprocess.Popen(['aws', 'ec2', 'describe-instances', '--query', 'Reservations[*].Instances[*].[InstanceId]', '--filters', 'Name=instance-state-name,Values=running', '--profile', self.profile, '--region', self.region, '--output', self.output], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output.wait()
            for instance in output.stdout.readlines():
                instance_fqdn = instance.strip() + '.workdaysuv.com'
                ec2_instance.append(instance_fqdn)
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)

        if ec2_instance == []:
            return None
        else:
            return ec2_instance
