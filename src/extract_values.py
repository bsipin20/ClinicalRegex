import csv
import re
import string
import sys
import pdb
# import chardet
import xlrd
import numpy as np
import pandas as pd
import time

def process_data(info):
    """Generator for processing the data with the UC_PROPS"""

    # go through the lines and perform any in-place modifications
    for i, line in enumerate(info['data']):
        # process user-specified properties  
        if self.options['lowercase']:
            info['data'][i] = line.lower()

            # Remove blank lines
    if self.options['ignore_blank_lines']:
        info["data"] = [line for line in info["data"] if line.strip()]

    # text wrapping
    if self.wrap:
        info["data"] = self.wrap.wrap(''.join(info['data']))
        info["data"] = [line + "\n" for line in info["data"]]	# should not need to do this

    if self.unwrapper:
        # do not include the first line
        unwrapped = self.unwrapper.process(''.join(info['data'][1:]))
        info["data"] = [info["data"][0]] + self.unwrapper.render(unwrapped, "reflow").splitlines(True)
        
    return info

def get_document( info):
    document = ''.join(self.process_data(info)['data'])
    return document



def _remove_punctuation(s):
    return s.translate(None, string.punctuation)


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


class ClinicianNotes(object):

    PHRASE_TYPE_WORD = 0
    PHRASE_TYPE_NUM = 1
    PHRASE_TYPE_DATE = 2

    RPDR_NOTE_KEYWORD = 'NOTE'
    RPDR_PATIENT_KEYWORD = 'EMPI'

    def __init__(
            self,
            input_file,
            row,
            note_keyword="NOTE",
            is_rpdr=False,
            patient_keyword="EMPI",
            extract_numerical_value=False):

        self.report_description = None
        self.report_type = None
        self.ignore_punctuation = False

        phrase_type = ""
        extract_date = False

        if extract_numerical_value:
            self.phrase_type = PHRASE_TYPE_NUM
        elif extract_date:
            self.phrase_type = PHRASE_TYPE_DATE
        else:
            self.phrase_type = PHRASE_TYPE_WORD

        self.patient_keyword = patient_keyword
        self.note_keyword = note_keyword
        self.extract_numerical_value = extract_numerical_value
        self.note_dicts = input_file.to_dict('records')

    def search_phrases(self, phrases):
        self.phrases = [p.strip() for p in phrases.split(',')]
        return(self._extract_values_from_notes(self.phrases))

    def _extract_values_from_notes(self, phrases):
        """Return a list of NotePhraseMatches for each note in note_dict."""
        note_phrase_matches = []

        if self.ignore_punctuation:
            phrases = [_remove_punctuation(phrase) for phrase in phrases]

        for note_dict in self.note_dicts:
            if self.ignore_punctuation:
                note_dict[self.note_keyword].translate(
                    None, string.punctuation)
            phrase_matches = self._extract_phrase_from_notes(note_dict)
            note_phrase_matches.append(phrase_matches)

        return(note_phrase_matches)

    def _extract_phrase_from_notes(self, note_dict):
        """Return a PhraseMatch object with the value as a binary 0/1 indicating
        whether one of the phrases was found in note"""

        string_lookup = {
            self.PHRASE_TYPE_WORD: [
                r'(\s%s\s)',
                r'(^%s\s)',
                r'(\s%s$)',
                r'(^%s)',
                r'(\s%s(?=\W))',
                r'(^%s(?=\W))'],
            self.PHRASE_TYPE_NUM: [r'(?:%s)\s*(?:of|is|was|were|are|\:)?[:]*[\s]*([0-9]+\.?[0-9]*)'],
            self.PHRASE_TYPE_DATE: [
                r'(?:%s)\s*(?:of|is|was|were|are|\:)?[:]*[\s]*(\d+/\d+/\d+)',
                r'(?:%s)\s*(?:of|is|was|were|are|\:)?[:]*[\s]*(\d+-\d+-\d+)']}

        pattern_strings = string_lookup[self.phrase_type]

        try:
            note = str(note_dict[self.note_keyword])
        except KeyError:
            print("Wrong Note Keyword entered")
            raise

        phrase_matches = NotePhraseMatches(note_dict)

        for phrase in self.phrases:

            for pattern_string in pattern_strings:

                pattern_string = pattern_string % phrase
                re_flags = re.I | re.M | re.DOTALL
                pattern = re.compile(pattern_string, flags=re_flags)
                match_iter = pattern.finditer(note)

                try:
                    while True:
                        match = next(match_iter)

                        try:
                            float_create = float(match.groups()[0])
                        except ValueError:
                            float_create = None

                        extracted_value_lookup = {
                            self.PHRASE_TYPE_WORD: 1,
                            self.PHRASE_TYPE_NUM: float_create,
                            self.PHRASE_TYPE_DATE: match.groups()[0]

                        }

                        extracted_value = extracted_value_lookup[self.phrase_type]

                        new_match = PhraseMatch(extracted_value, match.start(),
                                                match.end(), phrase)

                        phrase_matches.add_phrase_match(new_match)

                except StopIteration:
                    continue

        phrase_matches.finalize_phrase_matches()
        return phrase_matches

