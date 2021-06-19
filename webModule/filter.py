import sys

import nltk

# from nltk.corpus import stopwords
# from xml_parser import XmlParser
from pyService.FilterService.stop_words_list  import stopWords
import re
from string import digits
from re import finditer


class Filter:
    # ['Variant has no toString()', 'The Variant class has no toString() and one cannot call getString() in all cases
    # since it throws an Exception if the type is VT_EMPTY. So I suggest: /** * Always returns a String. * &#64;param
    # variant * &#64;return a String */ public static String toString() { if (this.getType() == COM.VT_EMPTY) {
    # return &quot;&quot;; } return this.getString(); } Version 3.1.M2.']
    def __init__(self):
        pass

    def departwords(self, word):
        p = re.compile(r'([a-z]|\d)([A-Z])')
        sub = re.sub(p, r'\1_\2', word).lower()
        # str=sub.split("_")
        sub = sub.replace("_", " ")
        return sub

    def camel_case_split(self,identifier):
        matches = finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
        return [m.group(0) for m in matches]

    def connectString(self, list):
        str = ""
        for word in list:
            str = str + word + " "
        # print(str[0:-1])
        return str[0:-1]

    def needepart(self, word):
        if (word.lower() == word):
            return False
        else:
            return True

    def numDepart(word):
        if (re.match(r"([a-zA-Z]+[0-9]+)", word) != None):
            return True
        else:
            return False

    def toWordNoNum(word):
        res = word.translate(str.maketrans('', '', digits))
        print(res)
        return res

    def splitWords(self, bug_dic):
        SW = stopWords()
        for key, value in bug_dic.items():
            # 获取该bugreport对应的信息
            # 全部小写
            isPart = True
            list = []
            if not isPart:
                list = [i.lower() for i in bug_dic.get(key)]
            else:
                for str in bug_dic.get(key):
                    if self.needepart(str):
                        list.append(self.departwords(str))
                    list.append(str)

                list = [i.casefold() for i in list]
            # print(list)
            # ['Variant has no toString()', 'The Variant class has no toString() and one cannot c..']
            # word装载分词后的结果
            words = []
            for sent in list:
                tem = SW.del_all_parten(nltk.word_tokenize(sent))
                words.extend(tem)
            # 输出
            bug_dic[key] = words
        bug_dic1 = {}
        for key in bug_dic.keys():
            bug_dic1[key] = self.connectString(bug_dic[key])
        return bug_dic1


if __name__ == '__main__':
    # bug_dic=XmlParser('SWTBugRepository.xml').get_bug_contents()
    # print(bug_dic)
    # f=Filter().splitWords(bug_dic)
    # f=Filter.numdepart("win32")
    print()
    s="getHRsudaHuida"
    print(Filter().camel_case_split(s))
    print(Filter().departwords(s))
    # f=Filter.numdepart("win")
    # print(f)
    # print(Filter.toWordnonum("win32"))
    # nltk.download('punkt')
    # sent="sd ds sda sa"
    # print(nltk.word_tokenize(sent))
