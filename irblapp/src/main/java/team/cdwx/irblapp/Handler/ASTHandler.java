package team.cdwx.irblapp.Handler;


import com.alibaba.fastjson.JSONObject;
import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.ImportDeclaration;
import com.github.javaparser.ast.PackageDeclaration;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.FieldDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.comments.BlockComment;
import com.github.javaparser.ast.comments.LineComment;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

/**
 * @author Daiqj
 */
public class ASTHandler {
    private static Map<String, String> methods;
    private static Map<String, String> attributes;
    private static Map<String, String> Classes;
    private static Map<String, String> LineComments;
    private static Map<String, String> BlockedComments;
    //private static Map<String,String>Comments;
    private static Map<String, String> all;
    private static Map<String, String> packages;
    private static String current_key;
    private static ArrayList<String> errs;
    private static final int numof = 0;
    private static ArrayList<String> name;
    private static ArrayList<String> without;
    private static Map<String, String> imports;

    public static void run(String pathOfProject, String pathOfResult) throws IOException {
        errs = new ArrayList();
        name = new ArrayList<>();
        without = new ArrayList<>();

        current_key = "";
        methods = new HashMap<>();
        attributes = new HashMap<>();
        Classes = new HashMap<>();
        LineComments = new HashMap<>();
        BlockedComments = new HashMap<>();
        all = new HashMap<>();
        packages = new HashMap<>();
        imports = new HashMap<>();
        ArrayList<String> arrs = new ArrayList<>();
        Map<String, String> map = new HashMap<>();
        recursion(pathOfProject, map, arrs);//传入路径
//        System.out.println(arrs);

        //toJson(map,"result");//调用转化为json的函数，传入map和json名字 默认当前路径
        for (String r : map.keySet()) {
            //System.out.println(map.get(r));
        }


        for (int i = 0; i < arrs.size(); i++) {
            // 选择文件
            FileInputStream in = new FileInputStream(arrs.get(i));
            //System.out.println(arrs.get(i));
            CompilationUnit cu = StaticJavaParser.parse(in);
            ///try {
            //    cu = StaticJavaParser.parse(in);
            //} catch (Exception e) {
            //    errs.add(arrs.get(i));
            //    packages.remove(arrs.get(i));
            //    continue;
            //}

            String s = arrs.get(i);
            String[] s1 = s.split("\\\\");
            String str = s.split("\\\\")[s.split("\\\\").length - 1];

            current_key = str;
            new importVisitor().visit(cu, null);
            new ClassOrInterfaceVisitor().visit(cu, null);
            new PackageVisitor().visit(cu, null);
            new FieldVisitor().visit(cu, null);
            new MethodVisitor().visit(cu, null);
            new BlockCommentVisitor().visit(cu, null);
            new LineCommentVisitor().visit(cu, null);
            new PackageVisitor().visit(cu, null);


        }
        toJson(imports, "import", pathOfResult);

        toJson(methods, "methods", pathOfResult);
        toJson(attributes, "attributes", pathOfResult);
        toJson(Classes, "classes", pathOfResult);
        gather(LineComments, BlockedComments);
        toJson(LineComments, "comments", pathOfResult);

        gather(all, methods);
        gather(all, attributes);
        gather(all, Classes);
        gather(all, LineComments);


        toJson(all, "allWords", pathOfResult);


        toJson(packages, "packages", pathOfResult);

    }

    public static void main(String[] args) throws IOException {
        String pathOfProject = "astData\\swt-3.1";
        String pathOfResult = "astData\\resultOfAST\\" + pathOfProject.substring(8);
        run(pathOfProject, pathOfResult);

    }

    //传入map和filename 存为json
    public static void toJson(Map<String, String> map, String filename, String pathOfResult) throws IOException {
        OutputStreamWriter osw = new OutputStreamWriter(new FileOutputStream(pathOfResult + "\\" + filename + ".json"), StandardCharsets.UTF_8);

        JSONObject jsonObject = new JSONObject();
        for (String key : map.keySet()) {
            //System.out.println(key);
            //System.out.println(key.split(".java")[0]);
            jsonObject.put(key.substring(0, key.length() - 5), map.get(key));
        }
        osw.write(jsonObject.toString());
        osw.flush();
        osw.close();

    }

    //判断是不是java文件
    public static boolean isJava(String filename) {
        int index = filename.lastIndexOf(".");
        String prefix = filename.substring(index + 1);
        return index > 0 && prefix.equals("java");
    }

