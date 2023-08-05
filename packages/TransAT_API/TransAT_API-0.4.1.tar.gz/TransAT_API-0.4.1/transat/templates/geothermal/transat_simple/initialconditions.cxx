#include<stdio.h>
#include<cmath>
#include"cppinterface.decl.h"
extern "C"{
   void initialconditions();
}

void initialconditions() {


   int nblocks;
   int nijk;
   double *u,*v,*w;
   double *x,*y,*z;

   printf("\n ---------------------------------\n");
   printf(  " - initialconditions.cxx (start) -\n");
   printf(  " ---------------------------------\n");

   nblocks = get_integer("nblocks"); // number of blocks 

   // Loop on blocks
   for (int nb=0; nb < nblocks; nb++){
     // Access to the arrays to be initialised
      set_pointer(nb,&u,"uvelocity");
      set_pointer(nb,&v,"vvelocity");
      set_pointer(nb,&w,"wvelocity");

      // Cell coordinates
      set_pointer(nb,&x,"cellcenterX");
      set_pointer(nb,&y,"cellcenterY");
      set_pointer(nb,&z,"cellcenterZ");

      // Loop on cells
      nijk    = get_integer(nb,"nijk"); // number of cells in the block
      for (int ii=0; ii < nijk; ii++) {
         // Enter the initial values here.
         properties_initialize(nb, ii);
         u[ii]   = 0.01;
         v[ii]   = 0.0;
         w[ii]   = 0.0;
         properties_set_state("pressure", 0.0);
         properties_set_state("temperature", 300.0);
         properties_set_back();
      }
   }
   
   printf("\n ---------------------------------\n");
   printf(  " - initialconditions.cxx (end)   -\n");
   printf(  " ---------------------------------\n");
}

