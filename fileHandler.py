
import pal #for the logging!
from extractionHander import findLidarUnitID, findSRAUnitID

class fileHandler:
    def __init__():
        self.logger = pal.setupLogging("fileHandler")
        pass

    # Move tool if user knows all the details!
    def moveFileToContainer(sourceFilePath: str, targetFilePath:str, containerName:str):
        os.system("docker cp " + sourceFilePath + " " + containerName + ":" + targetFilePath)
        self.logger("Moved file to: " + containerName)

    # Move tool with autofile sorting.
    def backupLidarFileToOwnCloud(filePath: str):
        containerName = os.getenv('OWNCLOUD_CONTAINER_NAME') # Make sure to export before running
        dataPath = os.getenv('OWNCLOUD_DATA_PATH')
        workingPath = os.getenv('WDED_WORKING_DIR')
        filename = filePath.split('/')[-1]
        fileType = filename.split(".")[-1]
        if fileType in ["CSV", "ZPH", "ZIP"]:
            unit = findLidarUnitID(filePath)
            targetPath = dataPath + fileType + "/" + unit + "/" + filename
            moveFileToContainer(filePath, targetPath, containerName)
            # TODO Remove files from machine?
        else:
            self.logger("File type did not match any expected options for Lidar [CSV, ZPH, ZIP]")
    
    def backupSRAFileToOwnCloud(filePath: str):
        containerName = os.getenv('OWNCLOUD_CONTAINER_NAME') # Make sure to export before running
        dataPath = os.getenv('OWNCLOUD_DATA_PATH')
        workingPath = os.getenv('WDED_WORKING_DIR')

        filename = filePath.split('/')[-1]
        fileType = filename.split(".")[-1]
        if fileType in ["rld", "CSV"]:
            unit = findSRAUnitID(filePath)
            targetPath = dataPath + fileType + "/" + unit + "/" + filename
            moveFileToContainer(filePath, targetPath, containerName)
            # TODO Remove files from machine?
        else:
            self.Logger("File type did not match any expected options for SRA [CSV, rld]")