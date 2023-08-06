%module CIntegrateAndFireTransferFunction
%include "../../../Standards/Interfacers/Swiger/SwigConfigs.swig"
%{ 
	#define SWIG_FILE_WITH_INIT
	#include "../../../Standards/Interfacers/Swiger/CTool.h"
	#include "CIntegrateAndFireTransferFunction.h"

%}
// Include the header file with above prototypes
%include "../../../Standards/Interfacers/Swiger/CTool.h"
%include "./CIntegrateAndFireTransferFunction.h"
