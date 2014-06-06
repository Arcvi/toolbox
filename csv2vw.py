'Convert CSV file to vw format.'
'argv[1]: csv file.'
'argv[2]: output file.'
'argv[3] does it have weights? If so they are expected in the second column.'
'argv[4] is it testing? No target or weights expected.'

import sys
import csv

def construct_line( label, line, headers, importance):
	new_line = []
	if float(label) == 0.0:
		label = '-1'
	new_line.append( "%s %s |n " % ( label, importance ))
	
	for i, item in enumerate( line ):
		if float( item ) == 0.0:
			continue	# sparse!!!	
		new_item = "%s:%s" % ( i + 1, item )
		if headers:
			new_item = "%s:%s" % ( headers[i], item )
		new_line.append( new_item )
	new_line = " ".join( new_line )
	new_line += "\n"
	return new_line

# ---

input_file = sys.argv[1]
output_file = sys.argv[2]

i = open( input_file )
o = open( output_file, 'w' )

reader = csv.reader( i )
headers = reader.next()

# argv[3]: importance variable?
try:
	check_importance = int(sys.argv[3])
except IndexError:
	check_importance = 0

# argv[4] test?
try:
	check_test = int(sys.argv[4])
except IndexError:
	check_test = 0

# clean headers
if not check_test:
	headers.pop(0) #remove target

if check_importance:
	headers.pop(0) #remove importance


n = 0
for line in reader:
	label = 1
	if not check_test:
		label = line.pop(0)

	importance = 1.0
	if check_importance:
		importance = line.pop(0)
		
	new_line = construct_line( label, line, headers, importance)
	o.write( new_line )
	
	n += 1
	if n % 10000 == 0:
		print n
		
		