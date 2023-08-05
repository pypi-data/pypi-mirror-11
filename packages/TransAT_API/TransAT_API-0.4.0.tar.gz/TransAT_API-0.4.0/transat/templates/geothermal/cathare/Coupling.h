#ifndef _Coupling_included_
#define _Coupling_included_

#include <Problem.h>



/*!
  *Class Coupling

  This class contains the variables that will be initialized from reading configure
  file, including the location of coupling interface in CATHARE, the files to read
  and write, the variable related to activating concentration calculation, and 
  initial guess of sensitivity parameters.
  It contains a vector to store the variables read from TransAT.
  It contains the function to initialize key variables, to read and write data, to 
  control the time advancing and to solve time steps while calculating the sensitivity
  parameters.
*/
//class Coupling : public ICoCo::Problem_Cathare {
class Coupling {
  private:
  ICoCo::Problem *_P;                                           //!< The pointer to the problem.

  std::string _element;                                        //!< The name of the CATHARE element which bears the coupling interface.
  std::string _location;                                       //!< The location of the coupling interface in CATHARE (here is the same as element).
  std::string _filename_T;                                     //!< The name of the 3D code file.
  std::string _filename_C;                                     //!< The name of the 1D code file.

  double _DPDQ_L, _DPDQ_G;                                     //!< Sensitivity parameters for liquid and gas phases.
  double _DENL, _DENG;                                         //!< Phase density set in TransAT.

  bool _RADCHEMI;                                              //!< Boolean variable to determine if concentration calculation is activated.

  bool _restore;                                               //!< Boolean variable to determine whether to conduct a restart or not.
  
  int _restore_label;                                          //!< The label of C2.label.RESTART file to save and restart.
  std::string _restore_method;                                 //!< Method to save and restart. Either "memory" or "disk".("memory" by default);

  double _time_stepping_tolerance;                             //!< Tolerance for the time control.
  double _tmax;                                                //!< Maximum time for the simualtion.
  double _length;
  std::string _mesh;
  std::string _axial;

  /**
   * \brief This function pauses CATHARE solver when time in CATHARE advances that in TransAT and 
   * force CATHARE to have the same dt as TransAT(not true when dt in CATHARE is smaller).
   * \param present is the present time in CATHARE 
   * \param dt      is the dt suggested by CATHARE 
   * \return        dt suggested by TransAT(when dt in CATHARE is the larger one) to be used for initializing next time step. 
   **/
  double Time_control(double &present, double &dt);

  /**
   * \brief This function carries out calculation for one time step, and calculates the sensitivity parameters. 
   * \param dt is the current dt
   * \return        updated ok for the solved time step to be used for determining whether to accept the time step or not.
   **/
  bool   Simulation(double &dt, double counter);

  /**
   * \brief This function reads from the 3D code file and stores the variable in a vector. 
   * \return a vector storing all the variables read from 3D code file.
   **/
  std::vector<std::string> read_data();

  /**
   * \brief This function writes variable to 1D code file. 
   * \param time is the current time in CATHARE plus one dt(and time_offset if needed)
   **/
  void write_data(double &time);

  /**
   * \brief This function collects data from CATHARE at the coupling interface.
   * \return a vector storing the collected data.
   **/
  std::vector<double> collect_data();

  /**
   * \brief This function sets new values back into CATHARE at Coupling interface. 
   * \param name  is the name of the variable to be written
   * \param value is the value of the variable to be written
   **/
  void setCATvar(std::string name, double value);

  /**
   * \brief This function sets new values back into CATHARE at Coupling interface. 
   * \param name is the name of the variable to be read 
   **/
  ////////Test///////////////////
  double getCATvar(std::string name, std::string object); 
 
  double alpha_compute(double MFR_transat);
  double slip_ratio_compute(double MFR_transat, double flow_quality_transat);
  public:
  
  /**
   * \brief This is the class constructor.
   * \param Problem is a pointer to the ICoCo problem.
   **/
  Coupling(ICoCo::Problem *Problem);

  /**
   * \brief This function carries out the simulation until maximum time.
   **/
  void runUntil();
} ;



#endif
