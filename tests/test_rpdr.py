import sys
sys.path.append('.')
import unittest 
from mock import patch
from src.rpdr import ReadRpdr

from src.rpdr import ReadRPDR


def test_IO():
    opts = { 
        'r_encoding' : 'utf-8',
        'preserve_header' : True
    }
    
    #t = ReadRPDR(options=opts,file_location='test_deidentified_rpdr_format.txt')
    #t = ReadRPDR().find_matches('
    #t = ReadRPDR(options=opts,file_location='/home/brian-tp/Downloads/ARE1__080519005036102066_MGH_Vis.txt')

    tester = t.read_data()

    first = next(tester)
    text = first['data']
    #print(type(text))
    str_ = ''.join(text)
    print(str_)
    #for i in text:
    #print(first['metadata'])
    #print(first.__dict__.keys)



if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.abspath('../src/'))

    from src.rpdr import ReadRPDR


    test_IO()
    

	




