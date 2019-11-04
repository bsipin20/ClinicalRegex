import tkinter as tk
from tkinter import font, filedialog, messagebox
from src.model import DataModel
from src.extract_values import run_regex
from src.rpdr import ReadRPDR
from src.helpers import find_matches,_extract_phrase_from_notes,_process_raw,AnnotationLedger
from src.model import Model
import pandas as pd
import ast
import re
import time
import os


class MainApplication(tk.Frame):
    def __init__(self, master):

        tk.Frame.__init__(self, master)
        self.master = master
        self.setup_interface(master)
        self.data_model = DataModel()
        self.checkvar = False

    # Set up button click methods
    def on_select_file(self):
        self.disable_button()
        self.load_annotation = False
        self.data_model = DataModel()
        self.checkvar = False
        chkValue = tk.BooleanVar()
        chkValue.set(False)
        self.positive_checkbox.config(var=chkValue)

        file = filedialog.askopenfilename(title="Select File")
        if file:
            self.data_model.input_fname = file
<<<<<<< HEAD
            self.file_text.config(text=self.data_model.input_fname.split('/')[-1])

    def on_select_output_file(self):
        self.output_fname = filedialog.askopenfilename(title="Select Output File")

        if output_fname:
            # Change note-key
            rpdr_checkbox = self.rpdr_checkbox.var.get()
            if rpdr_checkbox == 0:
                self.note_key = self.note_key_entry.get()
                self.patient_key = self.patient_id_entry.get()
            self.refresh_viewer(output_fname)


    def on_run_regex(self):
        """ Passes clinician note file to Model """ 

        self.phrases = self.regex_text.get(1.0, 'end-1c').strip()

        # GETS FILE NAMe, passes global path to ReadRPDR
        file_loc = self.data_model.input_fname
 
        #self.output_fname = '/'.join(self.data_model.input_fname.split('/')[:-1]) + '/' + self.regex_label.get()


        opts = {
            'r_encoding' : 'utf-8',
            'preserve_header' : True
        }
        phrases = [p.strip() for p in self.phrases.split(",")]



        self.model = Model(options_=opts,file_location_=file_loc,keywords_=phrases)

        first_note = self.model.first()
    
        self.display_output_note(first_note)


    def write_out_output_csv(self):
        #output_fname = filedialog.asksaveasfile(title="Select Output File",filetypes=("

        self.model.write_output("output.csv",self.checkvar)

    def write_out_output_stata(self):
        #output_fname = filedialog.asksaveasfile(title="Select Output File",filetypes=("

        self.model.write_output("output.dta",self.checkvar)



    def display_output_note(self,current_note_row):

        """ displays highlighting """ 

        current_note_text= current_note_row['data']
        current_patient_id = current_note_row['metadata']['empi']
        match_indices = current_note_row['matches']

        self.number_label.config(text='%d of %d' % (self.model.get_index()+ 1, self.model.get_length(self.checkvar)))
        self.patient_num_label.config(text='Patient ID: %s' % self.model.get_patient_id())


        tag_start = '1.0'

        # Add highlighting 
