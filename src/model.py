import pandas as pd
import numpy as np
import copy
from src.rpdr import ReadRPDR
import pandas as pd
from src.helpers import _process_raw, _extract_phrase_from_notes,_clean_note_phrase


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
    def __init__(self,options_,file_location_,keywords_):
        t = ReadRPDR(options=options_,file_location=file_location_).read_data()

        self.process_all_notes(t,keywords_)


    def process_all_notes(self,t,keywords_):
        self.notes = []
        self.current_index = 0


        self.output_dicts = dict()
        self.keywords = keywords_

        numbered  = enumerate(t)

        for note,i in numbered:
            new_note = copy.deepcopy(i)
            matches = self.find_matches(i)
            new_note['matches'] = matches
            new_note['data'] = _process_raw(i['data'])
            self.notes.append(new_note)


    def filter_only_positives(self):
        self.original = copy.deepcopy(self.notes)
        self.positives = list()

        for i in self.notes:
            if len(i['matches']) > 0:
                self.positives.append(i)

        self.notes = copy.deepcopy(self.positives)

    def find_matches(self,current_note,index=None):
        #current_note_text = ""
        #if index:
        #    current_note_text = self.notes[index]
        #else:
        #    current_note_text = self.notes[self.current_index]
        cleaned_note = _process_raw(current_note['data'])
        phrases = self.keywords

        #= [p.strip() for p in self.keywords.split(",")]
        match_indices = _extract_phrase_from_notes(phrases,cleaned_note)
        return(match_indices)

    def refresh(self,checkvar):
        if checkvar:
            self.filter_only_positives()
        else:
            self.notes = self.original # backup

    def first(self):
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

    def prev(self):
        self.current_index -=1
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
            "annotation" : annotation,
            "matches" : note['matches']
        }
        
        self.output_dicts[self.current_index] = output_dict 

    def get_patient_id(self):
        patient_key = 'empi'
        note = self.notes[self.current_index]
        return(note['metadata'][patient_key])

    def get_length(self,positive=False):
        return(len(self.notes))

    def get_index(self):
        return(self.current_index)


       
    def write_output(self,filename,positive=False):
        final_output = list()
        
        for k,v in self.output_dicts.items():
            final_output.append(v)
        
        df = pd.DataFrame(final_output)
        file_ending = filename.split(".")[1]
        if file_ending == "csv":
            df.to_csv(filename)
        elif file_ending == "dta":
            df.to_stata(filename,version=117)
        
   
