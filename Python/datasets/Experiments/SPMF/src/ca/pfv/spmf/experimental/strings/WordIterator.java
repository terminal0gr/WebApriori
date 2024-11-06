package ca.pfv.spmf.experimental.strings;
public class WordIterator {
    private String str;

    public WordIterator(String str) {
        this.str = str;
    }

    public void iterateWords() {
        StringBuilder word = new StringBuilder();
        for (int i = 0; i < str.length(); i++) {
            char c = str.charAt(i);
            if (Character.isWhitespace(c)) {
                if (word.length() > 0) {
                    System.out.println(word.toString());
                    word.setLength(0);
                }
            } else {
                word.append(c);
            }
        }
        if (word.length() > 0) {
            System.out.println(word.toString());
        }
    }
    
    public void reverseIterateWords() {
        StringBuilder word = new StringBuilder();
        for (int i = str.length() - 1; i >= 0; i--) {
            char c = str.charAt(i);
            if (Character.isWhitespace(c)) {
                if (word.length() > 0) {
                    System.out.println(word.reverse().toString());
                    word.setLength(0);
                }
            } else {
                word.append(c);
            }
        }
        if (word.length() > 0) {
            System.out.println(word.reverse().toString());
        }
    }
    
    public static void main(String[] args) {
        String str = "This is a test string";
        WordIterator wordIterator = new WordIterator(str);
        wordIterator.iterateWords();
        wordIterator.reverseIterateWords();
    }
}