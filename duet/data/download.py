import gdown
import json
import shutil
from duet.const import const as constants


def download_save():
    with open(constants.DRIVE_JSON_PATH, 'r') as r:
        drive_dict = json.load(r)

    for key, value in drive_dict.items():
        gdown.download(
            url=value, output="drive/"+key+".zip", fuzzy=True)
        shutil.unpack_archive("drive/"+key+".zip",
                              f"drive/{key}")


download_save()
