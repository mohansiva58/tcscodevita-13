import java.util.*;
class Main{
  static class P{double x,y;P(double a,double b){x=a;y=b;}}
  static double area(List<P> p){
    double A=0;int n=p.size();
    for(int i=0;i<n;i++){
      P a=p.get(i),b=p.get((i+1)%n);
      A+=a.x*b.y-b.x*a.y;
    }
    return Math.abs(A)/2;
  }
  static List<P> shrink(List<P> p,double h){
    int n=p.size();List<P> r=new ArrayList<>();
    for(int i=0;i<n;i++){
      P a=p.get((i-1+n)%n),b=p.get(i),c=p.get((i+1)%n);
      double dx1=b.x-a.x,dy1=b.y-a.y,dx2=c.x-b.x,dy2=c.y-b.y;
      double l1=Math.hypot(dx1,dy1),l2=Math.hypot(dx2,dy2);
      dx1/=l1;dy1/=l1;dx2/=l2;dy2/=l2;
      double nx1=-dy1,ny1=dx1,nx2=-dy2,ny2=dx2;
      double A1=dy1,B1=-dx1,C1=A1*(b.x+nx1*h)+B1*(b.y+ny1*h);
      double A2=dy2,B2=-dx2,C2=A2*(b.x+nx2*h)+B2*(b.y+ny2*h);
      double D=A1*B2-A2*B1;if(Math.abs(D)<1e-9)return List.of();
      r.add(new P((C1*B2-C2*B1)/D,(A1*C2-A2*C1)/D));
    }
    return r;
  }
  public static void main(String[]a){
    Scanner s=new Scanner(System.in);
    int n=s.nextInt();List<P> p=new ArrayList<>();
    for(int i=0;i<n;i++)p.add(new P(s.nextDouble(),s.nextDouble()));
    double m=0;
    for(double h=0.1;h<=25;h+=0.1){
      var in=shrink(p,h);if(in.isEmpty())break;
      double A=area(in);if(A<1e-4)break;m=Math.max(m,A*h);
    }
    System.out.printf("%.2f",m);
  }
}
