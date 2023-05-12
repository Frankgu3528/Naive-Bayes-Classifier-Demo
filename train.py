import os
import math
import jieba
# 垃圾邮件和非垃圾邮件的文档路径
spam_dir = "./data/SPAM"
ham_dir = "./data/HAM"

# 将所有训练样本读入内存中
train_samples = []
train_labels = []
total_spam_count = 0
total_ham_count = 0
for filename in os.listdir(spam_dir):
    with open(os.path.join(spam_dir, filename), "r",encoding="utf-8") as f:
        train_samples.append(f.read())
        train_labels.append(1)  # 标签为1表示垃圾邮件
        total_spam_count+=1 # 2191
for filename in os.listdir(ham_dir):
    with open(os.path.join(ham_dir, filename), "r", encoding="utf-8") as f:
        train_samples.append(f.read())
        train_labels.append(0)  # 标签为0表示非垃圾邮件
        total_ham_count+=1 # 4271

# 构建词典
word_dict = {}
for i, sample in enumerate(train_samples):
    words = sample.split(",")
    for word in words:
        if word not in word_dict:
            word_dict[word] = [0, 0]
            # 如果是垃圾邮件，第二位++
        word_dict[word][train_labels[i]] += 1

# sorted_items = sorted(word_dict.items(), key=lambda x: x[1][0], reverse=True)

# # 输出前 10 个条目
# for key, value in sorted_items[:10]:
#     print(key, ":", value)

# 计算每个词在垃圾邮件和非垃圾邮件中出现的概率
p_word_spam = {}
p_word_ham = {}
# total_spam_count = sum(word_dict[w][1] for w in word_dict) + 2
# total_ham_count = sum(word_dict[w][0] for w in word_dict) + 2

for word, (count_ham, count_spam) in word_dict.items():
    p_word_spam[word] = (count_spam + 1) / (total_spam_count + 2) 
    p_word_ham[word] = (count_ham + 1) / (total_ham_count + 2)

# sorted_items = sorted(p_word_ham.items(), key=lambda x: x[1], reverse=True)

# # 输出前 10 个条目
# for key, value in sorted_items[:10]:
#     print(key, ":", value)
# 定义分类函数
def classify(sample):
    '''
    sum(train_labels):垃圾邮件的数目
    len(train_labels):所有邮件的个数
    p_spam : log(spam先验概率=0.66) 
    p_ham : log(ham先验概率)
    '''
    p_spam = math.log(sum(train_labels) / (len(train_labels)) )
    p_ham = math.log(1 - sum(train_labels) / len(train_labels))
    h = 0
    s = 0
    for word in sample:
        if word in p_word_spam:
            p_spam += math.log(min(p_word_spam[word],1))
            print(word,"垃圾:",p_word_spam[word])
            s+=1
    for word in sample:
        if word in p_word_ham:        
            p_ham += math.log(min(p_word_ham[word],1))
            h+=1
            print(word,":",p_word_ham[word])
    print(p_ham,p_spam,s,h)
    return int(p_spam > p_ham)

# 测试程序
# test_samples = [
#     "晚上回来吃饭吗?老婆孩子在家里等你"
#     # "晚上回来吃饭吗?老婆孩子在家里等你",
#     # "恭喜，你中奖了",
#     # "感情,东西,付出,会,收回,找个,值得,付出",
# ]
stopwords = set()
with open(os.path.join("./", "stopWord.txt"), "r", encoding="utf-8") as f:
    for line in f:
        stopwords.add(line.strip())
# text = "有钱挣是千真万确的，只要你用心，你就可以在一个月之内赚3000元！ "
#text = "“世界读书日”到来之际，CASHL将于2023年4月23日-5月23日面向馆际互借成员馆用户，全面推出“畅读”原版外文图书免费借阅活动，以满足广大用户对人文社科外文图书的借阅需求。"
text = "同学你好，关于CUHK暑期项目报名的简历已收到，由于名额限制，除本次报名外，你也可以进行自行申请。（联系意向教授，获得推荐）项目申请详见附件1-3，CUHK截止日期为2月24日。"
words = [word for word in jieba.cut(text) if word not in stopwords]
label = classify(words)
a = "正常邮件" if label==0 else "垃圾邮件"
print(a)
# for sample in test_samples:
#     label = classify(sample)
#     a = "正常邮件" if label==0 else "垃圾邮件"
#     # print(f"\"{sample}\" is {(\"spam\" if label else \"not spam\")}.")
#     print(f"{sample} is {a}")