=======
            self.file_text.config(
                text=self.data_model.input_fname.split('/')[-1])
        f = self.data_model.input_fname.split('.')[-1]
        ## RPDR format ##
        if f == 'txt':
            csvfile = ''.join(
                self.data_model.input_fname.split('.')[
                    :-1]) + '.csv'
            # corresponding CSV already exist
            if os.path.isfile(csvfile) and 'report_text' in pd.read_csv(
                    csvfile).columns.values.tolist():
                self.data_model.input_fname = ''.join(
                    self.data_model.input_fname.split('.')[:-1]) + '.csv'
            # reformat RPDR to CSV file
            else:
                with open(self.data_model.input_fname, 'r') as file:
                    data, header, fields = [], [], []
                    for line in file:
                        line = line.rstrip()
                        if line.strip() == '':
                            continue
                        if not header:
                            if line.count('|') < 8:
                                messagebox.showerror(
                                    title="Error",
                                    message="Something went wrong, did you select an appropriately formatted RPDR file to perform the Regex on?")
                                return
                            header = [field.lower().strip()
                                      for field in line.split('|')]
                            continue
                        if not fields and '|' in line:
                            fields = [field.lower().strip()
                                      for field in line.split('|')]
                            fields[-1] = line
                            report = []
                        elif 'report_end' in line:
                            report.append(line)
                            fields[-1] += '\n'.join(report)
                            data.append(fields)
                            fields = []
                        else:
                            report.append(line)
                data = pd.DataFrame(data, columns=header)
                self.data_model.input_fname = ''.join(
                    self.data_model.input_fname.split('.')[:-1]) + '.csv'
                data.to_csv(self.data_model.input_fname, index=False)

        self.regex_button.config(state='normal')
        self.load_button.config(state='normal')

        # set the default value of note and id key
        if f in ['csv', 'txt']:
            self.note_key_entry = tk.StringVar(self.right_options_frame)
            self.patient_id_entry = tk.StringVar(self.right_options_frame)
            OPTIONS = pd.read_csv(
                self.data_model.input_fname).columns.values.tolist()
            if f == 'csv' or 'report_text' not in OPTIONS or 'empi' not in OPTIONS:
                self.note_key_entry.set(OPTIONS[1])
                self.patient_id_entry.set(OPTIONS[0])
            else:
                self.note_key_entry.set('report_text')
                self.patient_id_entry.set('empi')
            try:
                self.note_key_entry_menu = tk.OptionMenu(
                    self.right_options_frame, self.note_key_entry, *OPTIONS)
                self.note_key_entry_menu.grid(column=1, row=1, sticky='we')
                self.note_key_entry_menu.config(
                    font=font.Font(family='Roboto', size=12))
                self.patient_id_entry_menu = tk.OptionMenu(
                    self.right_options_frame, self.patient_id_entry, *OPTIONS)
                self.patient_id_entry_menu.grid(column=1, row=2, sticky='we')
                self.patient_id_entry_menu.config(
                    font=font.Font(family='Roboto', size=12))
            except BaseException:
                messagebox.showerror(
                    title="Error",
                    message="Something went wrong, did you select an appropriately file to perform the Regex on?")
                return
        else:
            messagebox.showerror(
                title="Error",
                message="Something went wrong, did you select an appropriately formatted RPDR or CSV file to perform the Regex on?")
            return

    def on_run_regex(self):
        if not self.data_model.input_fname:
            messagebox.showerror(
                title="Error",
                message="Please select an input file using the 'Select File' button.")
            return

        # Retrieve phrases
        self.phrases = {}
        for i in range(1, 4):
            self.phrases[i] = self.regex_text[i].get(1.0, 'end-1c').strip()
            self.label_name[i] = self.label_text[i].get(1.0, 'end-1c').strip()

        if self.phrases[1] == self.original_regex_text or len(
                self.phrases[1]) == 0:
            messagebox.showerror(
                title="Error",
                message="Please input comma-separated phrases to search for. ")
            return

        # get the note and id key from CSV or RPDR file
        self.note_key = self.note_key_entry.get()
        self.patient_key = self.patient_id_entry.get()
        if not self.note_key:
            messagebox.showerror(
                title='Error',
                message='Please input the column name for notes.')
            return
        if not self.patient_key:
            messagebox.showerror(
                title='Error',
                message='Please input the column name for patient IDs.')
            return

        self.enable_button()
        self.load_button.config(state='disabled')

    def on_load_annotation(self):
        if not self.data_model.input_fname or '.csv' not in self.data_model.input_fname:
            messagebox.showerror(
                title="Error",
                message="Please select an input file using the 'Select File' button.")
            return
        self.phrases = {}
        self.load_annotation = True
        self.regex_button.config(state='disabled')
        self.data_model.output_df = pd.read_csv(
            self.data_model.input_fname)
        columns = self.data_model.output_df.columns.values.tolist()
        if len(columns) not in [6, 10, 14] or 'L1_' not in columns[2]:
            messagebox.showerror(
                title="Error",
                message="Something went wrong, did you select an appropriately output CSV file?")
            return
        self.patient_key, self.note_key = columns[:2]
        self.label_name[1] = columns[2][3:]
        self.phrases[2] = self.phrases[3] = self.original_regex_text

        if len(columns) == 6:
            self.phrases[1] = columns[-1][3:]
        elif len(columns) == 10:
            self.label_name[2] = columns[5][3:]
            self.phrases[1] = columns[-2][3:]
            self.phrases[2] = columns[-1][3:]
        elif len(columns) == 14:
            self.label_name[2] = columns[5][3:]
            self.label_name[3] = columns[8][3:]
            self.phrases[1] = columns[-3][3:]
            self.phrases[2] = columns[-2][3:]
            self.phrases[3] = columns[-1][3:]

        for i in range(1, 4):
            if len(columns) >= (2 + i * 4):
                self.label_text[i].delete(1.0, tk.END)
                self.label_text[i].insert(tk.END, self.label_name[i])
                self.regex_text[i].delete(1.0, tk.END)
                self.regex_text[i].insert(tk.END, self.phrases[i])

        self.enable_button()

    def enable_button(self):
        self.prev_button.config(state='normal')
        self.next_button.config(state='normal')
        self.add_ann_button.config(state='normal')
        self.del_ann_button.config(state='normal')
        self.save_button.config(state='normal')

        output_fname = self.regex_label.get()
        self.refresh_viewer(output_fname)

    def disable_button(self):
        self.prev_button.config(state='disabled')
        self.next_button.config(state='disabled')
        self.add_ann_button.config(state='disabled')
        self.del_ann_button.config(state='disabled')
        self.save_button.config(state='disabled')

    # Functions that change display
    def refresh_viewer(self, output_fname):
        def clean_phrase(phrase):
            cleaned = str(phrase.replace('||', '|').replace('\\r', '\\n'))
            cleaned = re.sub(r'(\n+|\r\r)', '\n', cleaned)
            cleaned = re.sub(r'( +|\t+)', ' ', cleaned)
            cleaned = re.sub(r'\r', '', cleaned)
            return str(cleaned.strip())

        # run regex
        try:
            if not self.load_annotation:
                self.data_model.output_df = pd.read_csv(
                    self.data_model.input_fname, usecols=[
                        self.patient_key, self.note_key])
                self.data_model.output_df[self.note_key] = self.data_model.output_df[self.note_key].apply(
                    lambda x: clean_phrase(x))
            else:
                self.data_model.output_df = pd.read_csv(
                    self.data_model.input_fname)
            # Display only positive hits
            if self.checkvar:
                phrases = []
                for i in range(1, 4):
                    if self.phrases[i] != self.original_regex_text and len(
                            self.phrases[i]) > 0:
                        phrases.extend(self.phrases[i].split(','))
                        if not self.load_annotation:
                            self.data_model.output_df['L%d_' %
                                                      i + self.label_name[i]] = 0
                            self.data_model.output_df['L%d_' %
                                                      i + self.label_name[i] + '_span'] = None
                            self.data_model.output_df['L%d_' %
                                                      i + self.label_name[i] + '_text'] = None
                self.data_model.output_df['regex'] = self.data_model.output_df[self.note_key].apply(
                    lambda x: 1 if any(re.search(p, x.lower()) for p in phrases) else 0)
                self.data_model.nokeyword_df = self.data_model.output_df[self.data_model.output_df['regex'] == 0].reset_index(
                    drop=True)
                self.data_model.output_df = self.data_model.output_df[self.data_model.output_df['regex'] == 1].reset_index(
                    drop=True)
                self.data_model.output_df = self.data_model.output_df.drop(columns=[
                    'regex'])
                self.data_model.nokeyword_df = self.data_model.nokeyword_df.drop(columns=[
                    'regex'])
            else:
                self.data_model.nokeyword_df = []
        except BaseException:
            messagebox.showerror(
                title="Error",
                message="Something went wrong, did you select an appropriately columns?")
            return
        self.data_model.output_fname = output_fname
        self.refresh_model()

    def refresh_model(self):
        if not self.load_annotation:
            self.data_model.current_row_index = 0
        else:
            try:
                self.data_model.current_row_index = self.data_model.output_df.index[
                    self.data_model.output_df['L1_' + self.label_name[1]] == 0].tolist()[0]
            except BaseException:
                self.data_model.current_row_index = 0

        if self.data_model.input_fname:
            try:
                self.data_model.display_df = self.data_model.output_df.copy()
                self.data_model.num_notes = self.data_model.display_df.shape[0]
                self.display_output_note()
            except BaseException:
                pass

    def display_output_note(self):
        current_note_row = self.data_model.display_df.iloc[self.data_model.current_row_index]
        try:
            current_note_text = current_note_row[self.note_key]
        except BaseException:
            messagebox.showerror(
                title='Error',
                message='Unable to retrieve note text. Did you select the correct key?')
            return

        try:
            current_patient_id = current_note_row[self.patient_key]
        except BaseException:
            messagebox.showerror(
                title='Error',
                message='Unable to retrieve patient ID. Did you select the correct key?')
            return

        self.number_label.config(
            text='%d of %d' %
            (self.data_model.current_row_index + 1, self.data_model.num_notes))
        self.patient_num_label.config(
            text='Patient ID: %s' %
            current_patient_id)
