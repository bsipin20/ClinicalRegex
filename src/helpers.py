import re

def _clean_note_phrase(note_phrase):
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

def _is_match(keywords,word):
    match_ = False
    if word.lower() in keywords.lower():
        match_ = True
    return(match_)

   
    

def _create_sent_list(sentence):
    words = tuple(sentence.split(" "))
    return(words)

def _process_raw(whole_note):
    words = [x.rstrip() for x in whole_note]
    words = list(_create_sent_list(" ".join(words)))
    no_spaces = [x for x in words if x]
    return(no_spaces)
    

def get_coordinates(keywords,whole_note):
    """ 
        finds match from string and returns coordinates 
        Args : 
            patterns : list of words to search
            sentences : the whole note that is cleaned and words separated by spaces
    """

    indexer = 0
    matches = list()

    #for sentence in whole_note:

    for word in whole_note:

        if _is_match(keywords,word):

            matches.append((indexer, indexer + len(word)-1))

        indexer += len(word) + 1

    return(matches)

def _extract_phrase_from_notes(keywords,whole_note):
    """Return a PhraseMatch object with the value as a binary 0/1 indicating
    whether one of the phrases was found in note"""

    string_lookup = {
        "word" : [
            r'(\s%s\s)',
            r'(^%s\s)',
            r'(\s%s$)',
            '(^%s$)',
            r'(\s%s[\,\.\?\!\-])',
            r'(^%s[\,\.\?\!\-])'],
        "num" : ['(?:%s)\s*(?:of|is|was|were|are|\:)?[:]*[\s]*([0-9]+\.?[0-9]*)'],
        "date" : [
                                r'(?:%s)\s*(?:of|is|was|were|are|\:)?[:]*[\s]*(\d+/\d+/\d+)',
                                '(?:%s)\s*(?:of|is|was|were|are|\:)?[:]*[\s]*(\d+-\d+-\d+)'
                                ]

    }

    pattern_strings = string_lookup["word"]
    note = " ".join(whole_note)



        #note = str(note_dict[self.note_keyword])
    #except KeyError:
    #    print("Wrong Note Keyword entered")
    #    raise

    phrase_matches = list()

    for phrase in keywords:

        for pattern_string in pattern_strings:

            pattern_string = pattern_string % phrase
            re_flags = re.I | re.M | re.DOTALL
            pattern = re.compile(pattern_string, flags=re_flags)
            match_iter = pattern.finditer(note)

            try:
                while True:
                    match = next(match_iter)
                    #print(match.start())
                    #print(match.end())

                    new_match =  (match.start()+1,match.start() + len(phrase)+1)

                    phrase_matches.append(new_match)

            except StopIteration:
                continue

    #phrase_matches.finalize_phrase_matches()
    return phrase_matches







def find_matches(keywords,whole_note):
    no_spaces = _process_raw(whole_note)
    coords = get_coordinates(keywords,no_spaces)
    return(no_spaces,coords)


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


