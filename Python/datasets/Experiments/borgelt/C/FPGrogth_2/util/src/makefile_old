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

# Compile all .c source files to .o object files
%.o: %.c
	$(CC) $(CFLAGS) $(INCS) -o $@ -c $<

# Clean target for Windows
clean:
	del /Q *.o *.exe *.d 2>NUL

# Dependency files (optional, not necessary for Windows builds)
# You can uncomment if needed with proper rules
# %.d: %.c
# 	$(CC) -MM $(CFLAGS) $(INCS) $< > $@
