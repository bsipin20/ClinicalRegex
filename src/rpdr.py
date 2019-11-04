
"""Contains class for reading in RPDR files"""
import sys, traceback
from src.read import ReadDelimTXT,ReadTXT
import configparser
import os
#from .read import ReadDelimTXT

CONFIG = configparser.ConfigParser()

CONFIG.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),'read.ini'))

class ReadRPDR(ReadDelimTXT):
    """RPDR Reader"""

    # required class variables, EXTENSIONS is inherited
    GUI_LABELS = ['RPDR']
    CLI_LABELS = ['rpdr']
    DESCRIPTION = 'Files from the Research Partners Data Registry, a centralized data registry that  gathers data from hospital systems and stores it in one place. These files are plain text files with a ".txt" extension.'
    # get the possible text fields from the config file
    TEXT_FIELDS = [field.lower().strip() for field in CONFIG.get('read.rpdr', 'Text_Fields', fallback='Report_Text, Comments, Organism_Text').split(',')]

    # Add UC_PROPS to ones from ReadTXT
    UC_PROPS = [
        {'flag': '--ignore-headers',
         'name': '--ignore-record-headers',
         'label': 'Preserve Record Headers',
         'action': 'store_false',
         'default': True,
         'help': 'Ignore the headers of each RPDR record in output',
         'gui_help': 'Preserve the metadata headers of each RPDR record in output',
         'var': 'preserve_header',
         'position': 0,
         'required': False}
    ] + ReadTXT.UC_PROPS

    # sort UC_PROPS
    UC_PROPS = sorted(UC_PROPS, key=lambda k: k['position'])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # instantiate text field variable
        self.text_field = None
        # the fields variable stores the metadata field titles in the file
        self.fields = []
        # the user doesn't have an option for the delimiter, RPDR is always this
        self.options['sep_delim'] = '[report_end]'
        # this bool is to make sure the file is valid
        valid = False
        # open the file to validate file and get fields
        self.cached_index  = 0
        self.current_index = 0
        self.cache = []




        try:
            with open(self.info['metadata']['filepath'], 'r', encoding=self.options['r_encoding']) as file:
                # read line-by-line, the first two lines with text is all we need
                for line in file:
                    # skip any blank lines
                    if line.strip() == '':
                        continue
                    else:
                        # here, valid tells us if we already checked the first line
                        if not valid:
                            # store first line, we need to remove it from first doc
                            self.first_line = line
                            # if not, read in the metadata fields
                            self.fields = [field.lower().strip() for field in line.split('|')]
                            # if not a pipe-delimited list, break with valid = False
                            if len(self.fields) <= 1:
                                break
                            # otherwise, it looks good so far, continue to next line
                            else:
                                valid = True
                        # if first line is checked and all set, check next line
                        else:
                            # if not pipe-delimited list set valid to False
                            if len(line.split('|')) <= 1:
                                valid = False
                                break
                            # if it is, break with valid set to True
                            else:
                                break
        except (UnicodeDecodeError, UnicodeError) as e:
            # There was a decoding error
            self.put_error(self.info['metadata']['filename'], 'Unable to decode file with given encoding: ' + (str(e)))
            return
        except:
            error = traceback.format_exc()
            excp = sys.exc_info()[1]

            self.put_error(self.info['metadata']['filename'], 'Unable to read input file: ' + str(excp), error)
            return

        # if it's not valid, log the error
        if not valid:
            self.put_error(self.info['metadata']['filename'], 'Not a valid RPDR file')
            return
        # else look for text field
        else:
            # update the metadata fields
            self.info['metadata'].update({field: None for field in self.fields})
            # iterate through possible text fields and find which one is there
            for field in self.TEXT_FIELDS:
                if field in self.fields:
                    self.text_field = field
                    break
            # if it can't find it, put a warning
            if self.text_field is None:
                self.put_warning(self.info['metadata']['filename'], 'Could not determine file\'s text field.')



    def read_data(self):
        """Generator to yield lines from each document in file"""
        
        #self.put_error("Test", "Test Error")
        all_notes = []
        
        
        # get the super generator
        super_generator = super().read_data()
        # read in first doc first to get rid of the header
        first_doc = next(super_generator)
        # remove the header line
        first_doc['data'].remove(self.first_line)
        # use the helper method to process it
        self.read_helper(first_doc)
        # if it's not empty, yield it
        #if self.info['data']:
        #    yield self.info
        # now go through the rest of the records
        for lines in super_generator:
            self.read_helper(lines)
            # yield if there is something to yield
            if self.info['data']:
                #all_notes.append(self.info)
                yield self.info

    def read_helper(self, lines):
        """Helper that processes the lines"""
        # keep track if we're on the first line
        first_line = True
        # iterate through lines
        for line in lines['data']:
            # if we're on the first line, store metadata
            if first_line:
                # just continue if the first line is blank
                if line.strip() == '':
                    continue
                # zip together the fields and the values in record header
                # add it to the dict
                self.info['metadata'].update(dict(zip(self.fields, line.split('|'))))
                # if the text field is in the header
                if self.text_field in self.info['metadata']:
                    # add the record header to the lines if the user wants it
                    if self.options['preserve_header']:
                        self.info['data'] = [line]
                        # delete text from the metadata so it's not stored twice
                        del self.info['metadata'][self.text_field]
                    # if the user doesn't want to keep the header, just add
                    # the text to the dictionary and remove it from the metadata
                    else:
                        self.info['data'] = [self.info['metadata'].pop(self.text_field)]
                # if the text field isn't there
                else:
                    # add the header if the user wants it
                    if self.options['preserve_header']:
                        self.info['data'] = [line]
                    # if there's a text field, warn user we couldn't find it
                    if self.text_field is not None:
                        self.put_warning(self.info['metadata']['filename'], 'Medical record has no content', self.info['line'])
                # set the first line bool to false
                first_line = False
            # if it's not the first line, just add the line to the dict
            else:
                self.info['data'].append(line)

