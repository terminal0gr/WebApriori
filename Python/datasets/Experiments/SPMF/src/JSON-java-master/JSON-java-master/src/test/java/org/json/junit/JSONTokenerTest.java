package org.json.junit;

/*
Public Domain.
*/

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;
import java.io.StringReader;

import org.json.*;
import org.junit.Test;

/**
 * Test specific to the {@link org.json.JSONTokener} class.
 * @author John Aylward
 *
 */
public class JSONTokenerTest {

    /**
     * verify that back() fails as expected.
     * @throws IOException thrown if something unexpected happens.
     */
    @Test
    public void verifyBackFailureZeroIndex() throws IOException {
        Reader reader = new StringReader("some test string"); 
        try {
            final JSONTokener tokener = new JSONTokener(reader);
            try {
                // this should fail since the index is 0;
                tokener.back();
                fail("Expected an exception");
            } catch (JSONException e) {
                assertEquals("Stepping back two steps is not supported", e.getMessage());
            } catch (Exception e) {
                fail("Unknown Exception type " + e.getClass().getCanonicalName()+" with message "+e.getMessage());
            }
            
        } finally {
            reader.close();
        }
    }
    /**
     * verify that back() fails as expected.
     * @throws IOException thrown if something unexpected happens.
     */
    @Test
    public void verifyBackFailureDoubleBack() throws IOException {
        Reader reader = new StringReader("some test string");
        try {
            final JSONTokener tokener = new JSONTokener(reader);
            tokener.next();
            tokener.back();
            try {
                // this should fail since the index is 0;
                tokener.back();
                fail("Expected an exception");
            } catch (JSONException e) {
                assertEquals("Stepping back two steps is not supported", e.getMessage());
            } catch (Exception e) {
                fail("Unknown Exception type " + e.getClass().getCanonicalName()+" with message "+e.getMessage());
            }
       } finally {
           reader.close();
       }
    }
    
    @Test
    public void testValid() {
        checkValid("0",Number.class);
        checkValid(" 0  ",Number.class);
        checkValid("23",Number.class);
        checkValid("23.5",Number.class);
        checkValid(" 23.5  ",Number.class);
        checkValid("null",null);
        checkValid(" null  ",null);
        checkValid("true",Boolean.class);
        checkValid(" true\n",Boolean.class);
        checkValid("false",Boolean.class);
        checkValid("\nfalse  ",Boolean.class);
        checkValid("{}",JSONObject.class);
        checkValid(" {}  ",JSONObject.class);
        checkValid("{\"a\":1}",JSONObject.class);
        checkValid(" {\"a\":1}  ",JSONObject.class);
        checkValid("[]",JSONArray.class);
        checkValid(" []  ",JSONArray.class);
        checkValid("[1,2]",JSONArray.class);
        checkValid("\n\n[1,2]\n\n",JSONArray.class);

        // Test should fail if default strictMode is true, pass if false
        JSONParserConfiguration jsonParserConfiguration = new JSONParserConfiguration();
        if (jsonParserConfiguration.isStrictMode()) {
            try {
                checkValid("1 2", String.class);
                assertEquals("Expected to throw exception due to invalid string", true, false);
            } catch (JSONException e) { }
        } else {
            checkValid("1 2", String.class);
        }
    }
    
    @Test
    public void testErrors() {
        // Check that stream can detect that a value is found after
        // the first one
        checkError(" { \"a\":1 }  4 ");
        checkError("null \"a\"");
        checkError("{} true");
    }
    
    private Object checkValid(String testStr, Class<?> aClass)  {
        Object result = nextValue(testStr);

        // Check class of object returned
        if( null == aClass ) {
            if(JSONObject.NULL.equals(result)) {
                // OK
            } else {
                throw new JSONException("Unexpected class: "+result.getClass().getSimpleName());
            }
        } else {
            if( null == result ) {
                throw new JSONException("Unexpected null result");
            } else if(!aClass.isAssignableFrom(result.getClass()) ) {
                throw new JSONException("Unexpected class: "+result.getClass().getSimpleName());
            }
        }
        
        return result;
    }

    private void checkError(String testStr) {
        try {
            nextValue(testStr);
            
            fail("Error should be triggered: (\""+testStr+"\")");
        } catch (JSONException e) {
            // OK
        }
    }
    
