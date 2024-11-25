objects = data.o eclat.o testeclat.o
CC = g++
flags = -O3 -Wall -ansi -pedantic

eclat: $(objects)
	$(CC) $(flags) $(objects) -o eclat

data.o: data.cpp data.h
	$(CC) $(flags) -c data.cpp

eclat.o: eclat.cpp data.h item.h eclat.h
	$(CC) $(flags) -c eclat.cpp

testeclat.o: testeclat.cpp data.h item.h eclat.h
	$(CC) $(flags) -c testeclat.cpp

clean: 
	rm -f $(objects) eclat
