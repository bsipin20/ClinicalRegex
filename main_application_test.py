import unittest
from main_application import get_matches_repo_num
#
class MainAppTestCase(unittest.TestCase):
    def test_get_matches_repo_num(self):
        df = pd.read_csv("test_deidentified_rpdr_format.txt",header=0)
        matches = src.main_appication.get_matches_repo_num(df,1000000)

        
        print(matches)
 

if __name__ == '__main__':
    unittest.main()