>>>>>>> 22669b543280746f650297b93b29db203e2224cc

        self.pttext.config(state=tk.NORMAL)
        self.pttext.delete(1.0, tk.END)
        self.pttext.insert(tk.END, " ".join(current_note_text))
        self.pttext.config(state=tk.DISABLED)
        print(match_indices)

<<<<<<< HEAD
=======
        input_df = self.data_model.display_df.iloc[[
            self.data_model.current_row_index]]
        for i in range(1, 4):
            if self.phrases[i] != self.original_regex_text and len(
                    self.phrases[i]) > 0:
                self.find_matches(
                    self.phrases[i],
                    "keyword_%d" %
                    i,
                    "L%d_" %
                    i +
                    self.label_name[i] +
                    '_span',
                    input_df)

        self.pttext.tag_raise("sel")
        self.length, l = {}, 0
        for i in range(1, int(self.pttext.index("end").split('.')[0])):
            self.length[i] = l
            l += int(self.pttext.index(str(i) + ".end").split('.')[1]) + 1

    def find_matches(
            self,
            phrases,
            keyword,
            label_name,
            input_df):
        match_indices = self.data_model.output_df.at[self.data_model.current_row_index, label_name]

        if match_indices and isinstance(match_indices, str):
            match_indices = [i.split(',') for i in match_indices.split('|')]
        else:
            match_indices = run_regex(
                input_df,
                phrases,
                self.data_model.current_row_index,
                False,
                self.note_key,
                self.patient_key)
>>>>>>> 22669b543280746f650297b93b29db203e2224cc

        tag_start = '1.0'
        # Add highlighting
        for start, end in match_indices:
            pos_start = '{}+{}c'.format(tag_start, start)
            pos_end = '{}+{}c'.format(tag_start, end)
