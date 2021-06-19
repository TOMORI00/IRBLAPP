import os
import json


class LoadModule:
    def read_origin_reports(self):
        with open('./../JSON-AspectJ/JSON-SUMMARY&DESCRIPTION-NewAspectJBugRepository.json',encoding='utf-8') as f:
            reports = json.load(f)
        return reports

    def read_report(self):
        # 读取report，存放在一个字典中，key为report的文件名，value为report文件的内容（是个list）
        # reports = {}
        # for file in os.listdir('data/report_preprocessed'):
        #     data = open(os.path.join('data/report_preprocessed', file), 'r', encoding='utf-8').read()
        #     reports[file] = data
        with open('./../pyService/FilterService/AspectJ_SummaryAndDescription-no.json') as f:
            reports = json.load(f)
        return reports

    def read_codes(self):
        # codes = {}
        # for file in os.listdir('data/class_preprocessed'):
        #     data = open(os.path.join('data/class_preprocessed', file), 'r', encoding='utf-8').read()
        #     codes[file] = data
        with open('.././pyService/FilterService/resultsOfAST/aspectj-RB_V152/processedallWords.json',encoding='utf-8') as f:
            codes = json.load(f)
        return codes

    def read_methods(self):
        with open('./../pyService/FilterService/resultsOfAST/aspectj-RB_V152/processedmethods.json') as f:
            methods = json.load(f)
        return methods

    def read_classes(self):
        with open('./../pyService/FilterService/resultsOfAST/aspectj-RB_V152/processedclasses.json') as f:
            classes = json.load(f)
        return classes

    def read_attributes(self):
        with open('./../pyService/FilterService/resultsOfAST/aspectj-RB_V152/processedattributes.json') as f:
            attributes = json.load(f)
        return attributes

    def read_comments(self):
        with open('./../pyService/FilterService/resultsOfAST/aspectj-RB_V152/processedcomments.json') as f:
            comments = json.load(f)
        return comments

    def read_summaries(self):
        with open('./../pyService/FilterService/AspectJ_Summary_no.json') as f:
            summaries = json.load(f)
        return summaries

    def read_descriptions(self):
        with open('./../pyService/FilterService/AspectJ_Description_no.json') as f:
            descriptions = json.load(f)
        return descriptions

    def read_fixedfiles(self):
        with open('./../JSON-AspectJ/JSON-FIXEDFILES-NewAspectJBugRepository.json') as f:
            fixedfiles = json.load(f)
        # 全类名 ----> 类名  a.b.c
        for reportName in fixedfiles.keys():
            code_list = fixedfiles[reportName]
            new_code_list = []
            for codeName in code_list:
                # new_code_list.append(codeName.split('.')[-2])
                new_code_list.append(codeName.split('.')[-2].split('/')[-1])
            fixedfiles[reportName] = new_code_list


        return fixedfiles

    def read_fixdate(self):
        with open('./../JSON-AspectJ/JSON-FIXDATE-NewAspectJBugRepository.json') as f:
            fixdate = json.load(f)
        return fixdate


    def read_opendate(self):
        with open('./../JSON-AspectJ/JSON-OPENDATE-NewAspectJBugRepository.json') as f:
            opendate = json.load(f)
        return opendate

    def read_classes_tfidf(self):
        with open('./tfidfForAspectJ/classes_AspectJ.json') as f:
            s = json.load(f)
        return s

    def read_methods_tfidf(self):
        with open('./tfidfForAspectJ/methods_AspectJ.json') as f:
            s = json.load(f)
        return s

    def read_comments_tfidf(self):
        with open('./tfidfForAspectJ/comments_AspectJ.json') as f:
            s = json.load(f)
        return s

    def read_attributes_tfidf(self):
        with open('./tfidfForAspectJ/attributes_AspectJ.json') as f:
            s = json.load(f)
        return s

    def read_summaries_tfidf(self):
        with open('./tfidfForAspectJ/summaries_AspectJ.json') as f:
            s = json.load(f)
        return s

    def read_descriptions_tfidf(self):
        with open('./tfidfForAspectJ/descriptions_AspectJ.json') as f:
            s = json.load(f)
        return s

    def read_corpus(self):
        with open('./tfidfForAspectJ/corpus_AspectJ.json') as f:
            s = json.load(f)
        return s



if __name__ == '__main__':
    loadModule = LoadModule()
    print(loadModule.read_fixdate())

