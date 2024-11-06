package ca.pfv.spmf.experimental.strings;

import java.util.ArrayList;
import java.util.List;

public class StringSplit {
	
	////===============================================
	////    THIS CLASS IS ONLY FOR TESTING SOME CODE....
	////  ===============================================
	///

	/**
	 * Split a String quickly (based on StackOverflow)
	 * @param line
	 * @param delimiter
	 * @return
	 */
	public static String[] splitToStringArray(final String line, final char delimiter)
	{
	    CharSequence[] temp = new CharSequence[(line.length() / 2) + 1];
	    int wordCount = 0;
	    int i = 0;
	    int j = line.indexOf(delimiter, 0); // first substring

	    while (j >= 0)
	    {
	        temp[wordCount++] = line.substring(i, j);
	        i = j + 1;
	        j = line.indexOf(delimiter, i); // rest of substrings
	    }

	    temp[wordCount++] = line.substring(i); // last substring

	    String[] result = new String[wordCount];
	    System.arraycopy(temp, 0, result, 0, wordCount);

	    return result;
	}
	
	/** 
	 * Extract integers from a String  (based on stack overflow)
	 * @param input
	 * @return
	 */
	
	public static List<Integer> splitToIntegerList(String input)
	{
	    List<Integer> result = new ArrayList<Integer>();
	    int index = 0;
	    int v = 0;
	    int l = 0;
	    while (index < input.length())
	    {
	        char c = input.charAt(index);
	        if (Character.isDigit(c))
	        {
	            v *= 10;
	            v += c - '0';
	            l++;
	        } else if (l > 0)
	        {
	            result.add(v);
	            l = 0;
	            v = 0;
	        }
	        index++;
	    }
	    if (l > 0)
	    {
	        result.add(v);
	    }
	    return result;
	}
	
	private static List<String> splitToStringList(final String text, char delimiter) {

	    final List<String> result = new ArrayList<String>();

	    final int len = text.length();
	    int tokenStart = 0;
	    boolean prevCharIsSeparator = true;  // "preceding char is separator" flag

	    char[] chars = text.toCharArray();

	    for (int pos = 0; pos < len; ++pos) {
	        if (chars[pos] == delimiter) {
	            if (!prevCharIsSeparator) {
	                result.add(text.substring(tokenStart, pos));
	                prevCharIsSeparator = true;
	            }
	            tokenStart = pos + 1;
	        } else {
	            prevCharIsSeparator = false;
	        }
	    }

	    if (tokenStart < len) {
	        result.add(text.substring(tokenStart));
	    }

	    return result;
	}
	
    public static List<String> fasterSplit(String text, char delimiter) {
    	List<String> stringSplit = new ArrayList<>();
        int pos = 0, end;
        while ((end = text.indexOf(delimiter, pos)) >= 0) {
            stringSplit.add(text.substring(pos, end));
            pos = end + 1;
        }
        //Add last token of string
        stringSplit.add(text.substring(pos));
        return stringSplit;
    }
	
	
	public static void main(String[] args) {
		///////////////////////////////////////////////////////////////////
		System.out.println(" METHOD 1 :  splitToStringArray()");
		long start = System.currentTimeMillis();
		for(int i=0; i< 50000000; i++) {
			splitToStringArray("10 20 30 10 100 6 7 6 5 3 4 5 3 4", ' ');
		}
		long end = System.currentTimeMillis();
		System.out.println(end - start);
		///////////////////////////////////////////////////////////////////
		System.out.println(" METHOD 2 : Java String.split()");
		long start2 = System.currentTimeMillis();
		for(int i=0; i< 50000000; i++) {
			"10 20 30 10 100 6 7 6 5 3 4 5 3 4".split(" ");
		}
		long end2 = System.currentTimeMillis();
		System.out.println(end2 - start2);
		///////////////////////////////////////////////////////////////////
		System.out.println(" METHOD 3 :  splitToIntegerList()");
		long start3 = System.currentTimeMillis();
		for(int i=0; i< 50000000; i++) {
			splitToIntegerList("10 20 30 10 100 6 7 6 5 3 4 5 3 4");
		}
		long end3 = System.currentTimeMillis();
		System.out.println(end3 - start3);
		
		///////////////////////////////////////////////////////////////////
		System.out.println(" METHOD 4:  splitToStringList()");
		long start4 = System.currentTimeMillis();
		for(int i=0; i< 50000000; i++) {
			splitToStringList("10 20 30 10 100 6 7 6 5 3 4 5 3 4", ' ');
		}
		long end4 = System.currentTimeMillis();
		System.out.println(end4 - start4);
		
		///////////////////////////////////////////////////////////////////
		System.out.println(" METHOD 5:  fasterSplit()");
		long start5 = System.currentTimeMillis();
		for(int i=0; i< 50000000; i++) {
			fasterSplit("10 20 30 10 100 6 7 6 5 3 4 5 3 4", ' ');
		}
		long end5 = System.currentTimeMillis();
		System.out.println(end5 - start5);
	}
}