<<<<<<< HEAD
            self.pttext.tag_add('highlighted', pos_start, pos_end)

        self.show_annotation()

    def show_annotation(self):

        self.ann_textbox.delete(0, tk.END)
        try: 
            view = self.model.get_annotation()
        except KeyError:
            view = ""
        self.ann_textbox.insert(0, view)

    #def on_save_annotation(self):

    def on_prev(self):

        current_note_row = self.model.prev()
        self.display_output_note(current_note_row)
        
        
=======
            self.pttext.tag_add(keyword, pos_start, pos_end)

    def save_matches(self, keyword, label_name):
        tags = self.pttext.tag_ranges(keyword)
        match = ''
        text = ''
        for i in range(0, len(tags), 2):
            s = str(tags[i]).split('.')
            e = str(tags[i + 1]).split('.')
            start = int(s[1]) + self.length[int(s[0])]
            end = int(e[1]) + self.length[int(e[0])]
            if i > 0:
                text += '|'
                match += '|'
            text += '{}'.format(self.pttext.get(tags[i], tags[i + 1]))
            match += '{},{}'.format(start, end)
        current_row_index = self.data_model.display_df.index[self.data_model.current_row_index]
        self.data_model.output_df.at[current_row_index, label_name] = 1
        self.data_model.output_df.at[current_row_index,
                                     label_name + '_span'] = match
        self.data_model.output_df.at[current_row_index,
                                     label_name + '_text'] = text

    def on_save_annotation(self):
        if self.data_model.output_fname[-4:] not in ['.csv', '.dta']:
            messagebox.showerror(
                title='Error',
                message='Did you key in the correct CSV or DTA output filename?')
        for i in range(1, 4):
            if self.phrases[i] != self.original_regex_text and len(
                    self.phrases[i]) > 0:
                self.save_matches(
                    "keyword_%d" %
                    i,
                    'L%d_' %
                    i +
                    self.label_name[i])
                self.data_model.output_df['K%d_' %
                                          i + str(self.phrases[i])] = ''
        if len(self.data_model.nokeyword_df) > 0:
            self.data_model.save_df = pd.concat(
                [self.data_model.output_df, self.data_model.nokeyword_df], axis=0, sort=False)
        else:
            self.data_model.save_df = self.data_model.output_df
        self.data_model.write_to_annotation()

    def on_prev(self):
        self.on_save_annotation()
        if self.data_model.current_row_index > 0:
            self.data_model.current_row_index -= 1
        self.display_output_note()

>>>>>>> 22669b543280746f650297b93b29db203e2224cc
    def on_next(self):
        annotation = self.ann_textbox.get()
        if len(annotation) > 0:

            self.model.write_to_annotation(annotation)

        current_note_row= self.model.next()
        self.display_output_note(current_note_row)
 

    def on_add_annotation(self):
        self.modify_annotation('add')

    def on_delete_annotation(self):
        self.modify_annotation('delete')

    def modify_annotation(self, action):
        if self.pttext.tag_ranges(tk.SEL):
            if self.label == 1:
                keyword = "keyword_1"
            elif self.label == 2:
                keyword = "keyword_2"
            else:
                keyword = "keyword_3"
            s0 = self.pttext.index("sel.first").split('.')
            s1 = self.pttext.index("sel.last").split('.')
            pos_start = '{}.{}'.format(*s0)
            pos_end = '{}.{}'.format(*s1)
            self.pttext.tag_remove(tk.SEL, "1.0", tk.END)
            if action == 'add':
                self.pttext.tag_add(keyword, pos_start, pos_end)
            else:
                self.pttext.tag_remove(keyword, pos_start, pos_end)
        else:
            messagebox.showerror(
                title='Error',
                message='No text selected!')

    def clear_textbox(self, event, widget, original_text):
        if widget.get(1.0, 'end-1c') == original_text:
            widget.delete(1.0, 'end-1c')

    def on_positive_checkbox_click(self, event, widget):
        if self.checkvar:
            self.checkvar = False
        else:
            self.checkvar = True
<<<<<<< HEAD
        
        self.model.refresh(self.checkvar)
