import unittest
# import unittest.mock as mock
from mock import patch

from extract_values import NotePhraseMatches, _extract_phrase_from_notes, _extract_values_from_notes
from extract_values import RPDRNote


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

        rpdr_note3 = extract_values.RPDRNote(
            {'EMPI': 'empi3', 'MRN_Type': 'mrn_type3',
             'Report_Number': '1233', 'MRN': '1233',
             'Report_Type': 'report_type3',
             'Report_Description': 'report_description3'}, 'note3')

        self.rpdr_notes = [rpdr_note1, rpdr_note2, rpdr_note3]

    def test_no_filters_does_nothing(self):
        filtered_rpdr_notes = (
            extract_values._filter_rpdr_notes_by_column_val(
                self.rpdr_notes, None, None))
        self.assertEqual(self.rpdr_notes, filtered_rpdr_notes)

    def test_one_filter_works(self):
        filtered_rpdr_notes = (
            extract_values._filter_rpdr_notes_by_column_val(
                self.rpdr_notes, 'report_description1', None))
        self.assertEqual(1, len(filtered_rpdr_notes))

    def test_two_filters_work(self):
        filtered_rpdr_notes = (
            extract_values._filter_rpdr_notes_by_column_val(
                self.rpdr_notes, 'report_description1',
                'report_type1'))
        self.assertEqual(1, len(filtered_rpdr_notes))

    def test_extract_phrase_notes(self):
        phrases = ['hospice', 'patient']
        phrases = [extract_values._remove_punctuation(phrase) for phrase in phrases]
        rpdr_note2.remove_punctiation_from_note()
        not_phrase_matches= extract_values._extract_phrase_from_notes(0, phrases, rpdr_note2, phrase_match_context)
        phrase_matches=note_phrase_matches.phrase_matches
        self.assertEqual(2, len(phrase_matches))
        self.assertEqual(0, phrase_matches[0].match_start)
        self.assertEqual(10, phrase_matches[0].match_end)
        for phrase_match in phrase_matches:
            self.assertEqual(1, phrase_match.extracted_value)


    def test_three_filter(self):
        filtered_rpdr_notes=(
            extract_values._extract_phrase_from_notes(
                self.rpdr_notes, 'report_description1',
                'report_type1'))
        self.assertEqual(1, len(filtered_rpdr_notes))



if __name__ == "__main__":
    unittest.main()
