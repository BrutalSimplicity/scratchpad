#!/usr/bin/python
import re


class PascalParser:
	comments = {'{' : '}', '(*' : ')', '//' : ''}

	def __init__(self, filename, units_only=True):
		self.filename = filename
		header = self.strip_comment(self.get_header()).split()
		self.header = (header[0].strip().lower(), header[1].rstrip(';').lower())
		# if (self.header[0] != 'unit'):
		# 	return

		(self.interface, self.implementation) = self.parse_structure()
		self.interface_list = self.parse_interface()


	def get_header(self):
		with open(self.filename) as pas_file:
			for line in pas_file:
				com_type = self.get_comment_type(line)
				if com_type:
					if com_type == 'SC':
						continue
					else:
						next_line = line
						while (next_line.find('}') < 0) and (next_line.find('*)') < 0):
							next_line = next(pas_file)
				#first line of code should be the header
				if line.rfind(';') > -1:
					return line.strip()
		return None

	def get_comment_type(self,line):
		for comment in self.comments.keys():
			com_st = line.rfind(comment)
			if (com_st > -1):
				if (comment == '//' or 
					line.rfind(self.comments[comment]) > -1):
					return 'SC'
				else:
					return 'MC'
		return None

	def strip_comment(self, line):
		ctype = self.get_comment_type(line)
		ret_line = line
		while ctype == 'SC':
			print ret_line
			if (ret_line.rfind('//') > -1):
				ret_line = ret_line[:ret_line.rfind('//')]
			else:
				for comment in self.comments.keys():
					comment_start = ret_line.rfind(comment)
					if (comment_start > -1):
						comment_end = ret_line.rfind(self.comments[comment])
						ret_line = ret_line[:comment_start] + ret_line[comment_end+1:]
						break
			ctype = self.get_comment_type(ret_line)
		return ret_line


	def parse_structure(self):
		definitions = None
		discard = []
		with open(self.filename) as lines:
			for line in lines:
				line = line.strip()
				if not line: continue
				discard.append(line)
				if line.lower() == 'interface':
					definitions = []
					break
			for line in lines:
				line = line.strip()
				if line.lower() == 'implementation': 
					discard.append(line)
					break
				definitions.append(line)
			for line in lines:
				discard.append(line.strip())

			definitions = filter(bool, definitions)
			discard = filter(bool, discard)
			definitions = map(self.strip_comment, definitions)
			discard = map(self.strip_comment, discard)

		return (definitions, discard)

	def parse_interface(self):
		inst_list = []
		inst_line = []
		for inst in self.interface:
			inst_line.append(inst.strip())

			if inst.rfind(';') > -1:
				inst_list.append(' '.join(inst_line).rstrip(';') if len(inst_line) > 1 else inst_line[0].rstrip(';'))
				inst_line = []
			else:
				if 

		return inst_list

	def get_imports(self):
		imports = []
		for decl in self.interface_list:
			found = decl.find('uses')
			if (found > -1):
				imports = map(str.strip, decl[found+4:].split(','))
				break
		return imports



if __name__ == '__main__':
	print 'Script auto-executing with default parameters.'
	p = PascalParser('tc_config.pas')
