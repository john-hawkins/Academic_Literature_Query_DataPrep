#!/bin/bash

pip install nltk
pip install gensim
pip install textdistance
pip install jellyfish
pip install pandas

cd models 

curl -L -o lexvec.commoncrawl.ngramsubwords.bin.gz https://www.dropbox.com/s/buix0deqlks4312/lexvec.commoncrawl.ngramsubwords.300d.W.pos.bin.gz?dl=1
 
gzip -d lexvec.commoncrawl.ngramsubwords.bin.gz

