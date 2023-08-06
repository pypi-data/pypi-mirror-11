
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


The Processer

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Interfacers.Capturer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Representer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import os
#</ImportSpecificModules>

#<DefineLocals>
ProcessingFileStr="ProcessTemp"
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class ProcesserClass(BaseClass):

	#Definition
	RepresentingKeyStrsList=[
								'ProcessingBashStr',
								'ProcessedBashStr'
							]
	
	def default_init(self,
						_ProcessingBashStr="",
						_ProcessedBashStr="",
						**_KwargVariablesDict
					):
		
		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)
		
	#<DefineDoMethod>	
	def do_process(self):

		#file
		self.file(ProcessingFileStr+'.sh','w')

		#Define
		ProcessedBashPathStr=self.FolderingPathVariable+ProcessingFileStr+'.txt'

		#set
		self.ProcessedBashStr='OUTPUT="$('+self.ProcessingBashStr+')"\n'
		self.ProcessedBashStr+='echo "${OUTPUT}" > '+ProcessedBashPathStr

		#write
		self.FiledHardVariable.write(
			self.ProcessedBashStr
		)
		self.FiledHardVariable.close()

		#debug
		'''
		self.debug(('self.',self,[
									'FiledPathStr',
								]))
		'''
		
		#popen
		os.popen('sh '+self.FiledPathStr)

		#load
		self.ProcessedBashStr=self.load(	
					**{
						'FilingKeyStr':ProcessingFileStr+'.txt',
						'FilingModeStr':'r'
					}
				).LoadedReadVariable

#</DefineClass>


```

<small>
View the Processer sources on <a href="https://github.com/Ledoux/ShareYourSystem/tree/master/Pythonlogy/ShareYourSystem/Interfacers/Processer" target="_blank">Github</a>
</small>

