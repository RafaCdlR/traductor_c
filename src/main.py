from CLexer import CLexer
import sys
from CParser import CParser
import os


def main(argv):
    cLexer = CLexer()
    cParser = CParser()
    cTokens = cLexer.tokens

    if len(argv) != 3:
        print(f"usage: {__file__} <input file> <output file>")
        exit(1)

    ifile = os.path.abspath(argv[1])
    ofile = os.path.abspath(argv[2])

    # for tok in cLexer.tokenize("int a"): print('type=%r, value=%r' % (tok.type, tok.value)) lexer = CLexer() parser = CParser()
    text = ''
    with open(ifile, 'r') as file:
        text = file.read()

    # print(f"File {ifile}: \n{text}")

    print("\n\n\n\n", text, " :")
    tokens = cLexer.tokenize(text)
    result = cParser.parse(tokens)
    print(result)


if __name__ == '__main__':
    main(sys.argv)
