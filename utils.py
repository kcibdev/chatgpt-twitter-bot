
import re


tweets_thread_list = [
    {
        "id": 1,
        "keyword": "List top 5 reasons, opportunity someone should learn tech in this Day and age. Before you list them write this first as a header \"Top 5 reason you learn or go into tech \" New line write \"\nA thread\"\n before listing them"
    },
    {
        "id": 2,
        "keyword": "List top 8 tech jobs that people should go into and reason why and where to find resources for it, start with a header \"Top 8 tech jobs you can learn and get into now\" A new line \"A thread\" before listing it"
    },
    {
        "id": 3,
        "keyword": "List 5 ways on how to make yourself known on social media with examples, start with the header \"How do you engage and make yourself known on social Media\" a new line \"A thread\", before listing"
    },
    {
        "id": 4,
        "keyword": "List top 5 reasons, benefit and why you should learn software development, start with a header \"Top 5 reasons to learn software development\" A new line \"A thread\", before listing"
    },
]

replace_words = ["A thread:", "1.", "2.", "3.",
                 "4.", "5.", "6.", "7.", "8.", "9.", "10."]


def replace_words_in_tweet(text):
    d_text = text
    for word in replace_words:
        if word == "A thread:":
            d_text = d_text.replace(word, f"\n{word}\n\n")
        else:
            d_text = d_text.replace(word, f"\n\n{word}")

    return d_text


def trimText(text):
    result = re.sub(r"@\w+", "", text.lower())
    trimmed = result.strip()
    return trimmed


def retreive_last_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id


def store_last_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return
