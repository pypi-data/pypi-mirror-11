__version__ = '0.4.6'

from .args import HelpfulArgumentParser
from .io.fasta import (
	SequenceReader, FastaReader, FastqReader, FastaWriter, FastqWriter,
	IndexedFasta, guess_quality_base )
from .io.gtf import GtfReader
from .cigar import Cigar
#from .align import multialign, consensus
