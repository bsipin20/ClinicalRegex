import datetime
import multiprocessing
import os
import queue
import random
import sys
import time

#from .. import read

def get_ucprop(proplist, flag):
    """Get a UCProp element by flag"""
    return next((i for i in proplist if i['flag'] == flag), None)

def update_ucprop(proplist, flag, values):
    """Update a UCProp element by flag"""
    prop = get_ucprop(proplist, flag)
    
    if prop:
        prop.update(values)

    
class UCPropMixin:
    """
    UCProp related variables and members.
    """
    
    # Static UC_PROPS list
    UC_PROPS = []

import configparser
import importlib
import logging
import os
import sys
# append outer directory to path so toplevel package can import in other files
# do't need to do it if frozen into exe
if not getattr(sys, 'frozen', False):
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# all list for all of the package's modules
__all__ = []

# path to the gui config file (this is what holds last opened directories)
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gui.ini')

# open the GUI config file
CONFIG = configparser.ConfigParser()
CONFIG.read(CONFIG_PATH)

# create the GUI package logger constant
LOGGER = logging.getLogger('log')

# dynamically add files to __all__
# get all of the files in this directory
#for f in os.listdir(os.path.dirname(__file__)):
#    # make sure it's a module
#    file_list = f.split('.')
#    if f.startswith('_') or 'py' not in file_list[-1]:
#        continue
#    # get rid of extension
#    file = file_list[0]
#    # import module
#    mod = importlib.import_module('cdc.gui.{}'.format(file))
#    # append to all
#    __all__.append(file)


TIME_FORMAT = CONFIG.get('GUI', 'gui_log_timestamp', fallback='%H:%M:%S - %m-%d-%Y')
CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),'read.ini'))

class Read(UCPropMixin, object):
    """Superclass for reading in files"""

    def __init__(self, options, file_location, progress_queue=None, msg_queue=None):
        # create instance variables for options and queues
        self.options = options
        self.progress_queue = progress_queue
        self.msg_queue = msg_queue
        self.warnings = []
        # get the report rate from the config file
        self.report_rate = CONFIG.getint('PROGRESS', 'report_rate', fallback=10000)
        # create info dictionary - this is used to communicate with writer
        self.info = {
            'data': None,
            'metadata': {
                'location': file_location,
                'conversion_id': str(random.randint(1, 999999))
            }
        }
        # create progress dictionary - used to send progress to main process
        self.progress = {
            'filename': None,
            'conversion_id': self.info['metadata']['conversion_id'],
            'size': 0,
            'progress': 0,
            'state': 'Waiting',
            'warning': None,
            'error': None,
            'timer': None
        }

    def _clean_note_phrase(self,note_phrase):
        current_note = note_phrase.strip()
        current_note = current_note.replace(
            "$1$",
            "").replace(
            "$\\1$",
            "").replace(
            "$-1$",
            "").replace(
            "$\\-1$",
            "").replace(
                "$2$",
                "").replace(
                    "$\\2$",
                    "").replace(
                        "$-2$",
                        "").replace(
                            "$\\-2$",
                            "").replace(
                                "$3$",
                                "").replace(
                                    "$\\3$",
                                    "").replace(
                                        "$-3$",
                                        "").replace(
                                            "$\\-3$",
            "")
        return(current_note)

    def _find_matches(self,pattern,string):
        """ finds match from string and returns coordinates """
        start_index = string.find(pattern)
        end_index = start_index + len(pattern)

        return([start_index,end_index])

    def clean_phrase(phrase, needs_decode=True):
        if isinstance(phrase, float):
            return phrase
        if needs_decode:
            phrase = phrase.decode('ascii', errors='ignore')
        cleaned = str(
            phrase.replace(
                '\r\r',
                '\n').replace(
                '\r',
                '').replace(
                    '||',
                '|'))
        cleaned = str(phrase.replace('\\r', '\\n'))
        cleaned = re.sub(r'\n+', '\n', cleaned)
        cleaned = re.sub(r' +', ' ', cleaned)
        cleaned = re.sub(r'\t', ' ', cleaned)
        cleaned = cleaned.strip('\r\n')
        return str(cleaned.strip())


    def check_msg_queue(self, message=None):
        """Checks msg_queue for messages to cancel, pause, resume, etc."""
        if self.msg_queue is not None:
            if message is None:
                # check for a message without waiting, return if there's nothing
                try:
                    msg = self.msg_queue.get_nowait()
                except queue.Empty:
                    return
            else:
                msg = message
            # if the message is to cancel, report progress and exit process
            if msg == 'cancel':
                if self.progress_queue is not None:
                    self.progress['state'] = 'Cancelled'
                    self.progress_queue.put(self.progress)
                sys.exit()
            # if it's an error, exit the process
            elif msg == 'error':
                # send the sentinel message
                self.progress_queue.put(self.info['metadata']['conversion_id'])
                sys.exit()
            # if paused, set state to Paused and report progress
            elif msg == 'pause':
                if self.progress_queue is not None:
                    self.progress['state'] = 'Paused'
                    self.progress_queue.put(self.progress)
                # this will block until a message is received, pausing process
                resume_msg = self.msg_queue.get()
                # if the message is to resume, report progress, set state to Running
                if resume_msg == 'resume':
                    if self.progress_queue is not None:
                        self.progress['state'] = 'Running'
                        self.progress_queue.put(self.progress)
                # else, check the message
                else:
                    self.check_msg_queue(message=resume_msg)

    def put_warning(self, filename, message, line=None):
        """Adds a warning"""
        time_str = datetime.datetime.now().strftime(TIME_FORMAT)
        # create string and add to warnings list
        if line is not None:
            warning = '{} | {}, line {}: {}'.format(time_str, filename, line, message)
        else:
            warning = '{} | {}: {}'.format(time_str, filename, message)
        self.warnings.append(warning)
        if len(self.warnings) == CONFIG.getint('PROGRESS', 'warning_list_size', fallback=1000):
            self.progress_queue.put(self.warnings)
            self.warnings = []

    def put_error(self, filename, message, stack_info=None):
        """Adds an error"""
        # put progress into the queue
        self.prog_wait()

        if self.progress_queue is not None:
            # set state to Error
            self.progress['state'] = 'Error'

            # put warnings in the queue so they get logged
            self.progress_queue.put(self.warnings)
            self.warnings = []
            
            # copy progress dict
            progress = dict(self.progress)

            # add error to progress dict
            progress['error'] = {
                'filename': filename,
                'message': message,
                'stack': stack_info
            }

            # report progress
            self.progress_queue.put(progress)
        raise read.ReaderError(message)
    
    def file_gen(self, file):
        """A generator based off of enumerate that checks for messages and reports progress periodically"""
        # iterate over lines in file
        try:
            for index, line in enumerate(file):
                # check 
                if index % self.report_rate == 0:
                    # check messages
                    self.check_msg_queue()
                    # flush read-ahead buffer to allow use of tell()
                    file.flush()
                    # get position in file and add to progress dict
                    self.progress['progress'] = file.tell()
                    try:
                        self.progress_queue.put_nowait(self.progress)
                    except (queue.Full, AttributeError):
                        pass
                # yield index and line
                yield index, line
        except UnicodeDecodeError as e:
            # There was an error decoding the data
            self.put_error(self.info["metadata"]["location"], str(e) + " (Did you choose the correct encoding?)")
        except:
            raise
            
            
    def refresh_file_prog(self, file):
        # flush read-ahead buffer to allow use of tell()
        file.flush()
        # get position in file and add to progress dict
        self.progress['progress'] = file.tell()

    def prog_nowait(self):
        """Report progress and check for messages without waiting"""
        if type(multiprocessing.current_process()) == multiprocessing.Process:
            self.check_msg_queue()
        if self.progress_queue is not None:
            try:
                self.progress_queue.put_nowait(self.progress)
            except queue.Full:
                pass

    def prog_wait(self):
        """Report progress and block until it can be reported"""
        if type(multiprocessing.current_process()) == multiprocessing.Process:
            self.check_msg_queue()
        if self.progress_queue is not None:
            self.progress_queue.put(self.progress)



