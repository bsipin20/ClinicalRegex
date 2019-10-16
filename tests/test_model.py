import unittest
from unittest.mock import patch
from src.rpdr import ReadRPDR



class TestReadRPDR(unittest.TestCase):
    def testfind_matches(self):
        ret_val = find_matches("stuff","123 stuff 678")
        self.assertEqual([(3,7)],ret_val)

    def test_find_long_matches(self):
        with patch.object(ReadRPDR,"__init__",lambda x,y,z: None): 
            m = ReadRPDR(None,None)
            ret_val = find_matches(["stuff"],"123 stuff 678")
            self.assertEqual([(4,8)],ret_val)

    def test_find_long_matches_newline(self):
        with patch.object(ReadRPDR,"__init__",lambda x,y,z: None): 
            m = ReadRPDR(None,None)
            ret_val = find_matches(["stuff"],"123 stuff 678 stuff ")
            self.assertEqual([(4,8),(14,18)],ret_val)

    def testfind_matches_multi_doublespace(self):
        with patch.object(ReadRPDR,"__init__",lambda x,y,z: None): 
            m = ReadRPDR(None,None)
            ret_val = find_matches(["stuff"],"123  stuff 678 stuff ")
            self.assertEqual([(5,9),(15,19)],ret_val)



    def test_clean_note_phrase_newline(self):
        with patch.object(ReadRPDR,"__init__",lambda x,y,z: None): 
            m = ReadRPDR(None,None)
            ret_val = m._clean_note_phrase("\nstuff\r")
            self.assertEqual("stuff",ret_val)

    def test_clean_note_phrase_leading_space(self):
        with patch.object(ReadRPDR,"__init__",lambda x,y,z: None): 
            m = ReadRPDR(None,None)
            ret_val = m._clean_note_phrase("    stuff")
            self.assertEqual("stuff",ret_val)

    def test_create_sent_list(self):
        with patch.object(ReadRPDR,"__init__",lambda x,y,z: None): 
            m = ReadRPDR(None,None)
            ret_val = m._create_sent_list("test two three")
            self.assertEqual(("test","two","three"),ret_val,msg=ret_val)

    def test_create_sent_list_trailing_spaces(self):
        with patch.object(ReadRPDR,"__init__",lambda x,y,z: None): 
            m = ReadRPDR(None,None)
            ret_val = m._create_sent_list("test two three ")
            self.assertEqual(("test","two","three"),ret_val,msg=ret_val)

    def test_create_so_many_spaces(self):
        with patch.object(ReadRPDR,"__init__",lambda x,y,z: None): 
            m = ReadRPDR(None,None)
            ret_val = m._create_sent_list("test   two three ")
            self.assertEqual(("test","","","two","three",""),ret_val,msg=ret_val)

    def test_create_so_three_spaces(self):
        with patch.object(ReadRPDR,"__init__",lambda x,y,z: None): 
            m = ReadRPDR(None,None)
            ret_val = m._create_sent_list("test  two three ")
            self.assertEqual(("test","","two","three",""),ret_val,msg=ret_val)








    #def test_clean_note_phrase_(self):
    #    with patch.object(ReadRPDR,"__init__",lambda x,y,z: None): 
    #        m = ReadRPDR(None,None)
    #        ret_val = m._clean_note_phrase("car aaa car")
    #        self.assertEqual("stuff",ret_val)



















if __name__ == "__main__":
    unittest.main()
