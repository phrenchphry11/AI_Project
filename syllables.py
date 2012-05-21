from BeautifulSoup import BeautifulSoup

def makeSyllableFile(fileName):
	wordFile = open(fileName)
	newFile = open('syllableDict.txt', 'w')
	for line in wordFile:
		line = line.strip()
		line = line.split("\\")
		pos = line[-1]
		word = line[:-1]
		sCount = get_syllables(word)
		newLine = word + '\t' + pos + '\t' + sCount + '\n'
		print >>newFile, newLine
	wordFile.close()
	newFile.close()

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

def main():
	makeSyllableFile('mobypos.txt')

main()