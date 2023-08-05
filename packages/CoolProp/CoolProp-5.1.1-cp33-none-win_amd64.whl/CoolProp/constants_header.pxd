# This file is automatically generated by the generate_constants_module.py script in wrappers/Python.
# DO NOT MODIFY THE CONTENTS OF THIS FILE!

cdef extern from "DataStructures.h" namespace "CoolProp":
	ctypedef enum parameters:
		INVALID_PARAMETER
		igas_constant
		imolar_mass
		iacentric_factor
		irhomolar_reducing
		irhomolar_critical
		iT_reducing
		iT_critical
		irhomass_reducing
		irhomass_critical
		iP_critical
		iP_reducing
		iT_triple
		iP_triple
		iT_min
		iT_max
		iP_max
		iP_min
		iT
		iP
		iQ
		iTau
		iDelta
		iDmolar
		iHmolar
		iSmolar
		iCpmolar
		iCp0molar
		iCvmolar
		iUmolar
		iGmolar
		iDmass
		iHmass
		iSmass
		iCpmass
		iCp0mass
		iCvmass
		iUmass
		iGmass
		iviscosity
		iconductivity
		isurface_tension
		iPrandtl
		ispeed_sound
		iisothermal_compressibility
		iisobaric_expansion_coefficient
		ifundamental_derivative_of_gas_dynamics
		ialphar
		idalphar_dtau_constdelta
		idalphar_ddelta_consttau
		ialpha0
		idalpha0_dtau_constdelta
		idalpha0_ddelta_consttau
		iBvirial
		iCvirial
		idBvirial_dT
		idCvirial_dT
		iZ
		iPIP
		ifraction_min
		ifraction_max
		iT_freeze
		iGWP20
		iGWP100
		iGWP500
		iFH
		iHH
		iPH
		iODP
		iPhase
		iundefined_parameter
	ctypedef enum input_pairs:
		INPUT_PAIR_INVALID
		QT_INPUTS
		PQ_INPUTS
		QSmolar_INPUTS
		QSmass_INPUTS
		HmolarQ_INPUTS
		HmassQ_INPUTS
		PT_INPUTS
		DmassT_INPUTS
		DmolarT_INPUTS
		HmolarT_INPUTS
		HmassT_INPUTS
		SmolarT_INPUTS
		SmassT_INPUTS
		TUmolar_INPUTS
		TUmass_INPUTS
		DmassP_INPUTS
		DmolarP_INPUTS
		HmassP_INPUTS
		HmolarP_INPUTS
		PSmass_INPUTS
		PSmolar_INPUTS
		PUmass_INPUTS
		PUmolar_INPUTS
		HmassSmass_INPUTS
		HmolarSmolar_INPUTS
		SmassUmass_INPUTS
		SmolarUmolar_INPUTS
		DmassHmass_INPUTS
		DmolarHmolar_INPUTS
		DmassSmass_INPUTS
		DmolarSmolar_INPUTS
		DmassUmass_INPUTS
		DmolarUmolar_INPUTS
	ctypedef enum fluid_types:
		FLUID_TYPE_PURE
		FLUID_TYPE_PSEUDOPURE
		FLUID_TYPE_REFPROP
		FLUID_TYPE_INCOMPRESSIBLE_LIQUID
		FLUID_TYPE_INCOMPRESSIBLE_SOLUTION
		FLUID_TYPE_UNDEFINED
	ctypedef enum phases:
		iphase_liquid
		iphase_supercritical
		iphase_supercritical_gas
		iphase_supercritical_liquid
		iphase_critical_point
		iphase_gas
		iphase_twophase
		iphase_unknown
		iphase_not_imposed
