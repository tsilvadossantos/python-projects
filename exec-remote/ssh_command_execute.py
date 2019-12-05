__author__ = 'Thiago dos Santos'
__email__ = 'thiago.santos@workday.com'

import time
import sys
from resources.Args import getargs
from multiprocessing.dummy import Pool as ThreadPool
from resources.File import read_file
from resources.Command import run_command, copy_file
from resources.Usage import printusage

def my_threading(func_name, args_list):
    pool = ThreadPool(30)
    pool.starmap(func_name, args_list)
    pool.close()
    pool.join()

def verify_input():
    user_input = None
    while user_input not in ('yes', 'no'):
        user_input = input('Confirm yes/no: ')
        if user_input == 'yes':
            continue
        elif user_input == "no":
            sys.exit(0)
        else:
            print("Please enter yes or no.")

if __name__ == '__main__':
    start = time.time()

    command, scpfile, hostpath, hostlist, usage = getargs()

    if usage[0] == 'yes':
        printusage()
    elif command != None and hostlist != None:
        verify_input()
        instance_list = read_file(hostlist[0])
        command_list = [command[0],] * len(instance_list)
        zipped_args_list = zip(command_list, instance_list)
        my_threading(run_command, zipped_args_list)
        print('Number of hosts: %d' % (len(instance_list)))
        print('Check report.out file for the full report of this run')
    elif scpfile != None and hostpath != None:
        verify_input()
        instance_list = read_file(hostlist[0])
        scpfile_list = [scpfile[0],] * len(instance_list)
        hostpath_list = [hostpath[0],] * len(instance_list)
        zipped_args_list = zip(scpfile_list, hostpath_list, instance_list)
        my_threading(copy_file, zipped_args_list)
        print('Total Hosts: %d' % (len(instance_list)))
        print('Check report.out file for the full report of this run')
    else:
        printusage()

    end = time.time()
    total_time = end - start
    print('Completed in %s seconds' % (total_time))
