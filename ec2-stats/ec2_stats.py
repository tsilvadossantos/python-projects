__author__ = 'Thiago dos Santos'
__email__ = 'thiago.santos@workday.com'

from core.Args import GetArgs
from core.AwsClient import AwsClient
from core.HostInfo import disk_usage_pct
from core.Csv import Csv
from core.Chart import Chart
from multiprocessing import Pool
import time

if __name__ == '__main__':
    start = time.time()

    #get the cli arguments
    cli_args = GetArgs()
    arg1, arg2, arg3 = cli_args.get_args()
    region, profile, chart_gen = arg1[0], arg2[0], arg3[0]

    # #Obtain List of Instances
    instance_id = AwsClient(profile, region)
    running_instances = instance_id.get_instance_fqdn()

    if running_instances != None:
        #Ssh to list of instances
        p = Pool(20)
        instance_info = p.map(disk_usage_pct, running_instances)

        # #Write to File (CSV Format)
        csv_file_path = '/Users/thiago.santos/workspace/python/ec2-stats/data'
        csv = Csv(instance_info, region)
        csv.write_file_csv_format(csv_file_path)

        if chart_gen == 'yes':
            total_instances = len(running_instances)
            c = Chart(csv_file_path, region, 'bar')
            c.set_chart('Label')
            title = 'Disk Usage (%) - {} {} Total EC2 Running Instances: {}'.format(region, '\n', total_instances)
            c.set_title(title)
            c.plot_chart()
    else:
        print 'There are no running instances in {}'.format(region)

    end = time.time()
    print(end - start)
