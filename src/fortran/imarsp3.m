
F77=gfortran
FFLAGS = -O3
LFLAGS = -O3

OBJECTS = imarsp3.o
HOSTLIBS= -lm
NUMREC =  ~gebhardt/lib/numrec/numrec.a
BIWT   =  ~gebhardt/progs/biwgt.o
QUEST  =  ~gebhardt/lib/libquest/libquest.o
GCV    =  ~gebhardt/lib/gcv/gcvspl.o
PGPLOT =  ~gebhardt/lib/pglib/libpgplot.a -L/usr/X11R6/lib -lX11
FITSIO =  ~gebhardt/lib/cfitsio/libcfitsio.a

imarsp3:  imarsp3.o 
	$(F77) $(LFLAGS) -o imarsp3 $(OBJECTS) $(FITSIO) $(BIWT) $(QUEST)

imarsp3.o:  imarsp3.f
	$(F77) -c $(FFLAGS) imarsp3.f
