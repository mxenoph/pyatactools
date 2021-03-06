#!/usr/bin/python

########################################################################
# 27 April 2015
# Patrick Lombard, Centre for Stem Stem Research
# Core Bioinformatics Group
# University of Cambridge
# All right reserved.
########################################################################

import subprocess
import sys, re, os
import ConfigParser
import itertools
import argparse
import tempfile
import pkg_resources
from multiprocessing import Pool, Manager
import pybedtools


def ConfigSectionMap(section, Config):
	dict1 = {}
	options = Config.options(section)
	for option in options:
		try:
			dict1[option] = Config.get(section, option)
			if dict1[option] == -1:
				DebugPrint("skip: %s" % option)
		except:
			print("exception on %s!" % option)
			dict1[option] = None
	return dict1

def transdense(sam, transdense_dir, return_dict):
	fh = tempfile.NamedTemporaryFile(delete = False)
	filename = os.path.basename(sam)
	name = re.sub(".sam$", "", filename)
	with open(sam) as f:
		for line in f:
			if line.startswith("@"):
				pass
			else:
				word = line.rstrip().split("\t")
				if len(word) > 8: #Presumes it removes unaligned reads
					if word[2] == "chrM" or word[2] == "M": #Filter because of not relevant
						pass
					else:
						if int(word[8]) > 0:		
							start = int(word[3]) - 11 
							end = int(word[3]) + 17
							if start > 0:
								fh.write("{}\t{}\t{}\tT\t0\t+\n".format(word[2], start, end)),
						elif int(word[8]) < 0:
							start = int(word[3]) - int(word[8])
							start -= 19
							end = int(word[3]) - int(word[8])
							end += 9

							if start > 0:
								fh.write("{}\t{}\t{}\tT\t0\t+\n".format(word[2], start, end)),
	fh.close()
	command = "sort -k1,1 -k2,2n {} | uniq > {}/{}_mytransDense.bed".format(fh.name, transdense_dir, name)
	return_dict["{}/{}_mytransDense.bed".format(transdense_dir, name)] = 1
	subprocess.call(command, shell=True)
	os.remove(fh.name)

def get_nfree(sam, nfree_dir, return_dict):
	filename = os.path.basename(sam)
	name = re.sub(".sam", "", filename)
	fh = tempfile.NamedTemporaryFile(delete = False)
	with open(sam) as f:
		for line in f:
			if line.startswith("@"):
				pass
			else:
				word = line.rstrip().split("\t")
				if len(word) < 9: #Presumes it removes unaligned reads
					pass
				else:
					if word[2] == "chrM" or word[2] == "M": #Filter because of not relevant
						pass
					else:
						if int(word[8]) == 0:
							pass
						else:
							if int(word[8]) < 100 and int(word[8]) > -100:
								if int(word[8]) > 0:		
									start = int(word[3]) - 11 
									end = int(word[3]) + 17
									if start > 0:
										fh.write("{}\t{}\t{}\tT\t0\t+\n".format(word[2], start, end)),
								elif int(word[8]) < 0:
									start = int(word[3]) - int(word[8])
									start -= 19
									end = int(word[3]) - int(word[8])
									end += 9
									if start > 0:
										fh.write("{}\t{}\t{}\tT\t0\t+\n".format(word[2], start, end)),
	fh.close()
	command = "sort -k1,1 -k2,2n {} | uniq > {}/{}_mynfree.bed".format(fh.name, nfree_dir, name)
	return_dict["{}/{}_mynfree.bed".format(nfree_dir, name)] = 1
	subprocess.call(command, shell=True)
	os.remove(fh.name)

