import csv
from core.File import File

class Csv(object):

    def __init__(self, raw_data, region):
        self.raw_data = raw_data
        self.region = region

    def write_file_csv_format(self, path_to_file=None):
        if path_to_file != None:
            csv_file = path_to_file + '/' + self.region + '.csv'
        else:
            csv_file = self.region + '.csv'
        csv_columns = '{},{},{},{}'.format('Instance ID', 'Disk-Usage-Pct', 'Region', 'Label')
        f = File(csv_file)
        f.write_to_file(csv_columns, 'w')
        for d in self.raw_data:
            for k, v in d.iteritems():
                if v != '':
                    #Generate Label Range (0-10, 10-20, up to 90-100)
                    for r in xrange(0, 100, 10):
                        if r <= int(v) < r + 10:
                            r_start = str(r)
                            r_end_int = r + 10
                            r_end = str(r_end_int)
                            label = r_start + '-' + r_end
                            csv_instance = '{},{},{},{}'.format(k, v, self.region, label)
                            f.write_to_file(csv_instance, 'a')
