#include<stdio.h>
#include<cmath>
#include"cppinterface.h"
extern "C"{
   void initialconditions();
}

void initialconditions() {


   int nblocks;
   int glob_nb, nijk;
   double *p,*u,*v,*w,*t;

   printf("\n ---------------------------------\n");
   printf(  " - initialconditions.cxx (start) -\n");
   printf(  " ---------------------------------\n");

   nblocks = get_integer("nblocks");

   printf(" nblocks = %i\n",nblocks);

   for (int nb=0; nb < nblocks; nb++){
      set_pointer(nb,&p,"pressure");
      set_pointer(nb,&u,"uvelocity");
      set_pointer(nb,&v,"vvelocity");
      set_pointer(nb,&w,"wvelocity");
      set_pointer(nb,&t,"temperature");

      glob_nb = get_integer(nb,"gnb"); // glob_nb is the global block number
      nijk    = get_integer(nb,"nijk");
      for (int ii=0; ii < nijk; ii++) {
         u[ii]  =   1;
         v[ii]  =   0.0;
         w[ii]  =   0.0;
         p[ii]  =   0.0;
         t[ii]  = 300.0;
      }
   }
   
   printf("\n ---------------------------------\n");
   printf(  " - initialconditions.cxx (end)   -\n");
   printf(  " ---------------------------------\n");
}
