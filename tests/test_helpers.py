

from helpers import _sdr, sdr_folder


def test_same_file():
    original_stem_track = 'tests/other_ft.wav'
    separated_stem_track = 'tests/other_ft.wav'
    assert _sdr(original_stem_track,
                separated_stem_track) == 112.43124505706774


def test_different_file():
    original_stem_track = 'tests/other_ft.wav'
    separated_stem_track = 'tests/other_ens.wav'
    assert _sdr(original_stem_track,
                separated_stem_track) == 17.211375480357447
