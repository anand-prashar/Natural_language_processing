'''
Created on Oct 22, 2017

@author: anand
'''
import nltk
import csv

wordList=[]
wordCountDict={}

with open('vocab') as f:
    for line in f:
        line=line.split(' ')
        wordList.append(line[0])
        wordCountDict[line[0]]=line[1]   

pos_tags= nltk.pos_tag(wordList)

result=[]
tag_counts = {}
for word,tag in pos_tags:
    result.append( [tag, int(wordCountDict[word]), word])
    tag_counts.setdefault(tag,0)
    tag_counts[tag]+=1

tag_list = [] 
for k,v in tag_counts.iteritems():
    tag_list.append([k,v])

tag_list = sorted( tag_list, key = lambda x: x[1], reverse = True)
for tag,count in tag_list:
    print tag,'-',count

       
result = sorted( result, key = lambda x:(x[0],x[1]), reverse = True )    

with open('q8_help_tagged_words.csv', 'wb') as f:
    cw = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    for row in result:
        cw.writerow(row)
    print 'Done'