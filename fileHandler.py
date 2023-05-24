
import pal #for the logging!
import extractionHandler
import os # To get environment variables
import glob

class fileHandler:
    def __init__(self):
        self.logger = pal.setupLogging("fileHandler")
        self.extractor = extractionHandler.extractionHandler()

    # Move tool if user knows all the details!
    def moveFileToContainer(self,sourceFilePath: str, targetFilePath:str, containerName:str):
        os.system("docker cp " + sourceFilePath + " " + containerName + ":" + targetFilePath)
        self.logger.debug("Moved file to: " + containerName)
        os.system("docker exec " + containerName + " /bin/bash /root/refresh.sh") # ! If this fails, os will still remove the file!!
        os.remove(sourceFilePath)

    # Move tool with autofile sorting.
    def backupLidarFileToOwnCloud(self,filePath: str):
        containerName = os.getenv('OWNCLOUD_CONTAINER_NAME') # Make sure to export before running
        dataPath = os.getenv('OWNCLOUD_DATA_PATH')
        workingPath = os.getenv('WDED_WORKING_DIR')
        filename = filePath.split('/')[-1]
        fileType = filename.split(".")[-1]
        if fileType in ["CSV", "ZPH", "zip", "ZIP"]:
            if fileType == "zip":
                fileType = "ZIP"
            unit = self.extractor.findLidarUnitID(filePath)
            targetPath = dataPath + fileType + "/" + unit + "/" + filename
            self.moveFileToContainer(filePath, targetPath, containerName)
        else:
            self.logger.debug("File type did not match any expected options for Lidar [CSV, ZPH, ZIP]")
    
    def backupSRAFileToOwnCloud(self,filePath: str):
        containerName = os.getenv('OWNCLOUD_CONTAINER_NAME') # Make sure to export before running
        dataPath = os.getenv('OWNCLOUD_DATA_PATH')
        workingPath = os.getenv('WDED_WORKING_DIR')
        filename = filePath.split('/')[-1]
        fileType = filename.split(".")[-1]
        if fileType in ["rld", "RLD", "CSV"]:
            if fileType == "rld":
                fileType = "RLD"
            unit = self.extractor.findSRAUnitID(filePath)
            targetPath = dataPath + fileType + "/" + unit + "/" + filename
            self.moveFileToContainer(filePath, targetPath, containerName)
        else:
            self.logger.debug("File type did not match any expected options for SRA [CSV, rld]")

    def processLocalFolder(self):
        workingPath = os.getenv('WDED_WORKING_DIR')
        for filePath in glob.glob(workingPath+"data/*.RLD"):
            print(filePath)
        for filePath in glob.glob(workingPath+"data/*.rld"):
            print(filePath)
            self.backupSRAFileToOwnCloud(filePath)
        for filePath in glob.glob(workingPath+"data/*.zip"):
            print(filePath)
            self.extractor.extractDownloadedFile(filePath)
        for filePath in glob.glob(workingPath+"temp/*/*.CSV"):
            print(filePath)
            self.backupLidarFileToOwnCloud(filePath)
        for filePath in glob.glob(workingPath+"temp/*/*.ZPH"):
            print(filePath)
            self.backupLidarFileToOwnCloud(filePath)