=======
>>>>>>> 22669b543280746f650297b93b29db203e2224cc

        if self.data_model.output_df is not None:
            self.on_run_regex()
        self.refresh_model()

    def on_radio_click(self):
        self.label = self.radio_value.get()
        for i in range(1, 4):
            self.regex_text[i].configure(bg='white')
            self.label_text[i].configure(
                font=font.Font(family='Roboto', size=14))

        color = {1: '#ffe6ff', 2: '#e6e6ff', 3: '#fff2e6'}
        i = self.label
        self.regex_text[i].configure(bg=color[i])
        self.label_text[i].configure(
            font=font.Font(
                family='Roboto',
                size=14,
                weight='bold'))

    def setup_interface(self, root):
        # Define fonts
        titlefont = font.Font(family='Open Sans', size=18, weight='bold')
        boldfont = font.Font(size=16, family='Open Sans', weight='bold')
        textfont = font.Font(family='Roboto', size=14)
        labelfont = font.Font(family='Roboto', size=12)

        left_bg_color = 'lightblue1'
        right_bg_color = 'azure'
        # Creating all main containers
        left_frame = tk.Frame(root, bg=left_bg_color)
        right_frame = tk.Frame(root, bg=right_bg_color)

        # Laying out all main containers
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)

        left_frame.grid(
            column=0,
            row=0,
            columnspan=2,
            rowspan=2,
            sticky='nsew')
        left_frame.grid_rowconfigure(0, weight=1)
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_rowconfigure(2, weight=1)
        left_frame.grid_rowconfigure(3, weight=1)
        left_frame.grid_rowconfigure(4, weight=1)
        left_frame.grid_rowconfigure(5, weight=1)
        left_frame.grid_rowconfigure(6, weight=1)
        left_frame.grid_rowconfigure(7, weight=1)
        left_frame.grid_rowconfigure(8, weight=1)
        left_frame.grid_rowconfigure(9, weight=1)
        left_frame.grid_rowconfigure(10, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_columnconfigure(1, weight=1)

        right_frame.grid(column=2, row=0, columnspan=2, sticky='nsew')
        right_frame.grid_rowconfigure(0, weight=1)
        right_frame.grid_rowconfigure(1, weight=1)
        right_frame.grid_rowconfigure(2, weight=1)
        right_frame.grid_rowconfigure(3, weight=1)
        right_frame.grid_rowconfigure(4, weight=1)
        right_frame.grid_rowconfigure(5, weight=1)
        right_frame.grid_rowconfigure(6, weight=1)
        right_frame.grid_rowconfigure(7, weight=1)
        right_frame.grid_rowconfigure(8, weight=1)
        right_frame.grid_rowconfigure(9, weight=1)
        right_frame.grid_rowconfigure(10, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        # Buttons
        header_frame = tk.Frame(left_frame, bg=left_bg_color)
        header_frame.grid(
            column=0,
            row=0,
            columnspan=2,
            padx=10,
            pady=10,
            sticky='nsew')
        header_frame.grid_propagate(False)
        header_frame.grid_rowconfigure(0, weight=1)
        header_frame.grid_rowconfigure(1, weight=1)
        header_frame.grid_columnconfigure(0, weight=2)
        header_frame.grid_columnconfigure(1, weight=1)
        header_frame.grid_columnconfigure(2, weight=1)

        title_text = tk.Label(
            header_frame,
            text='Clinical Note',
            font=titlefont,
            bg=left_bg_color)
        title_text.grid(column=0, row=0, sticky='w')

        button_frame = tk.Frame(header_frame, bg=left_bg_color)
        button_frame.grid(column=0, row=1, columnspan=1, sticky='nsew')
        button_frame.grid_propagate(False)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)
        button_frame.grid_rowconfigure(0, weight=1)
        button_frame.grid_rowconfigure(1, weight=1)

        self.prev_button = tk.Button(
            button_frame,
            text='Prev',
            width=5,
            state='disabled',
            command=self.on_prev)
        self.prev_button.grid(column=0, row=0, sticky='sw')

        self.number_label = tk.Label(
            button_frame,
            font=labelfont,
            text='',
            bg=left_bg_color)
        self.number_label.grid(column=1, row=0, sticky='sw')

        self.next_button = tk.Button(
            button_frame,
            text='Next',
            width=5,
            state='disabled',
            command=self.on_next)
        self.next_button.grid(column=2, row=0, sticky='sw')

        # Patient ID
        self.patient_num_label = tk.Label(
            header_frame, text='', font=labelfont, bg=left_bg_color)
        self.patient_num_label.grid(column=1, row=1)

        # Filter checkbox
        positive_checkbox_var = tk.BooleanVar()
        self.positive_checkbox = tk.Checkbutton(
            header_frame,
            text='Display only positive hits',
            font=labelfont,
            variable=positive_checkbox_var,
            bg=left_bg_color,
            offvalue=False,
            onvalue=True)
        self.positive_checkbox.var = positive_checkbox_var
        self.positive_checkbox.grid(column=2, row=1, sticky='e')
        self.positive_checkbox.bind(
            "<Button-1>",
            lambda event: self.on_positive_checkbox_click(
                event,
                self.positive_checkbox))

        # Text frame
        text_frame = tk.Frame(left_frame, borderwidth=1, relief="sunken")
        text_frame.grid(
            column=0,
            row=1,
            rowspan=9,
            columnspan=2,
            padx=10,
            pady=0,
            sticky='nsew')
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)
        text_frame.grid_propagate(False)

        # Modify annotation
        self.add_ann_button = tk.Button(
            left_frame,
            text='Add',
            font=textfont,
            width=15,
            state='disabled',
            command=self.on_add_annotation)
        self.add_ann_button.grid(column=0, row=10, padx=10, sticky='we')

        self.del_ann_button = tk.Button(
            left_frame,
            text='Delete',
            font=textfont,
            width=15,
            state='disabled',
            command=self.on_delete_annotation)
        self.del_ann_button.grid(column=1, row=10, padx=10, sticky='we')

        # Patient note container (with scrolling)
        self.pttext = tk.Text(
            text_frame,
            wrap="word",
            font=textfont,
            background="white",
            borderwidth=0,
            highlightthickness=0)
        scrollbar = tk.Scrollbar(text_frame)
        self.pttext.config(yscrollcommand=scrollbar.set)
        self.pttext.config(state=tk.DISABLED)
        scrollbar.config(command=self.pttext.yview)
        scrollbar.grid(column=1, row=0, sticky='nsw')
        self.pttext.grid(column=0, row=0, padx=15, pady=15, sticky='nsew')
        self.pttext.tag_config('keyword_1', background='#ffd2ff')
        self.pttext.tag_config('keyword_2', background='#ccccff')
        self.pttext.tag_config('keyword_3', background='#ffe6cc')
        self.pttext.bind("<1>", lambda event: self.pttext.focus_set())

        # Right upper frame
        right_upper_frame = tk.Frame(right_frame, bg=right_bg_color)
        right_upper_frame.grid(
            column=0,
            row=0,
            padx=10,
            pady=10,
            sticky='nsew')
        right_upper_frame.grid_propagate(False)
        right_upper_frame.grid_rowconfigure(0, weight=1)
        right_upper_frame.grid_columnconfigure(0, weight=1)
        right_upper_frame.grid_columnconfigure(1, weight=1)

        in_file_text = tk.Label(
            right_upper_frame,
            text='Input File',
            font=labelfont,
            bg=right_bg_color)
        in_file_text.grid(column=0, row=0, sticky='nsw')

        file_button = tk.Button(
            right_upper_frame,
            text='Select',
            command=self.on_select_file,
            bg=right_bg_color)
        file_button.grid(column=1, row=0, sticky='e')

        self.file_text = tk.Label(
            right_upper_frame,
            text='',
            bg=right_bg_color,
            font=labelfont,
            fg='dodgerblue4')
        self.file_text.grid(column=1, row=0, sticky='nsw')

        out_file_text = tk.Label(
            right_upper_frame,
            text='Output File',
            font=labelfont,
            bg=right_bg_color)
        out_file_text.grid(column=0, row=1, sticky='nsw')

        self.regex_label = tk.Entry(right_upper_frame, font=labelfont)
        self.regex_label.insert(0, 'output.csv')
        self.regex_label.grid(column=1, row=1, sticky='nswe')

        # Right upper regex options container
        self.right_options_frame = tk.Frame(right_frame, bg=right_bg_color)
        self.right_options_frame.grid(
            column=0, row=1, rowspan=1, padx=10, sticky='nsew')
        self.right_options_frame.grid_propagate(False)
        self.right_options_frame.grid_columnconfigure(0, weight=1)
        self.right_options_frame.grid_columnconfigure(1, weight=1)
        self.right_options_frame.grid_rowconfigure(0, weight=1)
        self.right_options_frame.grid_rowconfigure(1, weight=1)
        self.right_options_frame.grid_rowconfigure(2, weight=1)

        self.note_key_entry_label = tk.Label(
            self.right_options_frame,
            text='Note column key: ',
            font=labelfont,
            bg=right_bg_color)
        self.note_key_entry_label.grid(column=0, row=1, sticky='nsw')

        self.patient_id_label = tk.Label(
            self.right_options_frame,
            text='Patient ID column key: ',
            font=labelfont,
            bg=right_bg_color)
        self.patient_id_label.grid(column=0, row=2, sticky='nsw')

        # Right button regex container
        right_regex_frame = tk.Frame(right_frame, bg=right_bg_color)
        right_regex_frame.grid(column=0, row=3, padx=10, sticky='nsew')
        right_regex_frame.grid_propagate(False)
        right_regex_frame.grid_columnconfigure(0, weight=1)
        right_regex_frame.grid_rowconfigure(0, weight=1)

