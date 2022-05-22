import nltk
import sys
import os
import string
import numpy

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    
    wd=os.getcwd()
    result={}
    for i in os.listdir(wd+os.sep+directory+os.sep):
        file=open(wd+os.sep+directory+os.sep+i,'r',encoding='utf-8')
        result[i]=file.read()
        file.close()
        
    return result


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    
    memoire=nltk.tokenize.word_tokenize(document)
    test=False
    result=[]
    
    for i in range(len(memoire)):
        memoire[i]=memoire[i].lower()
        test=False
        for j in range(len(string.punctuation)):
            if(memoire[i].count(string.punctuation[j]) == len(memoire[i])):
                test=True
                break
        if(not test and not memoire[i] in nltk.corpus.stopwords.words("english")):
            result.append(memoire[i])
            
    return result


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    values=[]
    for i in documents.values():
        values+=i
    values=set(values)
    result={}
    for i in values:
        count=0
        for j in documents.keys():
            if i in documents[j]:
                count+=1
        result[i]=numpy.log(len(documents.keys())/count)
    
    return result


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    
    documents={}
    for i in files.keys():
        documents[i]=0
        for j in query:
            if(j in files[i]):
                documents[i]+=files[i].count(j)*idfs[j]
    result=[i[0] for i in sorted(documents.items(), key=lambda t: t[1], reverse=True)]
    
    return result[0:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    
    phrases={}
    number={}
    for i in sentences.keys():
        phrases[i]=0
        for j in query:
            if(j in sentences[i]):
                phrases[i]+=idfs[j]
    result={i[0]:i[1] for i in sorted(phrases.items(), key=lambda t: t[1], reverse=True)}
    count=[result.values()].count([result.values()][0])
    if(count!=1):
        for i in sentences.keys():
            if(result[i]==[result.values()][0]):
                number[i]=0
                for j in query:
                    if(j in sentences[i]):
                        number[i]+=1
        resultbis=[i[0] for i in sorted(number.items(), key=lambda t: t[1], reverse=True)]
        result=[i for i in result.keys()]
        result=resultbis+result[len(resultbis):]
    else: 
        result=[i for i in result.keys()]
    
    return result[:n]


if __name__ == "__main__":
    main()