    /**
     * Verifies that JSONTokener can read a stream that contains a value. After
     * the reading is done, check that the stream is left in the correct state
     * by reading the characters after. All valid cases should reach end of stream.
     * @param testStr
     * @return
     * @throws Exception
     */
    private Object nextValue(String testStr) throws JSONException {
        StringReader sr = new StringReader(testStr);
        try {
            JSONTokener tokener = new JSONTokener(sr);
    
            Object result = tokener.nextValue();
    
            if( result == null ) {
                throw new JSONException("Unable to find value token in JSON stream: ("+tokener+"): "+testStr);
            }
            
            char c = tokener.nextClean();
            if( 0 != c ) {
                throw new JSONException("Unexpected character found at end of JSON stream: "+c+ " ("+tokener+"): "+testStr);
            }
    
            return result;
        } finally {
            sr.close();
        }

    }
    
    /**
     * Tests the failure of the skipTo method with a buffered reader. Preferably
     * we'd like this not to fail but at this time we don't have a good recovery.
     * 
     * @throws IOException thrown if something unexpected happens.
     */
    @Test
    public void testSkipToFailureWithBufferedReader() throws IOException {
        final byte[] superLongBuffer = new byte[1000001];
        // fill our buffer
        for(int i=0;i<superLongBuffer.length;i++) {
            superLongBuffer[i] = 'A';
        }
        
        Reader reader = new BufferedReader(new InputStreamReader(
                new ByteArrayInputStream(superLongBuffer)));
        try {
            final JSONTokener tokener = new JSONTokener(reader);
            try {
                // this should fail since the internal markAhead buffer is only 1,000,000
                // but 'B' doesn't exist in our buffer that is 1,000,001 in size
                tokener.skipTo('B');
                fail("Expected exception");
            } catch (JSONException e) {
                assertEquals("Mark invalid", e.getMessage());
            } catch (Exception e) {
                fail("Unknown Exception type " + e.getClass().getCanonicalName()+" with message "+e.getMessage());
            }
        } finally {
            reader.close();
        }
    }

    /**
     * Tests the success of the skipTo method with a String reader.
     * 
     * @throws IOException thrown if something unexpected happens.
     */
    @Test
    public void testSkipToSuccessWithStringReader() throws IOException {
        final StringBuilder superLongBuffer = new StringBuilder(1000001);
        // fill our buffer
        for(int i=0;i<superLongBuffer.length();i++) {
            superLongBuffer.append('A');
        }
        Reader reader = new StringReader(superLongBuffer.toString());
        try {
            final JSONTokener tokener = new JSONTokener(reader);
            try {
                // this should not fail since the internal markAhead is ignored for StringReaders
                tokener.skipTo('B');
            } catch (Exception e) {
                fail("Unknown Exception type " + e.getClass().getCanonicalName()+" with message "+e.getMessage());
            }
        } finally {
            reader.close();
        }
    }

