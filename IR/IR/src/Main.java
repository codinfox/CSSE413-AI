import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;


public class Main {

	private static final int N = 1;
	private Scanner s;
	//Tokens for the passage
	private ArrayList<String> p = new ArrayList<String>();
	
	//Tokens for the question
	private ArrayList<String> q = new ArrayList<String>();
	
	
	private double[][] score;
	public void start() {
		try {
			s = new Scanner(new File("res/processed/AbrahamLincoln.txt"));
		} catch (FileNotFoundException e) {	e.printStackTrace(); }
		
		q.add("lincoln");
		while(s.hasNext()) {
			p.add(s.next());
		}
		score = new double[q.size()][p.size()];
		for(int i = 0; i < q.size(); i++) {
			for(int j = 0; j < p.size(); j++) {
				score[i][j] = 0;
			}
		}
		
		for(int i = 0; i < q.size(); i++) {
			for(int j = 0; j < p.size(); j++) {
				score[i][j] = findTheMax(i, j);
				System.out.println(score[i][j]);
			}
		}
	}
	
	//will break when i = 0 || j = 0
	public double findTheMax(int i, int j) {
		double s1 = 0;
		if(i != 0 && j != 0)
			s1 = score[i-1][j-1] + sim(p.get(j), q.get(i));
		
		double s2 = 0;
		if(i != 0)
			s2 = score[i-1][j] + sim(p.get(j), "lincoln");
		
		double s3 = 0;
		if(j != 0)
			s3 = score[i][j-1] + sim("lincoln", q.get(i));
		
		double s4 = 0;
		return Math.max(Math.max(s1, s2), Math.max(s3, s4));
	}
	
	private double sim(String t1, String t2) {
		if(t1.equals(t2))
			return idf(t1);
		if(t2.equals("lincoln"))
			return -idf(t1);
		if(t1.equals("lincoln"))
			return -idf(t2);
		
		return -idf(t1);
		//return Math.log(40);
	}
	private double idf(String t) {
		double a = Math.log(N/(count(t) + 1));
		return a;
	}
	
	private int count(String token) {
		int sum = 0;
		for(int i = 0; i < p.size(); i++) {
			if(p.get(i).equals(token))
				sum++;
		}
		return sum;
	}
	
	
	public static void main(String[] args) {
		Main m = new Main();
		m.start();
	}
	
}
