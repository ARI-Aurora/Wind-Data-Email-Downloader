
import shutil # for extracting the files!
import os #to get environment variables
import nrgpy
import pal

class extractionHandler:
    def __init__(self):
        self.logger = pal.setupLogging("Extraction Handler")

    def extractDownloadedFile(self, sourceFilePath: str) -> str:
        workingPath = os.getenv('WDED_WORKING_DIR')
        extractedDir = workingPath + "temp/"
        filename = sourceFilePath.split('/')[-1]
        print(sourceFilePath)
        extracted_type = sourceFilePath.split(".")[-2] # ? Should only return a usable value for the lidars, garbage for the SRAs
        if extracted_type in ["ZPH", "CSV"]:
            unit = self.findLidarUnitID(sourceFilePath)
            shutil.unpack_archive(sourceFilePath, extractedDir + str(unit))
            self.logger.debug("Unpacked " + sourceFilePath)
        elif extracted_type in ["rld", "RLD"]:
            unit = self.findSRAUnitID(sourceFilePath)
            client_id = os.getenv("NRG_CLIENT_ID")
            client_secret = os.getenv("NRG_CLIENT_SECRET")
            converter = nrgpy.cloud_convert(
                filename=sourceFilePath, 
                url_base="https://cloud-api.nrgsystems.com/nrgcloudcustomerapi/",
                client_id=client_id,
                client_secret=client_secret,
            )
        else:
            self.lo
            return "NULL"
        return extractedDir + str(unit) + filename

    def findLidarUnitID(self, filePath: str) -> int:
        filename = filePath.split("/")[-1]
        unit = filename.split("_")[1].split("@")[0]
        self.logger.debug("Found Lidar UNIT ID: " + str(unit))
        return unit

    def findSRAUnitID(self, filePath: str) -> int:
        filename = filePath.split("/")[-1]
        unit = filename.split("_")[0]
        self.logger.debug("Found SRA UNIT ID: " + str(unit))
        return unit
