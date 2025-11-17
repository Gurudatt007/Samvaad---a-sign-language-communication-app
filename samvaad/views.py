from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

import nltk
from django.contrib.staticfiles import finders
from django.contrib.auth.decorators import login_required

from pycorenlp import StanfordCoreNLP
from nltk.tree import *
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer


def home_view(request):
    return render(request, 'home.html')


def about_view(request):
    return render(request, 'about.html')


def contact_view(request):
    return render(request, 'contact.html')


@login_required(login_url="login")
def animation_view(request):
    if request.method == 'POST':
        text = request.POST.get('sen')
        text = text.lower()
        nlp = StanfordCoreNLP('http://localhost:9000')
        parsetree = nlp.annotate(text, properties={
            'annotators': 'tokenize,ssplit,pos,ner,parse',
            'ssplit.isOneSentence': True,
            'outputFormat': 'json'
        })
        dict = {}
    
# "***********subtrees**********"
        parenttree = ParentedTree.fromstring(
            parsetree['sentences'][0]['parse'])
# parenttree = ParentedTree.fromstring(parsetree)
        for sub in parenttree.subtrees():
            dict[sub.treeposition()] = 0

        # "----------------------------------------------"
        isltree = Tree('ROOT', [])
        i = 0
        for sub in parenttree.subtrees():
            if(sub.label() == "NP" and dict[sub.treeposition()] == 0 and dict[sub.parent().treeposition()] == 0):
                dict[sub.treeposition()] = 1
                isltree.insert(i, sub)
                i = i+1
            if(sub.label() == "VP" or sub.label() == "PRP"):
                for sub2 in sub.subtrees():
                    if((sub2.label() == "NP" or sub2.label() == 'PRP') and dict[sub2.treeposition()] == 0 and dict[sub2.parent().treeposition()] == 0):
                        dict[sub2.treeposition()] = 1
                        isltree.insert(i, sub2)
                        i = i+1
        for sub in parenttree.subtrees():
            for sub2 in sub.subtrees():
                # print sub2
                # print len(sub2.leaves())
                # print dict[sub2.treeposition()]
                if(len(sub2.leaves()) == 1 and dict[sub2.treeposition()] == 0 and dict[sub2.parent().treeposition()] == 0):
                    dict[sub2.treeposition()] = 1
                    isltree.insert(i, sub2)
                    i = i+1
        parsed_sent = isltree.leaves()
        words = parsed_sent
        # print(words)


# =======================Stop word ==========================

        WordSet = []
        for word in words:
            if word not in set(stopwords.words("english")):
                WordSet.append(word)
        # print(WordSet)

        # ====================Stemming ===========================
        ps = PorterStemmer()
        WordSetStem = []
        for word in WordSet:
            WordSetStem.append(ps.stem(word))
        # print(WordSetStem)
        # =====================Lemmatization ======================
        lm = WordNetLemmatizer()
        WordSetLem = []
        for word in WordSet:
            WordSetLem.append(lm.lemmatize(word))
        # print(WordSetLem)
        lem = []
        islsentence = ""
        for word in WordSetLem:
            lmword = lm.lemmatize(word, pos="v")
            lem.append(lmword)
            islsentence += lmword
            islsentence += " "
        print(islsentence)

        # tokenizing the sentence
        filtered_text = []
        for w in lem:
            path = w + ".mp4"
            f = finders.find(path)
            # splitting the word if its animation is not present in database
            if not f:
                for c in w:
                    filtered_text.append(c)
            # otherwise animation of word
            else:
                filtered_text.append(w)
        words = filtered_text

        return render(request, 'animation.html', {'words': words, 'text': text, 'lem': islsentence})
    else:
        return render(request, 'animation.html')


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # log the user in
            return redirect('animation')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            #log in user
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('animation')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect("home")
