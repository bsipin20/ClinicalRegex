import csv 
import re
import string
import sys 
#import chardet
import xlrd
import numpy as np
import pandas as pd

PHRASE_TYPE_WORD = 0
PHRASE_TYPE_NUM = 1
PHRASE_TYPE_DATE = 2

RPDR_NOTE_KEYWORD = 'NOTE'
RPDR_PATIENT_KEYWORD = 'EMPI'

class RPDRNote(object):
    """Works for Lno, Dis, Rad, and Opn RPDR files."""
    def __init__(self, rpdr_column_name_to_key, rpdr_note):
        self.empi = rpdr_column_name_to_key['EMPI']
        self.mrn_type = rpdr_column_name_to_key['MRN_Type']
        self.mrn = rpdr_column_name_to_key['MRN']
        self.report_type = (rpdr_column_name_to_key.get('Report_Type') or
                            rpdr_column_name_to_key.get('Subject'))
        self.report_number = (rpdr_column_name_to_key.get('Report_Number') or
                              rpdr_column_name_to_key.get('Record_Id'))
        self.report_description = rpdr_column_name_to_key.get(
            'Report_Description')
        self.report_date = (rpdr_column_name_to_key.get('Report_Date_Time') or
                            rpdr_column_name_to_key.get('LMRNote_Date'))
        self.note = rpdr_note

    def get_dictionary(self):
        return {
            'REPORT_NUMBER': self.report_number,
            RPDR_NOTE_KEYWORD: self.note,
            RPDR_PATIENT_KEYWORD: self.empi,
            'MRN_TYPE': self.mrn_type,
            'MRN': self.mrn,
            'REPORT_TYPE': self.report_type,
            'REPORT_DESCRIPTION': self.report_description,
            'REPORT_DATE': self.report_date
        }

    def remove_punctuation_from_note(self):
        self.note = _remove_punctuation(self.note)


class NotePhraseMatches(object):
    """Describes all phrase matches for a particular RPDR Note"""
    def __init__(self, note_dict):
        self.note_dict = note_dict
        self.phrase_matches = []

    def add_phrase_match(self, phrase_match):
        self.phrase_matches.append(phrase_match)

    def finalize_phrase_matches(self):
        self.phrase_matches.sort(key=lambda x: x.match_start)


class PhraseMatch(object):
    """Describes a single phrase match to a single RPDR Note for a phrase."""
    def __init__(self, extracted_value, match_start, match_end, phrase):
        # Binary 0/1s for extracting phrase presence, else numerical value.
        self.extracted_value = extracted_value
        self.match_start = match_start
        self.match_end = match_end
        self.phrase = phrase

def _remove_punctuation(s):
    return s.translate(None, string.punctuation)


def _extract_phrase_from_notes(phrase_type, phrases, note, note_dict):
    """Return a PhraseMatch object with the value as a binary 0/1 indicating
    whether one of the phrases was found in note"""


    if phrase_type == PHRASE_TYPE_WORD:
        pattern_strings = [
            '(\s%s\s)', '(^%s\s)', '(\s%s$)', '(^%s$)', '(\s%s[\,\.\?\!\-])',
            '(^%s[\,\.\?\!\-])'
        ]
    elif phrase_type == PHRASE_TYPE_NUM:
        pattern_strings = [
            '(?:%s)\s*(?:of|is|was|were|are|\:)?[:]*[\s]*([0-9]+\.?[0-9]*)']
    elif phrase_type == PHRASE_TYPE_DATE:
        pattern_strings = [
            '(?:%s)\s*(?:of|is|was|were|are|\:)?[:]*[\s]*(\d+/\d+/\d+)',
            '(?:%s)\s*(?:of|is|was|were|are|\:)?[:]*[\s]*(\d+-\d+-\d+)']
    else:
        raise Exception('Invalid phrase extraction type.')

    #print(phrases)

    phrase_matches = NotePhraseMatches(note_dict)
    for phrase in phrases:
        for pattern_string in pattern_strings:
            pattern_string = pattern_string % phrase
            re_flags = re.I | re.M | re.DOTALL
            pattern = re.compile(pattern_string, flags=re_flags)
            match_iter = pattern.finditer(note)
            try:
                while True:
                    match = next(match_iter)
                    if phrase_type == PHRASE_TYPE_WORD:
                        extracted_value = 1
                    elif phrase_type == PHRASE_TYPE_NUM:
                        extracted_value = float(match.groups()[0])
                    elif phrase_type == PHRASE_TYPE_DATE:
                        extracted_value = match.groups()[0]
                    new_match = PhraseMatch(extracted_value, match.start(),
                                            match.end(), phrase)
                    phrase_matches.add_phrase_match(new_match)

            except StopIteration:
                continue


    phrase_matches.finalize_phrase_matches()
    return phrase_matches

