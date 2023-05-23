
import shutil # for extracting the files!
import os #to get environment variables
import nrgpy


def extractDownloadedFile(sourceFilePath: str) -> str:
    workingPath = os.getenv('WDED_WORKING_DIR')
    extractedDir = workingPath + "temp/"
    filename = filePath.split('/')[-1]
    print(sourceFilePath)
    extracted_type = sourceFilePath.split(".")[-2] # ? Should only return a usable value for the lidars, garbage for the SRAs
    if extracted_type in ["ZPH", "CSV"]:
        unit = findLidarUnitID(sourceFilePath)
        shutil.unpack_archive(sourceFilePath, extractedDir + str(unit))
    elif extracted_type in ["rld", "RLD"]:
        unit = findSRAUnitID(sourceFilePath)
        client_id = os.getenv("NRG_CLIENT_ID")
        client_secret = os.getenv("NRG_CLIENT_SECRET")
        converter = nrgpy.cloud_convert(
            filename=sourceFilePath, 
            url_base="https://cloud-api.nrgsystems.com/nrgcloudcustomerapi/",
            client_id=client_id,
            client_secret=client_secret,
        )
    else:
        return "NULL"
    return extractedDir + str(unit) + filename

def findLidarUnitID(filePath: str) -> int:
    filename = filePath.split("/")[-1]
    unit = filename.split("_")[1].split("@")[0]
    #!logging.debug("Found Lidar UNIT ID: " + str(unit))
    return unit

def findSRAUnitID(filePath: str) -> int:
    filename = filePath.split("/")[-1]
    unit = filename.split("_")[0]
    #!logging.debug("Found SRA UNIT ID: " + str(unit))
    return unit
