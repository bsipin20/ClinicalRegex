import sys
sys.path.append('.')
import unittest 
from mock import patch
from src.rpdr import ReadRPDR
from src.helpers import _clean_note_phrase,_process_raw,find_matches,_extract_phrase_from_notes
import copy



def test_IO():
    opts = { 
        'r_encoding' : 'utf-8',
        'preserve_header' : True
    }
    
    t = ReadRPDR(options=opts,file_location='test_deidentified_rpdr_format.txt').read_data()
    all_notes = []
    for i in t:
        new_note = copy.deepcopy(i)
        all_notes.append(new_note)

    #t = ReadRPDR().find_matches('
    #`t = ReadRPDR(options=opts,file_location='/home/brian-tp/Downloads/ ARE1__080519005036102066_MGH_Vis.txt').read_data()

    #first_note = next(t)
    #look = _process_raw(first_note['data'])
    #matches = find_matches('Patient',look)
    #matches = _extract_phrase_from_notes('Patient',look)

    





if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.abspath('../src/'))

    from src.rpdr import ReadRPDR


    test_IO()
    

	




