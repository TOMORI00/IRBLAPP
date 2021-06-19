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
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;

/**
 * @author Daiqj
 */
public class ReportXMLHandler {

    @Value("${targetPath.path}")
    private String targetPath;

    public static void main(String[] args) {
        ReportXMLHandler reportXmlHandler = new ReportXMLHandler();
        reportXmlHandler.parseXML("C:\\WORK_SPACE\\SE3\\backend\\crawler\\output\\NewSWTBugRepository.xml", "SWT");
    }

    public JSONObject parseXML(String filename, String project) {
        targetPath = "d:\\target";
        JSONObject reportList = new JSONObject();
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
//            String filePath = "C:\\WORK_SPACE\\SE3\\backend\\crawler\\output\\NewEclipseBugRepository.xml";
            Document document = documentBuilder.parse(filename);
            NodeList nodeList = document.getElementsByTagName("bug");

            //description
            for (int i = 0; i < nodeList.getLength(); i++) {
                Node node = nodeList.item(i);
                String id = node.getAttributes().item(1).getNodeValue();
                String fixdate = node.getAttributes().item(0).getNodeValue();
                String opendate = node.getAttributes().item(2).getNodeValue();
                String summary = node.getFirstChild().getFirstChild().getTextContent();
                String description = node.getFirstChild().getFirstChild().getNextSibling().getTextContent();
                ArrayList<String> fixedFiles = new ArrayList<>();
                NodeList fixedFileLists = node.getFirstChild().getNextSibling().getChildNodes();
                for (int j = 0; j < fixedFileLists.getLength(); j++) {
                    fixedFiles.add(fixedFileLists.item(j).getTextContent());
                }
                String reporter = node.getFirstChild().getNextSibling().getNextSibling().getTextContent();
                reportList.put(id, description);
            }
            File file = new File(targetPath + "\\" + "JSON-DESCRIPTION-New" + project+ "BugRepository.json");
            try (PrintWriter output = new PrintWriter(file)) {
                output.print(JSONObject.toJSONString(reportList));
            }

            //fixdate
            reportList = new JSONObject();
            for (int i = 0; i < nodeList.getLength(); i++) {
                Node node = nodeList.item(i);
                String id = node.getAttributes().item(1).getNodeValue();
                String fixdate = node.getAttributes().item(0).getNodeValue();
                reportList.put(id, fixdate);
            }
            file = new File(targetPath + "\\" + "JSON-FIXDATE-New" + project+ "BugRepository.json");
            try (PrintWriter output = new PrintWriter(file)) {
                output.print(JSONObject.toJSONString(reportList));
            }

            //fixedfiles
            reportList = new JSONObject();
            for (int i = 0; i < nodeList.getLength(); i++) {
                Node node = nodeList.item(i);
                String id = node.getAttributes().item(1).getNodeValue();
                String fixdate = node.getAttributes().item(0).getNodeValue();
                String opendate = node.getAttributes().item(2).getNodeValue();
                String summary = node.getFirstChild().getFirstChild().getTextContent();
                String description = node.getFirstChild().getFirstChild().getNextSibling().getTextContent();
                ArrayList<String> fixedFiles = new ArrayList<>();
                NodeList fixedFileLists = node.getFirstChild().getNextSibling().getChildNodes();
                for (int j = 0; j < fixedFileLists.getLength(); j++) {
                    fixedFiles.add(fixedFileLists.item(j).getTextContent());
                }
                reportList.put(id, fixedFiles);
            }
            file = new File(targetPath + "\\" + "JSON-FIXEDFILES-New" + project+ "BugRepository.json");
            try (PrintWriter output = new PrintWriter(file)) {
                output.print(JSONObject.toJSONString(reportList));
            }

            //opendate
            reportList = new JSONObject();
            for (int i = 0; i < nodeList.getLength(); i++) {
                Node node = nodeList.item(i);
                String id = node.getAttributes().item(1).getNodeValue();
                String fixdate = node.getAttributes().item(0).getNodeValue();
                String opendate = node.getAttributes().item(2).getNodeValue();
                String summary = node.getFirstChild().getFirstChild().getTextContent();
                String description = node.getFirstChild().getFirstChild().getNextSibling().getTextContent();
                ArrayList<String> fixedFiles = new ArrayList<>();
                NodeList fixedFileLists = node.getFirstChild().getNextSibling().getChildNodes();
                for (int j = 0; j < fixedFileLists.getLength(); j++) {
                    fixedFiles.add(fixedFileLists.item(j).getTextContent());
                }
                reportList.put(id, opendate);
            }
            file = new File(targetPath + "\\" + "JSON-OPENDATE-New" + project+ "BugRepository.json");
            try (PrintWriter output = new PrintWriter(file)) {
                output.print(JSONObject.toJSONString(reportList));
            }

            //reporter
            reportList = new JSONObject();
            for (int i = 0; i < nodeList.getLength(); i++) {
                Node node = nodeList.item(i);
                String id = node.getAttributes().item(1).getNodeValue();
                String fixdate = node.getAttributes().item(0).getNodeValue();
                String opendate = node.getAttributes().item(2).getNodeValue();
                String summary = node.getFirstChild().getFirstChild().getTextContent();
                String description = node.getFirstChild().getFirstChild().getNextSibling().getTextContent();
                ArrayList<String> fixedFiles = new ArrayList<>();
                NodeList fixedFileLists = node.getFirstChild().getNextSibling().getChildNodes();
                for (int j = 0; j < fixedFileLists.getLength(); j++) {
                    fixedFiles.add(fixedFileLists.item(j).getTextContent());
                }
                String reporter = node.getFirstChild().getNextSibling().getNextSibling().getTextContent();
                reportList.put(id, reporter);
            }
            file = new File(targetPath + "\\" + "JSON-REPORTER-New" + project+ "BugRepository.json");
            try (PrintWriter output = new PrintWriter(file)) {
                output.print(JSONObject.toJSONString(reportList));
            }

            //sum&des
            reportList = new JSONObject();
            for (int i = 0; i < nodeList.getLength(); i++) {
                Node node = nodeList.item(i);
                String id = node.getAttributes().item(1).getNodeValue();
                String fixdate = node.getAttributes().item(0).getNodeValue();
                String opendate = node.getAttributes().item(2).getNodeValue();
                String summary = node.getFirstChild().getFirstChild().getTextContent();
                String description = node.getFirstChild().getFirstChild().getNextSibling().getTextContent();
                ArrayList<String> fixedFiles = new ArrayList<>();
                NodeList fixedFileLists = node.getFirstChild().getNextSibling().getChildNodes();
                for (int j = 0; j < fixedFileLists.getLength(); j++) {
                    fixedFiles.add(fixedFileLists.item(j).getTextContent());
                }
                String reporter = node.getFirstChild().getNextSibling().getNextSibling().getTextContent();
                reportList.put(id, summary);
                reportList.put(id, description);
            }
            file = new File(targetPath + "\\" + "JSON-SUMMARY&DESCRIPTION-New" + project+ "BugRepository.json");
            try (PrintWriter output = new PrintWriter(file)) {
                output.print(JSONObject.toJSONString(reportList));
            }

            //summary
            reportList = new JSONObject();
            for (int i = 0; i < nodeList.getLength(); i++) {
                Node node = nodeList.item(i);
                String id = node.getAttributes().item(1).getNodeValue();
                String fixdate = node.getAttributes().item(0).getNodeValue();
                String opendate = node.getAttributes().item(2).getNodeValue();
                String summary = node.getFirstChild().getFirstChild().getTextContent();
                String description = node.getFirstChild().getFirstChild().getNextSibling().getTextContent();
                ArrayList<String> fixedFiles = new ArrayList<>();
                NodeList fixedFileLists = node.getFirstChild().getNextSibling().getChildNodes();
                for (int j = 0; j < fixedFileLists.getLength(); j++) {
                    fixedFiles.add(fixedFileLists.item(j).getTextContent());
                }
                String reporter = node.getFirstChild().getNextSibling().getNextSibling().getTextContent();
                reportList.put(id, summary);
            }
            file = new File(targetPath + "\\" + "JSON-SUMMARY-New" + project+ "BugRepository.json");
            try (PrintWriter output = new PrintWriter(file)) {
                output.print(JSONObject.toJSONString(reportList));
            }

        } catch (ParserConfigurationException | IOException | SAXException e) {
            e.printStackTrace();
        }
        return reportList;
    }

    private JSONObject buildObject(String id, String summary, String description, ArrayList<String> fixedFiles, String reporter, String opendate, String fixdate) {
        JSONObject jsonObject = new JSONObject();
        jsonObject.put("id", id);
        jsonObject.put("summary", summary);
        jsonObject.put("description", description);
        jsonObject.put("fixedFiles", fixedFiles);
        jsonObject.put("reporter", reporter);
        jsonObject.put("opendate", opendate);
        jsonObject.put("fixdate", fixdate);
        return jsonObject;
    }
}

