import gzip
import sys
import os
import re
import string
"""
P1 project
CS466
Yangyang Lin
"""
# Your function start here
dictionary={}
vowels=['a', 'e', 'i', 'o', 'u','y']
stopword_lst = stopword_lst = ["a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
                    "has", "he", "in", "is", "it", "its", "of", "on", "that", "the", "to",
                    "was", "were", "with"]

def textProcessing(inputFile,outPrefix,tokenize_type,stoplist_type,stemming_type):
    group=[]
    collection=[]
    old_group=[]
    words=[]
    with gzip.open(inputFile,'rt') as lines:
        for line in lines:
            #line_count=line_count+1
            #get each line words array
            #print(f'line:{line}  len: {len(line)}')
            tokens=line.split()
            #print(f'len of to:{len(tokens)}')

            #print(f'tokens:{tokens}')
            #2d array
            if len(tokens)!=0:
               #print(tokens)
               group.append(tokens)
               for e in tokens:
                   words=[]
                   words.append(e)
                   old_group.append(words)
                   
    #print(f'group old:{old_group}')
    if tokenize_type=="fancy":
        collection=fancyToken(group)
        #print(collection)
        print(len(collection))
        print(len(old_group))
    elif tokenize_type=="spaces":
        collection=spaceToken(group)
    if stoplist_type=="yesStop":
        collection=stopping(collection)
    if stemming_type=="porterStem":
        collection=stemming(collection)
    
    #outputPrefix-token
    outputPrefixToken=outPrefix+'-tokens.txt'
    with open(outputPrefixToken,'w') as f:
        #print(f'group:{group}')
        for row in range(len(collection)):
            #print(collection[row])
            f.write(old_group[row][0])
            for col in range(len(collection[row])):
                f.write(' '+collection[row][col])
            f.write('\n')



    #outputPrefix-Heaps
    flatten_group=sum(collection,[])
    print(flatten_group)
    print('after filter')
    filter_group= list(filter(None, flatten_group))
    print(filter_group)
    numTokens=[]
    numUniqueTokens=[]
    count=0 
    total=0
    unique=[]
    token_matrix=[filter_group[i:i + 10] for i in range(0, len(filter_group), 10)]
    print(len(set(filter_group)))
    for tokens in token_matrix:
        for token in tokens:
            if token not in unique:
                unique.append(token)
                count=count+1
        total=total+len(tokens)
        numTokens.append(total)
        numUniqueTokens.append(count)
    outputPrefixHeaps=outPrefix+'-heaps.txt'
    with open(outputPrefixHeaps,'w') as f:
        for x in range(len(numTokens)):
            f.write(str(numTokens[x])+" "+str(numUniqueTokens[x])+'\n')
    #outputPrefix-stats
     #count frequency
    N=100
    tokens={}
    for x in filter_group:
        if x not in tokens.keys():
           tokens[x]=1
        else:
           tokens[x]=tokens[x]+1

    sorted_tokens=dict(sorted(tokens.items(), key=lambda kv: (-kv[1], kv[0])))
    topN=dict(list(sorted_tokens.items())[0: N])
    print(topN)
    outputPrefixStats=outPrefix+'-stats.txt'
    with open(outputPrefixStats,'w') as f:
        f.write(str(total)+'\n')
        f.write(str(count)+'\n')
        for key,value in topN.items():
            f.write(str(key)+" "+str(value)+'\n')
  
def spaceToken(group):
    seeds=[]
    for tokens in group:
        
        for token in tokens:
            seed=[]
            seed.append(token)
            seeds.append(seed)
    return seeds


def fancyToken(group):   
    #skip URL which not start with https:// or http://
    #text processing
    new_group=[]
    collection=[]
    #print(f'in:{len(group)}')
    x=0
    for tokens in group:
        for word in tokens:
            seed=[]
            word=word.lower()
            if word=='porter).':
                print(s)
            url=("https://","http://")
            if word.startswith(url) or bool(re.search("^[0-9+,.-]+$", word)):
                print(word)
                seed.append(word)
                new_group.append(seed)  
            else:    
                #deal with hyphens
                seed.append(word)
                #print(seed)
                if '-' in word:
                    seed.pop()
                    tokens=word.split('-') #remove "-" to get token array
                    #print(f'tokens is {tokens}')
                    token=''.join(tokens)#also whole words as single token
                    #print(f'tokens is {token}')
                    for w in tokens:
                        seed.append(w)
                    seed.append(token)
                #print(seed)
                
                temp=[]
                temp2=[]
                temp2=seed.copy()   
                for s in seed:
                    #print("in2")
                    #print(s)
                    if s=='porter).':
                        print(s)
                    if bool(re.search(r'[^\w\d\-\.\']',s)):
                        print(s)
                        w = re.sub(r'[^\w\-\.\']',' ',s)
                        #w = re.sub(r'[^\w\-\.\']',' ',s)
                        w = w.split()
                        for e in w:
                            if e not in string.punctuation:
                                temp.append(e)
                        print(temp)
                    else:
                        temp.append(s)
                #print(temp)
                #if len(temp)!=0:
                seed.clear()
                seed=temp.copy()
                temp.clear()

                #print(len(temp))
                #print(f'seeds:{seed}')
                temp2=[]
                #print(len(seed))
                for s in seed:
                    #çprint(s)
                    
                    #if "'" in s:
                           #using translate() to remove ' from token:
                    if s=='porter).':
                        print(s)
                    if not bool(re.search("^[0-9+,.-]+$", s)):
                        #print(f'in prime before {s}')
                        s=s.translate({ord("'"):None})
                        #print(f's in  prime:{s}')
                    #if bool(re.search("^[a-z.]+$", s)):
                    #if not bool(re.search("^[0-9+,.-]+$", s)):
                        #print(f'in dot before {s}')
                           #Treat abbreviations as a single token
                        s=s.translate({ord("."):None})
                        print(f's in  dot:{s}')
                    temp.append(s)
                if len(temp)!=0:
                   seed.clear()
                   seed=temp.copy()
                #print("seed")
                #print(seed)
                #print(f'new group:{new_group}')
                new_group.append(seed)
    #print(f'new group:{new_group}')
    return new_group
    

