#-----------------------------------------------------------------------
# Windows-Compatible Makefile for util/src using mingw32-make
#-----------------------------------------------------------------------

THISDIR = ../../util/src
CC      = gcc -std=c99
CFBASE  = -Wall -Wextra -Wno-unused-parameter -Wconversion -pedantic -c $(ADDFLAGS)
CFLAGS  = $(CFBASE) -DNDEBUG -O3 -funroll-loops
INCS    = -I.

OBJS = memsys.o symtab.o error.o fntypes.o arrays.o \
       escape.o tabread.o tabwrite.o scanner.o random.o \
       strlist.o idmap.o scform.o

all: $(OBJS)

%.o: %.c
	$(CC) $(CFLAGS) $(INCS) -o $@ -c $<

clean:
	del /Q *.o *.exe *.d 2>NUL
