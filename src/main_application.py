import tkinter as tk
from tkinter import font, filedialog, messagebox,ttk
from model import DataModel
from extract_values import multi_run_regex
import pandas as pd
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
        #self.var_names_of_textbox = ["one","two","three","four","five","six","seven","eight","nine"]

    # Set up button click methods
    def on_select_file(self):
        file = filedialog.askopenfilename(title="Select File")
        if file:
            self.data_model.input_fname = file
            self.file_text.config(text=self.data_model.input_fname.split('/')[-1])

    def on_select_output_file(self):
        "sends box to ask for output file "
        output_fname = filedialog.askopenfilename(title="Select Output File")

        if output_fname:
            # Change note-key
            rpdr_checkbox = self.rpdr_checkbox.var.get()
            if rpdr_checkbox == 0:
                self.note_key = self.note_key_entry.get()
                self.patient_key = self.patient_id_entry.get()
            self.refresh_viewer(output_fname)

    def delete_b(self):
        self.pack_forget()

    def delete_remaining(self):
        for item in self.entry_frame.winfo_children():
            item.grid_remove()

    def delete_remaining_text(self):
        for item in self.text_regex_frame.winfo_children():
            item.grid_remove()
 

    def on_choose_num_keywords(self,eventobject):
        # Right textbox container

        left_bg_color = 'lightblue1'
        right_bg_color = 'azure'
        boldfont = font.Font(size=16, family='Open Sans', weight='bold')
        textfont = font.Font(family='Roboto', size=15)
        num_boxes = eventobject.widget.get()
        self.delete_remaining()
        
        if num_boxes == "1":
            self.ann_textbox1= tk.Entry(self.entry_frame, font=textfont,relief="sunken",bg="skyblue",highlightthickness=0,borderwidth=2)
            self.ann_textbox1.grid(column=0, row=0, sticky='nsew',padx=10,pady=10)


        if num_boxes == "2":
            self.ann_textbox1= tk.Entry(self.entry_frame, font=textfont,relief="sunken",bg="skyblue",highlightthickness=0,borderwidth=2)
            self.ann_textbox1.grid(column=0, row=0, sticky='nsew',padx=10,pady=10)

            self.ann_textbox2= tk.Entry(self.entry_frame, font=textfont,relief="sunken",bg="wheat1",highlightthickness=0,borderwidth=2)
            self.ann_textbox2.grid(column=1, row=0, sticky='nsew',padx=10,pady=10)

        if num_boxes == "3":

            self.ann_textbox1= tk.Entry(self.entry_frame, font=textfont,relief="sunken",bg="skyblue",highlightthickness=0,borderwidth=2)
            self.ann_textbox1.grid(column=0, row=0, sticky='nsew',padx=10,pady=10)
 
            self.ann_textbox2= tk.Entry(self.entry_frame, font=textfont,relief="sunken",bg="wheat1")
            self.ann_textbox2.grid(column=1, row=0, sticky='nsew',padx=10,pady=10)

            self.ann_textbox3= tk.Entry(self.entry_frame, font=textfont,relief="sunken",bg="DarkSeaGreen1")
            self.ann_textbox3.grid(column=2, row=0, sticky='nsew',padx=10,pady=10)

        if num_boxes == "4":

            self.ann_textbox1= tk.Entry(self.entry_frame, font=textfont,relief="sunken",bg="skyblue",highlightthickness=0,borderwidth=2)
            self.ann_textbox1.grid(column=0, row=0, sticky='nsew',padx=10,pady=10)
 
            self.ann_textbox2= tk.Entry(self.entry_frame, font=textfont,relief="sunken",bg="wheat1")
            self.ann_textbox2.grid(column=1, row=0, sticky='nsew',padx=10,pady=10)

            self.ann_textbox3= tk.Entry(self.entry_frame, font=textfont,relief="sunken",bg="DarkSeaGreen1")
            self.ann_textbox3.grid(column=2, row=0, sticky='nsew',padx=10,pady=10)

            self.ann_textbox4= tk.Entry(self.entry_frame, font=textfont,relief="sunken",bg="pink1")
            self.ann_textbox4.grid(column=3, row=0, sticky='nsew',padx=10,pady=10)


    
        self.determine_annotated(num_boxes)


    def determine_annotated(self,num_boxes):
        # Right textbox container

        self.original_regex_text = "Type comma-separated keywords here."
        self.delete_remaining_text()

        titlefont = font.Font(family='Open Sans', size=18, weight='bold')
        boldfont = font.Font(size=16, family='Open Sans', weight='bold')
        textfont = font.Font(family='Roboto', size=15)
        labelfont = font.Font(family='Roboto', size=11)
        smallfont = font.Font(family='Roboto', size=13)

        if num_boxes == "1":

            self.regex_text1 = tk.Text(self.text_regex_frame, font=textfont, borderwidth=2, highlightthickness=0, height=5,relief="sunken",bg="skyblue")
            self.regex_text1.insert(tk.END, self.original_regex_text)
            self.regex_text1.grid(column=0, row=0,padx=10,pady=10,rowspan=2,sticky='nsew')
            self.regex_text1.bind("<Button-1>", lambda event: self.clear_textbox(event, self.regex_text1, self.original_regex_text))

        if num_boxes == "2":
            self.regex_text1 = tk.Text(self.text_regex_frame, font=textfont, borderwidth=2, highlightthickness=0, height=5,relief="sunken",bg="skyblue")
 
            self.regex_text1.insert(tk.END, self.original_regex_text)
            self.regex_text1.grid(column=0, row=0, sticky='nsew')
            self.regex_text1.bind("<Button-1>", lambda event: self.clear_textbox(event, self.regex_text1, self.original_regex_text))

            self.regex_text2 = tk.Text(self.text_regex_frame, font=textfont, borderwidth=2, highlightthickness=0, height=5,relief="sunken",bg="wheat1")
            self.regex_text2.insert(tk.END, self.original_regex_text)
            self.regex_text2.grid(column=1, row=0, sticky='nsew')
            self.regex_text2.bind("<Button-1>", lambda event: self.clear_textbox(event, self.regex_text2, self.original_regex_text))

        if num_boxes == "3":
            self.regex_text1 = tk.Text(self.text_regex_frame, font=textfont, borderwidth=2, highlightthickness=0, height=5,relief="sunken",bg="skyblue")
 
            self.regex_text1.insert(tk.END, self.original_regex_text)
            self.regex_text1.grid(column=0, row=0, sticky='nsew')
            self.regex_text1.bind("<Button-1>", lambda event: self.clear_textbox(event, self.regex_text1, self.original_regex_text))

            self.regex_text2 = tk.Text(self.text_regex_frame, font=textfont, borderwidth=2, highlightthickness=0, height=5,relief="sunken",bg="wheat1")
            self.regex_text2.insert(tk.END, self.original_regex_text)
            self.regex_text2.grid(column=1, row=0, sticky='nsew')
            self.regex_text2.bind("<Button-1>", lambda event: self.clear_textbox(event, self.regex_text2, self.original_regex_text))

            self.regex_text3 = tk.Text(self.text_regex_frame, font=textfont, borderwidth=2, highlightthickness=0, height=5,relief="sunken",bg="DarkSeaGreen1")

            self.regex_text3.insert(tk.END, self.original_regex_text)
            self.regex_text3.grid(column=2, row=0, sticky='nsew')
            self.regex_text3.bind("<Button-1>", lambda event: self.clear_textbox(event, self.regex_text3, self.original_regex_text))

        if num_boxes == "4":
            self.regex_text1 = tk.Text(self.text_regex_frame, font=textfont, borderwidth=2, highlightthickness=0, height=5,relief="sunken",bg="skyblue")
 
            self.regex_text1.insert(tk.END, self.original_regex_text)
            self.regex_text1.grid(column=0, row=0, sticky='nsew')
            self.regex_text1.bind("<Button-1>", lambda event: self.clear_textbox(event, self.regex_text1, self.original_regex_text))

            self.regex_text2 = tk.Text(self.text_regex_frame, font=textfont, borderwidth=2, highlightthickness=0, height=5,relief="sunken",bg="wheat1")
            self.regex_text2.insert(tk.END, self.original_regex_text)
            self.regex_text2.grid(column=1, row=0, sticky='nsew')
            self.regex_text2.bind("<Button-1>", lambda event: self.clear_textbox(event, self.regex_text2, self.original_regex_text))

            self.regex_text3 = tk.Text(self.text_regex_frame, font=textfont, borderwidth=2, highlightthickness=0, height=5,relief="sunken",bg="DarkSeaGreen1")
            self.regex_text3.insert(tk.END, self.original_regex_text)
            self.regex_text3.grid(column=2, row=0, sticky='nsew')
            self.regex_text3.bind("<Button-1>", lambda event: self.clear_textbox(event, self.regex_text3, self.original_regex_text))

            self.regex_text4= tk.Text(self.text_regex_frame, font=textfont, borderwidth=2, highlightthickness=0, height=5,relief="sunken",bg="pink1")
            self.regex_text4.insert(tk.END, self.original_regex_text)
            self.regex_text4.grid(column=3, row=0, sticky='nsew')
            self.regex_text4.bind("<Button-1>", lambda event: self.clear_textbox(event, self.regex_text4, self.original_regex_text))



       # Number of keywords button
        #tk.Entry(self.annotated_values_frame,width=2).grid(rowspan=1,columnspan=3)



    def create_text_boxes(self,num_boxes_to_make):
        pass

        #entry_frame.grid_propagate(False)

        
    def show_widgets(self,upto_widgetposition):

        for item in self.annotated_values_frame.winfo_children()[:int(upto_widgetposition)]:
            item.grid()
    def iterate_on_regex(self):
        for item in self.text_regex_frame.winfo_children():
            self.on_run_regex(item)

    def handle_all_current_regex(self):
        regex_texts =[]