def stopping(group):
    seeds=[]
    collection=[]
    for tokens in group:
        seed=[]
        for token in tokens:
            if token not in stopword_lst:
               seed.append(token)
            else:
                seed.append('')
        seeds.append(seed)
    return seeds


def stemming(new_group):
    #print('before')
    #print(new_group)
    seeds=[]
    for tokens in new_group:
      seed=[]
      for w in tokens:  
        #step 1a
        #Replace sses by ss (e.g., stresses→stress)
        ieds=("ies","ied")
        ssus=("us","ss")
        if w.endswith("sses"):
           w=w.replace("sses","ss")
        #ieds=("ies","ied")
        if w.endswith(ieds):
           if len(w)<=4:
              w=w.replace(w[len(w)-3:],"ie")
           else:
              w=w.replace(w[len(w)-3:],"i")
        if w.endswith('s') and not w.endswith(ssus):
            #print("in here")
            #print(w)
            vols=[x for x in w[:-2] if x in vowels]
            if len(vols)!=0:
                w=w[:-1]
        #step 1b
        eeds=("eed","eedly")
        edins=("ed","edly","ing","ingly")
        double=("bb","dd","ff","gg","mm","nn","pp","rr","tt")
        if w.endswith(eeds):
            ending=(5,3)[w.endswith("eed")]
            vols=[x for x in w[:-(ending+1)] if x not in vowels]
            if(w[-(ending+1)] not in vowels) and len(vols)!=0:
               #print(ending)
               w=w.replace(w[len(w)-ending:],"ee")
        #edins=("ed","edly","ing","ingly")
        #double=("bb","dd","ff","gg","mm","nn","pp","rr","tt")
        elif w.endswith(edins):
            ending=("ed","edly")[w.endswith("edly")]
            ending=(ending,"ingly")[w.endswith("ingly")]
            ending=(ending,"ing")[w.endswith("ing")]
            vols=[x for x in w[:-len(ending)] if x in vowels]
            if len(vols)!=0:
                w=w[:-(len(ending))]
                x=[x for x in w[:-2] if x in vowels]
               #w=w[:-(len(ending))]#delete the ending
                last_word=lambda x: x not in vowels and x!='w' and x!='x'
                atbliz=("at","bl","iz")
                #print(w)
                if w.endswith(atbliz):
                   #w.replace(w[len(w)-2:],"e")
                   w=w+'e'
                #double=("bb","dd","ff","gg","mm","nn","pp","rr","tt")
                elif w.endswith(double):
                    w=w[:-1]#remove the last letter
                #short stem add e
                elif len(w)==2 and w[0] in vowels and w[1] not in vowels:
                    w=w+'e'
                #last_word=lambda x: x not in vowels and x!='w' and x!='x'
                #x=[x for x in w[:-2] if x in vowels]
                
                elif w[-2] in vowels and last_word(w[-1]) and len(x)==0:
                    w=w+'e'
            
                #step 1c ending with y or
        if w.endswith('y'):
            #print("in")
            #print(w[-2])
            #print(len(w))
            if w[-2] not in vowels and len(w)>=3:
                    #print("in2")
                    #print(w[-1])
                    w=w.replace(w[-1],'i')
        seed.append(w)
      seeds.append(seed)
    return seeds

if __name__ == '__main__':
    # Read arguments from command line; or use sane defaults for IDE.
    argv_len = len(sys.argv)
    inputFile = sys.argv[1] if argv_len >= 2 else "P1-train.gz"
    outputFilePrefix = sys.argv[2] if argv_len >= 3 else "outPrefix"
    tokenize_type = sys.argv[3] if argv_len >= 4 else "spaces"
    stoplist_type = sys.argv[4] if argv_len >= 5 else "yesStop"
    stemming_type = sys.argv[5] if argv_len >= 6 else "porterStem"

    # Below is stopword list
    stopword_lst = stopword_lst = ["a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
                    "has", "he", "in", "is", "it", "its", "of", "on", "that", "the", "to",
                    "was", "were", "with"]
    textProcessing(inputFile,outputFilePrefix,tokenize_type,stoplist_type,stemming_type)
