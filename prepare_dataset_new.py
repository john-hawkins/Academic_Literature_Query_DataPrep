import sys
import argparse
import jellyfish
import textdistance
import pandas as pd
from io import StringIO
from pathlib import Path
from nltk.corpus import stopwords

stop_word_list = stopwords.words('english')

####################################################################################
def main():
    desc = 'Process dataset for literature review query'
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('dataset',
                       metavar='dataset',
                       type=str,
                       help='Path to the dataset to process')
    parser.add_argument('titles',
                       metavar='titles',
                       type=str,
                       help='Name of column containing titles')
    parser.add_argument('abstracts',
                       metavar='abstracts',
                       type=str,
                       help='Name of column containing abstracts')
    parser.add_argument('authors',
                       metavar='authors',
                       type=str,
                       help='Name of column containing authors')
    parser.add_argument('years',
                       metavar='years',
                       type=str,
                       help='Name of column containing years')
    parser.add_argument('questions',
                       metavar='questions',
                       type=str,
                       help='Name of column containing research questions')
    parser.add_argument('results',
                       metavar='results',
                       type=str,
                       help='Path to the write the resulting dataset')

    args = parser.parse_args()
    data_path = args.dataset
    title_col = args.titles
    year_col = args.years
    abstract_col = args.abstracts
    question_col = args.questions
    author_col = args.authors
    results = args.results

    if not os.path.isfile(data_path):
        print(" ERROR")
        print(" The input file '%s' does not exist" % data_path)
        sys.exit()

    df = process_data(data_path, title_col, abstract_col, author_col, year_col, question_col)

    output = StringIO()
    df.to_csv(output, index=False, header=True)
    output.seek(0)
    print(output.read())



#################################################################################
def process_data(data_path, title_col, abstract_col, author_col, year_col, question_col):
    """
    Main control function
    Load the data and then add the feature sets.
    Gradually building up a larger feature enriched dataframe.
    """
    df = pd.read_csv(data_path, encoding="ISO-8859-1")
    df2 = add_text_summary_features(df, title_col, abstract_col)
    df3 = add_author_features(df2, author_col)
    df4 = add_criteria_match_features(df3, question_col, abstract_col)
    df5 = add_criteria_match_features(df4, question_col, title_col)
    return df5

#################################################################################
def add_question_match_features(df, q_col, t_col, sfx=""):
    """
    Return a copy of a dataframe with features describing matching
    between the query keywords and the articles in the dataframe
    """
    df_new = df.copy()
    def q_feats(x):
        crit = x[q_col].lower()
        raw_text = x[t_col].lower()
        jd = jellyfish.jaro_distance(raw_text,crit)
        ld = jellyfish.levenshtein_distance(raw_text,crit)
        ji = textdistance.jaccard(raw_text,crit)
        sd = textdistance.sorensen(raw_text, crit)
        ro = textdistance.ratcliff_obershelp(raw_text, crit)
        return jd, ld, ji, sd, ro
    df_new[[t_col+'_jd_'+sfx, t_col+'_ld_'+sfx, t_col+'_ji_'+sfx, t_col+'_sd_'+sfx, t_col+'_ro_'+sfx]] = df_new.apply(q_feats, axis=1, result_type="expand")
    return df_new

#################################################################################
def add_author_features(df, author_col, sepa=";"):
    """
    Return a copy of a dataframe with summary features added for
    the named columns for the author of the paper.
    """
    df_new = df.copy()
    def author_features(x, col):
        auth_array = x[col].lower().split(sepa)
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
if __name__ == "__main__": 
    main()


