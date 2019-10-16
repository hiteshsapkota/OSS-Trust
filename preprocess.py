#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 16:25:40 2018

@author: hiteshsapkota
"""
import re
import string
import emoji
import json
from emojipedia import Emojipedia
from tweetokenize import Tokenizer
from nltk.tokenize.moses import MosesDetokenizer
import time
detokenizer = MosesDetokenizer()
import time
expanded_words={"tbh": "to be honest", "lgtm":"looks good to me", "r+": "Review", "wc": "Welcome", "btw":"by the way"}
with open("/Users/hiteshsapkota/Desktop/ICSETrust/Data/shortcodeemoji.json") as outfile:
    shortcodeemoji=json.load(outfile)
gettokens=Tokenizer()   
def expandwords(comment):
    words=[]
    keys=[k for k,v in expanded_words.items()]
    for word in comment.split():
        present=False
        for key in keys:
            if key in word.lower():
                present=True
                words.append(expanded_words[key])
        if present is False:
            words.append(word)
    return ' '.join(words)
    
def is_emoji(token):
    return token in emoji.UNICODE_EMOJI        
    
def removeurl(comment):
    modified_comment=re.sub(r'http\S+', 'url', comment)
    return modified_comment

def replacenewline(comment):
    comment=comment.replace('\r\n', '')
    comment=comment.replace('\n', '')
    
    return comment
    
def replacecode(comment):
    comment=re.sub('```[^>]+```' ,'code', comment)
    return comment

def removefilenames(comment):
    comment=re.sub('[\(\[].*?[\)\]]', '', comment)
    return comment
def replacesyntax(comment):
    comment=re.sub(r"\`(.*?)\`" ,'syntax', comment)
    return comment
    
    
    return comment

def iscoverall(comment):
    coverage1="[![Coverage Status]"
    coverage2="[Current Coverage]"
    if coverage1 in comment or coverage2 in comment:
        return 1
    else:
        return 0
    
def isattachedtext(comment):
    results=[]
    attached=False
    extract_comment=re.findall(r">[^>]+\n\n",comment)
    if len(extract_comment)!=0:
        attached=True
    results.append(attached)
    
    if attached:
        comment=comment.replace(extract_comment[0], '')
        results.append(comment)
        for each_comment in extract_comment:
            new_comment=each_comment.replace('>', '')
            new_comment=new_comment.replace('\n\n', '')
            break
        results.append(new_comment)
    return results
            
        
    

def issuccess(shortcodemoji, key):
    success=False
    try:
      description=Emojipedia.search(shortcodeemoji[key]).description
      success=True
      
    except:
        success=False
    return success

def isemojisuccess(token):
    success=False
    try:
       description=Emojipedia.search(token).description
       success=True
    except: 
        success=False
    return success
def getDescription(token):
    #description=emoji.UNICODE_EMOJI[token]
    try:
        description=Emojipedia.search(token).description
    except:
        print("Exception occurred in getting description of the emoji")
        prev_time=time.time()
        while True:
            next_time=time.time()
            if (next_time-prev_time)>300:
                description=token
                break
            
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(10)
            print("Was a nice sleep, now let me continue...")
            success=isemojisuccess(token)
            if success:
                description=Emojipedia.search(token).description
                break
    
    return description
    
def emojiprocess(comment):
    emojis_shortcodes=re.findall(r"\:(.*?)\:",comment)
    keys=[k for k,v in shortcodeemoji.items()]
    for emoji_shortcode in emojis_shortcodes:
        emoji_shortcode=":"+emoji_shortcode+":"
        for key in keys:
            if emoji_shortcode in key:
                try:
                  description=Emojipedia.search(shortcodeemoji[key]).description
                  description=description[0:description.find('\n\n')]
                  comment=comment.replace(emoji_shortcode, description)
                  
                except:
                   prev_time=time.time()
                   while True:
                     now=time.time()
                     if (now-prev_time)>300:
                         description=key
                         comment=comment.replace(emoji_shortcode, description)
                         break
                     print("Connection refused by the server..")
                     print("Let me sleep for 5 seconds")
                     print("ZZzzzz...")
                     time.sleep(10)
                     print("Was a nice sleep, now let me continue...")
                     success=issuccess(shortcodeemoji, key)
                     if success:
                          description=Emojipedia.search(shortcodeemoji[key]).description
                          description=description[0:description.find('\n\n')]
                          comment=comment.replace(emoji_shortcode, description)
                          break
                     
        ##If available then replace with the description
        ##else replace with the same text
    return comment

def referring(comment):
    results=[]
    usernames=[]
    present=False
    for word in comment.split():
        if '@' in word:
            present=True
            username=word.replace('@','')
            usernames.append(username)
    results.append(present)
    results.append(usernames)
    return results

def likereplace(comment):
    return comment.replace('+1', ':+1:')
            
    
            
            
def replacehash(comment):
    entity_prefix = '#'
    words=[]
    for word in comment.split():
        if entity_prefix in word:
            words.append("hashtag")
        else:
            words.append(word)
    return ' '.join(words)

def striprefer(comment):
    entity_prefix = '@'
    words=[]
    for word in comment.split():
        if entity_prefix in word:
            continue
        else:
            words.append(word)
    return ' '.join(words)
    

def isreplied(comment):
    str2="On"
    str1='notifications@github.com'
    str3='Reply to this email directly or view it on GitHub'  
    if str2 in comment and str1 in comment and str3 in comment:
        return True
    else:
        return False
    
def removereply(sentence):
    result=[]
    str2="On"
    str1='notifications@github.com'
    str3='Reply to this email directly or view it on GitHub'
    indices_str2=[a.start()  for a in re.finditer(str2, sentence)]
    indices_str1=[a.start()  for a in re.finditer(str1, sentence)]
    indices_str3=[a.start()  for a in re.finditer(str3, sentence)]
    name_extract_pair={}
    for index1 in indices_str1:
        name_extract_pair[index1]=0
        min_val=10^100000
        index_min_val=0
        for index2 in indices_str2:
            if index2>index1:
                continue
            if (index1-index2)<min_val:
                min_val=(index1-index2)
                index_min_val=index2
    
        name_extract_pair[index1]=index_min_val 
        
        
    names=[]
    for k,v in name_extract_pair.items():
        substring=sentence[v:k]
        index_comma=[a.start() for a in re.finditer(",", substring)]
        index=max(index_comma)
        name=substring[index+1:len(substring)]
        names.append(name)
    section_remove_pair={}   
    for index3 in indices_str3:
        section_remove_pair[index3]=0
        min_val=10^100000
        index_min_val=0
        for index2 in indices_str2:
            if index2>index3:
                continue
        
            if (index3-index2)<min_val:
                min_val=(index3-index2)
                index_min_val=index2
        section_remove_pair[index3]=index2
    for k,v in section_remove_pair.items():
        sentence=sentence[0:v]+sentence[k+len(str3):len(sentence)]
    result.append(names)
    result.append(sentence)
    return result

def transformemoji(comment):
     tokens=gettokens.tokenize(comment)
     i=0
     for token in tokens:
        if is_emoji(token):
            token=getDescription(token)#"EMOJI"
            token=token[0:token.find('\n\n')]
        tokens[i]=token.lower()
        i=i+1
            
     
     return tokens

def directemojidetect(sentence):
    tokens=transformemoji(sentence)
    sentence=detokenizer.detokenize(tokens, return_str=True)
    return sentence
    
 
if __name__== "__main__":
    sentence="hitesh [name.zip] hi"
    print(removefilenames(sentence))