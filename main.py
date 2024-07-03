import time

from helpers import get_current_datetime_string, get_run_guid, sdr_folder

start_time = time.time()

# You can extend this dict to your liking
# sdr_folder accept 'glob' string as parameter
test_data_glob = {
    "bass": {
        "original": 'multisong_musdb18/*_bass.wav',
        "calculated": 'test_ouput/*_bass.wav'
    },
    # "drums": {
    #     "original": '',
    #     "calculated": ''
    # },
    # "other": {
    #     "original": '',
    #     "calculated": ''
    # },
    # "vocals": {
    #     "original": '',
    #     "calculated": ''
    # },
    # "instrumental": {
    #     "original": '',
    #     "calculated": ''
    # },
    # "mixed": {
    #     "original": '',
    #     "calculated": ''
    # },
}

run_datetime = get_current_datetime_string()
run_guid = get_run_guid()
title = "MUSDB_18_HQ"
description = 'original stem'

for stem_name in test_data_glob:
    sdr_folder(glob_original=test_data_glob[stem_name]["original"],
               glob_calculated=test_data_glob[stem_name]["calculated"], stem_name=stem_name, run_datetime=run_datetime, run_guid=run_guid, title=title, description=description)


print("Finished. Elapsed time: {:.2f} sec".format(time.time() - start_time))
