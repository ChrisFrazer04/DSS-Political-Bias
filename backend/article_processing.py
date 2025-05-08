import re
import requests
from bs4 import BeautifulSoup
import spacy
import numpy as np

def filter_text(text: str, nlp):
    text = re.sub(r'\n\s*\n', '\n', text)  # Remove excess blank lines
    text = re.sub(r'\t\s*\t', '\t', text)
    text = text.encode("utf-8", errors='ignore').decode("utf-8") #Replacing unicode characters
    text = text.strip()
    doc: spacy.tokens.doc.Doc = nlp(text)
    first_subject = False
    relevant_lines = []
    article_flags = {}
    doc_sents = [x for x in doc.sents]

    #Making a list of relevant subjects/nouns in the title
    for sent in doc_sents:
        for word in sent:
            w_str = str(word).lower()
            if word.pos_ == 'PROPN':
                if w_str not in article_flags:
                    article_flags[w_str] = 0
                article_flags[w_str] += 1
            elif word.dep_ in ['nsubj', 'ROOT']:
                if w_str not in article_flags:
                    article_flags[w_str] = 0
                article_flags[w_str] += 1
            elif word.ent_id_ in ['PERSON', 'ORG', 'GPE']:
                if w_str not in article_flags:
                    article_flags[w_str] = 0
                article_flags[w_str] += 1
    common_flag_vals = sorted(list(article_flags.values()), reverse=True)[:3]
    common_flags = [x for x,y in article_flags.items() if y in common_flag_vals]
    #print(common_flags)
    #Keeping all sentences after first appearance of relevant word
    #print(doc_sents)
    doc_reverse = list(reversed(doc_sents))
    for sentence in doc_sents:
        if not first_subject:
            for word in sentence:
                word = str(word).lower()
                if word in common_flags:
                    first_subject = True
                    relevant_lines.append(str(sentence))
        else:
            relevant_lines.append(str(sentence))
    
    #Removing all ending text after the last mention of a relevant entity
    last_subject=False
    for ind, sentence in enumerate(doc_reverse):
        if not last_subject:
            for word in sentence:
                word = str(word).lower()
                if word in common_flags:
                    last_subject = True
                    last_subj_ind = ind

    relevant_lines = relevant_lines[:-last_subj_ind]
    seen_lines = []
    for sentence in relevant_lines:
        if sentence in seen_lines:
            continue
        seen_lines.append(sentence.strip())
    full_text = ' '.join(seen_lines)

    #Further processing 
    pattern = r"\n"
    full_text = re.sub(pattern, ".", full_text)
    pattern2 = r'\s{2,}'
    full_text = re.sub(pattern2, "", full_text)

    #removing sentences that have between 2 and 4 words
    sents = full_text.split(".")
    sents_cleaned = [x for x in sents if not 4 >= len(x.split()) >1]    

    return ".".join(sents_cleaned)

def scrape_url(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/105.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
    }
    try:
        response = requests.get(url, timeout=2.5, headers=headers)
        if response.status_code != 200:
            url = f"https://web.archive.org/web/{url}"
            response = requests.get(url, timeout=2.5, headers=headers)
            if response.status_code != 200:
                print('error')
                return 'Error'
    except:
        return 'Error'
    content = BeautifulSoup(response.text, "html.parser")
    all_p = content.find_all('p')
    clean_text = [x.text for x in all_p]
    full_text = ' '.join(clean_text)
    return full_text
