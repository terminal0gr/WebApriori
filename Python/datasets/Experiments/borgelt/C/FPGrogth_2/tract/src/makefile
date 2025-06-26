#-----------------------------------------------------------------------
# Windows-Compatible Makefile for tract/src using mingw32-make
#-----------------------------------------------------------------------

UTILDIR  = ../../util/src
CC       = gcc -std=c99
CFBASE   = -Wall -Wextra -Wno-unused-parameter -Wconversion -pedantic -c $(ADDFLAGS)
CFLAGS   = $(CFBASE) -DNDEBUG -O3 -funroll-loops
INCS     = -I. -I$(UTILDIR)

OBJS = tract.o clomax.o patspec.o report.o fim16.o 
#       taread.o tars.o repcm.o cm4seqs.o cmfilter.o

EXE  = fim16.exe

all: $(OBJS) $(EXE)

# Object file compilation
%.o: %.c
	$(CC) $(CFLAGS) $(INCS) -o $@ -c $<

# Example executable
fim16.exe: fim16.o tract.o
	$(CC) $(CFLAGS) $(INCS) fim16.o tract.o -o fim16.exe

# Clean for Windows
clean:
	del /Q *.o *.exe *.d 2>NUL
