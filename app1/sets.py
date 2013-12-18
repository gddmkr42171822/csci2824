# Robert Werthman CSCI 2824
# coding: utf-8
import csv

#1. WORegions	=	{country	codes	in	WorldBank2012DataWORegions.csv}
# Regions	=	{country	codes	in	WorldBank2012Regions.csv}

WOCountries = set()
Countries = set()
arable_countries = set()
with open('WorldBank2012DataWORegions.csv', 'rU') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    for row in reader:
        WOCountries.add(row[1])
        if row[3] == 'AG.LND.ARBL.ZS':
                if row[4] != '':
                	if float(row[4]) > 10.0:
        				arable_countries.add(row[1])
WOCountries.remove('Country Code')

with open('WorldBank2012Regions.csv', 'rU') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    for row in reader:
        Countries.add(row[1])
        
Countries.remove('Country Code')
print
print "1. Create WOCountries and Countries"
print
print "a. WOcountries " + str(WOCountries)
print
print "b. Countries " + str(Countries)

# 2. 	Determine	if	WORegions	=	Regions.	If	the	sets	are	not	equal	(Hint:	they’re
#       not),	determine	which	is	the	superset,	and	find	the	difference	between	the
#       sets.	Print	all	of	your	results	to	the	terminal.

print
if Countries == WOCountries:
    print "2. The sets are equal"
    print
else:
    print " 2. The sets are not equal"
    print
    if Countries.issuperset(WOCountries):
        print "a. Regions is the superset"
        print
        print "b. The difference between the sets is " + str(Countries.difference(WOCountries))
        print
    else:
        print "a. WORegions is the superset"
        print
        print "b. The difference between the sets is " + str(WOCountries.difference(Countries))
        print

#3. Find	WOCountries intersect Countries	and	print	your	results	to	the	terminal.

setintersection = Countries.intersection(WOCountries)
print "3. The elements of (WORegions intersect Regions) are " + str(setintersection)
print
#4. Generate	a	set	of	regions,	such	that: RegionCodes	=	{regions	in	WorldBank2012Regions.csv}

RegionCodes = set()
SpecCountries = set()
dict1 = {}
with open('WorldBank2012Regions.csv', 'rU') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    for row in reader:
    	dict1.setdefault(row[2], []).append(row[1]) #create dictionary-like partition of region codes mapped to countries
        if row[2] == 'Sub-Saharan Africa' or row[2] == 'South Asia':
        	SpecCountries.add(row[1])
        	
del dict1['Region']
print "4. Regions mapped to country codes " +str(dict1)
print

#5. Determine	if	RegionCodes	is	a	valid	partition	of	WORegions intersect Regions.
#There	are	three	steps	to	showing	that	a	partition	is	valid,	all	three	steps	need
#to	be	included	here.	Output	the	result	of	each	step	to	the	terminal.

print "5. RegionCodes is a valid partions of WORegions intersect Regions if..."
nonempty = True
for key in dict1.keys():
    if key == []:
        nonempty = False
if nonempty == True:
    print "a. RegionCodes is nonempty"
    
value_duplicates = set()
for value in dict1.values():
	for x in value:
		value_duplicates.add(x)
	
value_duplicates = len(value_duplicates)
l = 0
for value in dict1.values():
	for x in value:
		if x in setintersection:
			l += 1
if l == value_duplicates:
	print "b. All elements in the partition are unique"
else:
 	print "b. NO JOY"
# sets do not keep duplicates see http://neohaxor.org/index_files/removing-duplicates-with-python.html
#if regions is equal to setintersection
length = 0
for value in dict1.values():
	for x in value:
		if x in setintersection:
			length += 1
if length == len(setintersection):
	print "c. The Partition contains all of the elements in the set being partitioned"
else:
	print "c. Partition does not contain all of the elements of the set therefore it is not a partition."

# 6. Generate	a	set	of	countries	in	Sub-Saharan	Africa	and	South	Asia	from	the	set
#of	countries	in	WORegions intersect Regions,	such	as:
#SSASA	=	{(countries	in	SSA	or	Asia) ∩(WOCountries intersect Countries)}

print
SSASA = SpecCountries.intersection(setintersection)
print "6. Sub-Saharan Africa and South Asia intersect WORegions intersect Regions " + str(SSASA)

#7. Generate	a	set	of	countries	with	(Arable	land	(%	land	area))	>	10%	from	the
#set	of	countries	in	WORegions intersect Regions,	such	as
#ArableLand	=	{(countries	with	arable	land	>	10%) ∩(WORegions intersect Regions)}
#Use	the	indicator	code	for	arable	land	%.	It’s	just	easier.
# this code: AG.LND.ARBL.ZS

ArableLand = arable_countries.intersection(setintersection)
print
print "7. Countries with arable land > 10% intersect WORegions intersect Regions " + str(ArableLand)

#8. Find SSASA intersect Arableland.  Output the results to the terminal.
print
print "8. SSASA intersect Arableland " + str(SSASA.intersection(ArableLand))