#if hasattr(obj, 'attr_name'):
        if hasattr(self,"regex_text4"):
            phrase1 = self.regex_text1.get(1.0, 'end-1c').strip()
            phrase2 = self.regex_text2.get(1.0, 'end-1c').strip()
            phrase3 = self.regex_text3.get(1.0, 'end-1c').strip()
            #phrase4 = self.regex_text4.get(1.0, 'end-1c').strip()

            regex_texts =[phrase1,phrase2,phrase3,phrase4]

        elif hasattr(self,"regex_text3"):
            phrase1 = self.regex_text1.get(1.0, 'end-1c').strip()
            phrase2 = self.regex_text2.get(1.0, 'end-1c').strip()
            phrase3 = self.regex_text3.get(1.0, 'end-1c').strip()



            regex_texts =[phrase1,phrase2,phrase3]
            
        elif hasattr(self,"regex_text2"):
            phrase1 = self.regex_text1.get(1.0, 'end-1c').strip()
            phrase2 = self.regex_text2.get(1.0, 'end-1c').strip()
            regex_texts =[phrase1,phrase2]

        elif hasattr(self,"regex_text1"):

            phrase1 = self.regex_text1.get(1.0, 'end-1c').strip()
            regex_texts = [phrase1]
        return(regex_texts)



    def on_run_regex(self): 
