
from BeautifulSoup import BeautifulSoup

#from wordnik.api.APIClient import APIClient
#import wordnik.model
import urllib

#from wordnik.api.WordAPI import WordAPI
#from wordnik.api.WordsAPI import WordsAPI


import random

#api_key = 'a4175a965b1146ebd100109d2e106a9ed0ddcc28dd82a6b84'
url = 'http://www.wordcalc.com/index.php'

#my_client = APIClient(api_key, 'http://api.wordnik.com/v4')

#myW = WordAPI(my_client)
#w = WordsAPI(my_client)

#i = wordnik.model.WordsRandomWordInput()
#i.includePartOfSpeech = 'noun'

#example = w.getRandomWords()
#example.extend(w.getRandomWords())
"""
word_selection = []
for e in example:
	myW.getPhrases(e.word)
	post_data = urllib.urlencode(
	    {'text': e.word})
	post_data = '%s&optionSyllableCount&optionWordCount' % post_data


	cnxn = urllib.urlopen(url, post_data)
	response = cnxn.read()
	cnxn.close()

	soup = BeautifulSoup(response)
	h3_matches = [h3 for h3 in soup.findAll('h3') if h3.text == 'Statistics']
	if len(h3_matches) != 1:
	  raise Exception('Wrong number of <h3>Statistics</h3>')
	h3_match = h3_matches[0]
	table = h3_match.findNextSibling('table')

	td_matches = [td for td in table.findAll('td')
	              if td.text == 'Syllable Count']
	if len(td_matches) != 1:
	  raise Exception('Wrong number of <td>Syllable Count</td>')
	td_match = td_matches[0]

	td_value = td_match.findNextSibling('td')
	syllable_count = int(td_value.text)

	word_selection.append((syllable_count,e.word))
"""
def get_syllables(word):
	#myW.getPhrases(word)
	post_data = urllib.urlencode(
	    {'text': word})
	post_data = '%s&optionSyllableCount&optionWordCount' % post_data


	cnxn = urllib.urlopen(url, post_data)
	response = cnxn.read()
	cnxn.close()

	soup = BeautifulSoup(response)
	h3_matches = [h3 for h3 in soup.findAll('h3') if h3.text == 'Statistics']
	if len(h3_matches) != 1:
	  raise Exception('Wrong number of <h3>Statistics</h3>')
	h3_match = h3_matches[0]
	table = h3_match.findNextSibling('table')

	td_matches = [td for td in table.findAll('td')
	              if td.text == 'Syllable Count']
	if len(td_matches) != 1:
	  raise Exception('Wrong number of <td>Syllable Count</td>')
	td_match = td_matches[0]

	td_value = td_match.findNextSibling('td')
	syllable_count = int(td_value.text)
	return syllable_count

	#word_selection.append((syllable_count,word))

#print word_selection


def add_syllables(file):
	fname = open(file)
	fname1 = open('nouns_syllables', 'w')
	for line in file:
		print line
		line = line.split()

		syll = str(get_syllables(line[0]))
		print syll
		newline = str(line[0]) + " " + syll
		fname1.write(newline)
	fname.close()
	fname1.close()


#add_syllables('articles')


def generate_poem(word_selection):
	poem = ''

	#first line
	artic = open('articles')
	articles = []
	for line in artic:
		line = line.split()
		articles.append(line[0])

	random.shuffle(articles)

	index = random.randrange(0, len(articles))
	first_word = articles[index]
	tot_syllables = 5 - get_syllables(first_word)

	poem += first_word

	adjective = open('adjectives')
	adj = []
	for line in adjective:
		line = line.split()
		adj.append(line[0])

	random.shuffle(adj)

	index = random.randrange(0, len(adj))
	second_word = adj[index]
	tot_syllables -= get_syllables(second_word)

	poem += " " + second_word

	nouns = open('nouns')
	noun = []
	for line in nouns:
		line = line.split()
		noun.append(line[0])

	random.shuffle(noun)
	print noun, 'nounlist'

	for word in noun:
		syllables = get_syllables(word)
		temp_syllables = tot_syllables
		temp_syllables -= syllables
		if temp_syllables == 0:
			poem += " " + word
			break



	poem += '\n'

	#second line
	index = random.randrange(0, len(word_selection))
	first_word = word_selection[index][1]
	tot_syllables = 7 - word_selection[index][0]
	del word_selection[index]

	poem += first_word

	i = 0 
	while i < (len(word_selection)):
		if word_selection[i][0] < tot_syllables:
			poem += ' ' + word_selection[i][1]
			tot_syllables -= word_selection[i][0]
			del word_selection[i]
		i += 1
	poem += '\n'


	#third line
	index = random.randrange(0, len(word_selection))
	first_word = word_selection[index][1]
	tot_syllables = 5 - word_selection[index][0]
	del word_selection[index]

	poem += first_word


	i = 0
	while i < (len(word_selection)):
		if word_selection[i][0] < tot_syllables:
			poem += ' ' + word_selection[i][1]
			tot_syllables -= word_selection[i][0]
			del word_selection[i]
		i += 1
	poem += '\n'

	return poem

#print generate_poem(word_selection)


