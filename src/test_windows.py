# def run_regex(
#        input_filename,
#        phrases,
#        output_filename='output.csv',
#        is_rpdr=True,
#        note_keyword=RPDR_NOTE_KEYWORD,
#        patient_keyword=RPDR_PATIENT_KEYWORD,
#        extract_numerical_value=False,
#        extract_date=False,
#        report_description=None,
#        report_type=None,
#        ignore_punctuation=False):

from .extract_values import run_regex


run_regex('test_deidentified_rpdr_format.txt', "Patient")
