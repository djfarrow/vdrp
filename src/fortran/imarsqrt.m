
F77=gfortran
FFLAGS = -O3
LFLAGS = -O3

OBJECTS = imarsqrt.o
HOSTLIBS= -lm
NUMREC =  ~gebhardt/lib/numrec/numrec.a
BIWT   =  ~gebhardt/progs/biwgt.o
QUEST  =  ~gebhardt/lib/libquest/libquest.o
GCV    =  ~gebhardt/lib/gcv/gcvspl.o
PGPLOT =  ~gebhardt/lib/pglib/libpgplot.a -L/usr/X11R6/lib -lX11
FITSIO =  ~gebhardt/lib/cfitsio/libcfitsio.a

imarsqrt:  imarsqrt.o 
	$(F77) $(LFLAGS) -o imarsqrt $(OBJECTS) $(FITSIO) $(BIWT) $(QUEST)

imarsqrt.o:  imarsqrt.f
	$(F77) -c $(FFLAGS) imarsqrt.f
