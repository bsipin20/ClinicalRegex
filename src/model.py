import pandas as pd
import numpy as np


# Maintains all of the data and handles the data manipulation for this application
class DataModel:
        def __init__(self):
                self.input_fname = None
                self.output_fname = None
                self.output_df = None
                self.display_df = None
                self.current_row_index = None
                self.num_notes = None
                self.annotation_key = 'ANNOTATION'


        def write_to_annotation(self, annotations):
                if self.output_df is None or self.current_row_index is None:
                        return

                key_check = "ANNOTATION_1"
                if key_check not in self.output_df:
                        self.output_df[key_check] = np.nan
                #for num in range(1,len(annotations)):
                 #   self.output_df[self.annotation_key] = np.nan
                for i in range(0,len(annotations)):
        
                    new_annotation_key = "ANNOTATION_" + str(i+1)
                    annotation = annotations[i]
                    current_row_index = self.display_df.index[self.current_row_index]
                    self.output_df.at[current_row_index, new_annotation_key] = annotation
                    self.output_df.to_csv(self.output_fname)

        def get_annotation(self):
                if self.annotation_key in self.output_df:
                        current_row_index = self.display_df.index[self.current_row_index]
                        val = self.output_df.at[current_row_index, self.annotation_key]
                        if val is not None and not pd.isnull(val):
                                try:
                                        return int(float(val))
                                except:
                                        return val
                return ''
