import os
import glob
import argparse


# Usage: generate_tandem.py [arguments]
# see main at end of script

def generate_taxonomy(directory,fasta_path,use_crap=False):
	input_path = os.path.join(directory,'taxonomy.xml')
	input_xml = open(input_path,'w')
	input_xml_text = """<?xml version="1.0"?>
<bioml label="x! taxon-to-file matching list">
	<note type="description">The paths in this file must be changed to point to the fasta
		or fasta.pro files on your system
	</note>
	<taxon label="refseq">
		<file format="peptide" URL="%(fasta_path)s" />
	</taxon>

</bioml>
"""
	subs = {'fasta_path': fasta_path,
			}
	input_xml.write(input_xml_text % subs)
	input_xml.close()


def generate_input_file(directory,mzml_path,default_path,threads):
	mzml = os.path.basename(mzml_path)
	#mzml_relpath = os.path.relpath(mzml_path,directory)
	#default_relpath = os.path.relpath(default_path,directory)
	input_path = os.path.join(directory,mzml+'.input.xml')
	output = mzml+'.output.xml'
	input_xml = open(input_path,'w')
	input_xml_text = """<?xml version="1.0" encoding="iso-8859-1" ?>
<bioml>
<note type="input" label="spectrum, threads">%(threads)d</note>
<note type="input" label="spectrum, path">%(mzml_path)s</note>
<note type="input" label="spectrum, skyline path">%(mzml_path)s</note>
<note type="input" label="list path, default parameters">%(default_file)s</note>
<note type="input" label="output, path">%(output_path)s</note>
<note type="input" label="list path, taxonomy information">taxonomy.xml</note>
<note type="input" label="protein, taxon">refseq</note>
%(extra)s
</bioml>
"""
	extra = ''	
#	if taxonomy_file_path:
#		extra += '<note type="input" label="list path, taxonomy information">%s</note>' % taxonomy_file_path 
	
	subs = {'output_path': output,
			'default_file': default_path,
			'mzml_path': mzml_path,
			'extra': extra,
            'threads': threads,
			}
	
	input_xml.write(input_xml_text % subs)
	input_xml.close()


def generate_qsub_script(directory, threads, resources, number_of_jobs):
	job_name = directory.split('/')
	job_name = job_name[-1] # take the last folder from the output directory to be the job name
	script = open(os.path.join(directory,'tandem_qsub.bash'),'w')
	script_text = """#!/bin/bash
#$ -S /bin/bash
#$ -V
#$ -t 1-%(number_of_jobs)s
#$ -pe threaded %(threads)d
#$ -q all.q
#$ -j y
#$ -l %(resources)s
#$ -N %(job_name)s
##$ -e logs
##$ -o logs
# Create a bash array of all input files 
SAMPLE_LIST="$(find %(directory)s -type f -name '*input.xml')"

module load tandem

# Run each input through tandem
for FILE in $SAMPLE_LIST
do
	tandem.exe $FILE
done
"""
	script.write(script_text % {'number_of_jobs':number_of_jobs,'job_name':job_name,'threads':threads,'directory':directory,'resources':resources})
	

def generate_files(options):
	if not os.path.exists(options.directory):
		os.makedirs(options.directory)
	if not os.path.exists(os.path.join(options.directory,'logs')):
		os.makedirs(os.path.join(options.directory,'logs'))
	fasta_path = os.path.abspath(options.fasta_file)
	#Create taxonomy.xml file to be referenced in each XML input file
	generate_taxonomy(options.directory,fasta_path)
	#Create input XML drivers for each mzml file	
	mzmls = options.mzml
	default_path = os.path.abspath(options.default_file)
	for mzml in mzmls:
		mzml_path = os.path.abspath(mzml)
		generate_input_file(options.directory,mzml_path,default_path,options.threads)
	#Create shell script to run tandem on all input files as an SGE array job
	generate_qsub_script(options.directory, options.threads, options.resources, len(mzmls))


# Define and retrieve command line options for generation of input.xml files
def main():
	parser = argparse.ArgumentParser(description='Runs xtandem from Genome Center cluster')
	parser.add_argument('--mzml', required=True, nargs='+', help='An mzML file path.  May use wildcards to use multiple files, such as *.mzML')
	parser.add_argument('--directory', required=True, help='The name of the directory to output all files to.  The directory will be made if it does not exist.')
	parser.add_argument('--default_file', required=True, help='The path to the default xml file.')
	parser.add_argument('--fasta_file', required=True, help='Fasta file')
	parser.add_argument('--threads', required=False, default=8, type=int, help='The number of threads to run for each X! Tandem job')
	parser.add_argument('--resources', required=False, default='piledriver', help='The requested resources for the job') 
#	parser.add_argument('--taxon', required=True, help='Specify the correct reference from the taxonomy.xml file')
#	parser.add_argument('--taxonomy_file', required=False, help='Optional: The path of the taxonomy xml file if different from the default configuration',default=None)
	options = parser.parse_args()
	generate_files(options)

    #sys.stdout.flush()
    


if __name__ == '__main__':
	main()
    
