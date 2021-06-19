# 该类用于设置停用词
# 1.英文基本停用词
# 2.Java关键字
# 3.符号标点
from nltk.stem.porter import PorterStemmer
import string
from nltk.corpus import stopwords
import re


class stopWords:
    stop_words = []
    java_key = []
    temple = ["org", "args", "com", "swt", "item", "length", "eclips", "error"]

    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.java_key = ["class", 'extends', 'implements', 'interface', 'import', 'package', 'byte', 'boolean', 'char',
                         'double', 'int', 'long', 'float', 'short', 'flase', 'ture', 'null', 'break', 'case',
                         'continue', 'default', 'do', 'else', 'for ', 'if', 'return', 'switch', 'while', 'catch',
                         'finally', 'throw', 'throws', 'try', 'abstract', 'native', 'private', 'protected',
                         'synchronilzed', 'transient', 'volatitle', 'instanceof', 'new', 'this', 'supper', 'void',
                         'const', 'goto']
        # 一些标签集合
        # self.java_key=(["/li","/ul","/**"])
        self.java_key.extend(["/li", "/ul", "/**", "static", "public", "final", "false", "true", "get", "set"])
        # self.java_key.extend(["args", "method", "main", "param","aspectj", "swt", "eclipse", "zxing", "string", "java", "org", "javadoc"])
        self.java_key.extend(self.temple)

        self.porter_stemmer = PorterStemmer()

    def get_stop_words(self):
        return self.stop_words

    def get_java_key(self):
        return self.java_key

    def isPunctuation(self, word):
        if word in string.punctuation:
            return True
        return False

    def isNumber(self, s):
        try:
            float(s)
        except Exception:
            return False
        return True

    def del_all_parten(self, listOfWords):
        # 处理一下_分割的词
        temarr = []
        for word in listOfWords:
            if len(word.split('_')) > 1:
                arr = word.split('_')
                temarr.extend(arr)
            else:
                temarr.append(word)
        listOfWords = temarr

        # temarr=[]
        # for word in listOfWords:
        #     if 'a' <= word[0] <= 'z':
        #         for i in range(len(word)):
        #             if 'A' <= word[i] <= 'Z':
        #                 temarr.append(word[0:i])
        #     temarr.extend(re.findall('[A-Z][^A-Z]*', word))
        # listOfWords = temarr
        # listOfWords=[i.lower() for i in listOfWords]

        # print(listOfWords)
        # 删除列表中涉及的停用元素
        li = []
        ##方法：将点分割的词语挑选出并去除
        for i in range(0, len(listOfWords)):
            str = listOfWords[i].split('.')
            if (len(str) > 1):
                for wo in str:
                    li.append(wo)
            else:
                li.append(listOfWords[i])
        listOfWords = li
        # 清洗 第一个if：/************/类似数据
        # 第二个if 清洗网页含有/
        # 第三个if 清洗纯数字
        # 第四个if 清洗0x数字
        for word in listOfWords:
            if (word[1:3] == '**' and len(word) > 3):
                listOfWords.remove(word)
        for word in listOfWords:
            if (len(word.split('/')) > 1):
                str1 = word.split('/')
                str1 = list(filter(lambda x: x != '', str1))
                listOfWords.remove(word)
                listOfWords.extend(str1)
        # for word in listOfWords:
        #     if (self.isNumber(word)==True):
        #         listOfWords.remove(word)
        # for word in listOfWords:
        #     if(re.sub('0x[0-9a-hA-H]+',"",word)!=None):
        #         listOfWords.remove(word)
        target = []
        for i in listOfWords:
            if i in self.stop_words or i in self.java_key or self.isPunctuation(i) or len(i) <= 2:
                pass
            elif re.search(r"\W", i) != None:
                pass
            elif i.startswith('0x'):
                pass
            # elif i.isalpha()!=True:
            #     pass
            elif self.isNumber(i) == True:
                pass
            else:
                target.append(i)
        # 提取词根
        target = [self.porter_stemmer.stem(i) for i in target]
        ans = []
        for i in target:
            if i in self.stop_words or i in self.java_key or self.isPunctuation(i) or len(i) <= 2:
                pass
            else:
                ans.append(i)

        return ans


if __name__ == '__main__':
    re.findall(r'at [^()]+\([^()]+.java:[0-9]*[)]',
                     'at org.eclipse.core.launcher.Main.main(Main.java:871) asdhiaodhio aidhiaohd')

