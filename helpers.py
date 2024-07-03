import datetime
import glob
import time
import uuid
import soundfile as sf
import numpy as np
from tqdm import tqdm

from persist_results import persist_result


def _sdr(original_track, calculated_track):
    original_stem_track_sf, sr1 = sf.read(original_track)
    separated_stem_track_sf, sr2 = sf.read(calculated_track)

    references = np.expand_dims(original_stem_track_sf, axis=0)
    estimates = np.expand_dims(separated_stem_track_sf, axis=0)
    # compute SDR for one song
    delta = 1e-7  # avoid numerical errors
    num = np.sum(np.square(references), axis=(1, 2))
    den = np.sum(np.square(references - estimates), axis=(1, 2))
    num += delta
    den += delta
    result = 10 * np.log10(num / den)
    return float(result[0])


def get_current_datetime_string():
    tz = datetime.timezone.utc
    ft = "%Y-%m-%dT%H:%M:%S%z"
    t = datetime.datetime.now(tz=tz).strftime(ft)
    return t


def get_run_guid():
    return str(uuid.uuid4())


def sdr_folder(glob_original, glob_calculated, stem_name, run_datetime=None, run_guid=None, persist_result=persist_result, title=None, description=None):
    """
    Files are processed in alphabetical ascending order

    persist_result() function is exposed for alternative persistence methods 
    """
    start_time = time.time()

    if (run_datetime == None):
        run_datetime = get_current_datetime_string()

    if (run_guid == None):
        run_guid = get_run_guid()

    print(f"Processing '{stem_name}' files")

    # checking params
    if (glob_original == None or glob_calculated == None):
        raise Exception('glob patters not set')

    # finding & sorting all files
    files_original = glob.glob(glob_original)
    files_calculated = glob.glob(glob_calculated)
    if (len(files_original) != len(files_calculated)):
        raise Exception('number of files dont match')
    # sorting both arrays
    files_original.sort()
    files_calculated.sort()
    print('Total originals: {}'.format(len(files_original)))
    if len(files_original) == 0:
        return

    # progress bar just for eye candy
    progress_bar = tqdm(total=len(files_original))

    # calculating SDR
    all_sdr = []
    for i, original_file in enumerate(files_original):
        calculated_file = files_calculated[i]
        sdr = _sdr(original_track=original_file,
                   calculated_track=calculated_file)
        all_sdr.append(sdr)

        # persisting individual SDRs for audit
        result_audit = {
            "sdr": sdr,
            "stem": stem_name,
            "run_guid": run_guid,
            "original_track": original_file,
            "calculated_track": calculated_file,
            "run_datetime": run_datetime
        }

        persist_result(result=result_audit, csv_file='results_audit.csv')
        progress_bar.update(i - progress_bar.n)

    all_sdr = np.array(all_sdr).mean()

    # persisting total SDR for audit
    result_audit['sdr'] = all_sdr
    del result_audit['original_track']
    del result_audit['calculated_track']
    result_audit['processing_time_sec'] = "{:.2f}".format(
        time.time() - start_time)
    result_audit['title'] = title
    result_audit['description'] = description
    persist_result(result=result_audit, csv_file='results.csv')
