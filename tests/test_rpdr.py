import sys
sys.path.append('.')
import unittest 
from mock import patch
from src.rpdr import ReadRPDR
from src.helpers import _clean_note_phrase,_process_raw,find_matches,_extract_phrase_from_notes
import copy
from src.model import Model



def test_IO():
    opts = { 
        'r_encoding' : 'utf-8',
        'preserve_header' : True
    }
    file_location = 'test_deidentified_rpdr_format.txt'
    t = Model(opts,file_location,"Patient")
    print(t.notes)



if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.abspath('../src/'))

    from src.rpdr import ReadRPDR


    test_IO()
    

	