<<<<<<< HEAD
        regex_title = tk.Label(right_regex_frame, text='Regular Expression', font=boldfont, bg=right_bg_color)
        regex_title.grid(column=0, row=0)

        regex_button = tk.Button(right_regex_frame, text='Run Regex', width=7, command=self.on_run_regex)
        regex_button.grid(column=0, row=1, sticky='sw')

        self.regex_label = tk.Entry(right_regex_frame, font=labelfont)
        self.regex_label.insert(0, 'output.dta')
        self.regex_label.grid(column=1, row=1, sticky='se')

        # Right regex options container
        right_options_frame = tk.Frame(right_frame, bg=right_bg_color)
        right_options_frame.grid(column=0, row=1, rowspan=2, padx=10, sticky='nsew')
        right_options_frame.grid_propagate(False)
        right_options_frame.grid_columnconfigure(0, weight=1)
        right_options_frame.grid_columnconfigure(1, weight=1)
        right_options_frame.grid_rowconfigure(0, weight=1)
        right_options_frame.grid_rowconfigure(1, weight=1)
        right_options_frame.grid_rowconfigure(2, weight=1)

        checkbox_var = tk.IntVar()
        self.rpdr_checkbox = tk.Checkbutton(right_options_frame, padx=10, anchor='e', font=labelfont, text='RPDR format', variable=checkbox_var, bg=right_bg_color)
        self.rpdr_checkbox.var = checkbox_var
        self.rpdr_checkbox.select()
        self.rpdr_checkbox.bind("<Button-1>", lambda event: self.on_checkbox_click(event, self.rpdr_checkbox))
        self.rpdr_checkbox.grid(column=1, row=0, sticky='e')

        self.note_key_entry_label = tk.Label(right_options_frame, text='Note column key: ', font=labelfont, bg=right_bg_color)
        self.note_key_entry_label.grid(column=0, row=1, sticky='e')

        self.note_key_entry = tk.Entry(right_options_frame, font=labelfont)
        self.note_key_entry.grid(column=1, row=1, sticky='e')

        self.patient_id_label = tk.Label(right_options_frame, text='Patient ID column key: ', font=labelfont, bg=right_bg_color)
        self.patient_id_label.grid(column=0, row=2, sticky='e')

        self.patient_id_entry = tk.Entry(right_options_frame, font=labelfont)
        self.patient_id_entry.grid(column=1, row=2, sticky='e')

        self.hide_regex_options()

        # Regex text box
        text_regex_frame = tk.Frame(right_frame, borderwidth=1, relief="sunken")
        text_regex_frame.grid_rowconfigure(0, weight=1)
