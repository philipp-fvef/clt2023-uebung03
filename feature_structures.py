import nltk


fsgram = nltk.grammar.FeatureGrammar.fromstring("""
    S -> NP[NUM=?a, GND=?b, CASE=nom, CAP=True] VP[NUM=?a, GND=?b, CAP=False]
    NP[NUM=?a, GND=?b, CASE=?c, CAP=?d] -> Det[NUM=?a, GND=?b, CASE=?c, CAP=?d] N[NUM=?a, GND=?b, CASE=?c]
    VP[NUM=?a, GND=?b, CASE=?c, CAP=False] -> V[NUM=?a, GND=?b, CAP=False, TYPE=intrans]
    VP[NUM=?a, GND=?b, CASE=?c, CAP=False] -> V[NUM=?a, GND=?b, CAP=False, TYPE=trans] NP[NUM=?n, GND=?m, CASE=akk, CAP=False]
    Det[NUM=sg, GND=fem, CASE=nom, CAP=False] -> 'die'
    Det[NUM=sg, GND=fem, CASE=dat, CAP=False] -> 'der'
    Det[NUM=sg, GND=fem, CASE=akk, CAP=False] -> 'die'
    Det[NUM=sg, GND=masc, CASE=nom, CAP=False] -> 'der'
    Det[NUM=sg, GND=masc, CASE=dat, CAP=False] -> 'dem'
    Det[NUM=sg, GND=masc, CASE=akk, CAP=False] -> 'den'
    Det[NUM=pl, GND=?n, CASE=?m, CAP=False] -> 'die'
    Det[NUM=pl, GND=?n, CASE=dat, CAP=False] -> 'den'
    Det[NUM=sg, GND=fem, CASE=nom, CAP=True] -> 'Die'
    Det[NUM=sg, GND=fem, CASE=dat, CAP=True] -> 'Der'
    Det[NUM=sg, GND=fem, CASE=akk, CAP=True] -> 'Die'
    Det[NUM=sg, GND=masc, CASE=nom, CAP=True] -> 'Der'
    Det[NUM=sg, GND=masc, CASE=dat, CAP=True] -> 'Dem'
    Det[NUM=sg, GND=masc, CASE=akk, CAP=True] -> 'Den'
    Det[NUM=pl, GND=?n, CASE=?m, CAP=True] -> 'Die'
    Det[NUM=pl, GND=?n, CASE=dat, CAP=True] -> 'Den'
    N[NUM=sg, GND=fem] -> 'Frau'
    N[NUM=pl, GND=fem] -> 'Frauen'
    N[NUM=sg, GND=masc] -> 'Mann'
    N[NUM=pl, GND=masc] -> 'Maenner'
    V[NUM=sg, GND=?n, CAP=False, TYPE=intrans] -> 'lacht'
    V[NUM=pl, GND=?n, CAP=False, TYPE=intrans] -> 'lachen'
    V[NUM=sg, GND=?n, CAP=False, TYPE=trans] -> 'liebt'
    V[NUM=pl, GND=?n, CAP=False, TYPE=trans] -> 'lieben'
    """)


if __name__ == "__main__":
    parser = nltk.FeatureChartParser(fsgram, trace=1)
    print(parser.parse("Die Mann lieben dem Frauen".split()))
    print(parser.parse("Der Mann liebt die Frauen".split()))

