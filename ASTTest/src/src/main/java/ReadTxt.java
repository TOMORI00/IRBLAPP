package src.main.java;

import com.alibaba.fastjson.JSONObject;

import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class ReadTxt {

    private static Map<String,String> map;

    public static void ReadDataFromTxt(String path) {


        System.out.println(path);
        map = new HashMap<>();
        File file = new File(path);
        File[] subFile = file.listFiles();
        for (int i = 0; i < subFile.length; i++) {
            String s = "";
            try {
                FileReader fr = new FileReader(subFile[i].getAbsoluteFile());
                BufferedReader bf = new BufferedReader(fr);

                String str;
                while ((str = bf.readLine()) != null) {
                    s = s + str;
                }
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
            map.put(subFile[i].getName().substring(0,(subFile[i].getName().length()-4)), s);

        }

    }

    public static void toJson( Map<String,String>map,String filename) throws IOException {
        OutputStreamWriter osw = new OutputStreamWriter(new FileOutputStream(filename+".json"),"UTF-8");

        JSONObject jsonObject=new JSONObject();
        for(String key:map.keySet()){
            //System.out.println(key);
            //System.out.println(key.split(".java")[0]);
            jsonObject.put(key.split(".java")[0],map.get(key));
        }
        osw.write(jsonObject.toString());
        osw.flush();
        osw.close();

    }

    public static void main(String[]args) throws IOException {
        ReadDataFromTxt("class_preprocessed");
        toJson(map,"class_pre");
        ReadDataFromTxt("report_preprocessed");
        toJson(map,"report_pre");
    }
}





