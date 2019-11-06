import pandas as pd
import numpy as np
import copy
import csv
from src.rpdr import ReadRPDR
import pandas as pd
import ast
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
        """ initializes RPDR generator """ 

        self.current_index = 0
        
        if (file_location_.split(".")[1] == "csv") and not (options_['rpdr']):
            print(file_location_)

            with open(file_location_) as f:
                a = [{k: v for k, v in row.items()}
                    for row in csv.DictReader(f)]


            numbered  = enumerate(a)

            self.all_notes = list()

            for i,note in numbered:


                clean_words = _process_raw(note[options_['note_key']].split(" ")),


                match_indices = _extract_phrase_from_notes(keywords_,clean_words[0]),
                matches = match_indices[0]


                #new_note['empi'] = note[options_['patient_id']]
                #new_note['matches'] = str(matches),
                #new_note['extracted_value'] = 0,
                #new_note['text'] = note[options_['note_key']]
                #new_note['total_index'] = i
                new_note = {

                    'empi' : note[options_['patient_id']],
                    'matches' : str(matches),
                    'extracted_value' : 0,
                    'text' : note[options_['note_key']],
                    'total_index' : i

                }

                self.all_notes.append(new_note)




            self.current_index = 0
            self.all_notes = self.filter_positives(self.all_notes)





        elif file_location_.split(".")[1] == "csv":
            try:


                with open(file_location_) as f:
                    a = [{k: v for k, v in row.items()}
                        for row in csv.DictReader(f)]

                    a[options_['patient_id']] = a['empi']
                    a[options_['note_key']] = a['text']

                    self.all_notes = a

                    self.current_index = ast.literal_eval(self.all_notes[0]['last_row'])
            except TypeError:
                t = ReadRPDR(options=options_,file_location=file_location_)

                self.all_notes = self.process_all_notes(t,keywords_)
                self.all_notes = self.filter_positives(self.all_notes)





        else: 
            t = ReadRPDR(options=options_,file_location=file_location_)

            self.all_notes = self.process_all_notes(t,keywords_)
            self.all_notes = self.filter_positives(self.all_notes)

    def process_all_notes(self,t,keywords):
        """ creates own instance of new list and adds generator to  all_notes """ 

        notes = []
        self.current_index = 0

        for i,note in enumerate(t.read_data()):
            new_note = copy.deepcopy(note)
            clean_words = _process_raw(new_note['data'])
            match_indices = _extract_phrase_from_notes(keywords,clean_words)

            output_dict = {
                "empi"  : new_note['metadata']['empi'],
                "mrn" : new_note['metadata']['mrn'],
                "mrn_type" : new_note['metadata']['mrn_type'],
                "report_description" : new_note['metadata']['report_description'],
                "report_status" : new_note['metadata']['report_status'],
                "report_type" : new_note['metadata']['report_type'],
                "text" : " ".join(clean_words),
                "total_index" : i,
                "extracted_value" : 0,
                "annotation" : "",
                "positive_index" : "",
                "matches" : str(match_indices)
            }

            notes.append(output_dict)

        return(notes)

    def filter_positives(self,notes):
        all_notes = list()
        counter = 0

        for i in notes:
            if len(ast.literal_eval(i['matches'])) > 0:
                i['extracted_value'] = 1
                i['positive_index'] = counter
                counter += 1
            all_notes.append(i)
        return(all_notes)

    def write_to_annotation(self,annotation):
        self.all_notes[self.current_index]['annotation'] = annotation
    
    def refresh(self,checkvar):
        if checkvar:
            self.filter_only_positives()
        else:
            self.all_notes = self.original # backup


    def first(self,positive):

        reported_index = self.current_index

        if positive:
            while self.all_notes[self.current_index]['extracted_value'] < 1:
                self.current_index += 1
            reported_index = self.all_notes[self.current_index]['positive_index']

        current_note = self.all_notes[self.current_index]

        return(current_note,reported_index)

    def next(self,positive):
        self.current_index += 1
        reported_index = self.current_index

        if positive:
            while self.all_notes[self.current_index]['extracted_value'] < 1:
                self.current_index += 1
            reported_index = self.all_notes[self.current_index]['positive_index']

        current_note = self.all_notes[self.current_index]

        return(current_note,reported_index)


    def current(self,positive):
        reported_index= self.current_index

        if positive:

            while (self.all_notes[self.current_index]['extracted_value'] < 1):
                self.current_index += 1
            reported_index = self.all_notes[self.current_index]['positive_index']


        current_note = self.all_notes[self.current_index]

        return(current_note,reported_index)
 


    def prev(self,positive):
        self.current_index -=1
        reported_index = self.current_index

        if positive:
            while self.all_notes[self.current_index]['extracted_value'] < 1:
                self.current_index -= 1
            reported_index = self.all_notes[self.current_index]['positive_index']

        current_note = self.all_notes[self.current_index]
        return(current_note,reported_index)
 

    def get_annotation(self):
        note = self.all_notes[self.current_index]
        annotation = ""
        if "annotation" in note:
            annotation = note['annotation']
        return(annotation)


    def get_patient_id(self):
        patient_key = 'empi'
        note = self.all_notes[self.current_index]
        return(note['empi'])

    def get_num_notes_positive(self):
        num_notes = 0
        for i in self.all_notes:
            if i['extracted_value'] == 1:
                num_notes +=1
        return(num_notes)

    def get_num_notes(self):
        return(len(self.all_notes))


    def get_index(self):
        return(self.current_index)

       
    def write_output(self,filename,positive=False):
        """ no test function for this yet"""
        file_ending = filename.split(".")[1]
        df = pd.DataFrame(self.all_notes)
        df['last_row'] = self.current_index
        df = df.drop(columns="positive_index")
        if file_ending == "csv":
            df.to_csv(filename)
        elif file_ending == "dta":
            df.to_stata(filename,version=117)
        
   
