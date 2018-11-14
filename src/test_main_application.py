import unittest
import main_application 
import tkinter as tk
import pandas as pd
from model import DataModel
from extract_values import multi_run_regex

class MainAppTestCase(unittest.TestCase):

    def test_get_matches_repo_num(self):
        root = tk.Tk()
        root.geometry('{}x{}'.format(900, 700))
        main_app = main_application.MainApplication(root).grid(column=0, row=0)
        print(main_app)
        title = "Clinical Notes Regular Expression Tool"
        root.title(title)
 
        print(main_app)
        df = pd.read_csv("/Users/bsipin_mb/lindvall/ClinicalRegex/output.csv",header=0)
        matches = main_app.get_matches_repo_num(df=df,report_num=1000000)
        
        print(matches)
 

if __name__ == '__main__':
    unittest.main()


