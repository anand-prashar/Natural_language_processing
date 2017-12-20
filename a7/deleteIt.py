    def standardize_string(userString):
        global punct
        returnList = []
        try:
            word_tokens = [x.lower() for x in word_tokenize(userString) if x not in punct ]
        except UnicodeDecodeError as _:
            word_tokens = []
            for word in userString.split():
                word =word.lower()
                if word[-1] in punct: word_tokens.append(word[:-1])
                else: word_tokens.append (word)    
        
        for word, pos in pos_tag(word_tokens):
            
            try:
                if pos == 'VBG':
                    if len(word)>3 and word[:-3] == 'ing':     #stemming
                        returnList.append( word[:-3])
                    elif len(word)>2 and word[:-2] == 'es':    #stemming
                        returnList.append( word[:-2])
                elif pos in ['VBD','VBN']:    
                    base = nltk.corpus.wordnet.morphy(str(word))
                    if base==None: base = word
                    returnList.append( base )  #morphing
                else: returnList.append( word )
            except Exception as _:
                returnList.append( word )
            
        return returnList