# Multiprocessing Script to Run Commands on Remote SUVs

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

```
python3.7
```

## Running the Script - Getting Help

```
->python ssh_command_execute.py -h
usage: ssh_command_execute.py [-h] [--command COMMAND [COMMAND ...]]
                              [--scpfile SCPFILE [SCPFILE ...]]
                              [--hostpath HOSTPATH [HOSTPATH ...]]
                              [--hostlist HOSTLIST [HOSTLIST ...]]
                              [--printusage PRINTUSAGE [PRINTUSAGE ...]]

Run Command on List of Hosts

optional arguments:
  -h, --help            show this help message and exit
  --command COMMAND [COMMAND ...]
                        Run Command on Remote Host
  --scpfile SCPFILE [SCPFILE ...]
                        SCP file to Remote Host
  --hostpath HOSTPATH [HOSTPATH ...]
                        Destination host path to SCP
  --hostlist HOSTLIST [HOSTLIST ...]
                        Path to file with hostname list
  --printusage PRINTUSAGE [PRINTUSAGE ...]
                        Option: yes - Print usage examples
```

## Running the Script

### Create a file with a list of the hosts/SUVs by inputing one FQDN per line:
```
->cat list_of_instances.txt
ec2-3-81-221-5.compute-1.amazonaws.com
ec2-34-220-132-106.us-west-2.compute.amazonaws.com
ec2-35-165-36-38.us-west-2.compute.amazonaws.com
```

### Example 1 - Getting system uptime
```
python ssh_command_execute.py --command "uptime" --hostlist list_of_instances.txt
```

### Example 2 - Resuming the SUV Build
```
python ssh_command_execute.py --command "nohup /etc/rc.resumebuild > resumebuild.out 2> resumebuild.err < /dev/null &" --hostlist list_of_instances.txt
```

### Example 3 - Retrieving disk usage
```
python ssh_command_execute.py --command "df --output=pcent /data" --hostlist list_of_instances.txt
```

### Example 4 - Copying a file or a script to a list of hosts
*1. Create a script*
```
->cat uptime.sh
uptime
```

*2. Copy the script over to the list of Hosts*
```
python ssh_command_execute.py --scpfile uptime.sh --hostpath '/root' --hostlist list_of_instances.txt
```

*3. Execute the script*
```
python ssh_command_execute.py --command 'bash /root/uptime.sh' --hostlist list_of_instances.txt
```

## Standard Output

```
Check report.out file for the full report of this run
Completed in N seconds
```

## Script Output - Saving Report to file
*Write a report to a file (report.out) as: host, stdout, stderr*

```
->cat report.out
ec2-3-81-221-5.compute-1.amazonaws.com, b'Use%\n 51%', b''
ec2-35-165-36-38.us-west-2.compute.amazonaws.com, b'', b'df: \xe2\x80\x98/fake-part\xe2\x80\x99: No such file or directory'
```
