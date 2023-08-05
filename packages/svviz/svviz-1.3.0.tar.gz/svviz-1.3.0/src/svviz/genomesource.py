import pyfaidx

from svviz.utilities import reverseComp

class GenomeSource(object):
    def __init__(self, seq, name=None):
        self.seq = seq
        self.name = name

    def getSeq(self, chrom, start, end, strand):
        seq = self.seq[start:end+1]
        if strand == "-":
            seq = reverseComp(seq)
        return seq


class FastaGenomeSource(GenomeSource):
    """ pickle-able wrapper for pyfaidx.Fasta """
    def __init__(self, path, name=None):
        self.name = name
        self.path = path
        self._fasta = None

    def getSeq(self, chrom, start, end, strand):
        seq = self.fasta[chrom][start:end+1]
        if strand == "-":
            seq = reverseComp(seq)
        return seq

    @property
    def fasta(self):
        if self._fasta is None:
            self._fasta = pyfaidx.Fasta(self.path, as_raw=True)
        return self._fasta

    def __getstate__(self):
        state = self.__dict__.copy()
        state["_fasta"] = None
        return state