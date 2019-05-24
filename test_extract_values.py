import unittest
# import unittest.mock as mock
from mock import patch

import src.extract_values as extract_values
from io import StringIO

#from src.extract_values import NotePhraseMatches, _extract_phrase_from_notes, _extract_values_from_notes
#from src.extract_values import RPDRNote


test_xlsx = 'test_data.xlsx'
test_xls = 'test_data.xls'
test_txt = 'test_data.txt'



#def load_test_data(filetype):
#    global test_data_obj,test_data_row_list 



class TestExtractValues(unittest.TestCase):
    def setUp(self):
        rpdr_note1 = extract_values.RPDRNote(
            {'EMPI': 'empi1', 'MRN_Type': 'mrn_type1',
             'Report_Number': '1231', 'MRN': '1231',
             'Report_Type': 'report_type1',
             'Report_Description': 'report_description1'}, 'note1')

        rpdr_note2 = extract_values.RPDRNote(
            {'EMPI': 'empi2', 'MRN_Type': 'mrn_type2',
             'Report_Number': '1232', 'MRN': '1232',
             'Report_Type': 'report_type2',
             'Report_Description': 'report_description2'}, 'note2')

        for note in note_dicts:

            self.rpdr_notes = [rpdr_note1, rpdr_note2]

#    def test_no_filters_does_nothing(self):
#        filtered_rpdr_notes = (
#            extract_values._filter_rpdr_notes_by_column_val(
#                self.rpdr_notes, None, None))
#        self.assertEqual(self.rpdr_notes, filtered_rpdr_notes)
#
#    def test_extract_phrase_notes(self):
#        phrases = ['hospice', 'patient']
#        phrases = [extract_values._remove_punctuation(phrase) for phrase in phrases]
#        print(phr
#        rpdr_note2.remove_punctiation_from_note()
#        not_phrase_matches= extract_values._extract_phrase_from_notes(0, phrases, rpdr_note2, phrase_match_context)
#        phrase_matches=note_phrase_matches.phrase_matches
#        self.assertEqual(2, len(phrase_matches))
#        self.assertEqual(0, phrase_matches[0].match_start)
#        self.assertEqual(10, phrase_matches[0].match_end)
#        for phrase_match in phrase_matches:
#            self.assertEqual(1, phrase_match.extracted_value)
#
#
#    def test_three_filter(self):
#        filtered_rpdr_notes=(
#            extract_values._extract_phrase_from_notes(
#                self.rpdr_notes, 'report_description1',
#                'report_type1'))
#        self.assertEqual(1, len(filtered_rpdr_notes))


class TestRPDR(unittest.TestCase):
    def setUp(self):
        self.rpdr_file = StringIO("""\
            100000|HSP|10000|3000|10000|8/24/2014 12:00:00 AM|ED Discharge Summary|Final|DIS|Patient Hospice
            [report_end]
        """)    
        rpdr_note_1 = {'REPORT_NUMBER': '1000000', 'NOTE': "Report Status: Final\rED DISCHARGE NOTIFICATION\r\rThe patient presented with a chief complaint of sbo\rFollowing evaluation and treatment, the patient's disposition at the end of the\rvisit was admitted as an inpatient.\rPlease note this\rinformation may have been updated on the inpatient unit.\n", 'EMPI': '100000000', 'MRN_TYPE': 'HSP', 'MRN': '1000000', 'REPORT_TYPE': 'DIS', 'REPORT_DESCRIPTION': 'ED Discharge Summary', 'REPORT_DATE': '8/01/2011 12:00:00 AM'}

    def test_rpdr(self):
        file_ = "test_deidentified_rpdr_format.txt"
        f = extract_values.process_rpdr_file_unannotated(file_)
        t = extract_values._filter_rpdr_notes_by_column_val(f,None,None)
        note_dicts = [r.get_dictionary() for r in t]
        print(note_dicts[1])


class TestDependencies(unittest.TestCase):
    def test_correct_pandas(self):
        pass

    def test_correct_openpyxl(self):
        pass

       



if __name__ == "__main__":
    unittest.main()
