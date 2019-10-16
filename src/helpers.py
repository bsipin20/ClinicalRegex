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

def _is_match(self,keywords,word):
    match_ = False
    if word in keywords:
        match_ = True
    return(match_)

def _create_sent_list(self,sentence):
    words = tuple(sentence.split(" "))
    return(words)

def find_matches(self,keywords,sentence):

    """ finds match from string and returns coordinates 
        Args : 
            patterns : list of words to search
            sentences : the whole note that is cleaned and words separated by spaces
    """

    whole_note = self._create_sent_list(sentence)
    indexer = 0
    matches = list()

    for word in whole_note:

        if not word:
            indexer += len(word)
            
        if self._is_match(keywords,word):

            matches.append((indexer, indexer + len(word)-1))

        indexer += len(word) + 1

    return(matches)

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


