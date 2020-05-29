#!/anaconda3/bin/python
import sys
import jellyfish
import textdistance
import pandas as pd
from io import StringIO
from pathlib import Path
from nltk.corpus import stopwords

stop_word_list = stopwords.words('english')

#################################################################################
def main():
    if len(sys.argv) < 9:
        print("*** ERROR: MISSING ARGUMENTS *** ")
        print_usage(sys.argv)
        exit(1)
    else:
        articles = (sys.argv[1])
        title_col = (sys.argv[2])
        abstract_col = (sys.argv[3])
        author_col = (sys.argv[4])
        keywords_col = (sys.argv[5])
        inclusion = (sys.argv[6])
        exclusion = (sys.argv[7])
        keywords_1 = (sys.argv[8])
        keywords_2 = (sys.argv[9])

        df = process_data(articles, title_col, abstract_col, author_col, 
                     keywords_col, inclusion, exclusion, keywords_1, keywords_2)

        output = StringIO()
        df.to_csv(output, index=False, header=True)
        output.seek(0)
        print(output.read())


#################################################################################
def print_usage(args):
    print("USAGE ")
    print(args[0], "<ARTICLES CSV> <TITLE COL> <ABSTRACT COL> <AUTHOR COL> <KEYWORDS_COL> <INCLUSION CRITERIA> <EXCLUSION CRITERIA> <KEYWORDS 1> <KEYWORDS 2>")
    print(" All files but the first are raw text files. The kewords files should be one per line.")
    print()


#################################################################################
def process_data(articles, title_col, abstract_col, author_col, keywords_col, inclusion, exclusion, keywords_1, keywords_2):
    """
    Main control function
    Load the required files and then add the feature sets.
    Gradually building up a larger feature enriched dataframe.
    """
    df = pd.read_csv(articles, encoding="ISO-8859-1")
    inc = Path(inclusion).read_text()
    exc = Path(exclusion).read_text()
    keys1 = Path(keywords_1).read_text()
    keys2 = Path(keywords_2).read_text()
    k1list = [x for x in keys1.split("\n") if x]
    k2list = [x for x in keys2.split("\n") if x]
    df2 = add_text_summary_features(df, title_col, abstract_col)
    df3 = add_author_features(df2, author_col)
    df4 = add_query_features(df3, inc, exc, k1list, k2list)
    df5 = add_keywords_features(df4, title_col, abstract_col, keywords_col, k1list, k2list)
    return df5


#################################################################################
def add_keywords_features(df, title_col, abstract_col, keywords_col, k1list, k2list):
    """
    Return a copy of a dataframe with features describing matching 
    between the query keywords and the articles in the dataframe
    """
    df_new = df.copy()
    def keyword_features(x, col):
        raw_text = x[col].lower()
        k1matches = sum( x in raw_text for x in k1list)
        k2matches = sum( x in raw_text for x in k2list)
        return k1matches, k2matches
    df_new[['title_k1', 'title_k2']] = df_new.apply(keyword_features, col=title_col, axis=1, result_type="expand")
    df_new[['abstract_k1', 'abstract_k2']] = df_new.apply(keyword_features, col=abstract_col, axis=1, result_type="expand")
    df_new[['keywords_k1', 'keywords_k2']] = df_new.apply(keyword_features, col=keywords_col, axis=1, result_type="expand")
    return df_new

#################################################################################
def add_query_features(df, inc, exc, k1list, k2list):
    """
    Return a copy of a dataframe with summary features added for
    the named text files defining the query
    """
    df_new = df.copy()
    k1lens = list(map(len, k1list))
    k2lens = list(map(len, k2list))
    k1max = max(k1lens)
    k2max = max(k2lens)
    k1count = len(k1list)
    k2count = len(k2list)
    df_new['k1_count'] = k1count
    df_new['k2_count'] = k2count
    df_new['k1_max'] = k1max
    df_new['k2_max'] = k2max
    jaro_dist = jellyfish.jaro_distance(inc,exc)
    lev_dist = jellyfish.levenshtein_distance(inc,exc)
    ji = textdistance.jaccard(inc,exc)
    sd = textdistance.sorensen(inc, exc)
    ro = textdistance.ratcliff_obershelp(inc, exc)
    #jellyfish.damerau_levenshtein_distance(inc,exc)
    #jellyfish.jaro_winkler(inc,exc)
    df_new['inc_jaro_exc'] = jaro_dist
    df_new['inc_lev_exc'] = lev_dist
    df_new['inc_ji_exc'] = ji
    df_new['inc_sd_exc'] = sd
    df_new['inc_ro_exc'] = ro
    return df_new

#################################################################################
def add_author_features(df, author_col):
    """
    Return a copy of a dataframe with summary features added for
    the named columns for the author of the paper.
    """
    df_new = df.copy()
    def author_features(x, col):
        auth_array = x[col].lower().split('-//-')
        return len(auth_array)
    df_new['author_count'] = df_new.apply(author_features, col=author_col, axis=1)
    return df_new
 

#################################################################################
def add_text_summary_features(df, title_col, abstract_col):
    """
    Return a copy of a dataframe with summary features added for
    the named columns for the title and abstract of the paper.
    """
    df_new = df.copy()
    df_new['title_length'] = df_new[title_col].apply(len)
    df_new['abstract_length'] = df_new[abstract_col].apply(len)
    def text_features(x, col):
        word_array = x[col].lower().split()
        non_stop_words = list(set(word_array) - set(stop_word_list))
        word_count = len(word_array)
        word_lengths = list(map(len, word_array))
        max_word_len = max(word_lengths)
        avg_word_len = sum(word_lengths)/word_count
        content_wd = len(non_stop_words)/len(word_array)
        return word_count, max_word_len, avg_word_len, content_wd
    df_new[['title_wc', 'title_max_wl', 'title_avg_wl', 'title_cwd']] = df_new.apply(text_features, col=title_col, axis=1, result_type="expand")    
    df_new[['abstract_wc', 'abstract_max_wl', 'abstract_avg_wl', 'abstract_cwd']] = df_new.apply(text_features, col=abstract_col, axis=1, result_type="expand")
    return df_new



#################################################################################
if __name__ == "__main__": main()

