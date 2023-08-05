Assembling a mitochondrion genome from IPython
==============================================

.. _mitoindex:

Step 1 : indexing the reads
---------------------------

To assemble a genome from sequence reads, you need first to index them. This step allows an efficient access
to the reads during the assembling process. The organelle assembler is optimized for running with paired end 
Illumina reads. It can also works, but less efficiently, with single reads, and 454 or Ion Torrent reads. 

Considering two fastq files ``forward.fastq`` and ``reverse.fastq`` containing respectively the forward and the
reverse reads of the paired reads, to build the index named ``readindex`` from a UNIX terminal you have to run the
:ref:`orgasmi <orgasmi>` command :
 
.. code-block:: bash

	$ oa index readindex forward.fastq reverse.fastq
    
the ``oa`` command is able to manage with compressed read files :

	- by ``gzip`` if the file name ends by ``'.gz'``
	
	- by ``bzip2``if the file name ends by ``'.bz2'``
	
.. code-block:: bash

     $ oa index readindex forward.fastq.gz reverse.fastq.bz2
     

    
    
This will index the 30 first millions of reads stored in the ``forward.fastq.gz`` and ``reverse.fastq.gz`` files over their first 100bp.
    
    
Step 2 : Running the organelle assembler from IPython
-----------------------------------------------------

Launching Ipython
.................

The ipython environment has to be launched from a UNIX terminal using the :command:`ipython`

.. code-block:: bash

    $ ipython
    Python 2.7 (r27:82500, Jul  6 2010, 10:43:34) 
    Type "copyright", "credits" or "license" for more information.
    
    IPython 0.13.1 -- An enhanced Interactive Python.
    ?         -> Introduction and overview of IPython's features.
    %quickref -> Quick reference.
    help      -> Python's own help system.
    object?   -> Details about 'object', use 'object??' for extra details.
    
    In [1]: 

Loading the main functions and classes need from the assembling
...............................................................

We first need to import a set of classes and functions that we will use during the assembling process.

.. code-block:: ipython

    In [1]: from orgasm.indexer._orgasm import Index
    
    In [2]: from orgasm.multialign import *
    
    In [3]: from orgasm.tango import *
    
    In [4]: from orgasm.assembler import Assembler
    
    In [5]: from orgasm.backtranslate.fasta import fasta
    
 
Loading the indexed reads
.........................
 
We assume that following the method described :ref:`previously <mitoindex>` we have 
indexed our read in an indexed library called ``readindex <readindex>``. This library
has now to be loaded into the computer memory.
 
.. code-block:: ipython
 
    In [6]: r = Index('readindex')
    
    Loading global data...
    
    Done.
    
    Reading indexed sequence reads...
    
     30000000 sequences read
    
    Reading indexed pair data...
    
    Done.
    
    Loading reverse index...
    
    Done.
    
    Indexing reverse complement sequences ...
    
    
    Fast indexing forward reads...
    
    
    Fast indexing reverse reads...
    
    Done.

Looking for the reads to initiate the assembling process
........................................................

To target the assembling on the mitochondrion genome we need to select a set
of reads belonging it. This is done by looking for reads encoding for a well
conserved mitochondrion gene. 

We first load the protein sequence of the :abbr:`COXI (cytochrom oxidase I)` gene.
from a file ``COX1.fasta`` file.
    
.. code-block:: ipython
 
    In [7]: p = fasta('COX1.fasta')  
    
The set of reads matching the loaded protein sequences is selected using the 
:py:meth:`Index.lookForSeeds`

.. code-block:: ipython
 
    In [8]:  m = r.lookForSeeds(p)
    99.8 % |#################################################/ ] remain : 00:00:00

Running the assembler
.....................

We have to create an instance of the :py:class:`Assembler` class

.. code-block:: ipython
 
    In [9]: asm = Assembler(r)

    
Then the selected set of reads has to be converted into a set of seeds usable by the assembler.
This is assumed by the :py:func:`orgasm.tango.matchtoseed` function.
    
.. code-block:: ipython
 
    In [10]: s = matchtoseed(m,r)
    
The assembling process can then be initiated using the :py:func:`~organsm.tango.tango` function.
    
.. code-block:: ipython
 
    In [11]: a = tango(asm,s,mincov=1,minread=3,minoverlap=30)
    Cycle :      220  (438 nodes / 46.5% fake) Waiting points :        8 /   6.97  Gene: None 
    
    JumpGap on read 14233691
    
    Cycle :     1230  (2454 nodes / 61.0% fake) Waiting points :       11 /   8.31  Gene: None 
    
    JumpGap on read 25800833
    
    Cycle :    10798  (21586 nodes / 51.2% fake) Waiting points :        7 /  25.46  Gene: None 
    
    JumpGap on read 22888545
    
    Cycle :    16390  (32766 nodes / 52.5% fake) Waiting points :        5 /  23.90  Gene: None 
    
    JumpGap on read 22812874
    