"""Contains class for reading in plain text files"""

import os
import queue
import time
from encodings.aliases import aliases

#import cdc
#from .read import Read

class ReadTXT(Read):
    """.txt Reader"""

    # required class variables for extensions, interface labels, and description
    EXTENSIONS = ['txt']
    GUI_LABELS = ['Plain Text']
    CLI_LABELS = ['txt']
    DESCRIPTION = 'All files with the ".txt" extension.'

    # UC_PROPS class variable with the base class UC_PROPS added
    UC_PROPS = Read.UC_PROPS + [
        {'flag': '--indirsubdir',
         'name': '--input-dir-subdir',
         'label': 'Folder and Subfolders',
         'action': 'store',
         'default': None,
         'type': str,
         'help': 'Choose a directory that contains subfolders with files to be converted',
         'var': 'input_dir_subdir',
         'intype': 'dir',
         'position': -1000,
         'required': False},
        {'flag': '--indir',
         'name': '--input-dir',
         'label': 'Single Folder',
         'action': 'store',
         'default': None,
         'type': str,
         'help': 'Choose a directory that contains all files to be converted',
         'var': 'input_dir',
         'intype': 'dir',
         'position': -999,
         'required': False},
        {'flag': '--infile',
         'name': '--input-file',
         'label': 'File',
         'action': 'store',
         'default': None,
         'type': str,
         'help': 'Choose a single file to convert',
         'var': 'input_file',
         'intype': 'file',
         'position': -998,
         'required': False},
        {'flag': '--renc',
         'name': '--r-encoding',
         'label': 'Encoding',
         'action': 'store',
         'default': 'utf8',
         'type': str,
         'help': ('Choose what encoding to use for reading the input file. '
                 'utf8 is the default, which will work for most files.'),
         'var': 'r_encoding',
         'gui_choices': sorted(aliases.keys()),
         'position': 4,
         'required': True}
    ]
    # sort the UC_PROPS on the position key
    UC_PROPS = sorted(UC_PROPS, key=lambda k: k['position'])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Ensure that the input is a file
        if not os.path.isfile(self.info['metadata']['location']):
            self.put_error(self.info['metadata']['location'], "Not a valid file path.")
            return

        self.info['data'] = []
        self.info['metadata'].update({
                'filename': os.path.basename(self.info['metadata']['location']),
                'filepath': self.info['metadata']['location'],
                'size': os.path.getsize(self.info['metadata']['location']),
                'conversion_id': os.path.abspath(self.info['metadata']['location'])
        })
        self.progress.update({
            'filename': self.info['metadata']['filename'],
            'size': self.info['metadata']['size'],
            'conversion_id': os.path.abspath(self.info['metadata']['location'])
        })
        
        # check that the file is not empty
        if not self.progress['size'] > 0:
            # put_error will put a progress dict in, so don't put another in
            self.put_error(self.info['metadata']['filename'], 'File has no content.')
        else:
            # if there's no error, report the progress
            self.prog_wait()

    def read_data(self):
        """Generator to yield lines in file"""
        # open the file using with statement to avoid having to close file
        with open(self.info['metadata']['filepath'],
                  'r',
                  encoding=self.options['r_encoding']) as file:
            # set state to Reading
            self.progress['state'] = 'Reading'
            # put the progress dict without waiting
            self.prog_nowait()
            # iterate through lines in file
            for index, line in self.file_gen(file):
                # add the line to the info dictionary
                self.info['data'].append(line)
            # set the state to writing
            self.progress['state'] = 'Writing'
            # flush the read-ahead buffer, get position, report progress
            file.flush()
            self.progress['progress'] = file.tell()
            # let it block if it needs to, this message must go through
            self.prog_wait()
            # yield the info dictionary
            # although this seems weird as a generator that only yields once,
            # it's necessary so that the writers work with all readers
            yield self.info

    def _clean_note_phrase(self,note_phrase):
        current_note = note_phrase.strip()
        current_note = current_note.replace(
            "$1$",
            "").replace(
            "$\\1$",
            "").replace(
            "$-1$",
            "").replace(
            "$\\-1$",
            "").replace(
                "$2$",
                "").replace(
                    "$\\2$",
                    "").replace(
                        "$-2$",
                        "").replace(
                            "$\\-2$",
                            "").replace(
                                "$3$",
                                "").replace(
                                    "$\\3$",
                                    "").replace(
                                        "$-3$",
                                        "").replace(
                                            "$\\-3$",
            "")
        return(current_note)

    def _find_matches(self,pattern,string):
        """ finds match from string and returns coordinates """
        start_index = string.find(pattern)
        end_index = start_index + len(pattern)

        return([start_index,end_index])




