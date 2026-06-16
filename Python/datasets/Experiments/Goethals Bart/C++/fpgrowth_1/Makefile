objects = data.o fpgrowth.o fptree.o item.o testfpgrowth.o
CC = g++
flags = -O6 -Wall

fpgrowth: $(objects)
	$(CC) $(flags) $(objects) -o fpgrowth

data.o: data.cpp data.h
	$(CC) $(flags) -c data.cpp

fpgrowth.o: fpgrowth.cpp data.h item.h fptree.h fpgrowth.h
	$(CC) $(flags) -c fpgrowth.cpp

fptree.o: fptree.cpp data.h item.h fptree.h
	$(CC) $(flags) -c fptree.cpp

item.o: item.cpp item.h
	$(CC) $(flags) -c item.cpp

testfpgrowth.o: testfpgrowth.cpp data.h item.h fptree.h fpgrowth.h
	$(CC) $(flags) -c testfpgrowth.cpp

clean: 
	rm -f $(objects) fpgrowth
