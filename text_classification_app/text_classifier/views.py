from django.shortcuts import render, redirect
from .forms import FileUploadForm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import nltk
from pickle import load, dump
from django.conf import settings
import os
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
import pickle

def classify_text(request):
    print(settings.STATIC_ROOT)
    print(os.listdir(settings.STATIC_ROOT))
    nltk.download('punkt')
    swfile = open(f'{settings.STATIC_ROOT}\\stopwordsarabic.txt', 'r', encoding='utf-8') 
    stopwords_arabic = swfile.read().splitlines()
    
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('files')
            text_data = []
            for file in files:
                with file.open() as f:
                    text_data.append(preprocessText(f.read().decode(),stopwords_arabic))
                    
            vectorizer =  pickle.load(open(f'{settings.STATIC_ROOT}\\vectorizer.pkl', 'rb'))
            X = vectorizer.transform(text_data)
            model =  pickle.load(open(f'{settings.STATIC_ROOT}\\model.pkl', 'rb'))
            predictions = model.predict(X)
            preds = []
            for p in predictions:
                if p==0:
                    preds.append("Blog")
                else:
                    preds.append("News")
                
            results = list(zip(files, preds))
            return render(request, 'classification_results.html', {'results': results})
    else:
        form = FileUploadForm()
    return render(request, 'classify_text.html', {'form': form})


def removeStopWords(text,stopwords):
    text_tokens = word_tokenize(text)
    return " ".join([word for word in text_tokens if not word in stopwords])
    
def removePunctuation(text):
    tokenizer = RegexpTokenizer(r'\w+')
    return " ".join(tokenizer.tokenize(text))

def preprocessText(text,stopwords):
    noStop=removeStopWords(text,stopwords)
    noPunctuation=removePunctuation(noStop)
    return noPunctuation