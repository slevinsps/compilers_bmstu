from parser import GrammaticParser
from precedence import Precedence
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", help="path to grammatic txt file", required=True)
    args = parser.parse_args()
    path = args.path


    grammaticParser = GrammaticParser()
    precedenceHandler = Precedence()
    grammatic = grammaticParser.parse(path)
    precedenceHandler.buildOperatorPrecedenceMatrix(grammatic)
    precedenceHandler.printMatrix()
if __name__ == '__main__':
    main()