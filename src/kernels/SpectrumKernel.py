import os
import sys
import warnings
from six import string_types
from itertools import permutations
import numpy as np

base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../..")
sys.path.append(base_dir)

from src.kernels.Kernel import Kernel
from utils.decorators import accepts


class SpectrumKernel(Kernel):
    """Implementation of Leslie et al., 2002
    with strings preindexation
    """
    NMAX = 6

    @accepts(int, string_types)
    def __init__(self, n, charset):
        """
        Args:
            n (int): n-uplet size to consider
            charset (str): charset for preindexation (typically "ATCG")
        """
        self._n = n
        if self._n > SpectrumKernel.NMAX:
            warnings.warn(f"Becomes computationally expensive when n > {SpectrumKernel.NMAX}")
        self._charset = charset
        permutation_seed = (2 + max(n - len(charset), 0)) * charset
        helper = lambda x: "".join(x)
        self._char_permutations = list(map(helper, set(permutations(permutation_seed, self._n))))

    @property
    def n(self):
        return self._n

    @property
    def charset(self):
        return self._charset

    @property
    def char_permutations(self):
        return self._char_permutations

    @accepts(string_types, int)
    def _get_tuple(self, seq, position):
        try:
            return seq[position:position + self.n]
        except IndexError:
            raise IndexError("Position out of range for tuple")

    @accepts(string_types, string_types)
    def __call__(self, seq1, seq2):
        """Short summary.

        Args:
            seq1 (type): Description of parameter `seq1`.
            seq2 (type): Description of parameter `seq2`.

        Returns:
            type: Description of returned object.

        """
        min_len = min(len(seq1), len(seq2))
        max_len = max(len(seq1), len(seq2))
        assert min_len >= self.n, "Sequence longer than tuple size"
        counts1 = {perm: 0 for perm in self.char_permutations}
        counts2 = {perm: 0 for perm in self.char_permutations}

        for i in range(max_len - self.n):
            try:
                subseq1 = self._get_tuple(seq1, i)
                counts1[subseq1] += 1
            except KeyError:
                pass
            try:
                subseq2 = self._get_tuple(seq2, i)
                counts2[subseq2] += 1
            except KeyError:
                continue

        feats1 = np.fromiter(counts1.values(), dtype=np.float32)
        feats2 = np.fromiter(counts2.values(), dtype=np.float32)
        return np.inner(feats1, feats2)
