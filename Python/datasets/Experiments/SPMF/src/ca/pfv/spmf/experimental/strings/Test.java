package ca.pfv.spmf.experimental.strings;

public class Test {

	public static void main(String[] args) {
		System.out.println(splitString("hello this is a word", ' '));
		
		
		System.out.println("=============");


		String input = "This is a string";
		// Iterate through the string
		StringBuilder output = new StringBuilder();
		int startIndex  = 0;
		final int length = input.length();
		for (int i = 0; i < length; i++) {
		    // If the current character is a space
		    if (input.charAt(i) == ' ') {
		        // Append the current word to the output
		        output.append(input.substring(startIndex, i));
		        // Reset the starting index of the current word
		        startIndex = i + 1;
		    }
		    // If the end of the string is reached
		    else if (i == input.length() - 1) {
		        // Append the last word to the output
		        output.append(input.substring(startIndex));
		    }
		}

		// Print the output
		System.out.println(output.toString());
	}
	
	public static String splitString(String str, char separator ) {
	    StringBuilder sb = new StringBuilder();
	    for (int i = 0; i < str.length(); i++) {
	        char ch = str.charAt(i);
	        if (ch == separator) {
	            System.out.println(sb.toString());
	            sb.setLength(0);
	        } else {
	            sb.append(ch);
	        }
	    }
	    return sb.toString();
	}

}
