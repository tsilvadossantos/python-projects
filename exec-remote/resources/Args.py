import argparse

def getargs():
    parser = argparse.ArgumentParser(description='Run Command on List of Hosts')
    parser.add_argument('--command', type=str, help='Run Command on Remote Host', required=False, nargs='+')
    parser.add_argument('--scpfile', type=str, help='SCP file to Remote Host', required=False, nargs='+')
    parser.add_argument('--hostpath', type=str, help='Destination host path to SCP', required=False, nargs='+')
    parser.add_argument('--hostlist', type=str, help='Path to file with hostname list', required=False, nargs='+')
    parser.add_argument('--printusage', type=str, help='Option: yes - Print usage examples', default='yes', required=False, nargs='+')

    args = parser.parse_args()

    return args.command, args.scpfile, args.hostpath, args.hostlist, args.printusage
