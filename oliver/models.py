import numpy as np
import string
import heapq
import nltk
nltk.data.path.append('./nltk_data/')
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords



class CooccurrenceMatrix:
    """
    corpus        --  text file, declared when object created
    data          --  string
    sents         --  list of strings, all the sentences in text file (with punctiation)
    tokens        --  list of strings, all tokens in text file (with repetitions)
    unique_tokens --  list of strings, all unique tokens
    num_tokens    --  int, number of unique tokens in text
    fdist         --  fdist object
    cooc_matrix   --  2D list, initialized to all 0's in prepareCorpus
    word_indices  --  dictionary (key=word, value=index in cooc_matrix)
    """
    def __init__(self, c):
        self.corpus = c 
        self.data = ""
        self.sents = []
        self.tokens = []
        self.unique_tokens = []
        self.num_tokens = 0
        self.fdist = None
        self.cooc_matrix = None
        self.word_indices = {}
        
    def prepareCorpus(self):
        """Given a text file, removes punctuation, returns the list of all tokens, list of unique tokens, 
        list of sentences, the number of unique tokens, and the frequency distribution. 
        Also initializies cooc_matrix to all 0's with size = num_tokens"""
        with open(self.corpus, 'r') as myfile:
            self.data = myfile.read().replace('\n', '')
        self.data = self.data.lower()
        self.data = self.data.decode('utf-8')

        sw = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
                'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
                'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
                'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
                'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
                'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
                'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
                'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
                'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
                'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
                'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
                'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

        try:
            data_no_stop = [i for i in self.data.split() if i not in stopwords.words('english')] #can replace w/ stopwords.words('english')
        except UnicodeDecodeError as ude:
            raise ude
        self.data = " ".join(data_no_stop)
        self.sents = sent_tokenize(self.data)
        self.data = self.removePunctuation(self.data)
        self.tokens = word_tokenize(self.data)
        self.unique_tokens = set(self.tokens)
        self.num_tokens = len(self.unique_tokens)
        self.fdist = FreqDist(self.tokens)
        self.cooc_matrix = np.zeros((self.num_tokens, self.num_tokens))
        self.fillMatrix()
        return

    def fillMatrix(self):
        """Fills the cooccurrence matrix"""
        self.findIndices()
        for s in self.sents:
            s = self.removePunctuation(s)
            words = word_tokenize(s)
            self.examineSentence(words)
        return 
    
    def examineSentence(self, sentence):
        """Given a sentence (list of words), updates cooccurrence matrix with number of cooccurrences within sentence
        Ignores cooccurrences of word with itself"""
        for word1 in sentence:
            for word2 in sentence:
                index1 = self.word_indices[word1]
                index2 = self.word_indices[word2]
                if word1 != word2:
                    self.cooc_matrix[index1][index2] += 1
        return
    
    def findIndices(self):
        """Sets word_indices, where each key is a unique token and each value is a index in the cooc_matrix"""
        counter = 0
        for t in self.unique_tokens:
            self.word_indices[t] = counter
            counter += 1
        return

    def removePunctuation(self, text):
        """Given a piece of text, removes all punctuation (replacing periods, semicolons, colons with spaces)"""
        text = text.replace(".", " ")
        text = text.replace(";", " ")
        text = text.replace(":", ".")
        text = text.replace(",", "")
        text = text.replace("-", " ")
        exclude = set(string.punctuation)
        text = ''.join(ch for ch in text if ch not in exclude)
        return text
    
    def findCooccurrence(self, target_word):
        """returns the cooccurrences of a given word"""
        if target_word not in self.word_indices:
            return "Target word not in corpus. Try another word."
        index_target_word = self.word_indices[target_word]
        vals = []
        top3 = []
        max_index = 0
        for col in range(self.num_tokens):
            if len(top3) > 3:
                del(top3[-1])
            vals.append(self.cooc_matrix[index_target_word][col])
        top3 = heapq.nlargest(3, set(vals)) #number of coocs --> can change top-n
        coocs = [] #index of top3 coocs
        for i in top3:
            for j in range(self.num_tokens):
                if self.cooc_matrix[index_target_word][j] == i:
                    coocs.append(j)
                    break
        result = []
        for c in coocs:
            result.append((list(self.word_indices.keys())[list(self.word_indices.values()).index(c)]))
        return result
