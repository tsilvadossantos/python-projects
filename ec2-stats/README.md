# Multiprocessing Script to SSH AWS EC2 Instance and Collect Data

This project is a useful and efficient way of accessing hundreds of EC2 instances per AWS region and AWS account to collect data.
For the moment its only collecting storage usage, but the overall goal is to increase the amount of options for data collection.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

```
matplotlib==2.2.3
pandas==0.22.0
pyaml==17.12.1
simplejson==3.13.2
subprocess32==3.5.3
```

### Installing

```
pip install -r requirements/requirements.txt
```

## Running the tests

TBD

```
TBD
```

## Running the Script - Getting Help

```
usage: ec2_stats.py [-h] [--region REGION [REGION ...]]
                    [--profile PROFILE [PROFILE ...]]
                    [--chart CHART [CHART ...]]

Get EC2 Instance Details

optional arguments:
  -h, --help            show this help message and exit
  --region REGION [REGION ...]
                        aws region
  --profile PROFILE [PROFILE ...]
                        account profile
  --chart CHART [CHART ...]
                        generate and save chart - defaul is no
```

## Running the Script - Sample with Chart

```
python ec2_stats.py  --region <REGION_NAME> --profile <AWS_ACCOUNT_NAME> --chart yes
```

Running the script with the parameters above will generate a CSV file with the data collected and a chart grouping the data collected and saved in the CSV file. Both, CSV and Chart (PNG format) are saved to the data directory inside the project.
The format of the files are:
- CSV File: <REGION_NAME>.csv
- Chart PNG Image: <REGION_NAME>.png

To run the script and only generate the CSV file and not the Chart, run the following:
```
python ec2_stats.py  --region <REGION_NAME> --profile <AWS_ACCOUNT_NAME>
```

## Built With

* [Python 2.7.14](https://www.python.org/downloads/release/python-2714/) - The programming language used


## Versioning

TBD

## Authors

* **Thiago Santos** - *Initial work*