def get_nfree_2_types(sam, nfree_small, nfree_large, return_dict):
	filename = os.path.basename(sam)
	name = re.sub(".sam", "", filename)
	fh_small = open("{}/{}_tmp.bed".format(nfree_small, name), "w")
	fh_large = open("{}/{}_tmp.bed".format(nfree_large, name), "w")
	print sam, name
	with open(sam) as f:
		for line in f:
			if line.startswith("@"):
				pass
			else:
				word = line.rstrip().split("\t")
				if len(word) < 9: #Presumes it removes unaligned reads
					pass
				else:
					if word[2] == "chrM" or word[2] == "M": #Filter because of not relevant
						pass
					else:
						if int(word[8]) == 0:
							pass
						else:
							if int(word[8]) < 60 and int(word[8]) > -60:
								if int(word[8]) > 0:		
									start = int(word[3]) - 11 
									end = int(word[3]) + 17
									if start > 0:
										fh_small.write("{}\t{}\t{}\tT\t0\t+\n".format(word[2], start, end)),
								elif int(word[8]) < 0:
									start = int(word[3]) - int(word[8])
									start -= 19
									end = int(word[3]) - int(word[8])
									end += 9
									if start > 0:
										fh_small.write("{}\t{}\t{}\tT\t0\t+\n".format(word[2], start, end)),
							elif int(word[8]) < 100 and int(word[8]) > -100:
								if int(word[8]) > 0:		
									start = int(word[3]) - 11 
									end = int(word[3]) + 17
									if start > 0:
										fh_large.write("{}\t{}\t{}\tT\t0\t+\n".format(word[2], start, end)),
								elif int(word[8]) < 0:
									start = int(word[3]) - int(word[8])
									start -= 19
									end = int(word[3]) - int(word[8])
									end += 9
									if start > 0:
										fh_large.write("{}\t{}\t{}\tT\t0\t+\n".format(word[2], start, end)),
	fh_small.close()
	fh_large.close()
	command1 = "sort -k1,1 -k2,2n {}/{}_tmp.bed | uniq > {}/{}_mynfree.bed".format(nfree_small, name, nfree_small, name)
	command2 = "sort -k1,1 -k2,2n {}/{}_tmp.bed | uniq > {}/{}_mynfree.bed".format(nfree_large, name, nfree_large, name)
	return_dict["{}/{}_mynfree.bed".format(nfree_small, name)] = 1
	return_dict["{}/{}_mynfree.bed".format(nfree_large, name)] = 1
	subprocess.call(command1, shell=True)
	subprocess.call(command2, shell=True)
	os.remove(fh_small.name)
	os.remove(fh_large.name)

def get_npres(sam, npres_dir, return_dict): 
	fh = tempfile.NamedTemporaryFile(delete = False)
	filename = os.path.basename(sam)
	name = re.sub(".sam", "", filename)
	with open(sam) as f:
		for line in f:
			if line.startswith("@"):
				pass
			else:
				word = line.rstrip().split("\t")
				if len(word) > 9:
					if word[2] == "chrM" or word[2] == "M":
						pass
					else:
						if int(word[8]) > 180 and int(word[8]) < 247:
							mid = int(word[3])+ (float(word[8])/2)
							fh.write("{}\t{}\t{}\tT\t0\t+\n".format(word[2], int(round(mid-75-1)), int(round(mid+75-1)))), 
						elif int(word[8]) > 315 and int(word[8]) < 473:
							mid = float(word[8])/3
							fh.write("{}\t{}\t{}\tT\t0\t+\n".format(word[2], int(round(int(word[3])+mid-75-1)), int(round(int(word[3])+mid+75-1)))), 
							fh.write("{}\t{}\t{}\tT\t0\t+\n".format(word[2], int(round(int(word[3])+(mid*2)-75-1)), int(round(int(word[3])+(mid*2)+75-1)))), 
						elif int(word[8]) > 558 and int(word[8]) < 615:
							mid = int(word[3])+ (float(word[8])/4)
							fh.write("{}\t{}\t{}\tT\t0\t+\n".format(word[2], int(round(int(word[3])+mid-75-1)), int(round(int(word[3])+mid+75-1)))), 
							fh.write("{}\t{}\t{}\tT\t0\t+\n".format(word[2], int(round(int(word[3])+(mid*2)-75-1)), int(round(int(word[3])+(mid*2)+75-1)))), 
							fh.write("{}\t{}\t{}\tT\t0\t+\n".format(word[2], int(round(int(word[3])+(mid*3)-75-1)), int(round(int(word[3])+(mid*3)+75-1)))), 
	fh.close()
	command = "sort -k1,1 -k2,2n {} | uniq > {}/{}_mynPres.bed".format(fh.name, npres_dir, name)
	return_dict["{}/{}_mynPres.bed".format(npres_dir, name)] = 1
	subprocess.call(command, shell=True)                                             
	os.remove(fh.name) #Always do 