Cleaning the assembling
.......................
 
The assembling process create an assembling graph representing the relationship between the reads.
The sequence of the assembled sequence can be determined by followng a path of this graph. 
Further the main path corresponding to the true sequence, many short path exist. They correspond
to aborted extension created notably by all the sequencing errors.
 
The :py:meth:`~orgasm.assembler.Assembler.cleanDeadBranches` method of the :py:class:`~orgasm.assembler.Assembler`
class remove from the assembling graph all short path corresponding to those spurious extensions.
 
.. code-block:: ipython
 
    In [12]: asm.cleanDeadBranches()
    
    Remaining edges : 32498 node : 32500
    Out[12]: 134

Compacting the assembling graph
...............................

We can now post-process the assembling graph to produce a compact
graph where each edge corresponds to an unambiguous path in the 
original assembling graph.

.. code-block:: ipython
 
    In [13]: cg = asm.compactAssembling()
    Compacting graph :
     Stem           1 :  16249 bp (total :  16249) coverage :  71.43
     Stem          -1 :  16249 bp (total :  32498) coverage :  71.43
    
    Minimum stem coverage = 71

The resulting compact graph can be stored in a file to be analyzed using a standard
graph editor like :program:`yed`.
    
.. code-block:: ipython
 
    In [17]: print >>open('UGBT-B8-0101.clean.gml','w'),cg.gml()
    
.. figure:: mito-clean-1.png
   :scale: 50 %
   :alt: Assembling graph layout.
   
   The assembling graph display two edges corresponding to two sequences of 16249bp.
   They correspond to the same sequence in the complemented/reversed orientation.
   This can be easily recognized with the ``stemid`` which start the edge labels :
   ``-1`` and ``1``. Two opposite ``stemid`` indicate two reverse-complemented
   sequences.
   
The assembled sequence is linear because of a polyG sequence blocking the assembling
algorithm.

.. code-block:: ipython
 
    In [18]: ex = getPairedRead(asm,cg,1,300)
    
    In [19]: exr = getPairedRead(asm,cg,-1,300)
    
    In [20]: exr = set(-i for i in exr)
    
    In [21]: ali = multiAlignReads(ex|exr,r)
    
    In [22]: len(ali)
    Out[22]: 1
    

.. code-block:: ipython
 
    In [23]: s = insertFragment(asm,c)
    
    In [24]: asm.cleanDeadBranches()
    
    Remaining edges : 32676 node : 32676
    Out[25]: 0
    
    In [26]: cg = asm.compactAssembling()
    Compacting graph :
     Circle         1 :  16337 bp (total :  16337) coverage :  71.05
     Circle        -1 :  16337 bp (total :  32674) coverage :  71.05
    
    Minimum stem coverage = 71


.. code-block:: ipython
 
    In [27]: print assembling2fasta(cg)
    >stem@1 : GATTA->(16337)->TTCGA  [71]
    GATTAGGTCTTTGGAGTAGAATCCTGTGAGGAAGGGTATTCCTGTTAGTGCGAGACTGCC
    AACAATGAGGGCTGTTGTGGTGAATGGCATGGTTTTAAATAGGCCTCCTATTTTTCGAAT
    ATCTTGTTCGTCGTTTAGGCTGTGAATAATGGAACCGGAGCATATGAATAGTATAGCTTT
    GAAAAAGGCGTGGGTACAGATGTGGAGGAAAGCTAGGTAAGGTTGGTTAATGCCAATAGT
    TACTATTATAAGGCCCAGTTGACTGGATGTGGAGAAGGCGATGATTTTTTTAATGTCATT
    TTGGGTGAGGGCGCATATTGCTGTAAATAGTGTGGTAATGGCTCCTAAGCATAATGTAAT
    AGATTGGATGTATTTATTGTTTTCTGTGAGGGGATAGAAACGGATTAGTAGGAAGATACC
    TGCTACCACTATTGTGCTTGAATGGAGTAGTGCTGAGACGGGAGTTGGGCCTTCTATTGC
    AGAGGGAAGTCACGGGTGGAGGCCAAATTGGGCGGATTTTCCGGTTGCAGCTAATGCTAG
    TCCAATCAAGGGTATGTTTGAGTCGCTTGGGTTTAGTATGAAGATCTGTTGGAGGTCTCA
    ...
    
.. code-block:: ipython
 
    In [28]: print >>open('UGBT-B8-0101.fasta','w'),assembling2fasta(cg)

