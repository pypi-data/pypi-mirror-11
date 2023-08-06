Suppose your directory structure looks exactly same as the **Sample** folder
distributed with our source code.

Basic Pipeline
--------------
Change to the working directory::

    $ cd Sample/working

Simply run following command in a terminal prompt::

    $ runHiC pileup -p ../data -g hg19 --fastqDir SRA -F SRA --bowtiePath ../Tools/bowtie2/bowtie2 -m datasets.tsv --chunkSize 1500000 --libSize 500

*pileup* streamlines all analysis stages from mapping to ICE correcting.

If you want to perform a step-by-step analysis, you need to call *mapping*,
*filtering*, *binning*, *correcting* and *tosparse* separately, in order.

Mapping::

    $ runHiC mapping -p ../data -g hg19 --fastqDir SRA -F SRA --bowtiePath ../Tools/bowtie2/bowtie2 -m datasets.tsv --chunkSize 1500000

Filtering::

    $ runHiC filtering -p ../data -g hg19 --HDF5 hdf5-hg19 -m datasets.tsv --libSize 500 --duplicates --startNearRsite --level 2

Binning::

    $ runHiC binning -p ../data -g hg19 --filteredDir filtered-hg19 --mode wholeGenome --resolution 200000

Correcting::

    $ runHiC correcting -p ../data -g hg19 --HeatMap Raw-hg19
	
Convert to sparse format::

    $ runHiC tosparse -p ../data -g hg19 --cHeatMap Corrected-hg19

Parallel Tasks
--------------
a) Bowtie2 supports multiple threads for alignments. (You can specify the number
   of threads through ``-t/--threads`` when running *mapping* or *pileup*)
b) runHiC provides another layer for parallel computing. On this level of parallel,
   tasks are arranged based on separate SRA/FASTQ file, i.e., you can use this
   capacity only if you have two or more SRA/FASTQ files. Just submit the same command
   repeatedly and the program allocate a unique ID for each SRA/FASTQ to avoid conflicts
   between processes.

I give an example below to use these capacities as much as possible.

At first, run the similar but slightly changed command below::

    $ runHiC pileup -p ../data -g hg19 --fastqDir SRA -F SRA --bowtiePath ../Tools/bowtie2/bowtie2 -t 10 --logFile runHiC-pileup-1.log -m datasets.tsv --chunkSize 1500000 --libSize 500
	
This command uses 10 bowtie2 threads and redirect logging messages to another file
named "runHiC-pileup-1.log".

Several seconds later, run (If you are computing on a cluster, you may need to
switch to another node for efficiency)::

    $ runHiC pileup -p ../data -g hg19 --fastqDir SRA -F SRA --bowtiePath ../Tools/bowtie2/bowtie2 -t 10 --logFile runHiC-pileup-2.log -m datasets.tsv --chunkSize 1500000 --libSize 500
	
This time, logging messages are written to "runHiC-pileup-2.log".

That's not all, if you have three or more SRA files::

    $ runHiC pileup -p ../data -g hg19 --fastqDir SRA -F SRA --bowtiePath ../Tools/bowtie2/bowtie2 -t 10 --logFile runHiC-pileup-3.log -m datasets.tsv --chunkSize 1500000 --libSize 500
	
...

Experiment Quality Assessment
-----------------------------
Call *quality* after *filtering* or *pileup*::

    $ runHiC quality -p ../data -g hg19 -m datasets.tsv

Statistic table on sequencing reads for each SRA/FASTQ (level 1), biological
replicate (level 2) and cell type (level 3) will be generated under filtered-hg19.

Read-pair type ratios will be reported in line-plot manner for each biological
replicate (level 2) and cell type (level 3) under filtered-hg19 too. Intra-chromosomal
contacts are broken down into four types: "left" pair (both reads map to the reverse
strand), "right" pair (both reads map to the forward strand), "inner" pair (reads map
to different strands and point towards each other) and "outer" pair (reads map to
different strands and point away from one another). If the reads come from proximity
ligation, each pair type should account for roughly 25% of contacts. Thus, distance
at which the percentage of each type converges to 25% is a good indication of the minimum
distance at which it is meaningful to examine Hi-C contact patterns.

