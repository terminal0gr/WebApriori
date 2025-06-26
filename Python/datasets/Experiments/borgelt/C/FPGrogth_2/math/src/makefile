#-----------------------------------------------------------------------
# Windows-Compatible Makefile for math/src using mingw32-make
#-----------------------------------------------------------------------

THISDIR  = ../../math/src
UTILDIR  = ../../util/src
TRACTDIR = ../../tract/src

CC       = gcc -std=c99
CFBASE   = -Wall -Wextra -Wno-unused-parameter -Wconversion \
           -pedantic -c $(ADDFLAGS)
CFLAGS   = $(CFBASE) -DNDEBUG -O3 -funroll-loops
INCS     = -I$(UTILDIR) -I$(TRACTDIR)

OBJS = gamma.o chi2.o ruleval.o
EXE  = testmath.exe

all: $(OBJS)

# Compilation rule for all .c files
%.o: %.c
	$(CC) $(CFLAGS) $(INCS) -o $@ -c $<

# Sample executable (if needed, optional)
testmath.exe: testmath.o $(OBJS)
	$(CC) $(CFLAGS) $(INCS) -o testmath.exe testmath.o $(OBJS)

# Windows-compatible clean rule
clean:
	del /Q *.o *.exe *.d 2>NUL
