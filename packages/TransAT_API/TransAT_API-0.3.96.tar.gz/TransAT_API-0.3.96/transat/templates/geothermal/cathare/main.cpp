// Example of program loading Cathare and running a computation while
// performing field input/output, saving/restoring the state at
// several times, on the disk or in the memory, and abort arbitrary
// timesteps.

#include <Problem.h>
#include <ICoCoTrioField.h>
#include <dlfcn.h>
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <sys/stat.h>

#include <boost/algorithm/string/split.hpp>
#include <boost/algorithm/string/classification.hpp>

#include <fpu_control.h>

#include "Coupling.h"

using namespace std;
using ICoCo::Problem;
using ICoCo::TrioField;

// Utility function to detect if a file is present
bool file_exists(string name) {
  struct stat info;
  int result = stat(name.c_str(),&info);
  return (result==0);
}

// Open a shared library
// Find the function getProblem
// Run it and return a pointer to the Problem
// Prints the errors if any

Problem* openLib(const char* libname, void* & handle) {
  Problem *(*getProblem)();
  handle=dlopen(libname, RTLD_LAZY | RTLD_LOCAL);
  if (!handle) {
    cerr << dlerror() << endl;
    throw 0;
  }
  getProblem=(Problem* (*)())dlsym(handle, "getProblem");
  if (!getProblem) {
    cout << dlerror() << endl;
    throw 0;
  }
  return (*getProblem)();
}

// Close a shared library
// Prints the errors if any

void closeLib(void* handle) {
  if (dlclose(handle)) {
    cout << dlerror() << endl;
    throw 0;
  }
}

//To read the configuration file. (For now, it is mocked up with a txt file.)
//May be deleted later.
std::string config(std::string key) {
  std::string values;
  std::vector<std::string> data;
  std::ifstream read_config;
  read_config.open("Configuration.txt", std::ios::in);
  if (!read_config.good()) {
    std::cout<<"ERROR: Not able to open configure file!"<<std::endl;
  }
  while (read_config.good() && getline(read_config,values)) {
    boost::algorithm::split(data, values, boost::algorithm::is_any_of(" "));
    if (data[0].c_str()==key)
      break;
  }
  read_config.close();
  
  return data[1];
}

//To convert string variable into boolean type.
bool to_bool(std::string const& s) {
  if (s=="false")
    return false;
  else if (s=="true")
    return true;
  else {
    std::cout<<"Bad value for RADCHEMI!"<<std::endl;
    exit (EXIT_FAILURE);
  }
    
}



//****************************************************
//*********Definitions of the main functions**********
//****************************************************

//Constructor
Coupling::Coupling(ICoCo::Problem *Problem) {
  _P = Problem;

  _element    = config("element");
  _axial     = config("axial");
  _filename_T = config("filename_T").c_str();
  _filename_C = config("filename_C").c_str();

  _time_stepping_tolerance = atof(config("time_stepping_tolerance").c_str());
  _tmax       = atof(config("tmax").c_str());

  _DPDQ_L     = atof(config("DPDQ_L").c_str());  
  _DPDQ_G     = atof(config("DPDQ_G").c_str());  

  _DENL       = atof(config("DENL").c_str());  
  _DENG       = atof(config("DENG").c_str());  

  _RADCHEMI   = to_bool(config("RADCHEMI").c_str());

  _restore    = to_bool(config("restore").c_str());
  _restore_label  = atoi(config("restore_label").c_str());
  _restore_method = config("restore_method").c_str();

  _length     = atof(config("LENGTH").c_str());
  _mesh       = config("MESH").c_str();

  _location = "_"+_element;
  
  //Delete context or create empty 1D code file.
  std::ofstream clear_file;

  std::stringstream filename;
  std::stringstream filename_locker;

  filename<<_filename_C;
  
  clear_file.open(filename.str().c_str(), std::ios::trunc);
  if (!clear_file.good()) {

    std::cout<<"ERROR: Failed to clear CATHARE data file!"<<std::endl;

  }
  
}

// Performs a simple time loop on Problem P :
// Uses the timestep suggested by P
// Modifies it to stop at _tmax

