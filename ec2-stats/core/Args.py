import argparse

class GetArgs(object):
    """Get command line arguments"""
    def __init__(self):
        parser = argparse.ArgumentParser(description='Get EC2 Instance Details')
        parser.add_argument('--region', type=str, help='aws region', nargs='+')
        parser.add_argument('--profile', type=str, help='account profile', nargs='+')
        parser.add_argument('--chart', type=str, default = 'no', help='generate and save chart - defaul is no', nargs='+')
        self.args = parser.parse_args()
        self.r = self.args.region
        self.p = self.args.profile
        self.c = self.args.chart

    def get_args(self):
        return self.r, self.p, self.c
