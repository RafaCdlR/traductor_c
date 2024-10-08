from CLexer import CLexer
import sys

if __name__ == '__main__':
    cLexer = CLexer()
    cTokens = cLexer.tokens

    for tok in cLexer.tokenize("int a"):
        print('type=%r, value=%r' % (tok.type, tok.value))
