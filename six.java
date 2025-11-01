import java.util.*;

public class SolveTheExpression {
    static class T { String v; boolean num; T(String v, boolean n){this.v=v;this.num=n;} }

    static String seg(List<String> a,int s){StringBuilder b=new StringBuilder();for(String r:a)b.append(r.substring(s,s+3).replaceAll("[_|]","1").replaceAll(" ","0"));return b.toString();}

    static long val(String op,String a,String b){
        int n=Math.max(a.length(),b.length());
        a=String.format("%"+n+"s",a).replace(' ','0');
        b=String.format("%"+n+"s",b).replace(' ','0');
        StringBuilder r=new StringBuilder();
        for(int i=0;i<n;i++)r.append(op.equals("|")?(a.charAt(i)=='1'||b.charAt(i)=='1'?'1':'0'):(a.charAt(i)=='1'&&b.charAt(i)=='1'?'1':'0'));
        return Long.parseLong(r.toString(),2);
    }

    static String not(String a){StringBuilder r=new StringBuilder();for(char c:a.toCharArray())r.append(c=='1'?'0':'1');return r.toString();}

    static int p(String o){return switch(o){case "!"->3;case "|","&"->2;default->0;};}

    static String eval(List<T> t){
        Stack<String> v=new Stack<>(),o=new Stack<>();
        for(T x:t){
            if(x.num)v.push(x.v);
            else if(x.v.equals("("))o.push("(");
            else if(x.v.equals(")")){while(!o.peek().equals("("))v.push(op(v,o.pop()));o.pop();}
            else{while(!o.isEmpty()&&p(o.peek())>=p(x.v))v.push(op(v,o.pop()));o.push(x.v);}
        }
        while(!o.isEmpty())v.push(op(v,o.pop()));
        return v.pop();
    }

    static String op(Stack<String> v,String o){
        if(o.equals("!"))return not(v.pop());
        String b=v.pop(),a=v.pop();
        return Long.toBinaryString(val(o,a,b));
    }

    public static void main(String[] z){
        Scanner sc=new Scanner(System.in);
        List<String> in=new ArrayList<>();
        while(sc.hasNextLine()){String s=sc.nextLine();if(s.isEmpty())break;in.add(s);}
        Map<String,String> m=new HashMap<>();
        for(int i=0;i<10;i++)m.put(seg(in.subList(0,3),i*4),""+i);
        String[] op={"|","&","!","(",")"};
        for(int i=0;i<5;i++)m.put(seg(in.subList(3,6),i*4),op[i]);
        List<String> e=in.subList(6,9);List<T> tok=new ArrayList<>();
        for(int i=0;i<e.get(0).length();i+=4){
            String s=seg(e,i),t=m.get(s);
            if(t==null)continue;
            if(t.matches("\\d"))tok.add(new T(Long.toBinaryString(Long.parseLong(t)),true));
            else tok.add(new T(t,false));
        }
        System.out.println(Long.parseLong(eval(tok),2));
    }
}