<<<<<<< HEAD




    def _filter_rpdr_notes_by_column_val(self,
                                          rpdr_notes,
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



    def clean_df(self,df, text_columns, needs_decode=True):
        # ALL NOTES
        # TODO
        # SPECIFY DTYPES????? MAYBE IDK HOW

        for label in text_columns:
            if label in df:
                df[label] = df[label].map(lambda x: clean_phrase(x, needs_decode))
        new_df = pd.DataFrame(columns=df.columns)
        for index, row in df.iterrows():
            new_df = new_df.append(row)
        return new_df



    def _write_csv_output(self,note_phrase_matches, note_key, output_fname):
        """Write one CSV row for each phrase_match where the row contains all of
        the RPDR note keys along with the extracted numerical value at the end of
        the row."""

=======
    def _findMaches(self, note_phrase_matches, note_key):
>>>>>>> 22669b543280746f650297b93b29db203e2224cc
        dict_list = []
        for note_phrase_match in note_phrase_matches:

            note = note_phrase_match.note_dict[self.note_keyword]
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

<<<<<<< HEAD
            extracted_value = 0

            if len(note_phrase_match.phrase_matches) > 0:
                extracted_value = note_phrase_match.phrase_matches[0].extracted_value

            note_phrase_match.note_dict['MATCHES'] = matches
            note_phrase_match.note_dict['EXTRACTED_VALUE'] = extracted_value
            dict_list.append(note_phrase_match.note_dict)

        df = pd.DataFrame(dict_list)
        df['MATCHES'] = df['MATCHES'].astype('object')
        df.index = np.arange(0, df.shape[0])
        df = self.clean_df(df, [RPDR_NOTE_KEYWORD], False)

        #df.to_csv('diff.csv',encoding="utf-8")

        with open(output_fname, mode='w', newline='\n') as f:
            df.to_csv(f, sep=",", float_format='%.2f',
                              index=True)

        #writer = pd.ExcelWriter(output_fname[:-4] + '.xlsx')
        #df.to_excel(writer, 'Sheet1')
=======
        return matches
>>>>>>> 22669b543280746f650297b93b29db203e2224cc


PHRASE_TYPE_WORD = 0
PHRASE_TYPE_NUM = 1
PHRASE_TYPE_DATE = 2

RPDR_NOTE_KEYWORD = 'NOTE'
RPDR_PATIENT_KEYWORD = 'EMPI'


def run_regex(
        input_filename,
        phrases,
        row,
        is_rpdr=True,
        note_keyword=RPDR_NOTE_KEYWORD,
        patient_keyword=RPDR_PATIENT_KEYWORD,
        extract_numerical_value=False,
        extract_date=False,
        report_description=None,
        report_type=None,
        ignore_punctuation=False):

    note = ClinicianNotes(
        input_filename,
        row,
        is_rpdr=is_rpdr,
        note_keyword=note_keyword,
        patient_keyword=patient_keyword)
    note_phrase_matches = note.search_phrases(phrases)
    return note._findMaches(note_phrase_matches, note_keyword)
