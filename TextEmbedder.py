sys.path.append("./lexvec")
import Lexvec as lexvec

pathtomodelbin = "models/lexvec.commoncrawl.ngramsubwords.bin"

model = lexvec.Model(pathtomodelbin)

def vectorize_text(txt):
    cleaned = clean_text(txt)
    words = cleaned.split()
    result = np.zeros(300)
    for wrd in words:    
        vector = model.word_rep(wrd)
        result = result + vector
    return result

def clean_text(txt):
    temp = txt.lower()
    temp2 = temp.replace("[-!?.,':;_]", "") 
    temp3 = temp.replace("[ ]*", " ") 