    /**
     * Verify that next and back are working properly and tracking the correct positions
     * with different new line combinations.
     */
    @Test
    public void testNextBackComboWithNewLines() {
        final String testString = "this is\nA test\r\nWith some different\rNew Lines";
        //                         ^       ^         ^                    ^
        // index positions         0       8        16                   36
        final JSONTokener tokener = new JSONTokener(testString);
        assertEquals(" at 0 [character 1 line 1]", tokener.toString());
        assertEquals('t',tokener.next());
        assertEquals(" at 1 [character 2 line 1]", tokener.toString());
        tokener.skipTo('\n');
        assertEquals("skipTo() improperly modifying indexes"," at 7 [character 8 line 1]", tokener.toString());
        assertEquals('\n',tokener.next());
        assertEquals(" at 8 [character 0 line 2]", tokener.toString());
        assertEquals('A',tokener.next());
        assertEquals(" at 9 [character 1 line 2]", tokener.toString());
        tokener.back();
        assertEquals(" at 8 [character 0 line 2]", tokener.toString());
        tokener.skipTo('\r');
        assertEquals("skipTo() improperly modifying indexes"," at 14 [character 6 line 2]", tokener.toString());
        // verify \r\n combo doesn't increment the line twice
        assertEquals('\r', tokener.next());
        assertEquals(" at 15 [character 0 line 3]", tokener.toString());
        assertEquals('\n', tokener.next());
        assertEquals(" at 16 [character 0 line 3]", tokener.toString());
        // verify stepping back after reading the \n of an \r\n combo doesn't  increment the line incorrectly
        tokener.back();
        assertEquals(" at 15 [character 6 line 2]", tokener.toString());
        assertEquals('\n', tokener.next());
        assertEquals(" at 16 [character 0 line 3]", tokener.toString());
        assertEquals('W', tokener.next());
        assertEquals(" at 17 [character 1 line 3]", tokener.toString());
        assertEquals('i', tokener.next());
        assertEquals(" at 18 [character 2 line 3]", tokener.toString());
        tokener.skipTo('\r');
        assertEquals("skipTo() improperly modifying indexes"," at 35 [character 19 line 3]", tokener.toString());
        assertEquals('\r', tokener.next());
        assertEquals(" at 36 [character 0 line 4]", tokener.toString());
        tokener.back();
        assertEquals(" at 35 [character 19 line 3]", tokener.toString());
        assertEquals('\r', tokener.next());
        assertEquals(" at 36 [character 0 line 4]", tokener.toString());
        assertEquals('N', tokener.next());
        assertEquals(" at 37 [character 1 line 4]", tokener.toString());
        
        // verify we get the same data just walking though, no calls to back
        final JSONTokener t2 = new JSONTokener(testString);
        for(int i=0; i<7; i++) {
            assertTrue(t2.toString().startsWith(" at " + i + " "));
            assertEquals(testString.charAt(i), t2.next());
        }
        assertEquals(" at 7 [character 8 line 1]", t2.toString());
        assertEquals(testString.charAt(7), t2.next());
        assertEquals(" at 8 [character 0 line 2]", t2.toString());
        for(int i=8; i<14; i++) {
            assertTrue(t2.toString().startsWith(" at " + i + " "));
            assertEquals(testString.charAt(i), t2.next());
        }
        assertEquals(" at 14 [character 6 line 2]", t2.toString());
        assertEquals('\r', t2.next());
        assertEquals(" at 15 [character 0 line 3]", t2.toString());
        assertEquals('\n', t2.next());
        assertEquals(" at 16 [character 0 line 3]", t2.toString());
        assertEquals('W', t2.next());
        assertEquals(" at 17 [character 1 line 3]", t2.toString());
        for(int i=17; i<37; i++) {
            assertTrue(t2.toString().startsWith(" at " + i + " "));
            assertEquals(testString.charAt(i), t2.next());
        }
        assertEquals(" at 37 [character 1 line 4]", t2.toString());
        for(int i=37; i<testString.length(); i++) {
            assertTrue(t2.toString().startsWith(" at " + i + " "));
            assertEquals(testString.charAt(i), t2.next());
        }
        assertEquals(" at "+ testString.length() +" [character 9 line 4]", t2.toString());
        // end of the input
        assertEquals(0, t2.next());
        assertFalse(t2.more());
   }

   @Test
   public void testAutoClose(){
       Reader reader = new StringReader("some test string");
       try {
           JSONTokener tokener = new JSONTokener(reader);
           tokener.close();
           tokener.next();
       } catch (Exception exception){
           assertEquals("Stream closed", exception.getMessage());
       }
   }

    @Test
    public void testInvalidInput_JSONObject_withoutStrictModel_shouldParseInput() {
        String input = "{\"invalidInput\": [],}";
        JSONTokener tokener = new JSONTokener(input);

        // Test should fail if default strictMode is true, pass if false
        JSONParserConfiguration jsonParserConfiguration = new JSONParserConfiguration();
        if (jsonParserConfiguration.isStrictMode()) {
            try {
                Object value = tokener.nextValue();
                assertEquals(new JSONObject(input).toString(), value.toString());
                assertEquals("Expected to throw exception due to invalid string", true, false);
            } catch (JSONException e) { }
        } else {
            Object value = tokener.nextValue();
            assertEquals(new JSONObject(input).toString(), value.toString());
        }
    }

    @Test
    public void testInvalidInput_JSONArray_withoutStrictModel_shouldParseInput() {
        String input = "[\"invalidInput\",]";
        JSONTokener tokener = new JSONTokener(input);

        // Test should fail if default strictMode is true, pass if false
        JSONParserConfiguration jsonParserConfiguration = new JSONParserConfiguration();
        if (jsonParserConfiguration.isStrictMode()) {
            try {
                Object value = tokener.nextValue();
                assertEquals(new JSONArray(input).toString(), value.toString());
                assertEquals("Expected to throw exception due to invalid string", true, false);
            } catch (JSONException e) { }
        } else {
            Object value = tokener.nextValue();
            assertEquals(new JSONArray(input).toString(), value.toString());
        }
    }
}
