#!/bin/bash

./prepare_dataset.py data/sample/articles.csv Title Abstract Author Keywords data/sample/inclusion_criteria.txt data/sample/exclusion_criteria.txt data/sample/keywords_1.txt data/sample/keywords_2.txt > data/sample/processed.csv

