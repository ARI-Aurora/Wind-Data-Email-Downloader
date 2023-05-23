# Wind Data Email Downloader
A tool to download ZX300, SymphoniePRO, and Environment Canada Data for Analysis.

# Usage:

- The downloader requires an environment variable named 'WIND_GMAIL_PASS' to be set with an App password for the email you wish to download data from.
- The downloader expects to run next to a samba file share named 'wind_data_shr' and so will attempt to move downloaded files into that folder structure.

## Crontab Entry:

- The following entry calls the script everyday at 5am. 
- The setup-downloader-and-run.sh script sets the WIND_GMAIL_PASS environment variable before calling the script.

```0 5 * * * /home/pi/Documents/setup-downloader-and-run.sh python3 /home/pi/wind-data-downloader/data-email-downloader-test.py >> /home/pi/cron_output.log 2>&1```

# Dependencies

This program is intended to run on a machine hosting a owncloud instance via docker.

## Packages
- pip3
- data_email_client
- nrgpy ``https://github.com/nrgpy/nrgpy``

## Environment Variables

- WIND_GMAIL_PASS: App Password for the gmail account recieving the data emails