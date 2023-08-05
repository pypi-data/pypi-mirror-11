.. _oa_fillgaps:

The :program:`fillgaps` command
===============================

command prototype
-----------------

.. program:: oa fillgaps

    usage: oa fillgaps [-h] [--minread BUILDGRAPH:MINREAD]
                       [--coverage BUILDGRAPH:COVERAGE]
                       [--minratio BUILDGRAPH:MINRATIO]
                       [--mincov BUILDGRAPH:MINCOV]
                       [--minoverlap BUILDGRAPH:MINOVERLAP]
                       [--smallbranches BUILDGRAPH:SMALLBRANCHES]
                       [--lowcomplexity] [--back ORGASM:BACK] [--snp]
                       [--adapt5 adapt5] [--adapt3 adapt3] [--seeds seeds]
                       index [output]

.. include:: ../options/positional.txt

optional arguments:
  -h, --help            show this help message and exit
  --minread BUILDGRAPH:MINREAD
                        the minimum count of read to consider [default:
                        <estimated>]
  --coverage BUILDGRAPH:COVERAGE
                        the expected sequencing coverage [default:
                        <estimated>]
  --minratio BUILDGRAPH:MINRATIO
                        minimum ratio between occurrences of an extension and
                        the occurrences of the most frequent extension to keep
                        it. [default: <estimated>]
  --mincov BUILDGRAPH:MINCOV
                        minimum occurrences of an extension to keep it.
                        [default: 1]
  --minoverlap BUILDGRAPH:MINOVERLAP
                        minimum length of the overlap between the sequence and
                        reads to participate in the extension. [default:
                        <estimated>]
  --smallbranches BUILDGRAPH:SMALLBRANCHES
                        maximum length of the branches to cut during the
                        cleaning process [default: <estimated>]
  --lowcomplexity       Use also low complexity probes
  --back ORGASM:BACK    the number of bases taken at the end of contigs to
                        jump with pared-ends [default: <estimated>]
  --snp                 desactivate the SNP clearing mode
  --adapt5 adapt5       adapter sequences used to filter reads beginning by
                        such sequences; either a fasta file containing adapter
                        sequences or internal set of adapter sequences among
                        ['adapt5ILLUMINA'] [default: adapt5ILLUMINA]
  --adapt3 adapt3       adapter sequences used to filter reads ending by such
                        sequences; either a fasta file containing adapter
                        sequences or internal set of adapter sequences among
                        ['adapt3ILLUMINA'] [default: adapt3ILLUMINA]
  --seeds seeds         protein seeds; either a file containing seeds proteic
                        sequences or internal set of seeds among
                        ['nucrRNAAHypogastrura', 'nucrRNAArabidopsis',
                        'protChloroArabidopsis', 'protMitoCapra',
                        'protMitoMachaon']
