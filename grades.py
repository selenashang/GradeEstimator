# grades.py
#
# Grade estimator based on CS 161 Spring 2014
# Tested Versions: Python 2.7 and Python 3.5
"""
Usage: > python grades.py NUMBER TOTAL
Sample: > python grades.py -v 300 536
        Grade Percentile Cutoffs:
        A+: 0.0170
        A: 0.2244
        A-: 0.2472
        B+: 0.4375
        B: 0.6733
        B-: 0.7812
        C+: 0.8977
        C: 0.9631
        C-: 0.9688
        D: 0.9858
        F: 1.0000
        Estimated grade for percentile 0.559701492537: B
"""
from collections import OrderedDict as OD
from collections import namedtuple
from bisect import bisect_left
import argparse

Result = namedtuple("Result", ["verbose", "percentile"])

class ZDict(OD):
    def __init__(self, *args, **kwargs):
        super(ZDict, self).__init__(*args, **kwargs)

    def __getitem__(self, key):
        try:
            res = super(ZDict, self).__getitem__(key)
        except KeyError:
            cutoffs = list(self.keys())
            assert cutoffs == sorted(cutoffs), "Must be sorted keys"
            idx = bisect_left(cutoffs, key)
            # print(cutoffs[idx])
            return self[cutoffs[idx]]
        except Exception as e:
            raise(e)
        else:
            return res

    def get(self, key, default = None):
        return self.__getitem__(key)

def main():
    """Grade distribution data pulled from Wagner's Spring 2014 grades via CalAnswers."""
    result = parse_cmd_options()
    verbose, user_percentile  = result.verbose, result.percentile
    letters = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D', 'F']
    values = [6, 73, 8, 67, 83, 38, 41, 23, 2, 6, 5]
    total = sum(values)
    cutoffs = ZDict([ (float(sum(values[0:i+1])) / total, letters[i])
                for i in range(len(letters)) ])
    if verbose:
        pairs = cutoffs.items()
        msg = "\n".join(["%s: %0.4f" % (v,k) for (k,v) in pairs])
        print("Grade Percentile Cutoffs:\n%s" % msg)

    grade = cutoffs[user_percentile]
    print("Estimated grade for percentile %s: %s" % (user_percentile, grade))

def parse_cmd_options():
    parser = argparse.ArgumentParser(
        description="A simple grade estimator",
        usage = "%(prog)s [-h | -v] index total",
        formatter_class= argparse.RawDescriptionHelpFormatter,
        epilog= '')
    parser.add_argument("-v", "--verbosity", action="store_true",
                        required = False, default = False,
                        help='adds verbosity')
    parser.add_argument("index", type=int,
                        help='Relative score index in the class')
    parser.add_argument("total", type=int,
                        help='Number of total students in your class')
    args = parser.parse_args()

    index = args.index
    total = args.total

    verbose = args.verbosity

    if not total:
        # catch ZeroDivision error this way as well
        raise(ValueError("Bad input for total found: %s" % (total)))

    percentile = float(index) / total
    if percentile > 1:
        raise(ValueError("Your relative index must be less than the total"))

    return Result(verbose, percentile)

if __name__ == '__main__':
    main()