    //递归所有文件及其子文件 如果是非文件夹就调用isjava判断是不是java 是java项目就调用getContents获取java内容
    public static void recursion(String root, Map<String, String> map, ArrayList<String> arrs) {
        File file = new File(root);
        File[] subFile = file.listFiles();

        for (int i = 0; i < subFile.length; i++) {
            if (subFile[i].isDirectory()) {
                recursion(subFile[i].getAbsolutePath(), map, arrs);
            } else {
                //System.out.println(subFile[i].getName());

                if (isJava(subFile[i].getName()) == true) {
                    String st = subFile[i].getAbsolutePath().split("\\\\")[(subFile[i].getAbsolutePath()).split("\\\\").length - 1];
                    /*
                    if(name.contains(st)){
                        System.out.println("error!!!!!");
                        System.out.println(subFile[i].getAbsolutePath());
                    }
                    else {
                        name.add(st);
                    }

                     */

                    methods.put(subFile[i].getAbsolutePath().split("\\\\")[(subFile[i].getAbsolutePath()).split("\\\\").length - 1], "");
                    attributes.put(subFile[i].getAbsolutePath().split("\\\\")[(subFile[i].getAbsolutePath()).split("\\\\").length - 1], "");
                    Classes.put(subFile[i].getAbsolutePath().split("\\\\")[(subFile[i].getAbsolutePath()).split("\\\\").length - 1], "");
                    LineComments.put(subFile[i].getAbsolutePath().split("\\\\")[(subFile[i].getAbsolutePath()).split("\\\\").length - 1], "");
                    BlockedComments.put(subFile[i].getAbsolutePath().split("\\\\")[(subFile[i].getAbsolutePath()).split("\\\\").length - 1], "");
                    all.put(subFile[i].getAbsolutePath().split("\\\\")[(subFile[i].getAbsolutePath()).split("\\\\").length - 1], "");
                    packages.put(subFile[i].getAbsolutePath().split("\\\\")[(subFile[i].getAbsolutePath()).split("\\\\").length - 1], "");
                    imports.put(subFile[i].getAbsolutePath().split("\\\\")[(subFile[i].getAbsolutePath()).split("\\\\").length - 1], "");
                    String filename = subFile[i].getName();
                    arrs.add(subFile[i].getAbsolutePath());
                    map.put(subFile[i].getAbsolutePath(), getContents(subFile[i]));
                }
            }
        }

    }

    //获取java内容
    public static String getContents(File file) {
        String encoding = "UTF-8";
        Long filelen = file.length();
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

    //第一个map放合并后的 第二个放被合并的
    private static void gather(Map<String, String> map, Map<String, String> replace) {
        for (String key : replace.keySet()) {
            if (!map.containsKey(key)) {
                map.put(key, replace.get(key));
            } else {
                map.replace(key, map.get(key) + " " + replace.get(key));
            }

        }
    }

    private static class importVisitor extends VoidVisitorAdapter {
        @Override
        public void visit(ImportDeclaration n, Object arg) {
            if (imports.get(current_key).equals("")) {

                imports.put(current_key, n.getName().toString());
            } else {
                imports.replace(current_key, imports.get(current_key) + " " + n.getNameAsString());
            }
        }

    }

    /**
     * 打印package相关内容
     */
    private static class PackageVisitor extends VoidVisitorAdapter {
        private String re;

        @Override
        public void visit(PackageDeclaration n, Object arg) {
            re = n.getNameAsString();
        }

        public String getS(CompilationUnit compilationUnit) {
            this.visit(compilationUnit, null);
            return this.re;
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
            if (packages.get(current_key).equals("")) {


                packages.put(current_key, n.getName().toString());
            } else {
                packages.replace(current_key, packages.get(current_key) + " " + n.getNameAsString());
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
            if (methods.get(current_key).equals("")) {

                methods.put(current_key, n.getName().toString());
            } else {
                methods.replace(current_key, methods.get(current_key) + " " + n.getNameAsString());
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
            for (int i = 0; i < n.getVariables().size(); i++) {
                if (n.getVariables().get(i).toString().split("=").length > 1) {
                    if (attributes.get(current_key).equals("")) {

                        attributes.put(current_key, n.getVariables().get(i).getName().toString());
                    } else {
                        attributes.replace(current_key, attributes.get(current_key) + " " + n.getVariables().get(i).getName().toString());
                    }
                    //n.getVariables().get(i).toString().split("=")[0];
                    //attributes.put(current_key,n.getVariables().get(i).toString().split("=")[0]);
                } else {
                    if (attributes.get(current_key).equals("")) {

                        attributes.put(current_key, n.getVariables().get(i).getName().toString());
                    } else {
                        attributes.replace(current_key, attributes.get(current_key) + " " + n.getVariables().get(i).getName().toString());
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
            if (Classes.get(current_key).equals("")) {

                Classes.put(current_key, n.getFullyQualifiedName().toString().split("\\[")[1].substring(0, n.getFullyQualifiedName().toString().split("\\[")[1].length() - 1));
            } else {
                Classes.replace(current_key, Classes.get(current_key) + " " + n.getFullyQualifiedName().toString().split("\\[")[1].substring(0, n.getFullyQualifiedName().toString().split("\\[")[1].length() - 1));
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
            if (BlockedComments.get(current_key).equals("")) {
                BlockedComments.put(current_key, n.toString());
            } else {
                BlockedComments.replace(current_key, BlockedComments.get(current_key) + " " + n.toString());
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
            if (LineComments.get(current_key).equals("")) {
                if (n.toString().split("/").length >= 2) {
                    LineComments.put(current_key, n.toString().split("/")[2]);
                } else {
                    LineComments.put(current_key, n.toString());
                }
            } else {
                if (n.toString().split("/").length >= 2) {
                    LineComments.replace(current_key, LineComments.get(current_key) + " " + n.toString().split("/")[2]);
                } else {
                    LineComments.replace(current_key, LineComments.get(current_key) + " " + n);

                }
            }
        }
    }

}
