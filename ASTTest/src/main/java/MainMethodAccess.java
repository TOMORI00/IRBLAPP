import com.alibaba.fastjson.JSONObject;
import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.PackageDeclaration;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.FieldDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.comments.BlockComment;
import com.github.javaparser.ast.comments.LineComment;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class MainMethodAccess {


    private static Map<String,String>methods;
    private static Map<String,String>attributes;
    private static Map<String,String>Classes;
    private static Map<String,String>LineComments;
    private static Map<String,String>BlockedComments;
    private static Map<String,String>Comments;
    private static Map<String,String> all;
    private static Map<String,String> packages;
    private static String current_key;
    private static ArrayList<String> errs;
    private static int numof=0;
    private static ArrayList<String> name;
    private static ArrayList<String> without;

    public static void main(String[] args) throws IOException {

        errs = new ArrayList();
        name = new ArrayList<>();
        without = new ArrayList<>();

        current_key = new String();
        methods = new HashMap<>();
        attributes = new HashMap<>();
        Classes = new HashMap<>();
        LineComments = new HashMap<>();
        BlockedComments = new HashMap<>();
        all = new HashMap<>();
        packages = new HashMap<>();
        ArrayList<String> arrs = new ArrayList<>();
        Map<String, String> map = new HashMap<>();
        recursion("aspectj_new", map, arrs);//传入路径
        //System.out.println(arrs);

        //System.out.println(arrs);
        //toJson(map,"result");//调用转化为json的函数，传入map和json名字 默认当前路径
        for (String r : map.keySet()) {
            //System.out.println(map.get(r));
        }


        for (int i = 0; i < arrs.size(); i++) {
            // 选择文件
            FileInputStream in = new FileInputStream(arrs.get(i));
            //if(arrs.get(i).equals("C:\\Users\\11159\\Desktop\\astproject\\eclipse-3.1\\plugins\\org.eclipse.core.resources\\src\\org\\eclipse\\core\\resources\\ISaveParticipant.java")
            //        ||arrs.get(i).equals("C:\\Users\\11159\\Desktop\\astproject\\eclipse-3.1\\plugins\\org.eclipse.pde.ui\\templates\\preferences\\java\\$pageClassName$.java")
            //        ||arrs.get(i).equals("C:\\Users\\11159\\Desktop\\astproject\\eclipse-3.1\\plugins\\org.eclipse.pde.ui\\templates\\view\\java\\$className$.java")
            //){
            //     continue;
            //}

            // 创建parser
            /*

            if(arrs.get(i).split("\\\\")[(arrs.get(i)).split("\\\\").length-1].equals("$packageName$.ApplicationActionBarAdvisor.java")){
                System.out.println("11111111");
            }
            else{
                if(arrs.get(i).split("\\\\")[(arrs.get(i)).split("\\\\").length-1].startsWith("$") || arrs.get(i).equals("C:\\Users\\11159\\Desktop\\astproject\\eclipse-3.1\\plugins\\org.eclipse.core.resources\\src\\org\\eclipse\\core\\resources\\ISaveParticipant.java")){
                    continue;
                }
            }

             */


            CompilationUnit cu = null;
            try {
                cu = StaticJavaParser.parse(in);
            } catch (Exception e) {

                /*
                System.out.println(arrs.get(i));
                FileInputStream inof1 = new FileInputStream(arrs.get(i));
                String r="aspect";
                BufferedReader bufferedReader=new BufferedReader(new InputStreamReader((inof1)));
                File file=new File(arrs.get(i));
                File tmpfile = new File(file.getAbsolutePath()+".tmp");
                BufferedWriter writer=new BufferedWriter(new FileWriter(tmpfile));
                boolean flag=false;
                String strof;
                while(true){
                    strof=bufferedReader.readLine();
                    if(strof==null)
                        break;
                    if(strof.contains(r)){
                        String[] strofs=strof.split(r);
                        System.out.println(strof);
                        if(strofs.length==1){
                            strof="class"+strofs[0];
                            flag=true;
                        }
                        else{
                            if(strofs[0].substring(0,3).equals("imp")){

                            }
                            else {
                                strof = strofs[0] + "class" + strofs[1];
                                flag = true;
                            }
                        }

                    }
                    writer.write(strof);
                }
                if(flag==false){
                    tmpfile.delete();
                }
                else {
                    file.delete();
                    tmpfile.renameTo(new File(file.getAbsolutePath()));
                    in=new FileInputStream(arrs.get(i));
                    try {
                        cu = StaticJavaParser.parse(in);
                    } catch (Exception exception) {
                        errs.add(arrs.get(i));
                        continue;
                    }
                }
                //System.out.println(arrs.get(i));
                //e.printStackTrace();

                 */
                errs.add(arrs.get(i));
                packages.remove(arrs.get(i));
                continue;
            }
            //System.out.println(errs);
            //System.out.println();
            ;
            String s = arrs.get(i);
            String[] s1 = s.split("\\\\");
            String str = s.split("\\\\")[s.split("\\\\").length - 1];
            //System.out.println(str+"\n");
            // 打印所需内容
            current_key = str;

            //new MethodVisitor().visit(cu, null);
            //System.out.println();
            //new FieldVisitor().visit(cu, null);
            //System.out.println();
            //new ClassOrInterfaceVisitor().visit(cu, null);
            //System.out.println();
            //new BlockCommentVisitor().visit(cu, null);
            //new LineCommentVisitor().visit(cu, null);


            new PackagrVisitor().visit(cu, null);
        }
        /*
        int k=errs.size();
        k+=1;


         */
/*
        System.out.println(methods);
        System.out.println(attributes);
        System.out.println(Classes);


 */

        //toJson(methods,"methods");
        //toJson(attributes,"attributes");
        //toJson(Classes,"classes");
        //toJson(LineComments,"LineComments");
        //toJson(BlockedComments,"BlockComments");
        //gather(LineComments,BlockedComments);
        //toJson(LineComments,"comments");

        for (String key : packages.keySet()) {
            if (packages.get(key).equals("")) {
                without.add(key);
            }
        }
        System.out.println("w");
        System.out.println(without);
        System.out.println("ithout");
        System.out.println(packages);

        for (int i = 0; i < arrs.size(); i++) {
            String str = arrs.get(i).split("\\\\")[(arrs.get(i)).split("\\\\").length - 1];
            if (without.contains(str)) {
                String path = arrs.get(i);
                File file = new File(path);
                String pathOfParent = file.getParentFile().getAbsolutePath();
                File parentFile = new File(pathOfParent);
                File[] files_equalDire = parentFile.listFiles();
                ArrayList<String> val = new ArrayList<>();
                boolean flag_of_is_all_empty = false;
                for (int j = 0; j < files_equalDire.length; j++) {
                    String files_equ_j = files_equalDire[j].getName();
                    int files_equ_j_len = files_equ_j.length();
                    if (files_equalDire[j].equals(str)) {
                        continue;
                    }
                    if (files_equalDire[j].getName().length() > 5) {
                        if (files_equalDire[j].getName().substring(files_equ_j_len - 5, files_equ_j_len).equals(".java")) {
                            String val_of_other = files_equalDire[j].getName().substring(0, files_equ_j_len - 5);
                            System.out.println(val_of_other);
                            if (packages.get(val_of_other) != null) {

                                System.out.println(packages.get(val_of_other));
                                if (packages.get(val_of_other).indexOf(" ") == -1) {
                                    flag_of_is_all_empty = true;
                                    if (val.contains(packages.get(val_of_other)) == false) {
                                        val.add(packages.get(val_of_other));
                                    }
                                }
                                /*else {
                                    FileInputStream inf=new FileInputStream(files_equalDire[j].getAbsolutePath());;
                                    CompilationUnit cum;
                                    String strofmult;
                                    try {
                                        cum = StaticJavaParser.parse(inf);
                                        strofmult = new PackageVisitor().getS(cum);
                                    } catch (Exception e) {
                                        //e.printStackTrace();
                                        if(val.size()==0){
                                            flag_of_is_all_empty=false;
                                        }
                                        continue;
                                    }
                                    if (val.contains(strofmult) == false) {
                                        val.add(packages.get(val_of_other));
                                    }
                                }

                                 */
                            }

                        }
                    }
                }
                if (flag_of_is_all_empty == false) {
                    packages.put(str,pathOfParent);
                    System.out.println(pathOfParent);
                }
                else {
                    String res_val="";
                    for (String KEY:val){
                        if (res_val.equals("")){
                            res_val+=KEY;
                        }
                        else res_val=res_val+" "+KEY;
                    }
                    packages.put(str,res_val);
                }
            }
        }


            //合并
        /*
        gather(all,methods);
        gather(all,attributes);
        gather(all,Classes);
        gather(all,LineComments);

        //gather(all,BlockedComments);
        toJson(all,"allWords");
        //toJson();

         */
        /*
        System.out.println(methods.size());
        System.out.println(errs.size());
         */

        toJson(packages, "packages");
    }

    /**
     * 打印package相关内容
     */
    private static class PackageVisitor extends VoidVisitorAdapter {
        private String re;
        @Override
        public void visit(PackageDeclaration n, Object arg) {
            re=n.getNameAsString();
        }
        public String getS(CompilationUnit compilationUnit){
            this.visit(compilationUnit,null);
            return this.re;
        }
    }
    //传入map和filename 存为json
    public static void toJson( Map<String,String>map,String filename) throws IOException {
        OutputStreamWriter osw = new OutputStreamWriter(new FileOutputStream(filename+".json"),"UTF-8");

        JSONObject jsonObject=new JSONObject();
        for(String key:map.keySet()){
            //System.out.println(key);
            //System.out.println(key.split(".java")[0]);
            jsonObject.put(key.substring(0,key.length()-5),map.get(key));
        }
        osw.write(jsonObject.toString());
        osw.flush();
        osw.close();

    }
    //判断是不是java文件
    public static boolean isJava(String filename){
        int index=filename.lastIndexOf(".");
        String prefix=filename.substring(index+1,filename.length());
        if(index>0 && prefix.equals("java")){
            return true;
        }
        else return false;
    }
    //递归所有文件及其子文件 如果是非文件夹就调用isjava判断是不是java 是java项目就调用getContents获取java内容
    public static void recursion(String root, Map<String,String>map,ArrayList<String> arrs) {
        File file = new File(root);
        File[] subFile = file.listFiles();

        for (int i = 0; i < subFile.length; i++) {
            if (subFile[i].isDirectory()) {
                recursion(subFile[i].getAbsolutePath(), map,arrs);
            } else {
                //System.out.println(subFile[i].getName());

                if(isJava(subFile[i].getName())==true) {
                    String st=subFile[i].getAbsolutePath().split("\\\\")[(subFile[i].getAbsolutePath()).split("\\\\").length-1];
                    /*
                    if(name.contains(st)){
                        System.out.println("error!!!!!");
                        System.out.println(subFile[i].getAbsolutePath());
                    }
                    else {
                        name.add(st);
                    }

                     */

                    methods.put(subFile[i].getAbsolutePath().split("\\\\")[(subFile[i].getAbsolutePath()).split("\\\\").length-1],"");
                    attributes.put(subFile[i].getAbsolutePath().split("\\\\")[(subFile[i].getAbsolutePath()).split("\\\\").length-1],"");
                    Classes.put(subFile[i].getAbsolutePath().split("\\\\")[(subFile[i].getAbsolutePath()).split("\\\\").length-1],"");
                    LineComments.put(subFile[i].getAbsolutePath().split("\\\\")[(subFile[i].getAbsolutePath()).split("\\\\").length-1],"");
                    BlockedComments.put(subFile[i].getAbsolutePath().split("\\\\")[(subFile[i].getAbsolutePath()).split("\\\\").length-1],"");
                    all.put(subFile[i].getAbsolutePath().split("\\\\")[(subFile[i].getAbsolutePath()).split("\\\\").length-1],"");
                    packages.put(subFile[i].getAbsolutePath().split("\\\\")[(subFile[i].getAbsolutePath()).split("\\\\").length-1],"");
                    String filename = subFile[i].getName();
                    arrs.add(subFile[i].getAbsolutePath());
                    map.put(subFile[i].getAbsolutePath().toString(),getContents(subFile[i]));
                }
            }
        }

    }
    //获取java内容
    public static String getContents(File file){
        String encoding="UTF-8";
        Long filelen=file.length();
        byte[] filecontent = new byte[filelen.intValue()];
        try {
            FileInputStream in = new FileInputStream(file);
            in.read(filecontent);
            in.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        try {
            return new String(filecontent, encoding);
        } catch (UnsupportedEncodingException e) {
            System.err.println("The OS does not support " + encoding);
            e.printStackTrace();
            return null;
        }

    }
    /**
     * 打印package相关内容
     */
    private static class PackagrVisitor extends VoidVisitorAdapter {
        @Override
        public void visit(PackageDeclaration n, Object arg) {
            // 这里有很多方法以get开头的，选取最合适的信息
            //System.out.println(n.getName());
            if(packages.get(current_key).equals("")) {


                packages.put(current_key, n.getName().toString());
            }
            else{
                packages.replace(current_key,packages.get(current_key)+" "+n.getNameAsString());
            }
            //System.out.println(n.getBody());
            //System.out.println(n.getParameters());
            //System.out.println(n.getDeclarationAsString());
        }
    }

    /**
     * 打印方法相关内容
     */
    private static class MethodVisitor extends VoidVisitorAdapter {
        @Override
        public void visit(MethodDeclaration n, Object arg) {
            // 这里有很多方法以get开头的，选取最合适的信息
            //System.out.println(n.getName());
            if(methods.get(current_key).equals("")) {

                methods.put(current_key, n.getName().toString());
            }
            else{
                methods.replace(current_key,methods.get(current_key)+" "+n.getNameAsString());
            }
            //System.out.println(n.getBody());
            //System.out.println(n.getParameters());
            //System.out.println(n.getDeclarationAsString());
        }
    }

    /**
     * 打印属性相关内容
     */
    private static class FieldVisitor extends VoidVisitorAdapter {
        @Override
        public void visit(FieldDeclaration n, Object arg) {
            //打印了所有的变量，注意格式，把具体的值删除
            for(int i=0;i<n.getVariables().size();i++){
                if(n.getVariables().get(i).toString().split("=").length>1){
                    if(attributes.get(current_key).equals("")) {

                        attributes.put(current_key, n.getVariables().get(i).getName().toString());
                    }
                    else{
                        attributes.replace(current_key,attributes.get(current_key)+" "+n.getVariables().get(i).getName().toString());
                    }
                    //n.getVariables().get(i).toString().split("=")[0];
                    //attributes.put(current_key,n.getVariables().get(i).toString().split("=")[0]);
                }
                else{
                    if(attributes.get(current_key).equals("")) {

                        attributes.put(current_key, n.getVariables().get(i).getName().toString());
                    }
                    else{
                        attributes.replace(current_key,attributes.get(current_key)+" "+n.getVariables().get(i).getName().toString());
                    }
                }
            }

            //System.out.println(n.getVariables());
        }
    }

    /**
     * 打印类和接口相关信息
     */
    private static class ClassOrInterfaceVisitor extends VoidVisitorAdapter {
        @Override
        public void visit(ClassOrInterfaceDeclaration n, Object arg) {
            //这里也有很多方法，选取最合适的
            //System.out.println(n.getFullyQualifiedName().toString());
            if(Classes.get(current_key).equals("")) {

                Classes.put(current_key, n.getFullyQualifiedName().toString().split("\\[")[1].substring(0,n.getFullyQualifiedName().toString().split("\\[")[1].length()-1));
            }
            else{
                Classes.replace(current_key,Classes.get(current_key)+" "+n.getFullyQualifiedName().toString().split("\\[")[1].substring(0,n.getFullyQualifiedName().toString().split("\\[")[1].length()-1));
            }
            //System.out.println(n.getImplementedTypes());
            //System.out.println(n.getTypeParameters());
        }
    }
    /**
     * 打印类和接口相关信息
     */
    private static class BlockCommentVisitor extends VoidVisitorAdapter {
        @Override
        public void visit(BlockComment n, Object arg) {

            //System.out.println(n.toString());
            if(BlockedComments.get(current_key).equals("")) {
                BlockedComments.put(current_key,n.toString());
            }
            else {
                BlockedComments.replace(current_key,BlockedComments.get(current_key)+" "+n.toString());
            }
            }

        }


    /**
     * 打印类和接口相关信息
     */
    private static class LineCommentVisitor extends VoidVisitorAdapter {
        @Override
        public void visit(LineComment n, Object arg) {
            //System.out.println(n.toString());
            if(LineComments.get(current_key).equals("")) {
                if (n.toString().split("/").length >= 2) {
                    LineComments.put(current_key, n.toString().split("/")[2]);
                } else {
                    LineComments.put(current_key, n.toString());
                }
            }
            else{
                if (n.toString().split("/").length >= 2) {
                    LineComments.replace(current_key, LineComments.get(current_key) + " " + n.toString().split("/")[2]);
                }
                else{
                    LineComments.replace(current_key, LineComments.get(current_key) + " " + n.toString());

                }
            }
        }
    }


    //第一个map放合并后的 第二个放被合并的
    private static void gather(Map<String,String> map,Map<String,String> replace){
        for(String key :replace.keySet()){
            if(!map.containsKey(key)){
                map.put(key,replace.get(key));
            }
            else{
                map.replace(key,map.get(key)+" "+replace.get(key));
            }

        }
    }




}