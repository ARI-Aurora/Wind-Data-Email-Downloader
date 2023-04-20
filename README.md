# Wind Data Email Downloader
A tool to download ZX300, SymphoniePRO, and Environment Canada Data for Analysis.

## Usage:

- The downloader requires an environment variable named 'WIND_GMAIL_PASS' to be set with an App password for the email you wish to download data from.

# Road Map:

- [ ] Add python virtual environment
- [ ] Move keys to environment variables!!


## Script Features
- Add back some of the safety features from the library
- Add the archiving feature (move downloaded emails to another folder)
- Add data logging (Make log file appear on samba)
- Create file structure. ZIPs, ZPH, and CSV folders
- Detect file extension and move file accordinly
- Detect from which device is returning data
- Extract zip files
- Add archive script that will go through the whole mainbox and pull out all the items from all time.

## Recall Features
- Add to cron
- Add log file to cron

## Docker
- Create a basic compose file
- Load python script
- install samba
- load the samba config file