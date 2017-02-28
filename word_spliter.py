from math import log


class WordSpliter:
    # Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
    words = None
    wordcost = None
    maxword = None

    @staticmethod
    def infer_spaces(s):
        if not WordSpliter.words:
            WordSpliter.words = open("words-by-frequency.txt").read().split()
            WordSpliter.wordcost = dict((k, log((i+1)*log(len(WordSpliter.words)))) for i,k in enumerate(WordSpliter.words))
            WordSpliter.maxword = max(len(x) for x in WordSpliter.words)
        """Uses dynamic programming to infer the location of spaces in a string
        without spaces."""

        # Find the best match for the i first characters, assuming cost has
        # been built for the i-1 first characters.
        # Returns a pair (match_cost, match_length).
        def best_match(i):
            candidates = enumerate(reversed(cost[max(0, i - WordSpliter.maxword):i]))
            return min((c + WordSpliter.wordcost.get(s[i-k-1:i], 9e999), k+1) for k,c in candidates)

        # Build the cost array.
        cost = [0]
        for i in range(1,len(s)+1):
            c,k = best_match(i)
            cost.append(c)

        # Backtrack to recover the minimal-cost string.
        out = []
        i = len(s)
        while i>0:
            c,k = best_match(i)
            assert c == cost[i]
            out.append(s[i-k:i])
            i -= k

        return " ".join(reversed(out))

if __name__ == '__main__':
    s = 'rateandreview'
    print(WordSpliter.infer_spaces(s))
    s = 'SubmittedDepositsActivity'
    print(WordSpliter.infer_spaces(s))
    print(len(s) == len(WordSpliter.infer_spaces(s).split(' ')))
    s = 'com'
    print(len(s))
    print(WordSpliter.infer_spaces(s))
