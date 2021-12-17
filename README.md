# cloudtrail-export-logs

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

This is a script to export logs from AWS CloudTrail to a local file.

## Getting Started

### Prerequisites

- python 3
- boto3
- pip

### Installing

First of all you need to clone this repository:

``` bash
git clone https://github.com/claick-oliveira/cloudtrail-export-logs.git
```

After clone access the folder:

```bash
cd cloudtrail-export-logs
```

## Running the script

To run the script you need to feel some arguments:

- **"-s", "--startime"**: The start time to get the logs, example 2021-12-01
- **"-e", "--endtime"**: The end time to get the logs, example 2021-12-31
- **"-r", "--region"**: The AWS region to get the logs, example us-east-1
- **"-a", "--accountid"**: The Account ID to get the logs: example 012345678901

> Valid timestamp formats:
>
> - 1422317782
> - 1422317782.0
> - 01-27-2015
> - 01-27-2015,01:16PM
> - "01-27-2015, 01:16 PM"
> - "01/27/2015, 13:16"
> - 2015-01-27
> - "2015-01-27, 01:16 PM"

Example of command:

``` bash
python3 export.py --startime 2021-12-01 --endtime 2021-12-31 --region us-east-1 --accountid 012345678901
```

The script will generate a structure like this:

```bash
|-- output
|   `-- 012345678901
|       `-- us-east-1
|           `-- cloudtrail-from-2021-12-01-to-2021-12-31-ID-012345678901-region-us-east-1.txt
```

### Switch role

To execute this script on environment with switch role, use the script `export_role.py`. This script there is an argument to specify the role ARN:

- **"-arn", "--arn"**: The Role ARN to switch, example arn:aws:iam::016075864677:role/CloudTrailAssumeRole

## Cleanup

To delete the script, you can run the following command to delete the folder:

```bash
rm -rf cloudtrail-export-logs
```

## Contributing

Please read [CONTRIBUTING.md](https://github.com/claick-oliveira/cloudtrail-export-logs/blob/main/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

- **Claick Oliveira** - *Initial work* - [claick-oliveira](https://github.com/claick-oliveira)

See also the list of [contributors](https://github.com/claick-oliveira/cloudtrail-export-logs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
