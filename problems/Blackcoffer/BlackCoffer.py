import pandas as pd
from nltk.corpus import stopwords
import urllib
import re

#Extract data and take usefull data
list=pd.read_excel("data/cik_list.xlsx")
master_dic=pd.read_csv("data/Master_dic.csv")
uncertainity_dic=pd.read_excel('data/uncertainty_dictionary.xlsx')
constraining_dic=pd.read_excel('data/constraining_dictionary.xlsx')

pos=[master_dic['Word'][i] for i in range(len(master_dic)) if master_dic['Positive'][i]==2009]
neg=[master_dic['Word'][i] for i in range(len(master_dic)) if master_dic['Negative'][i]==2009]

stop_words=stopwords.words('english')
uncertainity_word=[i for i in uncertainity_dic['Word']]
constraining_word=[i for i in constraining_dic['Word']]

#Create Functions for Major tasks
def getWords(text):
    return re.compile('\w+').findall(text)

def Syllable_count(list):
    n=0
    for word in list:
        word = word.lower()
        count=0
        vowels = "aeiouy"
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
                if word.endswith("es")|word.endswith("ed"):
                    count -= 1
        if count > 1:
            n +=1
    return n
    

def Sentimental_Analysis(page):
    p, n, word_count, sentence_count, complex_no, uncertainityWordCount, constrainingWordCount = 0,0,0,0,0,0,0
    
    for line in page: 
        line=line.decode('utf-8')
        sentence_count+=line.count(".")
                
        line=getWords(line)
        line=[i for i in line if not i in stop_words]
        
        complex_no+=Syllable_count(line)
        
        word_count+=len(line)
        
        p+=len(set.intersection(set(line),set(pos)))
        n+=len(set.intersection(set(line),set(neg)))
        
        uncertainityWordCount+=len(set.intersection(set(line),set(uncertainity_word)))
        constrainingWordCount+=len(set.intersection(set(line),set(constraining_word)))
        
    Pol = (p-n)/((p+n)+0.000001)
    asn=word_count/sentence_count
    pcw=complex_no/word_count
    fogIndex = 0.4*(asn+pcw)
    
    return(p,n,Pol,asn,pcw,fogIndex,complex_no,word_count,uncertainityWordCount,constrainingWordCount)

#Open csv file for data saving
file=open("data.csv",'w')
file.write("Positive_score,Negitive_score,Polerity_Score,Average_Sentence_length,Percentage_of_complex_words,Fog_index,Complex_word_count,Word_count,Uncertainity_score,Constraining_score\n")

#start Analysis
my_links=["https://www.sec.gov/Archives/"+i for i in list['SECFNAME']]
for i in my_links:
    page=urllib.request.urlopen(i)
    a=Sentimental_Analysis(page)
    file.write(str(a[0]) + "," + str(a[1]) + "," + str(a[2]) + "," + str(a[3]) + "," + str(a[4]) + "," + str(a[5]) + "," + str(a[6]) + "," + str(a[7]) + "," + str(a[8]) + "," + str(a[9]) + "\n")

file.close()

#Concatinate our data and cik_list file
list=pd.read_excel("data/cik_list.xlsx")
output=pd.read_csv("data.csv")
final=pd.concat([list,output],axis=1)
final.to_csv("final.csv",encoding='utf-8')
