# kate: syntax Python;
"""
Quality trimming.
"""

import sys

def quality_trim_index(str qualities, int cutoff, int base=33):
	"""
	Find the position at which to trim a low-quality end from a nucleotide sequence.

	Qualities are assumed to be ASCII-encoded as chr(qual + base).

	The algorithm is the same as the one used by BWA within the function
	'bwa_trim_read':
	- Subtract the cutoff value from all qualities.
	- Compute partial sums from all indices to the end of the sequence.
	- Trim sequence at the index at which the sum is minimal.
	"""
	cdef int s = 0
	cdef int max_qual = 0
	cdef int max_i = len(qualities)
	cdef int i
	cdef int q
	cdef bytes quals = qualities.encode()
	cdef char* cq = quals
	for i in reversed(range(len(quals))):
		q = cq[i] - base
		s += cutoff - q
		if s < 0:
			break
		if s > max_qual:
			max_qual = s
			max_i = i
	return max_i


def expected_errors(str qualities, int base=33):
	cdef int i, q
	cdef bytes quals = qualities.encode()
	cdef char* cq = quals
	cdef double e = 0.0
	for i in range(len(qualities)):
		q = cq[i] - base
		e += 10 ** (-q / 10)
	return e
