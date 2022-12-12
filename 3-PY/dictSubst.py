import json, re
import doctest

# loading data on where to find book
try:
	with  open("./sources/dictSubst.json", 'r') as f:
		dictSubst = json.load(f)
except FileNotFoundError:  
	dictSubst = {
#Normalizing white spaces, later <head> will have '\n\n'
' {1,}'                 : ' ',
'\n.{1,}' 			: '\n', # dealt in body of functioon
r'\
</p>'				: '</p>',

#Normalize some superscript
'ª'						: '<sup>a</sup>',

#HTML tags
'<b>'					: '<emph rend="bold">',
'<i>'					: '<emph rend="italic">',
'<u>'					: '<emph rend="underscore">',
'</b>|</i>|</u>'		: '</emph>',
'<br />'				: '<lb />',
'<head>'				: r'\n\n<head>',
'</head>'				: r'</head>\n',

#'\.\^a' :'.<sup>a</sup>',
'\.\^([a-z]{1,3})' : r'.<sup>\1</sup>'
}
	pass
except: print('ERRO: dicionário "dictSubst" não existe, nem pôde ser criado')

"""REVIEW!"""
def substDict(text,dictSubst):

	"""
	Given a text, do regex substitutions
    _based on a dictionary

	:param text: str
	:param dictSubst:  dict
	:return: str

	>>> substDict("O gato <b>preto</b> cruzou   a   estrada<br />",dictSubst)
	"O gato <emph rend='bold'>preto</emph> cruzou a estrada<lb />"
	>>> substDict("Que V. Ex.^a tem romances na sua bibliotheca",dictSubst)
	"Que V. Ex.<sup>a</sup> tem romances na sua bibliotheca"
	>>> substDict("Que o Il.^mo tem romances na sua bibliotheca",dictSubst)
	"Que o Il.<sup>mo</sup> tem romances na sua bibliotheca"
	"""

	# regex = re.compile("|".join(map(repr, dictSubst.keys())))
	# return regex.sub(lambda match: dictSubst[match.group(0)], text)
	for key, value in dictSubst.items():
		print(key)
		text = re.sub(key,value, text)
	return text

doctest.testmod()