=======
        # Label 1
        text_regex_frame = tk.Frame(right_frame, bg=right_bg_color)
        text_regex_frame.grid_rowconfigure(0, weight=2)
>>>>>>> 22669b543280746f650297b93b29db203e2224cc
        text_regex_frame.grid_rowconfigure(1, weight=1)
        text_regex_frame.grid_rowconfigure(2, weight=4)
        text_regex_frame.grid_rowconfigure(3, weight=1)
        text_regex_frame.grid_rowconfigure(4, weight=1)
        text_regex_frame.grid_rowconfigure(5, weight=4)
        text_regex_frame.grid_rowconfigure(6, weight=1)
        text_regex_frame.grid_rowconfigure(7, weight=1)
        text_regex_frame.grid_rowconfigure(8, weight=4)
        text_regex_frame.grid_columnconfigure(0, weight=1)
        text_regex_frame.grid_columnconfigure(1, weight=3)
        text_regex_frame.grid(
            column=0,
            row=3,
            rowspan=5,
            padx=10,
            pady=10,
            sticky='nsew')
        text_regex_frame.grid_propagate(False)

<<<<<<< HEAD
        self.original_regex_text = "Type comma-separated keywords here."
        self.regex_text = tk.Text(text_regex_frame, font=textfont, borderwidth=2, highlightthickness=0, height=5)
        self.regex_text.insert(tk.END, self.original_regex_text)
        self.regex_text.grid(column=0, row=0, sticky='nsew')
        self.regex_text.bind("<Button-1>", lambda event: self.clear_textbox(event, self.regex_text, self.original_regex_text))

        # Right textbox container
        entry_frame = tk.Frame(right_frame, bg=right_bg_color)
        entry_frame.grid(column=0, row=6, rowspan=2, padx=10, pady=10, sticky='nsew')
        entry_frame.grid_propagate(False)
        entry_frame.grid_rowconfigure(0, weight=1)
        entry_frame.grid_rowconfigure(1, weight=1)
        entry_frame.grid_rowconfigure(2, weight=1)

        ann_text = tk.Label(entry_frame, text='Annotated Value', font=boldfont, bg=right_bg_color)
        ann_text.grid(column=0, row=0, sticky='ws')

        self.ann_textbox = tk.Entry(entry_frame, font=textfont)
        self.ann_textbox.grid(column=0, row=1, sticky='e')

        #ann_button = tk.Button(entry_frame, text='Save Anno', width=8, command=self.on_save_annotation)
        #ann_button.grid(column=0, row=2, sticky='nw')

        output_button = tk.Button(entry_frame, text='To Csv', width=8, command=self.write_out_output_csv)
        output_button.grid(column=0, row=3, sticky='nw')

        output_button = tk.Button(entry_frame, text='To Stata', width=8, command=self.write_out_output_stata)
        output_button.grid(column=0, row=4, sticky='nw')



