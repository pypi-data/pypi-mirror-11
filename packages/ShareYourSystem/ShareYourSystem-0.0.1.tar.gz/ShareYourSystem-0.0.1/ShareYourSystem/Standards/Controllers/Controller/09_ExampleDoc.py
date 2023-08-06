#/######################/#
# Import
#

#ImportModules
import ShareYourSystem as SYS

#/######################/#
# Define you hierarchic objects
#

#Define a Moduler class
@SYS.ClasserClass()
class MultiplierClass(SYS.ControllerClass):
								
	def default_init(self,
						_MultiplyingFirstFloat=0,
						_MultiplyingSecondFloat=0,
						_MultipliedTotalFloat=0,
						**_KwargVariablesDict
					):

		#Call the parent init method
		SYS.ControllerClass.__init__(self,**_KwargVariablesDict)
			
		#Build the model		
		self['#map@set'](
			[
				('-Models',[
						('|Parameter',[
							('ModelKeyStrsList',['MultiplyingFirstFloat','MultiplyingSecondFloat'])
						]),
						('|Result',[
							('ModelKeyStrsList',['MultipliedTotalFloat']),
							('ParentingTriggerVariable',['<->/^/|Parameter'])
						])
					]
				)
			]
		)

#Define a Moduler class
@SYS.ClasserClass()
class ModulerClass(SYS.ControllerClass):
								
	def default_init(self,
						_ModulingPowerFloat=0.5,
						_ModuledTotalFloat=0,
						**_KwargVariablesDict
					):

		#Call the parent init method
		SYS.ControllerClass.__init__(self,**_KwargVariablesDict)

		#Build the components and the models
		self['#map@set'](
			[
				#MODELS
				(
					'-Models',
					[
						('|Parameter',[
							('ModelKeyStrsList',['ModulingPowerFloat']),
							(
								'ParentingTriggerVariable',
								[
									'<->/^/^/-Components/|Real/-Models/|Result',
									'<->/^/^/-Components/|Image/-Models/|Result',
								]
							)
						]), 
						('|Result',[
							('ModelKeyStrsList',['ModuledTotalFloat']),
							(
								'ParentingTriggerVariable',
								[
									'<->/^/|Parameter'
								]
							)
						])
					]
				),
				#COMPONENTS
				(
					'-Components',{
						'|Real':MultiplierClass(),
						'|Image':MultiplierClass()
					}
				)
			]
		)
						
#/######################/#
# Build your total model and insert
#

MyModuler=ModulerClass(
	).network(
		['Components','Models']
	)

#/######################/#
# Print
#

#print
print('MyModuler is ')
SYS._print(MyModuler)

