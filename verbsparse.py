verbs = open("verbs")

verbsparsed = open("verbs_parsed", "w")

for line in verbs:
	line = line.split()
	verb = line[0]
	verbsparsed.write(verb+"\n")

verbs.close()
verbsparsed.close()
