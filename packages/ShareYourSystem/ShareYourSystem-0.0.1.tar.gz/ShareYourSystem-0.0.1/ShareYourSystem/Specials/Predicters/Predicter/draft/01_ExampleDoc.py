
#ImportModules
import ShareYourSystem as SYS


#Define
MyPredicter=SYS.PredicterClass(
	).predict(
		#PredictingUnitsInt
		10,
		#PredictingSensorsInt
		1,
		#PredictingDynamicStr
		'leak',
		#PredictingConstantTimeFloat (ms)
		1.,
		#PredictingInputStatStr
		'norm',
		#PredictingDecoderMeanWeightFloat
		1.,
		#PredictingDecoderStdWeightFloat
		0.,
		#PredictingNormalisationInt
		0.5,			
		#PredictingCostFloat
		0.,
		#PredictingPerturbativeInputWeightFloat
		0.,
		#PredictingPerturbativeLateralWeightFloat
		0.,
		#PredictingInputRandomStatStr
		'norm',
		#PredictingLateralRandomStatStr
		'norm'
	)

#print
print('MyPredicter is')
SYS._print(MyPredicter)
