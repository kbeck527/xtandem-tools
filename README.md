xtandem-tools
=============

Scripts for making the use of X! Tandem easier.

Written by Adam Schaal, UC Davis Bioinformatics Core  
Revised by Kristen Beck, UC Davis Genome Center 

usage: generate_tandem_inputs.py [-h] 
	--mzml MZML [MZML ...]
	--directory		DIRECTORY 
	--default_file		DEFAULT_FILE
        --fasta_file 		FASTA_FILE 
	[--threads 		THREADS]
        [--resources 		RESOURCES] 
	[--email 		EMAIL]

Generates input.xml, taxonomy.xml (fasta database info), and qsub bash script 
to run xtandem from Genome Center cluster

optional arguments:
  -h, --help            
			show this help message and exit
  --mzml MZML [MZML ...]
                        An mzML file path. May use wildcards to use multiple
                        files, such as *.mzML
  --directory DIRECTORY
                        The of the directory to output all files to. The
                        directory will be made if it does not exist.
  --default_file DEFAULT_FILE
                        The path to the default xml file.
  --fasta_file FASTA_FILE
                        Fasta file
  --threads THREADS    
			 The number of threads to run for each X! Tandem job
  --resources RESOURCES 
			The requested resources for the job
  --email EMAIL         
			Email address for notification whe job begins, ends,
                        or aborts

**Note:**
Python version 2.7 or greater is required. It can be loaded with the following command:
	module load python/2.7.8


**Example usage for milk proteomics project:**

python generate_tandem_inputs.py --mzml /share/milklab/proteomics/Spectra/Human/*.mzML --directory /share/milklab/proteomics/output_XTandem/best_run_ever --default_file /share/milklab/proteomics/Tools/XTandem/tandem-linux-15-04-01-1/bin/default_input.xml --fasta_file /share/milklab/proteomics/FASTA/Uniprot_Human-decoy+cRAP.fasta --threads 2 --resources h_vmem=2g --email kristenbeck527@gmail.com
