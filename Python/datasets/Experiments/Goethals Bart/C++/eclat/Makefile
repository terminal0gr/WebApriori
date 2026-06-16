CXX = g++
# Crucial: Ensure -g is present. -O3 can be left out or changed to -O0 during debugging
CXXFLAGS = -g -Wall -O0 

all: eclat

eclat: main.o eclat.o item.o
	$(CXX) $(CXXFLAGS) -o eclat main.o eclat.o item.o