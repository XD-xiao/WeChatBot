import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag

# 下载必要的资源（如果尚未下载）
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')


def process_user_input(input_text):
    # 分词
    tokenized_text = word_tokenize(input_text)

    # 词性标注
    tagged_text = pos_tag(tokenized_text)

    # 打印标注后的结果
    for word, tag in tagged_text:
        print(f"{word}: {tag}")


if __name__ == "__main__":
    user_sentence = input("请输入一句话，程序将为您分析其中各词的词性：")
    process_user_input(user_sentence)