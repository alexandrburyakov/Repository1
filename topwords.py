#Функция отыскания из текста 50 самых частотных слов длиной более 2 букв с учетом стоп-слов
def topWords(text, stopwords, num = 50, lenWords = 2):
    import re
    from collections import Counter
    listOfWords = re.split(r'\W+', text)
    listOfWordsReduced = [wor.lower() for wor in listOfWords if len(wor) > lenWords and wor not in stopwords]
    words_counter = Counter(listOfWordsReduced)
    sorted_by_number = sorted(words_counter.items(), key=lambda kv: kv[1], reverse = True)
    words = [k for (k,v) in sorted_by_number][:num]
    return words
