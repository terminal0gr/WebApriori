#-----------------------------------------------------------------------
# File    : makefile
# Contents: build math utility modules (Windows version)
#-----------------------------------------------------------------------
SHELL    = cmd
THISDIR  = ../../math/src
UTILDIR  = ../../util/src
TRACTDIR = ../../tract/src

# Use MinGW gcc (or change to cl for MSVC)
CC       = gcc -std=c99
CFBASE   = -Wall -Wextra -Wno-unused-parameter -Wconversion \
           -pedantic -c $(ADDFLAGS)
CFLAGS   = $(CFBASE) -DNDEBUG -O3 -funroll-loops
# CFLAGS   = $(CFBASE) -g

LD       = gcc
LDFLAGS  = $(ADDFLAGS)
LIBS     = -lm $(ADDLIBS)

GAMMA    = gammapdf.exe gammacdf.exe gammaqtl.exe
NORMAL   = normpdf.exe  normcdf.exe  normqtl.exe
CHI2     = chi2pdf.exe  chi2cdf.exe  chi2qtl.exe
PRGS     = $(GAMMA) $(NORMAL) $(CHI2) gamma.exe choose.exe zeta.exe

#-----------------------------------------------------------------------
# Build Programs
#-----------------------------------------------------------------------
all:          $(PRGS)

gamma.exe:        gammain.o makefile
	$(LD) $(LDFLAGS) gammain.o $(LIBS) -o $@

choose.exe:       chsmain.o makefile
	$(LD) $(LDFLAGS) chsmain.o $(LIBS) -o $@

zeta.exe:         zetamain.o makefile
	$(LD) $(LDFLAGS) zetamain.o $(LIBS) -o $@

gammapdf.exe:     gammapdf.o makefile
	$(LD) $(LDFLAGS) gammapdf.o $(LIBS) -o $@

gammacdf.exe:     gammacdf.o makefile
	$(LD) $(LDFLAGS) gammacdf.o $(LIBS) -o $@

gammaqtl.exe:     gammaqtl.o normal.o makefile
	$(LD) $(LDFLAGS) normal.o gammaqtl.o $(LIBS) -o $@

normpdf.exe:      normpdf.o makefile
	$(LD) $(LDFLAGS) normpdf.o $(LIBS) -o $@

normcdf.exe:      normcdf.o makefile
	$(LD) $(LDFLAGS) normcdf.o $(LIBS) -o $@

normqtl.exe:      normqtl.o gamma.o makefile
	$(LD) $(LDFLAGS) gamma.o normqtl.o $(LIBS) -o $@

chi2pdf.exe:      chi2pdf.o gamma.o makefile
	$(LD) $(LDFLAGS) gamma.o chi2pdf.o $(LIBS) -o $@

chi2cdf.exe:      chi2cdf.o gamma.o makefile
	$(LD) $(LDFLAGS) gamma.o chi2cdf.o $(LIBS) -o $@

chi2qtl.exe:      chi2qtl.o gammall.o normal.o makefile
	$(LD) $(LDFLAGS) gammall.o normal.o chi2qtl.o $(LIBS) -o $@

#-----------------------------------------------------------------------
# Clean up (Windows version)
#-----------------------------------------------------------------------
clean:
	del /Q $(PRGS) *.d *.o *~ *.flc core 2>nul