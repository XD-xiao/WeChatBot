import nltk
from nltk.chat.util import Chat, reflections
from fuzzywuzzy import fuzz

# nltk.download('punkt')

loaded_pairs = []
with open('AIDialogueTemplate.txt', 'r') as file:
    for line in file:
        loaded_pairs.append(eval(line.strip()))

print(loaded_pairs)


def find_most_similar(target, string_list):
    max_similarity = 0
    most_similar_string = ""
    for s in string_list:
        similarity = fuzz.ratio(target, s[0])
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_string = s[0]
    return most_similar_string, max_similarity


chatbot = Chat(loaded_pairs, reflections)


def chatbot_response(user_input):
    return chatbot.respond(user_input)


while True:
    user_input = input('请输入您的问题：')

    most_similar_str, similarity_score = find_most_similar(user_input, loaded_pairs)

    response = chatbot_response(most_similar_str)
    print(response)
