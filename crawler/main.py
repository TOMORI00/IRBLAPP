import requests
from bs4 import BeautifulSoup
import time
from xml.dom.minidom import parse
import xml.dom.minidom

def func(file):
    # 定义要爬取的URL
    URL_prefix = "https://bugs.eclipse.org/bugs/show_bug.cgi?id="
    # 读取xml获得id
    DOMTree = xml.dom.minidom.parse("./resource/" + file)
    root = DOMTree.documentElement
    bugrepository = DOMTree.getElementsByTagName('bugrepository')[0]
    bugrepository.setAttribute("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    bugrepository.setAttribute("xsi:noNamespaceSchemaLocation", "./output/reports.xsd")
    nodeList = root.getElementsByTagName('bug')
    for node in nodeList:
        id = str(node.getAttribute("id"))
        URL = URL_prefix + id
        response = requests.get(URL).text
        # 定义用于html解析的soap工具
        soup = BeautifulSoup(response, 'lxml')
        reporterName = soup.find_all('span', attrs={'class': 'fn'})[1].string
        # 创建新节点
        newNode = DOMTree.createElement('reporter')
        node.appendChild(newNode)
        text = DOMTree.createTextNode(reporterName)
        newNode.appendChild(text)
        # ans = id + " " + reporterName
        # print(ans)
        # time.sleep(5)
    try:
        with open('New' + file, 'w', encoding='UTF-8') as fh:
            # writexml()第一个参数是目标文件对象，第二个参数是根节点的缩进格式，第三个参数是其他子节点的缩进格式，
            # 第四个参数制定了换行格式，第五个参数制定了xml内容的编码。
            DOMTree.writexml(fh, indent='', addindent='', newl='', encoding='UTF-8')
            print('OK')
    except Exception as err:
        print('错误')
if __name__ == '__main__':
    files = ["EclipseBugRepository.xml", "AspectJBugRepository.xml", "SWTBugRepository.xml"]
    for file in files:
        func(file)