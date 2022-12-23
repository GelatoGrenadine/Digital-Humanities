import spacy
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
import re
import csv

def naiveTokenizer(text):
	filterout = ['','0','1', 'N/A']
	
	if text in filterout: return []

	text = text if '[' not in text else re.sub('[...]','',text)
	
	if   '"' in text: tokens = re.findall('"([^"]*?)"',text)
	elif ',' in text: tokens = text.split(',')
	else: return []
	
	tokens = [t.strip() for t in tokens]
	return list(tokens)

def manual_input_checker(txt,listing):
    return [item for item in listing if item.lower() in txt.lower()]

def correct_global_sen(key):
    manual_global = [
    'Negativo','negativo','Negativo ','negativo ',
    'netro','Neutra','Neutro','neutro','neutro ','Neutro ',' Neutro',
    'Positivo','positivo','positivo '
    ]
    correction_global = ['NEGATIVE']*4 +['NEUTRAL']*7 +['POSITIVE']*3
    corrector_global = dict(zip(manual_global,correction_global))
    
    return corrector_global.get(key,'')

class Languager():
    __slots__ = 'nlp','doc','tokens','punct','words','uniques','lexical'

    def __init__(self, model):
        self.nlp = spacy.load(model)

    def __call__(self, text):
        self.doc = self.nlp(text)
        

        self.tokens = [token for token in self.doc]
        self.punct =  [token for token in self.tokens if token.is_punct]
        self.words =  [(token.text, token.pos_) for token in self.tokens if not token.is_punct]
        self.uniques = set(self.words)

        noun = 		len([token[0] for token in self.words if token[1] == 'NOUN'])
        adjective = len([token[0] for token in self.words if token[1] == 'ADJ' ])
        adverb = 	len([token[0] for token in self.words if token[1] == 'ADV' ])
        verb = 		len([token[0] for token in self.words if token[1] == 'VERB'])
        lexical_diversity = noun+adjective+adverb+verb
        lexical_density = 100*(lexical_diversity)/len(self.words)

        self.lexical = {
            '#noun': noun,
            '#adjective': adjective,
            '#adverb': adverb,
            '#verb': verb,
            'lexical_diversity': lexical_diversity,
            'lexical_density': lexical_density
        }


class Sentimenter():

    def __init__(self, model):
        self.model = model
        self.sentimenter = pipeline("sentiment-analysis", model=self.model)

    def __call__(self, text):
        try: self.sentiment = self.sentimenter(text)[0]
        except Exception: raise Exception('Error in sentiment analysis')


class Summarizer():

    def __init__(self, model):
        self.model = model
        self.summarizer = pipeline("summarization", model=self.model)

    def __call__(self, text):
        words = text.split()
        try:
            self.summary = self.summarizer(text, 
									max_length=len(words), 
									do_sample=False)[0].get('summary_text')
        except Exception: raise Exception('Error in sentiment analysis')


summary_model = ['phpaiola/ptt5-base-summ-xlsum', 
			     'phpaiola/ptt5-base-summ-cstnews', 
			     'phpaiola/ptt5-base-summ-temario', 
			     'phpaiola/ptt5-base-summ-wikilingua']

"""Init nlp instances"""
doc = Languager('pt_core_news_lg')
sen = Sentimenter('turing-usp/FinBertPTBR')
smm = Summarizer(summary_model[1])

input1 = './input/Camilo_AP_frases.csv'
input2 = './input/camilo_frases.csv'

header = ['ref', 'texto', 
          '#tokens', '#palavras', '#unicas', '#pontuação', 
          '#nomes', '#adjectivos', '#adverbios', '#verbos', 
        		'diversidade_lexical', 'densidade_lexical', 
          'input_sent', 'input_pos_tkn', 'input_neg_tkn',
          'fixed_sent', 'fixed_pos_tkn', 'fixed_neg_tkn',
		  'auto_sent', 'auto_score',
          'summarizador']

with open('./output/analysis.tsv', 'w', encoding='utf8') as csv_file:
    csvwriter = csv.writer(csv_file, delimiter='\t')
    csvwriter.writerow(header) 

out, summary = [], ''
with open(input2, 'r') as file:
    csvreader = csv.reader(file)
    next(csvreader)
    line = 1
    for i,row in enumerate(csvreader):
        """Fixing manual input"""
        if i == 444: row[6] = row[5]
        if row[1].find('CAPÍTULO') == 0: continue # to ignore line
        input_pos_tkns = naiveTokenizer(row[4])
        input_neg_tkns = naiveTokenizer(row[6])
        fixed_global   = correct_global_sen(row[2])
        fixed_pos_tkns = manual_input_checker(row[1],input_pos_tkns)
        fixed_neg_tkns = manual_input_checker(row[1],input_neg_tkns)

        """Call nlp instance"""
        doc(row[1])
        sen(row[1])
        smm(row[1])

        summary_instance = smm.summary

        out.append([line ,row[1]] \
                  +[len(doc.tokens),len(doc.words), \
                    len(doc.uniques),len(doc.punct)] \
                  + list(doc.lexical.values()) \
                  +[row[2],input_pos_tkns,input_neg_tkns] \
                  +[fixed_global, fixed_pos_tkns, fixed_neg_tkns] \
                  + list(sen.sentiment.values()) \
                  +[summary_instance]
        )
        summary += summary_instance
        with open('./output/analysis.tsv', 'a', encoding='utf8') as csv_file:
            csvwriter = csv.writer(csv_file, delimiter='\t')
            csvwriter.writerow(out[-1]) 
        line+=1
        # print(out[-1])
        # if i > 20: exit()
        #print(f'\033[1A\x1b[2K processing line: {(i+1):>4}')


with open('./output/summary.txt', 'w', encoding='utf8') as txt_file:
    txt_file.write(summary)

# with open('./output/analysis.tsv', 'w', encoding='utf8') as csv_file:
#     csvwriter = csv.writer(csv_file, delimiter='\t')
#     csvwriter.writerow(header) 
#     csvwriter.writerows(out)