#        self.regex_text = self.regex_text1
        if not self.data_model.input_fname:
            # Warning
            messagebox.showerror(title="Error", message="Please select an input file using the 'Select File' button.")
            return

        output_fname = '/'.join(self.data_model.input_fname.split('/')[:-1]) + '/' + self.regex_label.get()
        # Retrieve phrases, changed to list of tuples
        phrases= self.handle_all_current_regex()


        #TODO need to add none response error check in any potential regex text box
        if phrases == self.original_regex_text or len(phrases) == 0:
            messagebox.showerror(title="Error", message="Please input comma-separated phrases to search for. ")
            return

        rpdr_checkbox = self.rpdr_checkbox.var.get()

        if rpdr_checkbox == 0:
            note_keyword = self.note_key_entry.get()
            patient_keyword = self.patient_id_entry.get()
            if not note_keyword:
                messagebox.showerror(title='Error', message='Please input the column name for notes.')
                return
            if not patient_keyword:
                messagebox.showerror(title='Error', message='Please input the column name for patient IDs.')
                return
            try:
                multi_run_regex(self.data_model.input_fname, phrases, output_fname, False, note_keyword, patient_keyword)
                self.note_key = note_keyword
                self.patient_key = patient_keyword
            except:
                messagebox.showerror(title="Error", message="Something went wrong, did you select an appropriately formatted file to perform the Regex on?")
                return

  #########      """ this is when rdpr format is necessary """ 
        else:
            #try:
            multi_run_regex(self.data_model.input_fname, phrases, output_fname)
            self.note_key = RPDR_NOTE_KEYWORD
            self.patient_key = RPDR_PATIENT_KEYWORD

            #except:
            #    messagebox.showerror(title="Error", message="Something went wrong, did you select an appropriately formatted RPDR file to perform the Regex on?")
            #    return
        self.refresh_viewer(output_fname)



    # Functions that change display
    def refresh_viewer(self, output_fname):
        self.data_model.output_fname = output_fname
        self.data_model.output_df = pd.read_csv(self.data_model.output_fname, index_col=0, header=0, dtype=object)
        self.refresh_model()


    def refresh_model(self):
        self.data_model.current_row_index = 0
        if self.checkvar:
            self.data_model.display_df = self.data_model.output_df[self.data_model.output_df['EXTRACTED_VALUE'] == '1']
        else:
            self.data_model.display_df = self.data_model.output_df.copy()

        #change num_notes to num of unique notes


        self.data_model.num_notes = self.data_model.display_df.shape[0]
        self.regex_file_text.config(text=self.data_model.output_fname.split('/')[-1])
    

        self.display_output_note()

    def get_matches_repo_num(self,df,report_num):
        all_matches = []
        num_rows = df.shape[0]
        for i in range(0,num_rows): # get num of rows
            row_l = df.iloc[i]
            check = int(df['REPORT_NUMBER'][i])
            if report_num == check:
                row = df.iloc[i]
                values = eval(row["MATCHES"])
                all_matches = all_matches + values
        return(all_matches)


    def display_output_note(self):
        current_note_row = self.data_model.display_df.iloc[self.data_model.current_row_index]

        try:
            current_note_text = current_note_row[self.note_key]
        except:
            messagebox.showerror(title='Error', message='Unable to retrieve note text. Did you select the correct key?')
            return

        try:
            current_patient_id = current_note_row[self.patient_key]
        except:
            messagebox.showerror(title='Error', message='Unable to retrieve patient ID. Did you select the correct key?')
            return

        # needs to show num of unique notes 
        self.number_label.config(text='%d of %d' % (self.data_model.current_row_index + 1, self.data_model.num_notes))
        self.patient_num_label.config(text='Patient ID: %s' % current_patient_id)


        # match_indices need to get matches for all 
        match_indices = self.get_matches_repo_num(self.data_model.display_df,int(current_note_row['REPORT_NUMBER']))

        #match_indices = ast.literal_eval(current_note_row['MATCHES'])

        self.pttext.config(state=tk.NORMAL)
        self.pttext.delete(1.0, tk.END)
        self.pttext.insert(tk.END, current_note_text)
        self.pttext.config(state=tk.DISABLED)

        tag_start = '1.0'
        # Add highlighting 
        for start, end in match_indices:
            pos_start = '{}+{}c'.format(tag_start, start)
            pos_end = '{}+{}c'.format(tag_start, end)
            self.pttext.tag_add('highlighted', pos_start, pos_end)

        self.iter_show_annotate()

    def iter_show_annotate(self):
        for item in self.entry_frame.winfo_children():
            self.show_annotation(item)


    def show_annotation(self,item):
        self.ann_textbox = item
        self.ann_textbox.delete(0, tk.END)
        self.ann_textbox.insert(0, self.data_model.get_annotation())
    
    def iter_to_save_annotation(self):
        for item in self.entry_frame.winfo_children():
            self.on_save_annotation(item)

    def on_save_annotation(self,annotate):
        self.ann_textbox = annotate
        annotation = self.ann_textbox.get()
        if len(annotation) > 0:
            self.data_model.write_to_annotation(annotation)

    def on_prev(self):
        self.iter_to_save_annotation()
        if self.data_model.current_row_index > 0:
            self.data_model.current_row_index -= 1
        self.display_output_note()
        
    def on_next(self):
        self.iter_to_save_annotation()
        if self.data_model.current_row_index < self.data_model.num_notes:
            self.data_model.current_row_index += 1
        self.display_output_note()

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
        else:
            self.checkvar = True
        self.refresh_model()

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
    
    def create_right_frame(self,root):
        root

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
        right_frame.grid_rowconfigure(11, weight=1)


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
        right_regex_frame.grid(column=0, row=4, padx=10, pady=10, sticky='nsew')
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
        self.right_options_frame = tk.Frame(right_frame, bg=right_bg_color)
        self.right_options_frame.grid(column=0, row=1, rowspan=2, padx=10, sticky='nsew')
        self.right_options_frame.grid_propagate(False)
        self.right_options_frame.grid_columnconfigure(0, weight=1)
        self.right_options_frame.grid_columnconfigure(1, weight=1)
        self.right_options_frame.grid_rowconfigure(0, weight=1)
        self.right_options_frame.grid_rowconfigure(1, weight=1)
        self.right_options_frame.grid_rowconfigure(2, weight=1)

        checkbox_var = tk.IntVar()
        self.rpdr_checkbox = tk.Checkbutton(self.right_options_frame, padx=10, anchor='e', font=labelfont, text='RPDR format', variable=checkbox_var, bg=right_bg_color)
        self.rpdr_checkbox.var = checkbox_var
        self.rpdr_checkbox.select()
        self.rpdr_checkbox.bind("<Button-1>", lambda event: self.on_checkbox_click(event, self.rpdr_checkbox))
        self.rpdr_checkbox.grid(column=1, row=0, sticky='e')

        self.note_key_entry_label = tk.Label(self.right_options_frame, text='Note column key: ', font=labelfont, bg=right_bg_color)
        self.note_key_entry_label.grid(column=0, row=1, sticky='e')

        self.note_key_entry = tk.Entry(self.right_options_frame, font=labelfont)
        self.note_key_entry.grid(column=1, row=1, sticky='e')

        self.patient_id_label = tk.Label(self.right_options_frame, text='Patient ID column key: ', font=labelfont, bg=right_bg_color)
        self.patient_id_label.grid(column=0, row=2, sticky='e')

        self.patient_id_entry = tk.Entry(self.right_options_frame, font=labelfont)
        self.patient_id_entry.grid(column=1, row=2, sticky='e')

        self.hide_regex_options()

        # Regex text box

        # Right textbox container
        self.entry_frame = tk.Frame(right_frame, relief="sunken")
        self.entry_frame.grid(column=0, row=8, rowspan=1, padx=10, pady=10, sticky='nsew')
        self.entry_frame.grid_rowconfigure(0, weight=1)
