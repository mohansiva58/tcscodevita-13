import java.util.*;
import java.awt.geom.Point2D;

public class PickSmartPlayWise {
    static final double EPS = 1e-9;

    static class P {
        double x, y;
        P(double x, double y){this.x=x;this.y=y;}
        double d(P o){return Point2D.distance(x,y,o.x,o.y);}
        public boolean equals(Object o){if(!(o instanceof P))return false;P p=(P)o;return Math.abs(x-p.x)<EPS&&Math.abs(y-p.y)<EPS;}
        public int hashCode(){return Objects.hash(Math.round(x*100),Math.round(y*100));}
    }

    static class Stick {
        P a,b;int id;double len;
        Stick(double x1,double y1,double x2,double y2,int id){a=new P(x1,y1);b=new P(x2,y2);this.id=id;len=a.d(b);}
    }

    static class Seg {
        P u,v;Stick s;double len;
        Seg(P u,P v,Stick s){this.u=u;this.v=v;this.s=s;len=u.d(v);}
        public boolean equals(Object o){if(!(o instanceof Seg))return false;Seg t=(Seg)o;return (u.equals(t.u)&&v.equals(t.v))||(u.equals(t.v)&&v.equals(t.u));}
        public int hashCode(){return Objects.hash(u.hashCode()+v.hashCode());}
    }

    static boolean onSeg(P p,P a,P b){
        double c=(p.y-a.y)*(b.x-a.x)-(p.x-a.x)*(b.y-a.y);
        if(Math.abs(c)>EPS)return false;
        return p.x>=Math.min(a.x,b.x)-EPS&&p.x<=Math.max(a.x,b.x)+EPS&&p.y>=Math.min(a.y,b.y)-EPS&&p.y<=Math.max(a.y,b.y)+EPS;
    }

    static P inter(Stick s1,Stick s2){
        double x1=s1.a.x,y1=s1.a.y,x2=s1.b.x,y2=s1.b.y,x3=s2.a.x,y3=s2.a.y,x4=s2.b.x,y4=s2.b.y;
        double d=(x1-x2)*(y3-y4)-(y1-y2)*(x3-x4); if(Math.abs(d)<EPS)return null;
        double px=((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4))/d;
        double py=((x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4))/d;
        P p=new P(Math.round(px*100)/100.0,Math.round(py*100)/100.0);
        return onSeg(p,s1.a,s1.b)&&onSeg(p,s2.a,s2.b)?p:null;
    }

    static double area(List<P> poly){
        double a=0;int n=poly.size();
        for(int i=0;i<n;i++){P p1=poly.get(i),p2=poly.get((i+1)%n);a+=p1.x*p2.y-p2.x*p1.y;}
        return Math.abs(a)/2;
    }

    static List<P> dfs(Map<P,List<Seg>> g,P st,P c,P p,Set<P> vis,List<P> path){
        vis.add(c);path.add(c);
        for(Seg e:g.getOrDefault(c,List.of())){
            P n=e.u.equals(c)?e.v:e.u;
            if(n.equals(st)&&path.size()>2)return new ArrayList<>(path);
            if(!n.equals(p)&&!vis.contains(n)){
                var r=dfs(g,st,n,c,vis,path);
                if(r!=null)return r;
            }
        }
        path.remove(path.size()-1);vis.remove(c);
        return null;
    }

    public static void main(String[] args){
        Scanner sc=new Scanner(System.in);
        int n=sc.nextInt();
        List<Stick> S=new ArrayList<>();
        for(int i=0;i<n;i++)S.add(new Stick(sc.nextDouble(),sc.nextDouble(),sc.nextDouble(),sc.nextDouble(),i));
        Set<P> V=new HashSet<>();Map<Integer,Set<P>> map=new HashMap<>();
        for(Stick s:S){V.add(s.a);V.add(s.b);map.put(s.id,new HashSet<>(List.of(s.a,s.b)));}
        for(int i=0;i<n;i++)for(int j=i+1;j<n;j++){
            P p=inter(S.get(i),S.get(j));
            if(p!=null){V.add(p);map.get(S.get(i).id).add(p);map.get(S.get(j).id).add(p);}
        }

        Map<P,List<Seg>> G=new HashMap<>();Set<Seg> all=new HashSet<>();
        for(Stick s:S){
            List<P> pts=new ArrayList<>(map.get(s.id));
            pts.removeIf(p->!onSeg(p,s.a,s.b));
            pts.sort(Comparator.comparingDouble(p->p.d(s.a)));
            for(int i=0;i<pts.size()-1;i++){
                P u=pts.get(i),v=pts.get(i+1);
                if(u.d(v)>EPS){Seg seg=new Seg(u,v,s);all.add(seg);
                    G.computeIfAbsent(u,k->new ArrayList<>()).add(seg);
                    G.computeIfAbsent(v,k->new ArrayList<>()).add(seg);}
            }
        }

        List<P> cyc=null;
        for(P p:G.keySet()){cyc=dfs(G,p,p,null,new HashSet<>(),new ArrayList<>());if(cyc!=null)break;}
        if(cyc==null){System.out.println("Abandoned");return;}
        double a1=area(cyc);

        Set<Seg> used=new HashSet<>();
        for(int i=0;i<cyc.size();i++){
            Seg t=new Seg(cyc.get(i),cyc.get((i+1)%cyc.size()),null);
            for(Seg s:all)if(s.equals(t)){used.add(s);break;}
        }
        Map<Integer,Double> usedLen=new HashMap<>();
        for(Seg s:used)usedLen.put(s.s.id,usedLen.getOrDefault(s.s.id,0.0)+s.len);
        double rem=0;
        for(Stick s:S)rem+=s.len-usedLen.getOrDefault(s.id,0.0);
        double a2=rem*rem/(4*Math.PI);
        System.out.println(a1>a2?"Kalyan":"Computer");
    }
}
