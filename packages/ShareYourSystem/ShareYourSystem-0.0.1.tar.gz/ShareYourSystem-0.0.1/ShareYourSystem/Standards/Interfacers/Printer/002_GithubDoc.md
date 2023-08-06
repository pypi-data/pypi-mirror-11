
<!--
FrozenIsBool False
-->

##Code

----

<ClassDocStr>

----

```python
# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


The Printer is an object that can directly print 
Strs in the Representer context.

"""


#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Objects.Initiator"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Representer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
Representer=DecorationModule
#</ImportSpecificModules>


#<DefineClass>
@DecorationClass()
class PrinterClass(BaseClass):

	#Definition
	RepresentingKeyStrsList=[
									'PrintingCopyVariable'
								]
	
	def default_init(self,
						_PrintingCopyVariable=None,
						**_KwargVariablesDict
					):
		
		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)
	
	#<DefineDoMethod>	
	def do__print(self,**_KwargVariablesDict):

		#debug
		'''
		print('self.PrintingCopyVariable is ',self.PrintingCopyVariable)
		print('')
		'''

		#print
		print(
			Representer.getRepresentedStrWithVariable(
				self.PrintingCopyVariable,
				**_KwargVariablesDict
				)
		)

#</DefineClass>


```

<small>
View the Printer sources on <a href="https://github.com/Ledoux/ShareYourSystem/tree/master/Pythonlogy/ShareYourSystem/Objects/Printer" target="_blank">Github</a>
</small>

