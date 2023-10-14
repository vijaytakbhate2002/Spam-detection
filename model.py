import nltk
import joblib
import re
from urllib.parse import urlparse
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.preprocessing import LabelEncoder
import warnings 
warnings.filterwarnings('ignore')

nltk.download('omw-1.4') # Open Multilingual Wordnet, this is an lexical database 
nltk.download('wordnet') 
nltk.download('wordnet2022')
nltk.download('punkt')
nltk.download('stopwords')

lemmatizer = WordNetLemmatizer()
stop_words = list(stopwords.words('english'))

model = joblib.load("static\\spam detector tf-idf (1)")
tf_vec = joblib.load("static\\1 vectorizer")

def predictor(user_sms):
    def textProcess(sms):
        try:
            # brackets replacing by space
            sms = re.sub('[][)(]',' ',sms)

            # url removing
            sms = [word for word in sms.split() if not urlparse(word).scheme]
            sms = ' '.join(sms)

            # removing words starts from @
            sms = re.sub(r'\@\w+','',sms)

            # removing html tags 
            sms = re.sub(re.compile("<.*?>"),'',sms)
            
            # getting only characters and numbers
            sms = re.sub('[^A-Za-z0-9]',' ',sms)
            
            # make all words into lowercase
            sms = sms.lower()
            
            # word tokennization 
            tokens = word_tokenize(sms,language='english')
            
            # removing whitespaces
            sms = [word.strip() for word in tokens]
            
            # stopwords removing
            sms = [word for word in sms if word not in stop_words]
            
            # lemmatization
            sms = [lemmatizer.lemmatize(word) for word in sms]
            sms = ' '.join(sms)
            
            return sms
        except Exception as e:
            print("sms",sms)
            print("Error",e)
            return 0
        
    def manager(sms):
        sms = textProcess(sms)
        sms = tf_vec.transform([sms])
        result = model.predict(sms)
        return result[0]

    return manager(user_sms)
