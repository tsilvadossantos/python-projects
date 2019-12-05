class AwsInstance(object):

    def __init__(self, json_load=None):
        if json_load != None:
            self.json_load = json_load

    def get_ec2_info_from_file(self):
        self.ec2_instance_info = {}
        for item in xrange(0, len(self.json_load['Reservations']), 1):
            instances_info = self.json_load['Reservations'][item]['Instances']
            for instance in xrange(0, len(instances_info), 1):
                instance_id = self.json_load['Reservations'][item]['Instances'][instance]['InstanceId']
                instance_type = self.json_load['Reservations'][item]['Instances'][instance]['InstanceType']
                instance_state = self.json_load['Reservations'][item]['Instances'][instance]['State']['Name']
                self.ec2_instance_info[instance_id] = [instance_type, instance_state]
        return self.ec2_instance_info

    # def get_ec2_info_from_aws(self, filepath, region):
    #     try:
    #         output = subprocess.Popen(['aws', 'ec2', 'describe-instances', '--region', region, '--output', 'json', '--profile', 'devqa'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #         output.wait()
    #         f = File(filepath + '/' + region)
    #         for line in output.stdout.readlines():
    #             f.write_to_file(line.strip(), 'w')
    #             self.get_image_id()
    #     except IOError as e:
    #         print "I/O error({0}): {1}".format(e.errno, e.strerror)
