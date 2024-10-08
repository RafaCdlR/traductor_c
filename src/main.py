from CLexer import CLexer
import sys

if __name__ == '__main__':
    main(sys.argv)

def main(argv):
    cLexer = CLexer()
    cTokens = cLexer.tokens

    if len(argv) < 2:
        print("usage: traductor <input file> <output file>")
        exit 1       

    ifile = argv[1]
    ofile = argv[2]

    for tok in cLexer.tokenize("int a"):
        print('type=%r, value=%r' % (tok.type, tok.value))
