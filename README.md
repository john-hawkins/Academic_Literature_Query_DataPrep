Academic Literature Query DataPrep
===================================
 
This project contains a scripts for preparing datasets for the specific task
of building machine learning models to learn the features of academic abstracts that indicate
that they are of key interest for a specific academic enquiry.

```
Status: Not Functional

Current Work: Core Library Function
```
### Overview

The scripts will take a dataset contain information about a set of academic papers that have
been returned from an initial database search. This includes: title, abstract, authors.

They will then make use of information that describes the criteria of the academic search. This
includes separate files describing inclusion and exclusion criteria, and two sets of keywords
that could describe separate core topics (for multi-displinary papers).

All of this infomration is then used to generate features to help a machine learning algorithm
distinguish which of the papers are appropriate for the query. 


### Features Generated

These are the planned list of features.


#### Article Specific

- Abstract - Length *
- Abstract - Wordcount *
- Abstract - Mean Word Length *
- Abstract - Max Word Length *
- Abstract - Proportion of Content Words *
- Title - Length *
- Title - Wordcount *
- Title - Mean Word Length *
- Title - Max Word Length *
- Title - Proportion of Content Words *
- Authors - Count 


#### Article to Query Match 

- Abstract - Keywords 1 Matches
- Abstract - Keywords 2 Matches
- Abstract - Jaro Distance - Inclusion Criteria
- Abstract - Levenschtein Distance - Inclusion Criteria
- Abstract - Jaccard index - Inclusion Criteria
- Abstract - Sorensen-Dice - Inclusion Criteria
- Abstract - Ratcliff-Obershelp - Inclusion Criteria
- Abstract - Jaro Distance - Exclusion Criteria
- Abstract - Levenschtein Distance - Exclusion Criteria
- Abstract - Jaccard index - Exclusion Criteria
- Abstract - Sorensen-Dice - Exclusion Criteria
- Abstract - Ratcliff-Obershelp - Exclusion Criteria
- Keywords - Keywords 1 Matches
- Keywords - Keywords 2 Matches
- Title - Jaro Distance - Inclusion Criteria
- Title - Levenschtein Distance - Inclusion Criteria
- Title - Jaro Distance - Exclusion Criteria
- Title - Levenschtein Distance - Exclusion Criteria
- Title - Keywords 1 Matches
- Title - Keywords 2 Matches


#### Query Specific

- Keywords 1 - Count
- Keywords 1 - Average Length
- Keywords 2 - Count
- Keywords 2 - Average Length
- Inclusion Criteria - Jaro Distance - Exclusion Criteria
- Inclusion Criteria - Levenschtein Distance - Exclusion Criteria
- Inclusion Criteria - Jaccard index - Exclusion Criteria
- Inclusion Criteria - Sorensen-Dice - Exclusion Criteria
- Inclusion Criteria - Ratcliff-Obershelp - Exclusion Criteria




