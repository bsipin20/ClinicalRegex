import tkinter as tk
from tkinter import font, filedialog, messagebox
from src.model import DataModel
from src.extract_values import run_regex
from src.rpdr import ReadRPDR
from src.helpers import find_matches,_extract_phrase_from_notes,_process_raw,AnnotationLedger
from src.model import Model
import pandas as pd
import os
import ast


RPDR_NOTE_KEYWORD = 'NOTE'
RPDR_PATIENT_KEYWORD = 'EMPI'

class MainApplication(tk.Frame):
    def __init__(self, master):

        tk.Frame.__init__(self, master)
        self.master = master
        self.setup_interface(master)
        self.data_model = DataModel()
        self.note_key = RPDR_NOTE_KEYWORD
        self.patient_key = RPDR_PATIENT_KEYWORD
        self.checkvar = False

    # Set up button click methods
    def on_select_file(self):
        file = filedialog.askopenfilename(title="Select File")
        if file:
            self.data_model.input_fname = file
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
        self.dirname = os.path.dirname(file_loc)
 
        #self.output_fname = '/'.join(self.data_model.input_fname.split('/')[:-1]) + '/' + self.regex_label.get()


        opts = {
            'r_encoding' : 'utf-8',
            'preserve_header' : True,
            'patient_id' : self.patient_id_entry.get(),
            'note_key' : self.note_key_entry.get(),
            'rpdr' :self.rpdr_checkbox.var.get()




        }
        
        phrases = [p.strip() for p in self.phrases.split(",")]

        self.model = Model(options_=opts,file_location_=file_loc,keywords_=phrases)

        if self.checkvar:

            self.num_notes = self.model.get_num_notes_positive()


        else:

            self.num_notes = self.model.get_num_notes()

        first_note,index = self.model.first(self.checkvar)
    
        self.display_output_note(first_note,index)


    def write_out_output_csv(self):
        #output_fname = filedialog.asksaveasfile(title="Select Output File",filetypes=("
        filename = self.regex_label.get()
        filename = self.dirname + "/" + filename

        self.model.write_output(filename)


    def display_output_note(self,current_note_row,index):

        """ displays highlighting """ 

        current_note_text= current_note_row['text']
        current_patient_id = current_note_row['empi']
        match_indices = ast.literal_eval(current_note_row['matches'])

        self.number_label.config(text='%d of %d' % (index + 1, self.num_notes))
        self.patient_num_label.config(text='Patient ID: %s' % self.model.get_patient_id())

        tag_start = '1.0'

        # Add highlighting 

        self.pttext.config(state=tk.NORMAL)
        self.pttext.delete(1.0, tk.END)
        self.pttext.insert(tk.END, current_note_text)
        self.pttext.config(state=tk.DISABLED)


        for start, end in match_indices:
            pos_start = '{}+{}c'.format(tag_start, start)
            pos_end = '{}+{}c'.format(tag_start, end)
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

        current_note_row,reported_index = self.model.prev(self.checkvar)
        self.display_output_note(current_note_row,reported_index)
        
    def on_next(self):
        annotation = self.ann_textbox.get()

        if len(annotation) > 0:

            self.model.write_to_annotation(annotation)

        current_note_row,reported_index = self.model.next(self.checkvar)
        self.display_output_note(current_note_row,reported_index)

    ## GUI helper methods
    def clear_textbox(self, event, widget, original_text):
        if widget.get(1.0, 'end-1c') == original_text:
            widget.delete(1.0, 'end-1c')

    def on_checkbox_click(self, event, widget):
        if widget.var.get() == 0:
            self.hide_regex_options()
        else:
            self.show_regex_options()


    def on_positive_checkbox_click(self, event, widget):
        if self.checkvar:
            self.checkvar = False
            self.num_notes = self.model.get_num_notes()
            note,index = self.model.current(self.checkvar)
            self.display_output_note(note,index)

        else:

            self.checkvar = True
            self.num_notes = self.model.get_num_notes_positive()
            print(self.num_notes)
            note,index = self.model.current(self.checkvar)
            print(note['extracted_value'])
            self.display_output_note(note,index)



        
        #self.model.refresh(self.checkvar)

    def hide_regex_options(self):
        self.note_key_entry_label.grid_remove()
        self.note_key_entry.grid_remove()
        self.patient_id_label.grid_remove()
        self.patient_id_entry.grid_remove()

    def show_regex_options(self):
        self.note_key_entry_label.grid()
        self.note_key_entry.grid()
        self.patient_id_label.grid()
        self.patient_id_entry.grid()

    def setup_interface(self, root):
        # Define fonts
        titlefont = font.Font(family='Open Sans', size=18, weight='bold')
        boldfont = font.Font(size=16, family='Open Sans', weight='bold')
        textfont = font.Font(family='Roboto', size=15)
        labelfont = font.Font(family='Roboto', size=11)
        smallfont = font.Font(family='Roboto', size=13)

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

        left_frame.grid(column=0, row=0, columnspan=2, rowspan=5, sticky='nsew')
        left_frame.grid_rowconfigure(0, weight=1)
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_rowconfigure(2, weight=1)
        left_frame.grid_rowconfigure(3, weight=1)
        left_frame.grid_rowconfigure(4, weight=1)
        left_frame.grid_rowconfigure(5, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        right_frame.grid(column=2, row=0, columnspan=1, sticky='nsew')
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
        header_frame.grid(column=0, row=0, padx=10, pady=10, sticky='nsew')
        header_frame.grid_propagate(False)
        header_frame.grid_rowconfigure(0, weight=1)
        header_frame.grid_rowconfigure(1, weight=1)
        header_frame.grid_columnconfigure(0, weight=2)
        header_frame.grid_columnconfigure(1, weight=1)
        header_frame.grid_columnconfigure(2, weight=1)

        title_text = tk.Label(header_frame, text='Clinical Note', font=titlefont, bg=left_bg_color)
        title_text.grid(column=0, row=0, sticky='w')

        button_frame = tk.Frame(header_frame, bg=left_bg_color)
        button_frame.grid(column=0, row=1, sticky='nsew')
        button_frame.grid_propagate(False)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)
        button_frame.grid_rowconfigure(0, weight=1)
        button_frame.grid_rowconfigure(1, weight=1)

        prev_button = tk.Button(button_frame, text='Prev', width=5, command=self.on_prev)
        prev_button.grid(column=0, row=0, sticky='sw')

        self.number_label = tk.Label(button_frame, font=smallfont, text='', bg=left_bg_color)
        self.number_label.grid(column=1, row=0, sticky='sw')

        next_button = tk.Button(button_frame, text='Next', width=5, command=self.on_next)
        next_button.grid(column=2, row=0, sticky='sw')

        # Patient ID
        self.patient_num_label = tk.Label(header_frame, text='', font=labelfont, bg=left_bg_color)
        self.patient_num_label.grid(column=1, row=1)

        # Filter checkbox
        positive_checkbox_var = tk.BooleanVar()
        self.positive_checkbox = tk.Checkbutton(header_frame, text='Display only positive hits', font=labelfont, variable=positive_checkbox_var, bg=left_bg_color, offvalue=False, onvalue=True)
        self.positive_checkbox.var = positive_checkbox_var
        self.positive_checkbox.grid(column=2, row=1, sticky='e')
        self.positive_checkbox.bind("<Button-1>",  lambda event: self.on_positive_checkbox_click(event, self.positive_checkbox))

        # Text frame
        text_frame = tk.Frame(left_frame, borderwidth=1, relief="sunken")
        text_frame.grid(column=0, row=1, rowspan=4, padx=10, pady=0, sticky='nsew')
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)
        text_frame.grid_propagate(False)

        # Patient note container (with scrolling)
        self.pttext = tk.Text(text_frame, wrap="word", font=textfont, background="white", borderwidth=0, highlightthickness=0)
        scrollbar = tk.Scrollbar(text_frame)
        self.pttext.config(yscrollcommand=scrollbar.set)
        self.pttext.config(state=tk.DISABLED)
        scrollbar.config(command=self.pttext.yview)
        scrollbar.grid(column=1, row=0, sticky='nsw')
        self.pttext.grid(column=0, row=0, padx=15, pady=15, sticky='nsew')
        self.pttext.tag_config('highlighted', background='gold')
        self.pttext.bind("<1>", lambda event: self.pttext.focus_set())
        
        # Right button frame
        right_button_frame = tk.Frame(right_frame, bg=right_bg_color)
        right_button_frame.grid(column=0, row=0, padx=10, pady=10, sticky='nsew')
        right_button_frame.grid_propagate(False)
        right_button_frame.grid_rowconfigure(0, weight=1)
        right_button_frame.grid_columnconfigure(0, weight=2)
        right_button_frame.grid_columnconfigure(1, weight=1)

        self.file_text = tk.Label(right_button_frame, text='', bg=right_bg_color, font=labelfont, fg='dodgerblue4')
        self.file_text.grid(column=0, row=0, sticky='ne')

        file_button = tk.Button(right_button_frame, text='Select File', width=10, command=self.on_select_file, bg=right_bg_color)
        file_button.grid(column=1, row=0, sticky='ne')

        self.regex_file_text = tk.Label(right_button_frame, text='', bg=right_bg_color, font=labelfont, fg='dodgerblue4')
        self.regex_file_text.grid(column=0, row=1, sticky='ne')

        regex_file_button = tk.Button(right_button_frame, text='Select Output', width=10, command=self.on_select_output_file, bg=right_bg_color)
        regex_file_button.grid(column=1, row=1, sticky='ne')
        
        # Right button container
        right_regex_frame = tk.Frame(right_frame, bg=right_bg_color)
        right_regex_frame.grid(column=0, row=3, padx=10, pady=10, sticky='nsew')
        right_regex_frame.grid_propagate(False)
        right_regex_frame.grid_columnconfigure(0, weight=1)
        right_regex_frame.grid_columnconfigure(1, weight=3)
        right_regex_frame.grid_rowconfigure(0, weight=1)
        right_regex_frame.grid_rowconfigure(1, weight=1)

        regex_title = tk.Label(right_regex_frame, text='Regular Expression', font=boldfont, bg=right_bg_color)
        regex_title.grid(column=0, row=0)

        regex_button = tk.Button(right_regex_frame, text='Run Regex', width=7, command=self.on_run_regex)
        regex_button.grid(column=0, row=1, sticky='sw')

        self.regex_label = tk.Entry(right_regex_frame, font=labelfont)
        self.regex_label.insert(0, 'output.csv')
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
        text_regex_frame.grid_rowconfigure(1, weight=1)
        text_regex_frame.grid_columnconfigure(0, weight=1)
        text_regex_frame.grid(column=0, row=4, rowspan=2, padx=10, pady=10, sticky='nsew')
        text_regex_frame.grid_propagate(False)

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

        output_button = tk.Button(entry_frame, text='Output File', width=8, command=self.write_out_output_csv)
        output_button.grid(column=0, row=3, sticky='nw')

        #output_button = tk.Button(entry_frame, text='To Stata', width=8, command=self.write_out_output_stata)
        #output_button.grid(column=0, row=4, sticky='nw')