def _extract_values_from_notes(
        note_dicts, phrase_type, phrases, note_key, ignore_punctuation):
    """Return a list of NotePhraseMatches for each note in note_dict."""
    note_phrase_matches = []
    if ignore_punctuation:
        phrases = [_remove_punctuation(phrase) for phrase in phrases]
    for note_dict in note_dicts:
        if ignore_punctuation:
             note_dict[note_key].translate(None, string.punctuation)
        #print(phrase_type)
        #print(phrases)
        #print(note_dict[note_key])
        #print(note_dict)
        #print('eval')
        phrase_matches = _extract_phrase_from_notes(phrase_type, phrases, note_dict[note_key], note_dict)
        note_phrase_matches.append(phrase_matches)
    return note_phrase_matches


def _filter_rpdr_notes_by_column_val(rpdr_notes,
                                     required_report_description,
                                     required_report_type):
    """Filter the rpdr notes by column values.

    Input:
    rpdr_notes: the list of RPDR note objects.
    required_report_description: a value for report description such as "ECG"
    required_report_type: a value for the report type such as "CAR"

    Return rpdr_notes with all values filtered out whose keys differ
    from either `required_report_type` or `required_report_description` if
    those values are not None.
    """
    filtered_rpdr_notes = []
    for rpdr_note in rpdr_notes:
        if (required_report_description is not None and
                rpdr_note.report_description != required_report_description):
            continue
        if (required_report_type is not None and
                rpdr_note.report_type != required_report_type):
            continue
        filtered_rpdr_notes.append(rpdr_note)
    return filtered_rpdr_notes

def clean_df(df, text_columns, needs_decode=True):
    for label in text_columns:
        if label in df:
            df[label] = df[label].map(lambda x: clean_phrase(x, needs_decode))
    new_df = pd.DataFrame(columns=df.columns)
    for index, row in df.iterrows():
        new_df = new_df.append(row)
    return new_df

def clean_phrase(phrase, needs_decode=True):
    if type(phrase) == float:
        return phrase
    if needs_decode:
        phrase = phrase.decode('ascii', errors='ignore')
    cleaned = str(phrase.replace('\r\r', '\n').replace('\r', '').replace('||', '|'))
    cleaned = str(phrase.replace('\\r', '\\n'))
    cleaned = re.sub(r'\n+', '\n', cleaned)
    cleaned = re.sub(r' +', ' ', cleaned)
    cleaned = re.sub(r'\t', ' ', cleaned)
    cleaned = cleaned.strip('\r\n')
    return str(cleaned.strip())

def process_rpdr_file_unannotated(filename):
    with open(filename, 'rb') as rpdr_file:
        rpdr_lines = rpdr_file.readlines()
        rpdr_lines = [clean_phrase(line) for line in rpdr_lines]
        rpdr_lines = [line for line in rpdr_lines if len(line) > 0]

    # List of processed notes. Each entry is a dictionary
    note_index = 0
    notes = [] 
    current_note = ''
    current_dict = {}
    entry_keys = None

    for idx, line in enumerate(rpdr_lines):
        # Header line
        if idx == 0:
            entry_keys = line.split('|')
        # If it's a patient header line
        elif line.count('|') > 5:

            patient_keys = line.split('|')
            if len(patient_keys) != len(entry_keys):
                # Attempt to reformat header
                if '^' in patient_keys[3]:
                    items = patient_keys[3].split('^')
                    new_arr = list(patient_keys[:3]) + [items[0], items[1]] + list(patient_keys[4:])
                    if len(new_arr) == len(entry_keys):
                        patient_keys = list(new_arr)
                elif '/' in patient_keys[4]:
                    new_arr = list(patient_keys[:4]) + ['NA'] + list(patient_keys[4:])
                    if len(new_arr) == len(entry_keys):
                        patient_keys = list(new_arr)
            # Rename all Note column to note
            entry_keys[-1] = RPDR_NOTE_KEYWORD
            current_dict = {
                entry_key: patient_key for (entry_key, patient_key) in
                zip(entry_keys, patient_keys)
            }
        # Start a new notes
        elif '[report_end]' in line:
            current_note = current_note.strip()
            current_note = current_note.replace("$1$", "").replace("$\\1$", "").replace("$-1$", "").replace("$\\-1$", "").replace("$2$", "").replace("$\\2$", "").replace("$-2$", "").replace("$\\-2$", "").replace("$3$", "").replace("$\\3$", "").replace("$-3$", "").replace("$\\-3$", "")
            # Save current note

            if current_dict != {}:
                if RPDR_NOTE_KEYWORD in current_dict:
                    current_dict[RPDR_NOTE_KEYWORD] = current_dict[RPDR_NOTE_KEYWORD] + '\n' + current_note
                    rpdr_note = RPDRNote(current_dict, current_dict[RPDR_NOTE_KEYWORD])
                    notes.append(rpdr_note)

            note_index += 1
            current_note = ''
            current_dict = {}
        # Just part of a note
        else:
            current_note += line + "\n"
    return notes

