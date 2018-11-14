import unittest
import src.extract_values 
#import run_regex

class ExtractValuesTestCase(unittest.TestCase):

    def test_run_regex(self):
        pass
    
    def test_process_rdpr_file_unannotated(self):
        notes = src.extract_values.process_rpdr_file_unannotated("test_deidentified_rpdr_format.txt")
        for i in notes:
            dict_ =i.get_dictionary()
    def test_filter_rdpr_notes_by_column_val(self):
        notes = src.extract_values.process_rpdr_file_unannotated("test_deidentified_rpdr_format.txt")
        filtered_notes = src.extract_values._filter_rpdr_notes_by_column_val(notes,None,None)

    def test_extract_values_from_notes(self):
        notes = src.extract_values.process_rpdr_file_unannotated("test_deidentified_rpdr_format.txt")
        note_dicts = [r.get_dictionary() for r in notes]
        notes = src.extract_values._extract_values_from_notes(note_dicts=note_dicts,phrase_type=0,phrases="patient",note_key="NOTE",ignore_punctuation=False)
        """ under stand note phrase objects """


    def test_extract_phrases_from_notes(self):
        notes = src.extract_values.process_rpdr_file_unannotated("test_deidentified_rpdr_format.txt")
        note_dicts = [r.get_dictionary() for r in notes]
        notes = src.extract_values._extract_phrases_from_notes(note_dicts=note_dicts,phrase_type=0,phrases="patient",note_key="NOTE",ignore_punctuation=False)
        """ under stand note phrase objects """



            
 
        
        #self.assertTrue(is_prime(5))

if __name__ == '__main__':
    unittest.main()


