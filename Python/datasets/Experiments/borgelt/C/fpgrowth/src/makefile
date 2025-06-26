#-----------------------------------------------------------------------
# Windows-Compatible Makefile for fpgrowth using mingw32-make
#-----------------------------------------------------------------------
# Notes:
# - Replaces Unix shell commands with Windows equivalents
# - Assumes mingw32-make and GCC (MinGW) are installed and in PATH
# - Uses forward slashes for paths
#-----------------------------------------------------------------------

THISDIR  = ../../fpgrowth/src
UTILDIR  = ../../util/src
MATHDIR  = ../../math/src
TRACTDIR = ../../tract/src
APRIDIR  = ../../apriori/src

CC       = gcc -std=c99
CFBASE   = -Wall -Wextra -Wno-unused-parameter -Wconversion -pedantic -c $(ADDFLAGS)
CFLAGS   = $(CFBASE) -DNDEBUG -O3 -funroll-loops
INCS     = -I$(UTILDIR) -I$(MATHDIR) -I$(TRACTDIR) -I$(APRIDIR)

LD       = gcc
LDFLAGS  = $(ADDFLAGS)
LIBS     = -lm $(ADDLIBS)

HDRS     = \
  $(UTILDIR)/fntypes.h $(UTILDIR)/arrays.h $(UTILDIR)/memsys.h \
  $(UTILDIR)/symtab.h $(UTILDIR)/error.h $(MATHDIR)/ruleval.h \
  $(TRACTDIR)/tract.h $(TRACTDIR)/patspec.h $(TRACTDIR)/clomax.h \
  $(TRACTDIR)/report.h $(APRIDIR)/istree.h fpgrowth.h

OBJS = \
  $(UTILDIR)/memsys.o $(UTILDIR)/arrays.o $(UTILDIR)/idmap.o \
  $(UTILDIR)/escape.o $(UTILDIR)/tabread.o $(UTILDIR)/tabwrite.o \
  $(MATHDIR)/gamma.o $(MATHDIR)/chi2.o \
  $(MATHDIR)/ruleval.o $(TRACTDIR)/clomax.o $(TRACTDIR)/repcm.o \
  $(TRACTDIR)/fim16.o $(APRIDIR)/istree.o

# $(UTILDIR)/scform.o

FPGOBJS = $(OBJS) $(TRACTDIR)/taread.o $(TRACTDIR)/patspec.o fpgmain.o
PSPOBJS = $(OBJS) $(UTILDIR)/random.o $(TRACTDIR)/tars.o \
          $(TRACTDIR)/pspest.o fpgrowth.o pspmain.o

PRGS = fpgrowth.exe fpgpsp.exe

all: $(PRGS)

fpgrowth.exe: $(FPGOBJS)
	$(LD) $(LDFLAGS) $(FPGOBJS) $(LIBS) -o $@

fpgpsp.exe: $(PSPOBJS)
	$(LD) $(LDFLAGS) $(PSPOBJS) $(LIBS) -o $@

fpgmain.o: fpgrowth.c $(HDRS) $(UTILDIR)/tabread.h $(UTILDIR)/tabwrite.h $(TRACTDIR)/fim16.h
	$(CC) $(CFLAGS) $(INCS) -DFPG_MAIN fpgrowth.c -o $@

pspmain.o: fpgpsp.c $(HDRS) $(UTILDIR)/tabread.h $(UTILDIR)/tabwrite.h $(UTILDIR)/random.h fpgpsp.h
	$(CC) $(CFLAGS) $(INCS) -DFPGPSP_MAIN fpgpsp.c -o $@

fpgrowth.o: fpgrowth.c fpgrowth.h $(HDRS) $(TRACTDIR)/fim16.h
	$(CC) $(CFLAGS) $(INCS) fpgrowth.c -o $@

# External Module Builds
$(UTILDIR)/%.o:
	cd $(UTILDIR) && mingw32-make $(@F) ADDFLAGS="$(ADDFLAGS)"

$(MATHDIR)/%.o:
	cd $(MATHDIR) && mingw32-make $(@F) ADDFLAGS="$(ADDFLAGS)"

$(TRACTDIR)/%.o:
	cd $(TRACTDIR) && mingw32-make $(@F) ADDFLAGS="$(ADDFLAGS)"

$(APRIDIR)/%.o:
	cd $(APRIDIR) && mingw32-make $(@F) ADDFLAGS="$(ADDFLAGS)"

clean:
	del /Q *.o *.exe *.d 2>NUL
	cd $(UTILDIR) && mingw32-make clean
	cd $(MATHDIR) && mingw32-make clean
	cd $(TRACTDIR) && mingw32-make clean
	cd $(APRIDIR) && mingw32-make clean
