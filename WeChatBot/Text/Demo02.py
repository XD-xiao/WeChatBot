import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag

# ���ر�Ҫ����Դ�������δ���أ�
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')


def process_user_input(input_text):
    # �ִ�
    tokenized_text = word_tokenize(input_text)

    # ���Ա�ע
    tagged_text = pos_tag(tokenized_text)

    # ��ӡ��ע��Ľ��
    for word, tag in tagged_text:
        print(f"{word}: {tag}")


if __name__ == "__main__":
    user_sentence = input("������һ�仰������Ϊ���������и��ʵĴ��ԣ�")
    process_user_input(user_sentence)