class ReadDelimTXT(ReadTXT):
    """.txt Reader"""

    # required class variables, extensions are inherited from ReadTXT
    GUI_LABELS = ['Delimited Plain Text']
    CLI_LABELS = ['delim_txt']
    DESCRIPTION = 'Plain text files (with the ".txt" extension) that contain several documents separated by a delimiter.'

    # add UC_PROPS to inherited ones
    UC_PROPS = ReadTXT.UC_PROPS + [
        {'flag': '-indelim',
         'name': '--input-delimiter',
         'label': 'Delimiter',
         'action': 'store',
         'default': None,
         'type': str,
         'help': 'The separator between each document in your input file',
         'var': 'sep_delim',
         'required': True,
         'position': 3}
    ]

    # sort UC_PROPS on position key
    UC_PROPS = sorted(UC_PROPS, key=lambda k: k['position'])

    def read_data(self):
        """Generator to yield lines from each document in file"""
        # open file
        with open(self.info['metadata']['filepath'],
                  'r',
                  encoding=self.options['r_encoding']) as file:
            # count the number of records for the logs
            count = 0
            # set the start time and set state to Running
            self.progress['timer'] = time.time()
            self.progress['state'] = 'Running'
            # put the progress without waiting
            self.prog_nowait()
            # list to store lines in document
            lines = []
            # keep track of line numbers for warning reporting
            self.info['line'] = 1
            # read file line-by line
            for index, line in self.file_gen(file):
                # check for a delimiter
                if self.options['sep_delim'] in line:
                    # if there are lines to be yielded
                    if lines:
                        # increment the record count
                        count += 1
                        # put the lines in the dictionary and yield whole thing
                        self.info['data'] = lines
                        yield self.info
                        # update line number for warning reporting
                        self.info['line'] = index + 2
                        # clear lines list, but don't delete them from memory
                        lines = []
                # if the delimiter isn't there, add the line
                else:
                    lines.append(line)
            # increment the count if there are lines to yield
            if lines:
                count += 1
            # update progress
            self.progress['state'] = 'Finished'
            self.progress['processed'] = count
            # flush read-ahead buffer, get position in file, report progress
            file.flush()
            self.progress['progress'] = file.tell()
            # let this one block if it needs to
            self.prog_wait()
            # if there are lines to yield, yield them
            if lines:
                self.info['data'] = lines
                yield self.info