=======
        regex_title = tk.Label(
            text_regex_frame,
            text='Labels',
            font=boldfont,
            bg=right_bg_color)
        regex_title.grid(column=0, row=0, columnspan=2, sticky='nswe')

        self.label_name = {}
        self.label_text = {}
        self.regex_text = {}
        self.original_label_text = {}

        self.radio_value = tk.IntVar()
        self.radio_value.set(1)
        self.label = 1
        label_color = {1: '#ff99ff', 2: '#cc99ff', 3: '#ffcc99'}
        text_color = {1: '#ffe6ff', 2: 'white', 3: 'white'}

        # Label 1
        self.radio_1 = tk.Radiobutton(
            text_regex_frame,
            text='',
            variable=self.radio_value,
            value=1,
            font=textfont,
            bg=label_color[1],
            command=self.on_radio_click)
        self.radio_1.grid(column=0, row=1, sticky='nse')

        self.original_label_text[1] = "Label_1"
        self.label_text[1] = tk.Text(
            text_regex_frame,
            font=font.Font(family='Roboto', size=14, weight='bold'),
            highlightthickness=0,
            height=1,
            width=30,
            bg=label_color[1])
        self.label_text[1].insert(tk.END, self.original_label_text[1])
        self.label_text[1].grid(column=1, row=1, sticky='nswe')
        self.label_text[1].bind(
            "<Button-1>",
            lambda event: self.clear_textbox(
                event,
                self.label_text[1],
                self.original_label_text[1]))

        self.original_regex_text = "Type comma-separated regex/keywords here."
        self.regex_text[1] = tk.Text(
            text_regex_frame,
            font=labelfont,
            borderwidth=5,
            highlightthickness=0,
            height=2,
            bg=text_color[1])
        self.regex_text[1].insert(tk.END, self.original_regex_text)
        self.regex_text[1].grid(column=0, row=2, columnspan=2, sticky='new')
        self.regex_text[1].bind(
            "<Button-1>",
            lambda event: self.clear_textbox(
                event,
                self.regex_text[1],
                self.original_regex_text))

        # Label 2
        self.radio_2 = tk.Radiobutton(
            text_regex_frame,
            text='',
            variable=self.radio_value,
            value=2,
            font=textfont,
            bg=label_color[2],
            command=self.on_radio_click)
        self.radio_2.grid(column=0, row=4, sticky='nse')
        self.original_label_text[2] = "Label_2"
        self.label_text[2] = tk.Text(
            text_regex_frame,
            font=textfont,
            highlightthickness=0,
            height=1,
            width=30,
            bg=label_color[2])
        self.label_text[2].insert(tk.END, self.original_label_text[2])
        self.label_text[2].grid(column=1, row=4, sticky='nsew')
        self.label_text[2].bind(
            "<Button-1>",
            lambda event: self.clear_textbox(
                event,
                self.label_text[2],
                self.original_label_text[2]))

        self.regex_text[2] = tk.Text(
            text_regex_frame,
            font=labelfont,
            borderwidth=1,
            highlightthickness=0,
            height=2,
            bg=text_color[2])
        self.regex_text[2].insert(tk.END, self.original_regex_text)
        self.regex_text[2].grid(column=0, row=5, columnspan=2, sticky='new')
        self.regex_text[2].bind(
            "<Button-1>",
            lambda event: self.clear_textbox(
                event,
                self.regex_text[2],
                self.original_regex_text))

        # Label 3
        self.radio_3 = tk.Radiobutton(
            text_regex_frame,
            text='',
            variable=self.radio_value,
            value=3,
            font=textfont,
            bg=label_color[3],
            command=self.on_radio_click)
        self.radio_3.grid(column=0, row=7, sticky='nse')
        self.original_label_text[3] = "Label_3"
        self.label_text[3] = tk.Text(
            text_regex_frame,
            font=textfont,
            highlightthickness=0,
            height=1,
            width=30,
            bg=label_color[3])
        self.label_text[3].insert(tk.END, self.original_label_text[3])
        self.label_text[3].grid(column=1, row=7, sticky='nswe')
        self.label_text[3].bind(
            "<Button-1>",
            lambda event: self.clear_textbox(
                event,
                self.label_text[3],
                self.original_label_text[3]))

        self.regex_text[3] = tk.Text(
            text_regex_frame,
            font=labelfont,
            borderwidth=1,
            highlightthickness=0,
            height=2,
            bg=text_color[3])
        self.regex_text[3].insert(tk.END, self.original_regex_text)
        self.regex_text[3].grid(column=0, row=8, columnspan=2, sticky='new')
        self.regex_text[3].bind(
            "<Button-1>",
            lambda event: self.clear_textbox(
                event,
                self.regex_text[3],
                self.original_regex_text))

        # Right regex button container
        right_regex_button_frame = tk.Frame(right_frame, bg=right_bg_color)
        right_regex_button_frame.grid(
            column=0, row=9, rowspan=2, padx=10, sticky='nsew')
        right_regex_button_frame.grid_propagate(False)
        right_regex_button_frame.grid_columnconfigure(0, weight=1)
        right_regex_button_frame.grid_rowconfigure(0, weight=1)
        right_regex_button_frame.grid_rowconfigure(1, weight=1)
        right_regex_button_frame.grid_rowconfigure(2, weight=1)

        self.regex_button = tk.Button(
            right_regex_button_frame,
            text='Run Regex',
            font=textfont,
            state='disabled',
            command=self.on_run_regex)
        self.regex_button.grid(column=0, row=0, sticky='nwe')

        self.load_button = tk.Button(
            right_regex_button_frame,
            text='Load annotation',
            font=textfont,
            state='disabled',
            command=self.on_load_annotation)
        self.load_button.grid(column=0, row=1, sticky='nwe')
        self.load_annotation = False

        self.save_button = tk.Button(
            right_regex_button_frame,
            text='Save',
            font=textfont,
            state='disabled',
            command=self.on_save_annotation)
        self.save_button.grid(column=0, row=2, sticky='nwe')
>>>>>>> 22669b543280746f650297b93b29db203e2224cc