def _write_csv_output(note_phrase_matches, note_key, output_fname):
    """Write one CSV row for each phrase_match where the row contains all of
    the RPDR note keys along with the extracted numerical value at the end of
    the row."""
    dict_list = []
    for note_phrase_match in note_phrase_matches:
        note = note_phrase_match.note_dict[note_key]
        matches = []
        for phrase_match in note_phrase_match.phrase_matches:

            match_start = phrase_match.match_start
            match_end = phrase_match.match_end 
            matched_text = note[match_start:match_end]
            char_start = re.search(r'\w', matched_text).start()
            match_start += char_start
            matched_text = matched_text.strip()
            match_end = match_start + len(matched_text)
            matches.append((match_start, match_end))

        extracted_value = 0

        if len(note_phrase_match.phrase_matches) > 0:
            extracted_value = note_phrase_match.phrase_matches[0].extracted_value
        note_phrase_match.note_dict['MATCHES'] = matches
        note_phrase_match.note_dict['EXTRACTED_VALUE'] = extracted_value
        dict_list.append(note_phrase_match.note_dict)

    df = pd.DataFrame(dict_list)
    df['MATCHES'] = df['MATCHES'].astype('object')
    df.index = np.arange(0, df.shape[0])
    df = clean_df(df, [RPDR_NOTE_KEYWORD], False)
    df.to_csv(output_fname)
    writer = pd.ExcelWriter(output_fname[:-4] + '.xlsx')
    df.to_excel(writer,'Sheet1')

    

def run_regex(input_filename, phrases, output_filename='output.csv', is_rpdr=True, note_keyword=RPDR_NOTE_KEYWORD, patient_keyword=RPDR_PATIENT_KEYWORD, extract_numerical_value=False, 
        extract_date=False, report_description=None, report_type=None, ignore_punctuation=False):

    if extract_numerical_value:
        phrase_type = PHRASE_TYPE_NUM
    elif extract_date:
        phrase_type = PHRASE_TYPE_DATE
    else:
        phrase_type = PHRASE_TYPE_WORD
    phrases = [p.strip() for p in phrases.split(',')]

    is_rpdr = bool(is_rpdr)

    with open(input_filename, 'rb') as f:
        result = chardet.detect(f.read())

    if is_rpdr:
        rpdr_notes = process_rpdr_file_unannotated(input_filename)
        rpdr_notes = _filter_rpdr_notes_by_column_val(rpdr_notes, report_description, report_type)
        note_dicts = [r.get_dictionary() for r in rpdr_notes]

    elif input_filename.split(".")[1] == "xls":
        df = pd.read_excel(input_filename)
        df = clean_df(df,[note_keyword],False)
        note_dicts = df.to_dict('records')

    else:
        # pipe delimiated SEPARATED 
        df = pd.read_csv(input_filename,sep="|")
        df = clean_df(df, [note_keyword], False)
        note_dicts = df.to_dict('records')

    note_phrase_matches = _extract_values_from_notes(note_dicts, phrase_type, phrases, note_keyword, ignore_punctuation)
    _write_csv_output(note_phrase_matches, note_keyword, output_filename)

#
if __name__ ==  '__main__':
    #run_regex(sys.argv[1],'Patient', 'output.csv',sys.argv[2],sys.argv[3],sys.argv[4])
#    run_regex('duke_notes.xls','patient', 'output.csv',"","TEXT","HADM_ID")
    run_regex('pipe_delimited.txt','patient', 'output.csv',"","NOTE","ROW_ID")




        