#        self.entry_frame.grid_rowconfigure(1, weight=1)
#        self.entry_frame.grid_rowconfigure(2, weight=1)
        self.entry_frame.grid_columnconfigure(0, weight=1)
        self.entry_frame.grid_columnconfigure(1, weight=1)
        self.entry_frame.grid_columnconfigure(2, weight=1)
        self.entry_frame.grid_columnconfigure(3, weight=1)


        self.entry_frame.grid_propagate(False)
        

        save_buttom_frame = tk.Frame(right_frame,bg=right_bg_color)
        save_buttom_frame.grid(column=0,row=9,rowspan=2,padx=10,pady=10,sticky='nsew')
        save_buttom_frame.grid_propagate(False)
        save_buttom_frame.grid_rowconfigure(0, weight=1)
        save_buttom_frame.grid_rowconfigure(1, weight=1)
        save_buttom_frame.grid_rowconfigure(2, weight=1)


        ann_text = tk.Label(save_buttom_frame, text='Annotated Value', font=boldfont, bg=right_bg_color)
        ann_text.grid(column=0, row=0, sticky='ws')

        ann_button = tk.Button(save_buttom_frame, text='Save', width=8, command=self.iter_to_save_annotation())
        ann_button.grid(column=0, row=2, sticky='nw')

        #TODO get rid of this

        combo_box_frame= tk.Frame(right_frame, bg=right_bg_color)
        combo_box_frame.grid(column=0, row=3, rowspan=1)

        combo_box_frame.grid_columnconfigure(0, weight=1)
        combo_box_frame.grid_columnconfigure(1, weight=1)
        combo_box_frame.grid_columnconfigure(2, weight=1)
        
        combo_label= tk.Label(combo_box_frame, text='Number of Boxes', font=textfont, bg=right_bg_color)
        combo_label.grid(column=0, row=0, sticky='w')

        #combo_box_frame.grid_propagate(False)
        #combo_box_frame.grid_columnconfigure(0, weight=1)
        #combo_box_frame.grid_columnconfigure(1, weight=1)
        #self.entry_frame= tk.Frame(right_frame,bg=right_bg_color)

        combo = ttk.Combobox(combo_box_frame,values=(1,2,3,4))
        combo.grid(column=0,row=2,sticky="e")
        combo.bind('<<ComboboxSelected>>',self.on_choose_num_keywords)

        self.text_regex_frame = tk.Frame(right_frame,relief="sunken")
        self.text_regex_frame.grid_rowconfigure(0, weight=1)
        self.text_regex_frame.grid_rowconfigure(1, weight=1)
        self.text_regex_frame.grid_columnconfigure(0, weight=1)
        self.text_regex_frame.grid_columnconfigure(1, weight=1)
        self.text_regex_frame.grid_columnconfigure(2, weight=1)
        self.text_regex_frame.grid_columnconfigure(3, weight=1)


        self.text_regex_frame.grid(column=0, row=5,rowspan=2, padx=10, pady=10, sticky='nsew')
        self.text_regex_frame.grid_propagate(False)




       

        
