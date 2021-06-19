package team.cdwx.irblapp.Handler;

import com.alibaba.fastjson.JSONObject;
import org.springframework.beans.factory.annotation.Value;
import org.w3c.dom.Document;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;

/**
 * @author Daiqj
 */
public class CommitXMLHandler {

    @Value("${targetPath.path}")
    private String targetPath;

    public static void main(String[] args) throws FileNotFoundException {
        CommitXMLHandler commitXMLHandler = new CommitXMLHandler();
        JSONObject a = commitXMLHandler.parseXML("test", "");
        File file = new File("JSON-FIXEDFILES-AspectJCommitRepository.json");
        try (PrintWriter output = new PrintWriter(file)) {
            output.print(JSONObject.toJSONString(a));
        }
    }

    public JSONObject parseXML(String filename, String project) {
        targetPath = "d:\\target";
        JSONObject commitList = new JSONObject();
        DocumentBuilderFactory documentBuilderFactory = DocumentBuilderFactory.newInstance();
        documentBuilderFactory.setNamespaceAware(true);
        final String JAXP_SCHEMA_LANGUAGE = "http://java.sun.com/xml/jaxp/properties/schemaLanguage";
        final String W3C_XML_SCHEMA = "http://www.w3.org/2001/XMLSchema";
        documentBuilderFactory.setAttribute(JAXP_SCHEMA_LANGUAGE, W3C_XML_SCHEMA);
        documentBuilderFactory.setValidating(true);
        documentBuilderFactory.setIgnoringElementContentWhitespace(true);
        try {
            DocumentBuilder documentBuilder = documentBuilderFactory.newDocumentBuilder();
//            String filePath = ResourceUtils.getFile("").toURI().getPath();
//            String filePath = "C:\\WORK_SPACE\\SE3\\backend\\Resource\\AspectJCommitRepository.xml";
            Document document = documentBuilder.parse(filename);
            NodeList nodeList = document.getElementsByTagName("commit");

            //date
            for (int i = 0; i < nodeList.getLength(); i++) {
                Node node = nodeList.item(i);
                String id = node.getAttributes().item(2).getNodeValue();
                String author = node.getAttributes().item(0).getNodeValue();
                String date = node.getAttributes().item(1).getNodeValue();
                String title = node.getFirstChild().getTextContent();
                ArrayList<String> fixedFiles = new ArrayList<>();
                NodeList fixedFileLists = node.getFirstChild().getNextSibling().getChildNodes();
                for (int j = 0; j < fixedFileLists.getLength(); j++) {
                    fixedFiles.add(fixedFileLists.item(j).getTextContent());
                }
                commitList.put(id, date);
            }
            File file = new File(targetPath + "\\" + "JSON-DATE-" + project + "CommitRepository.json");
            try (PrintWriter output = new PrintWriter(file)) {
                output.print(JSONObject.toJSONString(commitList));
            }

            //fixedfiles
            for (int i = 0; i < nodeList.getLength(); i++) {
                Node node = nodeList.item(i);
                String id = node.getAttributes().item(2).getNodeValue();
                String author = node.getAttributes().item(0).getNodeValue();
                String date = node.getAttributes().item(1).getNodeValue();
                String title = node.getFirstChild().getTextContent();
                ArrayList<String> fixedFiles = new ArrayList<>();
                NodeList fixedFileLists = node.getFirstChild().getNextSibling().getChildNodes();
                for (int j = 0; j < fixedFileLists.getLength(); j++) {
                    fixedFiles.add(fixedFileLists.item(j).getTextContent());
                }
                commitList.put(id, fixedFiles);
            }
            file = new File(targetPath + "\\" + "JSON-FIXEDFILES-" + project + "CommitRepository.json");
            try (PrintWriter output = new PrintWriter(file)) {
                output.print(JSONObject.toJSONString(commitList));
            }

            //fixedfiles
            for (int i = 0; i < nodeList.getLength(); i++) {
                Node node = nodeList.item(i);
                String id = node.getAttributes().item(2).getNodeValue();
                String author = node.getAttributes().item(0).getNodeValue();
                String date = node.getAttributes().item(1).getNodeValue();
                String title = node.getFirstChild().getTextContent();
                ArrayList<String> fixedFiles = new ArrayList<>();
                NodeList fixedFileLists = node.getFirstChild().getNextSibling().getChildNodes();
                for (int j = 0; j < fixedFileLists.getLength(); j++) {
                    fixedFiles.add(fixedFileLists.item(j).getTextContent());
                }
                commitList.put(id, title);
            }
            file = new File(targetPath + "\\" + "JSON-TITLE-" + project + "CommitRepository.json");
            try (PrintWriter output = new PrintWriter(file)) {
                output.print(JSONObject.toJSONString(commitList));
            }




        } catch (ParserConfigurationException | IOException | SAXException e) {
            e.printStackTrace();
        }
        return commitList;
    }

    private JSONObject buildObject(String id, String author, String date, String title, ArrayList<String> fixedFiles) {
        JSONObject jsonObject = new JSONObject();
        jsonObject.put("id", id);
        jsonObject.put("author", author);
        jsonObject.put("date", date);
        jsonObject.put("title", title);
        jsonObject.put("fixedFiles", fixedFiles);
        return jsonObject;
    }
}