def convert_bed_bw(bed, chrom):
	name = re.sub(".bed", "", bed)
	command = "bedtools genomecov -i {} -bg -g {} > {}.bedGraph".format(bed, chrom, name)
	subprocess.call(command, shell=True)
	command = ["bedGraphToBigWig", name+".bedGraph", chrom, name+".bw"]
	subprocess.call(command)
	os.remove(name+".bedGraph")

def function1(args):
	return transdense(*args)

def function2(args):
	return get_nfree(*args)

def function3(args):
	return get_npres(*args)

def function4(args):
	return convert_bed_bw(*args)

def function5(args):
	return get_nfree_2_types(*args)

def main():
	parser = argparse.ArgumentParser(description='Takes deduplicated bam files and preprocess\'s for analysis\n')
	parser.add_argument('-c', '--config', help='Conditions containing Sam/Bam files, values are naming', required=True)
	parser.add_argument('-g', '--genome', help='Genome the samples are aligned to, options include	 mm10/mm9/hg19', required=True)
	parser.add_argument('-o', '--outdir', help='Output directory, will create transdense, nfree and npres directories', required=True)
	parser.add_argument('-t', '--threads', help='threads, default=1', default=1, required=False)
	parser.add_argument('-b', action='store_true', help='Use if Config contains bam files', required=False) 
	parser.add_argument('-n', action='store_true', help='Runs just nfree <60 and >60', required=False) 
	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)
	args = vars(parser.parse_args())

	Config = ConfigParser.ConfigParser()
	Config.optionxform = str
	Config.read(args["config"])
	conditions = ConfigSectionMap("Conditions", Config)

	chrom = pkg_resources.resource_filename('pyatactools', 'data/{}.chrom.sizes'.format(args["genome"]))
	if not os.path.isfile(chrom):
		raise Exception("Unsupported Genome!")

	transdense_dir = os.path.join(args["outdir"], "transdense")
	nfree_dir = os.path.join(args["outdir"], "nfree")
	npres_dir = os.path.join(args["outdir"], "npres")
	pool = Pool(int(args["threads"]))

	if not os.path.isdir(transdense_dir):
		os.makedirs(transdense_dir)
		os.makedirs(nfree_dir)
		os.makedirs(npres_dir)
	
	ddup_bams = list(conditions.keys())
	if args["n"]:
		manager = Manager()
		return_dict = manager.dict()
		pool = Pool(int(args["threads"]))
		return_dict = manager.dict()
		nfree_dir1 = os.path.join(args["outdir"], "nfree_small")
		nfree_dir2 = os.path.join(args["outdir"], "nfree_large")
		if not os.path.isdir(nfree_dir1):
			os.makedirs(nfree_dir1)
			os.makedirs(nfree_dir2)
		pool.map(function5, itertools.izip(ddup_bams, itertools.repeat(nfree_dir1),itertools.repeat(nfree_dir2), itertools.repeat(return_dict)))
		pool.map(function4, itertools.izip(list(return_dict.keys()), itertools.repeat(chrom)))
	else:
		manager = Manager()
		return_dict = manager.dict()
		pool = Pool(int(args["threads"]))
		pool.map(function1, itertools.izip(ddup_bams, itertools.repeat(transdense_dir), itertools.repeat(return_dict)))
		pool.map(function4, itertools.izip(list(return_dict.keys()), itertools.repeat(chrom)))
		return_dict = manager.dict()
		pool.map(function2, itertools.izip(ddup_bams, itertools.repeat(nfree_dir), itertools.repeat(return_dict)))
		pool.map(function4, itertools.izip(list(return_dict.keys()), itertools.repeat(chrom)))
		return_dict = manager.dict()
		pool.map(function3, itertools.izip(ddup_bams, itertools.repeat(npres_dir), itertools.repeat(return_dict)))
		pool.map(function4, itertools.izip(list(return_dict.keys()), itertools.repeat(chrom)))