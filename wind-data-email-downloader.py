# -*- coding: utf-8 -*-
"""NRGEmailRead-Test.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dvlFOPVyjtpEgwVWrtDSq3g2vyG9Y3S4

# Testing NRG Email Reader with GSuite

The goal of this notebook is to test the email downloader provided by NRG systems here: https://github.com/nrgpy/data_email_client

## Setup Packages

This codeblock installs the data email client. THis might need to be rerun everytime the runtime is started.
"""


"""## Include Packets"""

from data_email_client import mailer
import email # To be able to walk through the email
from email import message
import os # To retrieve environment variables
import sys # for standard out stream handler
from typing import List # for List return type hints
import errno
import zipfile #to perform the unziping!
import shutil # for moving files around once downloaded
import pal #for the logging!!
#from dataWorkBench import dataFileWorkBench
import fileHandler

class emailHandler:
    def __init__(self):
        self.logger = pal.setupLogging("Email Handler")
        self.logger.info(" ###### WDED SESSION START #####")
        self.imap = self.createEmailInstance()

    def createEmailInstance(self) -> mailer: 
        ## Create Credentials for the Mail Server
        server = 'imap.gmail.com' #'outlook.office365.com' # 'imap.gmail.com' for gmail
        username = "wind@nwtresearch.com"
        mail_pass = os.getenv('WIND_GMAIL_PASS') # Make sure to export before running
        try:
            self.logger.debug("Attempting to Connect to Email")
            imap = mailer(server=server, username=username, password=mail_pass)
            self.logger.debug("Email connected")
            return imap
        except OSError as e:
            self.logger.error("Could not connect to Email!")
            self.logger.error(str(e.errno) + " - " + os.strerror(e.errno))
            exit()
        except:
            self.logger.error("Something else went wrong!!")


    def findInboxWithName(self, folderName: str) -> List[str]:
        data_boxes = [m for m in self.imap.mailboxes if folderName in m]
        return data_boxes

    def clearDataLabelFromEmail(self, emailid: int):
        archive_folder = os.getenv("EMAIL_ARCHIVE_FOLDER")
        self.imap.imap4.store(emailid, '+X-GM-LABELS', archive_folder)
        self.imap.imap4.store(emailid, '-X-GM-LABELS', '(Data)')
        self.logger.debug("Data label cleared from: " + str(emailid.decode("UTF8")))

    def downloadAttachmentFromMessage(self, imap: mailer, emailid: int) -> str : 
        out_dir = os.getenv("WDED_WORKING_DIR") + "/data"
        self.logger.debug("Inspecting Email ID: " + str(emailid.decode("UTF8")))
        resp, data = self.imap.imap4.fetch(emailid, "(RFC822)")
        labelResp, labelData = self.imap.imap4.fetch(emailid, '(X-GM-LABELS)')
        for label in labelData:
            if("Wind_Archived" in label.decode("utf-8")):
                self.logger.debug("Email is already archived, skipping")
                return "NULL"
            else:
                try:
                    email_body = data[0][1] # Make this more informed!!
                    m = email.message_from_bytes(email_body)
                    count = 0
                    for part in m.walk():
                        self.logger.info("Part being Inspectect: " + str(count) + ". Part of type: " + str(part.get_content_maintype()))
                        count += 1
                        if(part.get_content_maintype() == "application"):
                            filename = part.get_filename()
                            self.logger.debug("Part has File associated: " + str(filename))
                            save_path = os.path.join(out_dir, filename)
                            if not os.path.isfile(save_path):
                                fp = open(save_path, 'wb')
                                fp.write(part.get_payload(decode=True))
                                fp.close()
                                self.logger.debug(str(filename) + " saved.")
                                return save_path
                            else:
                                self.logger.debug(str(filename) + " File Already Downloaded")
                                return save_path
                except AttributeError as e: # email_body is none!
                    # Dump email object for debug:
                    self.logger.error("Writing email object to crash file...")
                    crashFilename = os.getenv("WDED_WORKING_DIR") + "crash.txt"
                    if os.path.exists(crashFilename):
                        os.remove(crashFilename)
                    crashfile = open(crashFilename, "w")
                    crashfile.write(m.__str__())
                    crashfile.close()
                    self.logger.error("Email Data is Mostly Likely None Type...Skipping." + str(e.__dict__))
                    self.logger.error("Program Failure, Error Number not recognized")
                    return "NULL"

    def downloadAllAttachmentsFromSender(self, sender: str) -> List[str]:
        data_boxes = self.findInboxWithName("Data")
        self.imap.search_for_messages(text=sender, area='from', folder=data_boxes)
        try:
            self.logger.debug("imap.result[0][0]: " + str(self.imap.results[0][0]))
        except:
            self.logger.error("Could not print imap.results[0][0]")

        try:
            self.logger.debug("List of Message ID's: " + str(self.imap.results[0][1]))
            msgs = self.imap.results[0][1]
            savePaths = []
            for emailid in msgs:
                savePaths.append(self.downloadAttachmentFromMessage(self.imap, emailid))
            self.logger.debug("Downloading from: " + sender + " finished")
            for emailid in msgs:
                self.clearDataLabelFromEmail(emailid)
                self.logger.debug("Completed Clearing Data Labels for " + sender)
                self.imap.imap4.expunge()
                self.logger.debug("IMAP Expunged")
            return savePaths
        except:
            self.logger.error("Could not assing msgs from imap.results[0][1]")
            return []
        

    def cleanArchive(self): # TODO Will need to also clean the SRA data files!
        self.logger.info("Cleaning Wind Archive")
        data_boxes = self.findInboxWithName("Wind_Archived")
        senders = ['447498823060@packet-mail.net', 'status@support.zephirlidar.com', 'status@support.zxlidars.com']
        for sender in senders:
            self.imap.search_for_messages(text=sender, area='from', folder=data_boxes)
            try:
                msgs = self.imap.results[0][1]
                for emailid in msgs:
                    resp, data = self.imap.imap4.fetch(emailid, "(RFC822)")
                    email_body = data[0][1] # Make this more informed!!
                    m = email.message_from_bytes(email_body)
                    subject = str(email.header.make_header(email.header.decode_header(m['Subject'])))
                    self.logger.debug("Cleaning email: " + str(emailid.decode("UTF8")) + ": " + str(subject))
                    self.imap.imap4.store(emailid, '-X-GM-LABELS', '(Data)')
                    self.imap.imap4.expunge()
                self.logger.info("Archive Cleaned")
            except:
                self.logger.error("Could Not Clean Archive for " + sender + " -> Might not be any messages there")

    def checkEmailForData(self):
        if self.imap is not None:
            # TODO Move this definition to another location (SQLite3?)
            expectedSenders = ['447498823060@packet-mail.net', 'status@support.zephirlidar.com', 'status@support.zxlidars.com']
            for sender in expectedSenders:
                self.downloadAllAttachmentsFromSender(sender = sender)
            self.imap.imap4.expunge()
        else: 
            self.logger.error("IMAP was None on creation")

def main():
    email = emailHandler()
    email.checkEmailForData()
    # Process Local Data Folder only
    owncloud = fileHandler.fileHandler()
    owncloud.processLocalFolder()
    email.cleanArchive() # Clean Archive is going to become expensive as emails pile up!

    # ? Test Backup Only!
    #owncloud = fileHandler.fileHandler()
    #owncloud.backupSRAFileToOwnCloud("data/011359_2023-05-21_07.30_000317.rld")

if __name__ == "__main__":
    main()
