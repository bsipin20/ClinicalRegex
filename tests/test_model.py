import unittest
from unittest.mock import patch,Mock
#from src.rpdr import ReadRPDR


from src.helpers import find_matches,_process_raw,_extract_phrase_from_notes,AnnotationLedger



class TestReadRPDR(unittest.TestCase):

    def test_find_matches(self):
        test_note = ['The','patient','not','very','patient']
        ret_val = find_matches(["patient"],test_note)
        self.assertEqual([(4,10),(21,27)],ret_val)

    def test_process(self):
    

        test_note= ['Group', 'Designer', 'activity', 'Hyperspace', '', 'to', '', 'make', '', 'print', '', 'groups.', 'Contact', '','activity', 'your', 'technical', 'support',  'representative', 'for', 'more', 'information.', 'ED', 'Arrival', 'Information', '', 'Patient', 'not', 'seen', 'in', 'ED']



        ret_val = _process_raw(test_note)
        t = False
        if "" in ret_val: 
            t = True
        self.assertFalse(t)



    def test_Patient(self):
    

        test_note= ('Group', 'Designer', 'activity', '','','','', 'in', '', 'Hyperspace', '', 'to', '', 'make', '', 'print', '', 'groups.', '', 'Contact', '','activity', 'your', 'technical', 'support', '', 'representative', 'for', 'more', 'information.', '', 'ED', 'Arrival', 'Information', '', 'Patient', 'not', 'seen', 'in', 'ED')



        ret_val = find_matches(["activity"],test_note)
        self.assertEqual([],ret_val)

    def test_extract(self):
        test_note = ["find","activity","now"]
    





        ret_val = _extract_phrase_from_notes(["activity"],test_note)
        self.assertEqual([(4,14)],ret_val)

    def test_extract2(self):
        test_note = ["find","now","and","now"]


        ret_val = _extract_phrase_from_notes(["now"],test_note)
        self.assertEqual([(4,6),(12,14)],ret_val)


    def test_clean_note_phrase_newline(self):
        ret_val = _clean_note_phrase("\nstuff\r")
        self.assertEqual("stuff",ret_val)

    def test_clean_note_phrase_leading_space(self):
        ret_val = clean_note_phrase("    stuff")
        self.assertEqual("stuff",ret_val)

    def test_create_sent_list(self):
        ret_val = create_sent_list("test two three")
        self.assertEqual(("test","two","three"),ret_val,msg=ret_val)

    def test_create_sent_list_trailing_spaces(self):
        ret_val = create_sent_list("test two three ")
        self.assertEqual(("test","two","three"),ret_val,msg=ret_val)

    def test_create_so_many_spaces(self):
        ret_val = create_sent_list("test   two three ")
        self.assertEqual(("test","","","two","three",""),ret_val,msg=ret_val)

    def test_create_so_three_spaces(self):
        ret_val = create_sent_list("test  two three ")
        self.assertEqual(("test","","two","three",""),ret_val,msg=ret_val)


from src.model import Model

class TestModel(unittest.TestCase):

    @patch('src.rpdr.ReadRPDR')
    @patch('src.model.Model.output_dicts')
    def test_write_output(self,mock_RPDR,model_data):
        mock_RPDR.read_data.return_value = True
        note_one = {'note' : "Note1", "id" : 1}
        note_two = {'note' : "Note2", "id" : 2}
        test_obj = Model().prepare_output()
        self.assertEqual(1,result)


if __name__ == "__main__":
    unittest.main()
