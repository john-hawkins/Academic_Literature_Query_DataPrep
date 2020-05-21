#!/anaconda3/bin/python
import sys
import pandas as pd
from pathlib import Path
import jellyfish

#################################################################################
def main():
    if len(sys.argv) < 5:
        print("*** ERROR: MISSING ARGUMENTS *** ")
        print_usage(sys.argv)
        exit(1)
    else:
        articles = (sys.argv[1])
        inclusion = (sys.argv[2])
        exclusion = (sys.argv[3])
        keywords_1 = (sys.argv[4])
        keywords_2 = (sys.argv[5])

        process_data(articles, inclusion, exclusion, keywords_1, keywords_2)

#################################################################################
def print_usage(args):
    print("USAGE ")
    print(args[0], "<ARTICLES CSV> <INCLUSION CRITERIA> <EXCLUSION CRITERIA> <KEYWORDS 1> <KEYWORDS 2>")
    print(" All files but the first are raw text files. The kewords files should be one per line.")
    print()


#################################################################################
def process_data(articles, inclusion, exclusion, keywords_1, keywords_2):
    df = pd.read_csv(articles)
    inc_criteria = Path(inclusion).read_text()
    exc_criteria = Path(exclusion).read_text()
    keys1 = Path(keywords_1).read_text()
    keys2 = Path(keywords_2).read_text()



#################################################################################
if __name__ == "__main__": main()

