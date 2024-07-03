import datetime
import glob
import multiprocessing
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


def process_file_pair(args):
    index, original_file, calculated_file, stem_name, run_guid, run_datetime = args
    sdr = _sdr(original_track=original_file,
               calculated_track=calculated_file)

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

    return index, sdr


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

    # Prepare the arguments for the pool
    args_list = [(i, files_original[i], files_calculated[i], stem_name,
                  run_guid, run_datetime) for i in range(len(files_original))]

    # multi-core processing
    all_sdr = []
    num_cores = multiprocessing.cpu_count()
    p = multiprocessing.Pool(processes=int(num_cores/2))
    with tqdm(total=len(args_list)) as pbar:
        track_iter = p.imap(process_file_pair, args_list)
        for index, sdr in track_iter:
            all_sdr.append(sdr)
            pbar.update()
    p.close()

    all_sdr = np.array(all_sdr).mean()

    result = {
        "sdr": all_sdr,
        "stem": stem_name,
        "run_guid": run_guid,
        "run_datetime": run_datetime,
        "processing_time_sec": "{:.2f}".format(time.time() - start_time),
        "title": title,
        "description": description
    }
    # persisting total SDR for audit
    persist_result(result=result, csv_file='results.csv')