Visualization
-------------
You could plot the heatmap through *visualize*::

    $ runHiC visualize -p ../data -g hg19 -S Raw-hg19/Test-HindIII-allReps-filtered-200K.hm --RegionA 1 0 10000000 --RegionB X 0 10000000

That will plot a heatmap of contact matrix between "chr1: 0 ~ 10000000bp" and "chrX: 0 ~ 10000000bp"
under Raw-hg19.

To view the self-chromosomal contact information::

    $ runHiC visualize -p ../data -g hg19 -S Raw-hg19/Test-HindIII-allReps-filtered-200K.hm --RegionA 1 0 -1 --RegionB 1 0 -1
    
Note that the End Site of a region is allowed to be negative. "-1" indicates the end of a chromosome.

Similarly, to view the contact matrix between two whole chromosomes::

    $ runHiC visualize -p ../data -g hg19 -S Raw-hg19/Test-HindIII-allReps-filtered-200K.hm --RegionA 1 0 -1 --RegionB X 0 -1

Furthermore, you may want to plot the whole-genome heatmap::

    $ runHiC visualize -p ../data -g hg19 -S Raw-hg19/Test-HindIII-allReps-filtered-200K.hm

Data Access
-----------
You may have trouble with ".hdf5", ".hm" and ".npz" files generated by *runHiC*.
Suppose you have four files as follows::

    Test-HindIII-allReps-filtered.hdf5
    Test-HindIII-allReps-filtered-200K.hm
    Test-HindIII-allReps-filtered-10K_c-sparse.npz
    Test-HindIII-allReps-filtered-10K_c-csrsparse.npz

Now, open a Python Interpreter:

>>> from mirnylib import h5dict
>>> Reads = h5dict.h5dict('Test-HindIII-allReps-filtered.hdf5', 'r')
>>> Matrix = h5dict.h5dict('Test-HindIII-allReps-filtered-200K.hm', 'r')
>>> # You can manipulate Reads and Matrix using Python dictionary operations
>>> Matrix.keys()
[u'chromosomeStarts',
 u'genomeBinNum',
 u'genomeIdxToLabel',
 u'heatmap',
 u'resolution']
 >>> # Output the contact matrix into a TXT file
 >>> np.savetxt('Test-HindIII-allReps-filtered-200K.txt', Matrix['heatmap'], fmt = '%d', header = 'Resolution: %d' % lib['resolution'])
 
>>> import numpy as np
>>> Lib_1 = np.load('Test-HindIII-allReps-filtered-10K_c-sparse.npz')
>>> # Contact Matrices are saved chromosome by chromosome and can be extracted with chromosome labels
>>> chr1 = Lib_1['1'] # Chromosome 1
>>> chr1.dtype
dtype([('bin1', '<i8'), ('bin2', '<i8'), ('IF', '<f8')])
>>> # Write the sparse matrix into a TXT file
>>> np.savetxt('Test-HindIII-allReps-filtered-10K_c-sparse.chr1.txt', chr1, fmt = ['%d', '%d', '%.4f'], header = 'Resolution: %d' % lib['resolution'][()])

>>> Lib_2 = np.load('Test-HindIII-allReps-filtered-10K_c-csrsparse.npz')
>>> chr1 = Lib_2['1'][()]
>>> chr1
<1522x1522 sparse matrix of type '<type 'numpy.float64'>'
	with 680946 stored elements in Compressed Sparse Row format>
>>> # Output TXT
>>> x, y = chr1.nonzero()
>>> z = np.array(chr1[x,y]).ravel()
>>> cols = np.r_['1,2,0', x, y, z]
>>> np.savetxt('Test-HindIII-allReps-filtered-10K_c-csrsparse.chr1.txt', cols, fmt = ['%d', '%d', '%.4f'], header = 'Resolution: %d' % lib['resolution'][()])
