# Wind Data Email Downloader
A tool to download ZX300, and SymphoniePRO data files for Analysis.

# Usage:

This script expects to run on the host of a docker owncloud instance. When configured properly it will download data files and place then on the owncloud instance so that they can be accessed through the owncloud login.

## Crontab Entry:

There are three entries in the crontab. One to run the script, and two others that move the cron log file to the owncloud install so that it can be inspected daily.

```0 5 * * * /root/.set_env.sh python3 /root/Wind-Data-Email-Downloader/wind-data-email-downloader.py >> /root/cron_output.log 2>&1```
```0 6 * * * docker cp /root/cron_output.log owncloud_server:/mnt/data/files/admin/files/WindData/cron_output.log```
```0 7 * * * docker exec owncloud_server /bin/bash /root/refresh.sh```

## File Refresh Script:

Owncloud does not automatically detect when new files have been moved into it's folders. A file scan can be manually triggered 

To create the refresh script, use the root terminal of the owncloud container:
```echo "occ files:scan admin" >> /root/refresh.sh```

# Dependencies

This program is intended to run on a machine hosting a owncloud instance via docker. As a result, it depends on there being docker installed and an owncloud instance running.

## Packages
- pip3
- data_email_client
- nrgpy ``https://github.com/nrgpy/nrgpy``

## Environment Variables

- WIND_GMAIL_PASS: App Password for the gmail account recieving the data emails
- EMAIL_ARCHIVE_FOLDER: The label name inside Gmail that is used to signify that data has already been downloaded/processed
- OWNCLOUD_CONTAINER_NAME: The name of the container running owncloud. Try: ```docker container ls```
- OWNCLOUD_DATA_PATH: The path where owncloud is saving it's files. Default: '/mnt/data/files/admin/files/'
- WDED_WORKING_DIR: The absolute local directory where the downloader is working. Helps for portability
- NRG_CLIENT_ID: ID provided by NRG Systems for using their API.
- NRG_CLIENT_SECRET: Secret Key provided by NRG Systems for using their API

