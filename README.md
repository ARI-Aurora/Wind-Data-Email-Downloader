# Wind Data Email Downloader
A tool to download ZX300, SymphoniePRO, and Environment Canada Data for Analysis.

# Usage:

- The downloader requires an environment variable named 'WIND_GMAIL_PASS' to be set with an App password for the email you wish to download data from.
- The downloader expects to run next to a samba file share named 'wind_data_shr' and so will attempt to move downloaded files into that folder structure.

## Crontab Entry:

- The following entry calls the script everyday at 5am. 
- The setup-downloader-and-run.sh script sets the WIND_GMAIL_PASS environment variable before calling the script.

```0 5 * * * /home/pi/Documents/setup-downloader-and-run.sh python3 /home/pi/wind-data-downloader/data-email-downloader-test.py >> /home/pi/cron_output.log 2>&1```

# Next Steps

## Docker? Containerize?
- Create a basic compose file
- Load python script
- install samba
- load the samba config file