void Coupling::runUntil() {

  bool stop=false;  // P wants to stop
  bool ok=false;     // P solveTimeStep was OK

  if (_restore) {
    _P->restore(_restore_label, _restore_method);
  }

  while (!stop) {                     // Loop on timesteps
    
    ok=false;

    while (!ok && !stop) {                // Loop on timestep size

     std::cout<<"Before computing presentTime()!!!"<<std::endl;
     double present=_P->presentTime();
     std::cout<<"After computing presentTime()!!!"<<std::endl;
     double dt=_P->computeTimeStep(stop);

     // modify dt to stop at exactly _tmax without restraining too much the time step.
     // - modified dt will always be less than dt
     // - and always more than min(dt,previous dt)/2
     // where previous dt is the value returned by computeTimeStep for the last validated time step.
     if (present+dt/1000>_tmax) // dt/1000 is an epsilon to handle machine precision errors
     	stop=true;
     else if (present+dt>_tmax)
        dt=_tmax-present;
     else if (present+2*dt>_tmax)
     	dt=(_tmax-present)/2;

     if (stop)
	break;
	
      _P->initTimeStep(dt);
      if (present > 0.0) {
        double temperature_goal = 30.0;
        double temperature_b_goal = 61.4;
        for (int i(1); i<101; ++i ){
          temperature_goal = 30 + i*0.314;
          temperature_b_goal = 61.4 + i*0.314;
          std::stringstream ss, tt, ttb;
          std::string phi, temperature, temperature_b;
          ss<<"PHIEXT_HT_"<<i;
          phi = ss.str();
          tt<<"TEXT_HT_"<<i;
          ttb<<"TEXT_HTB_"<<i;
          temperature = tt.str();
          temperature_b = ttb.str();

          TrioField PHI, TO, TOB;
          _P->getInputFieldTemplate(temperature, TO);
          _P->getInputFieldTemplate(temperature_b, TOB);
          *TO._field = temperature_goal;
          *TOB._field = temperature_b_goal;
          _P->setInputField(temperature, TO);
          _P->setInputField(temperature_b, TOB);
        }
      }

      if (present > 0.0) {
        std::ifstream read_inject;
        std::vector< std::vector<std::string> > data;
        std::vector<std::string> row;
        std::string values;
        if (file_exists("INJECTION.txt")) {
          read_inject.open("INJECTION.txt", std::ios::in);
          while(read_inject.good() && getline(read_inject, values)){
            boost::algorithm::split(row, values, boost::algorithm::is_any_of("\t"));
            data.push_back(row);
          }
          for (unsigned i(0); i< data.size(); ++i) {
           TrioField TL, TG, AL, ML;
           double ml = atof(data[i][0].c_str());
           double tl = atof(data[i][1].c_str());
           std::stringstream mm, ttl, ttg, aa;
           std::string massflow, temperature_liquid, temperature_gas, voidf;
           mm<<"TOTFLOW_INJECT"<<i;
           ttl<<"TLIQEXT_INJECT"<<i;
           
           massflow = mm.str();
           temperature_liquid = ttl.str();
           temperature_gas = ttg.str();
           voidf = aa.str();
           
           _P->getInputFieldTemplate(massflow, ML);
           _P->getInputFieldTemplate(temperature_liquid, TL);
           *ML._field = ml;
           *TL._field = tl;
           _P->setInputField(massflow, ML);
           _P->setInputField(temperature_liquid, TL);
 
          }
          read_inject.close();
        }
      }
        

      ok=_P->solveTimeStep();

      if (!ok)
	_P->abortTimeStep();
      else
	_P->validateTimeStep();
	//_P->save(_restore_label, _restore_method); //Save current state with corresponding label and method.
    }                                     // End loop on timestep size

  }                                   // End loop on timesteps

  rename("INJECTION.txt", "INJECTION.txt.bak");

}

int main(int argc, char** argv) {

  void* handle_Cathare;
  Problem *C;
  C=openLib("./pipeflow.so",handle_Cathare);
  C->initialize();
  Coupling Coupling(C);
  Coupling.runUntil();
  C->terminate();
  delete C;
  closeLib(handle_Cathare);
  return 0;

}
