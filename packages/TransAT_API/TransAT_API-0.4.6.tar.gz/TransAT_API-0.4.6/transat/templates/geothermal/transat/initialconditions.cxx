#include<stdio.h>
#include<cmath>
#include"cppinterface.h"
extern "C"{
   void initialconditions();
}

void initialconditions() {


   int nblocks;
   int nijk;
   double *p,*u,*v,*w,*T;
   double *x,*y,*z;

   printf("\n ---------------------------------\n");
   printf(  " - initialconditions.cxx (start) -\n");
   printf(  " ---------------------------------\n");

   nblocks = get_integer("nblocks"); // number of blocks 

   double Tporous = 373 ; //temperature in pore
   double Twater  = 303 ; //water temperature
   double p_porous = 25.5e6 ; //pressure in pore
   double p_water =  24.5e6 ; //water pressure

   // Loop on blocks
   for (int nb=0; nb < nblocks; nb++){
     // Access to the arrays to be initialised
      set_pointer(nb,&p,"pressure");
      set_pointer(nb,&u,"uvelocity");
      set_pointer(nb,&v,"vvelocity");
      set_pointer(nb,&w,"wvelocity");
      set_pointer(nb,&T,"temperature");

      // Cell coordinates
      set_pointer(nb,&x,"cellcenterX");
      set_pointer(nb,&y,"cellcenterY");
      set_pointer(nb,&z,"cellcenterZ");

      // Loop on cells
      nijk    = get_integer(nb,"nijk"); // number of cells in the block
      for (int ii=0; ii < nijk; ii++) {
        // Enter the initial values here.
         u[ii]   = 0.0;
         v[ii]   = 0.0;
         w[ii]   = 0.0;
         p[ii]   = p_porous;
         T[ii]   = Tporous;
         if (x[ii] > 0.485 && x[ii] < 0.515 && y[ii] < 1.0 ){
            v[ii] = 0.001;
            p[ii] = p_water;
            T[ii] = Twater;
         }
      }
   }
   
   printf("\n ---------------------------------\n");
   printf(  " - initialconditions.cxx (end)   -\n");
   printf(  " ---------------------------------\n");
}

