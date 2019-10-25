import pandas as pd
import numpy as np
import copy
from src.rpdr import ReadRPDR
import pandas as pd
from src.helpers import _process_raw


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

	def write_to_annotation(self, annotation):
		if self.output_df is None or self.current_row_index is None:
			return

		if self.annotation_key not in self.output_df:
			self.output_df[self.annotation_key] = np.nan
			self.output_df[self.annotation_key] = np.nan
		current_row_index = self.display_df.index[self.current_row_index]
		self.output_df.at[current_row_index, self.annotation_key] = annotation
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

class Model(object):
    def __init__(self,options_,file_location_):
        t = ReadRPDR(options=options_,file_location=file_location_).read_data()
        self.notes = []
        self.output_dicts = dict()
        for i in t:
            new_note = copy.deepcopy(i)
            self.notes.append(new_note)

    def first(self):
        self.current_index = 0
        self.cached_index = 0

        return(self.notes[self.current_index])

    def next(self):
        if self.current_index < self.cached_index:
            self.current_index +=1
            return(self.notes[self.current_index])
        elif self.current_index == self.cached_index:
            self.cached_index +=1
            self.current_index += 1
            current_note = self.notes[self.current_index]
            return(current_note)

    def get_annotation(self):
        note = self.output_dicts[self.current_index]
        annotation = ""
        if "annotation" in note:
            annotation = note['annotation']
        return(annotation)




    def write_to_annotation(self,annotation):
        note = self.notes[self.current_index]
        words = note['data']
        clean_words = _process_raw(words)


        output_dict = {
            "empi"  : note['metadata']['empi'],
            "mrn" : note['metadata']['mrn'],
            "mrn_type" : note['metadata']['mrn_type'],
            "report_description" : note['metadata']['report_description'],
            "report_status" : note['metadata']['report_status'],
            "report_type" : note['metadata']['report_type'],
            "text" : " ".join(clean_words[1:]),
            "annotation" : annotation
        }
        
        self.output_dicts[self.current_index] = output_dict 

    def get_patient_id(self):
        patient_key = 'empi'
        note = self.notes[self.current_index]
        return(note['metadata'][patient_key])

    def get_length(self):
        return(len(self.notes))

    def get_index(self):
        return(self.current_index)


    def prev(self):
        self.current_index -=1
        current_note = self.notes[self.current_index]

        return(current_note)
        
    def write_output(self,filename):
        final_output = list()
        
        for k,v in self.output_dicts.items():
            final_output.append(v)
        
        df = pd.DataFrame(final_output)
        file_ending = filename.split(".")[1]
        if file_ending == "csv":
            df.to_csv(filename)
        elif file_ending == "dta":
            df.to_stata(filename,version=117)
        
   
