from elasticsearch import Elasticsearch
import nltk
import json
from nltk.corpus import wordnet
from nltk.tokenize import  word_tokenize
from nltk.corpus import stopwords
# nltk.download('wordnet')
elastic_host = {"host": "localhost", "port": 9200}
es = Elasticsearch(hosts=[elastic_host])


def expand_query(text):
    text = text.lower()
    # word_tokens = word_tokenize(text)
    tokens = word_tokenize(text)
    query_string=""
    token_nums=0
    for token in tokens:
        synonyms = []
        synset_array = wordnet.synsets(token)
        for syn in synset_array:
            for l in syn.lemmas():
                if l.name() not in synonyms:
                    synonyms.append(l.name())
                    # print(syn,syn.lemmas(),l,l.name())
        if(len(synset_array) == 0):
            synonyms.append(token)
        query_string+='('+' OR '.join(synonyms)+')'
        token_nums += 1
        if (token_nums < len(tokens)):
            query_string = query_string + ' AND '
        # print("***")
    print(text, '\n*******************\n', query_string)
    # synonyms_string = ' '.join(synonyms)
    return query_string

def doSearch(query):
    search_result = es.search(index='factchecks',
    body={
        # "size":10000,
        # "min_score":7,
        # "query": {
        #     "query_string": {
        #         "query": query,
        #         "fields": ["title", "url", "date_published", "rating", "author_name","category", "tags", "claim", "content"]
        #     }
        # }
        "query": {
            "query_string": {
                "fields": ["title", "url", "date_published", "rating", "author_name","category", "tags", "claim", "content"],
                "query": query
            }
        }
    })
    return search_result

def writeResultInFile(path,query,result):
    if(not path.endswith("/")):
        path+="/"
    path+=query+".txt"
    print(path)
    dest_file = open(path, 'w')
    dest_file.write(result)
    dest_file.close()

def doSimpleAndExtendedSearch(simple_query):
    search_result = doSearch(simple_query)
    writeResultInFile('../simple_queries/', simple_query, json.dumps({
        "max_score": search_result['hits']['max_score'],
        "hits": search_result['hits']['hits']
    }, indent=1))
    # writeResultInFile('../simple_queries/', query1, json.dumps(search_result['hits'], indent=1))
    expanded_query = expand_query(simple_query)
    expanded_search_result = doSearch(expanded_query)
    writeResultInFile('../extended_queries/', simple_query, json.dumps({
        "max_score": expanded_search_result['hits']['max_score'],
        "hits": expanded_search_result['hits']['hits']
    }, indent=1))


#1 word
# query1 ="Research" #"Research" "dishes" "politicians" "Trump"
# doSimpleAndExtendedSearch(query1)

# query2 = "politicians"
# doSimpleAndExtendedSearch(query2)

# query3="government"
# doSimpleAndExtendedSearch(query3)

# query4="Republican"
# doSimpleAndExtendedSearch(query4)

#2 words
# query4="national parks"
# doSimpleAndExtendedSearch(query4)

# query5="instagram account"
# doSimpleAndExtendedSearch(query5)

# query6="Mysterious Monolith"
# doSimpleAndExtendedSearch(query6)

#3 words
# query7="black lives matter"
# doSimpleAndExtendedSearch(query7)

# query8="Dangerous vacation spot"
# doSimpleAndExtendedSearch(query8)

# query9="New York Times"
# doSimpleAndExtendedSearch(query9)

#4 words
# query10="Nothing to Worry About"
# doSimpleAndExtendedSearch(query10)

# query11="former Fox News host"
# doSimpleAndExtendedSearch(query11)

# query12="Does This Photo Show"
# doSimpleAndExtendedSearch(query12)

#5 words
# query13="Mysterious Monolith Found in Utah"
# doSimpleAndExtendedSearch(query13)

# query14="Could Trump Defy Popular Vote"
# doSimpleAndExtendedSearch(query14)

# query15="Are Crab Cake Oreos Real"
# doSimpleAndExtendedSearch(query15)

##output

# ../simple_queries/Research.txt
# research inquiry enquiry search explore
# ../extended_queries/Research.txt
# ../simple_queries/politicians.txt
# politician politico pol political_leader
# ../extended_queries/politicians.txt
# ../simple_queries/government.txt
# government authorities regime governing governance government_activity administration politics political_science
# ../extended_queries/government.txt
# ../simple_queries/Republican.txt
# Republican republican Republican_River
# ../extended_queries/Republican.txt
# ../simple_queries/Newspaper.txt
# newspaper paper newspaper_publisher newsprint
# ../extended_queries/Newspaper.txt
# ../simple_queries/Tweets.txt
# tweet twirp pinch squeeze twinge nip twitch
# ../extended_queries/Tweets.txt
# ../simple_queries/social media.txt
# sociable social mixer societal medium culture_medium spiritualist sensitive mass_medium metier
# ../extended_queries/social media.txt
# ../simple_queries/youtube.txt
# youtube
# ../extended_queries/youtube.txt
