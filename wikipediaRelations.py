import wikipedia
import re
try:
   import cPickle as pickle
except:
   import pickle

'''
Once you have your word embedding
Your sort them by vector similarity, right

But the math you want is, 

Given several vectors, find a common word that links them
Naive dude, naive
You need to imagine you already have the data
Then figure out what you would do
What’s the point of cleaning and scraping data if it ends up useless
Nothing
I think you want to use a clustering algo that finds one word to summarize many
Basically it’s like

Given N word embeddings

Find one word that best embodies those N vectors
And better would be if you could rank the words
Given N word vectors for your enemy and M for your allies

Find the best hint that matches N and not M

Convex optimization would be really helpful for you
Since you have two goals; be similar to enemy AND NOT similar to ally
This means you really need to bust out the math
You cannot use a crappy rule of thumb hardcoding when you have two requirements

Minimize this objective function:
Sum of (L2norm(X - N) + L2norm(X + M))

For each N in your enemy words 

For each M in your ally words 

We want to find the best X that minimizes this, since that will be the best hint
L2 norm is a vector function

Basically minimize 

L2(X - n1) + L2(X - n2) .... + L2(X + m1) + L2(X + m2)

Assuming you want to be more similar to enemy and less similar to ally
'''

WORDY_OUTPUT = False

def processWiki():
    #  Read in the codenames
    codenameFile = open("codenameList.txt",'r')
    codenames = codenameFile.readlines()
    codenameFile.close()

    relations = []

    #  Parse the codenames
    for c in range(len(codenames)):
        codename = codenames[c] = codenames[c].strip()
        
        suggestions = wikipedia.search(codename)

        if suggestions is None or len(suggestions) == 0:
            print("----- %s has no Wikipedia suggestions! ----- " % codename)
            continue
        
        if WORDY_OUTPUT:
            print ("%s" % codename)
        
        count = 0

        related = codename
        for suggestion in suggestions:
            if len(suggestion) < 3:
                continue

            if "(disambiguation)" in suggestion:
                continue

            try:
                page = wikipedia.page(suggestion)

                if WORDY_OUTPUT:
                    print ("  %s" % suggestion)

                for link in page.links:
                    if len(link) < 3:
                        continue

                    link = link.lower()

                    if WORDY_OUTPUT:
                        print("    %s" % link)

                    for matchGroup in re.finditer("[a-z]+", link):
                        
                        match = matchGroup.group(0)

                        if len(match) < 3:
                            continue
                        count += 1
                        
                        if WORDY_OUTPUT:
                            print("      %s" % match)

                        relations.append([codename, match])
            except wikipedia.exceptions.DisambiguationError as e:
                pass
            except wikipedia.exceptions.PageError as o:
                pass

        print ("%s had %i links." % (codename, count))
    
    relationsFile = open( "codenamesRelationList.p", "wb" ) 
    pickle.dump(relations, relationsFile)

    return relations

def getWikipediaRelations():
    try:
        return pickle.load(open( "codenamesRelationList.p", "rb" ))
    except (OSError, IOError) as e:
        return processWiki()

getWikipediaRelations()