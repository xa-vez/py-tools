#!/usr/bin/python
import sys

class reports(object):
	def __init__(self):
		pass

	def add_file(self, file):
		new = open( file,"w")
		new.close() 
		
	def add_html(self, file):
		new = open( file,"w+")
		default = open( 'html/default.html', "r")
		lines = default.readlines()
		for x in lines:
			new.write(x)
		
		default.close()		
		new.close()
		
	def create(self, file):
		print(file + ' creating')

		self.add_file(file)
		self.add_html(file)
					
		print( file + ' was succesfully created')
		
if __name__== "__main__":
	import argparse

	options = argparse.ArgumentParser()
	#options.add_argument('-p', "--pdn", type=int, choices=[1,2,3], default=1, help="The PDN number")
	#options.add_argument('-l', "--lpm", type=int, choices=[1,2,3], default=1, help="The low power mode")
	options.add_argument('-n', "--name", type=str, default="", help="the generated file name")
	options.add_argument('-v', "--verbose", action="store_true", help="verbose mode")

	args = options.parse_args()

	if args.name != "" :
		title = str(args.name+'.html')
	else:
		title = str('report.html')
		
	if args.verbose :
		#print( 'verbose mode is runnig ' + args.domain + ' at PDN ' + str(args.pdn))
		print('verbose mode')
	
	print( 'generating: ' + title + ' ' + 'report' )
		
	doc = reports()
	doc.create(file=title)

