from __future__ import print_function


__author__ = 'Loris Mularoni'


# Import modules
import gzip
import math
import re
import os
import sys
from itertools import combinations_with_replacement as cwr
from itertools import cycle


# Global variables
DNA = "ACGT"
AA = "ACDEFGHIKLMNPQRSTUVWY"
PYTHON_3 = sys.version > '3'


# Progress Bar
class ProgressBar:
    def __init__(self, total):
        self.total = total
        self.count = 0
        self.done = 0
        self.length_progress = 50

    def draw_progress(self, percentage):
        left = self.length_progress - self.done
        print("\r |{}{}| {}%".format('=' * self.done,
                                     '-' * left,
                                     percentage),
              flush=True, end='')

    def update(self, count=1):
        self.count += count
        done = math.ceil(self.count * self.length_progress / self.total)
        if done > self.done:
            self.done = done
            percentage = math.ceil(self.count * 100 / self.total)
            self.draw_progress(percentage)

    def close(self):
        print("\r {}\n".format(" " * (self.length_progress + 7)))


class Microsatellite:
    def __init__(self, length, min_repetitions, imperfect, alphabet='dna'):
        """Initialize the Microsatellite class.
        :param length:
        :param min_repetitions:
        :param imperfect:
        :param alphabet:
        :return:
        """
        self.length = length
        self.min_repetitions = min_repetitions
        self.imperfect = imperfect
        self.blocks = list(DNA) if alphabet == 'dna' else list(AA)
        self.pattern = self.build_regex()
        self.sequence = ''
        self.header = ''

    def load_sequence(self, items):
        """Load a sequence.
        :param items:
        :return:
        """
        self.header, self.sequence = items

    def build_regex(self):
        """Build the regular expression
        :return:
        """
        pattern = "|".join("(?:" + "".join(i) + "){" +
                           str(self.min_repetitions if (self.length == 1 and self.imperfect <= 0)
                               else self.min_repetitions - 1) + ",}"
                           for i in cwr(self.blocks, self.length)
                           if (len(set(i)) > 1) or self.length == 1)
        return pattern

    def extend_upstream(self, start, micro, seed):
        """Extend the microsatellite upstream.
        :param start:
        :param micro:
        :param seed:
        :return:
        """
        seed = cycle(seed[::-1])
        while (start > 0) and (next(seed) == self.sequence[start - 1]):
            start -= 1
            micro = self.sequence[start] + micro
        return start, micro

    def extend_downstream(self, end, micro, seed):
        """Extend the microsatellite downstream
        :param end:
        :param micro:
        :param seed:
        :return:
        """
        seed = cycle(seed)
        while (end < len(self.sequence)) and (next(seed) == self.sequence[end]):
            micro += self.sequence[end]
            end += 1
        return end, micro

    def find_microsatellites(self, items=None):
        """Return the positions of the microsatellites.
        :param items:
        :return:
        """
        if items is not None:
            self.load_sequence(items)

        # Find the seeds of microsatellites
        matches = [[i.start(), i.end(), i.group(), i.group()[:self.length]]
                   for i in re.finditer(self.pattern, self.sequence)]

        # Do not extend the seeds
        if self.length == 1:
            results = [[self.header, start, end, seed, micro] for
                       (start, end, micro, seed) in matches]
        # Extend the seeds
        else:
            results = []
            for (start, end, micro, seed) in matches:
                end, micro = self.extend_downstream(end, micro, seed)
                start, micro = self.extend_upstream(start, micro, seed)
                results.append([self.header, start, end, seed, micro])

        # Search for imperfect repeats
        if (self.imperfect > 0) or (self.imperfect == 0 and self.length > 1):
            results = self.include_imperfect_repeats(results)

        # Get rid of microsatellites that are too short
        if self.length > 1 or self.imperfect > 0:
            results = list(filter(lambda x: (x[2] - x[1]) / self.length >= self.min_repetitions,
                                  results))

        return results

    def include_imperfect_repeats(self, results):
        """Include imperfect repeats.
        :param results:
        :return:
        """
        if len(results) == 0:
            return results

        results = sorted(results, key=lambda x: x[1])
        _results = [results[0]]
        for i in range(1, len(results)):
            if (_results[-1][3] == results[i][3]) and \
                    (results[i][1] - _results[-1][2] <= self.imperfect):
                # Extend the previous one
                if results[i][2] > _results[-1][2]:
                    # Extend the end
                    _results[-1][2] = results[i][2]
                    # Extend the sequence
                    if self.imperfect == 0:
                        _results[-1][4] += results[i][4]
                    else:
                        _results[-1][4] = self.sequence[_results[-1][1]: _results[-1][2]]
            else:
                # Append a new one
                _results.append(results[i])
        return _results


# Functions
def read_fasta(input_file):
    """Read a fasta file. Return the sequences as an iterator.
    :param input_file:
    :return:
    """
    header = ''
    sequence = ''
    open_function = gzip.open if os.path.splitext(input_file)[1] == '.gz' else open
    mode = 'rb' if os.path.splitext(input_file)[1] == '.gz' else 'r'
    with open_function(input_file, mode) as fasta_file:
        for line in fasta_file:
            line = line if mode == 'r' else line.decode()
            if line.startswith(">"):
                if header != '' and sequence != '':
                    yield (header, sequence)
                header = line.strip()[1:]
                sequence = ''
            else:
                sequence += line.strip().upper()
        yield (header, sequence)


def get_number_of_chromosomes(genome):
    """Return the number of chromosomes in the genome.
    :param genome:
    :return:
    """
    total = 0
    for _ in read_fasta(genome):
        total += 1
    return total

