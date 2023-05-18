
import pal #for the logging!

class fileHandler:
    def __init__():
        self.logger = pal.setupLogging("fileHandler")
        pass

    def moveCSVToOwnCloud(filePath: str):
        self.logger.debug("Moving CSV: " + filePath)
        filename = filePath.split('/')[-1]


    unit = findUnitID(filePath) # Maybe make utils??
    containerName = os.getenv('OWNCLOUD_CONTAINER_NAME') # Make sure to export before running
    dataPath = os.getenv('OWNCLOUD_DATA_PATH')
    workingPath = os.getenv('WDED_WORKING_DIR')
    extracted_type = filename.split(".")[-2] # file probably ends in either CSV.ZIP or ZPH.ZIP. this gives the first part
    shutil.unpack_archive(filePath, workingPath + "temp/" + str(unit))
    os.system("docker cp " + workingPath + "temp/" + str(unit) + "." + extracted_type + " " containerName + ":" + dataPath + extracted_type + "/" + str(unit) + "/" + filePath)
    logging.debug(str(unit) + " CSV moved to: " + containerName + ":" + dataPath + "CSV/" + str(unit) + "/" + filePath)
    os.remove(workingPath + "temp/" + str(unit) + "." + str(unit))




        pass

    def moveZPHToOwnCloud():
        pass

    def moveZIPToOwnCloud():
        pass

    def moveRLDToOwnCloud():
        pass

    