
F77=gfortran
FFLAGS = -O3
LFLAGS = -O3

OBJECTS = ftoaq.o
HOSTLIBS= -lm
NUMREC =  ~gebhardt/lib/numrec/numrec.a
BIWT   =  ~gebhardt/progs/biwgt.o
QUEST  =  ~gebhardt/lib/libquest/libquest.o
GCV    =  ~gebhardt/lib/gcv/gcvspl.o
PGPLOT =  ~gebhardt/lib/pglib/libpgplot.a -L/usr/X11R6/lib -lX11
FITSIO =  ~gebhardt/lib/cfitsio/libcfitsio.a

ftoaq:  ftoaq.o 
	$(F77) $(LFLAGS) -o ftoaq $(OBJECTS) $(FITSIO) $(BIWT) $(QUEST)

ftoaq.o:  ftoaq.f
	$(F77) -c $(FFLAGS) ftoaq.f
