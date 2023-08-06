
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


Findoer (sorry Finder is already an important module in python standards, so just to be sure to not override...)
instances helps to find in a hdf5 table RowedVariablesList corresponding to the FindingConditionVariable.

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Modelers.Retriever"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>

#from ShareYourSystem.Functers import Argumenter,Hooker
from ShareYourSystem.Standards.Modelers import Rower
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class FindoerClass(BaseClass):
	
	#Definition
	RepresentingKeyStrsList=[
									'FindingConditionVariable',
									'FoundRowDictsList',			
									'FoundFilterRowDictsList'
								]

	def default_init(self,
					_FindingConditionVariable=None,
					_FoundRowDictsList=None,			
					_FoundFilterRowDictsList=None, 
					_FoundIsBool=False,
					**_KwargVariablesDict
				):

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)
		
	#@Hooker.HookerClass(**{'HookingAfterVariablesList':[{'CallingMethodStr':"table"}]})
	#@Argumenter.ArgumenterClass()
	def do_find(self):

		#debug
		'''
		self.debug(("self.",self,['ModeledKeyStr','FindingConditionVariable']))
		'''

		#<NotHook>
		#table first
		self.table()
		#</NotHook>

		#If the FoundRowedTuplesList was not yet setted
		if self.FoundIsBool==False:

			#debug
			'''
			self.debug('FoundRowDictsList was not yet setted')
			'''

			#Take the first one in the list
			self.FoundRowDictsList=Rower.getRowedDictsListWithTable(
												self.TabularedGroupVariable._f_getChild(
													self.TabularedTableKeyStrsList[0]
												)
											)

			#set
			self.FoundIsBool=True
		
		#debug
		'''
		self.debug(
						[
							("self.",self,['FoundRowDictsList'])
						]
				)
		'''

		#Now find really ! 
		self.FoundFilterRowDictsList=SYS.filterNone(
								SYS.where(
											self.FoundRowDictsList,
											self.FindingConditionVariable
								)
							)

		#debug
		'''
		self.debug(
					[
						'The where is over now',
						("self.",self,['FoundFilterRowDictsList'])
					]

				)
		'''

		#<NotHook>
		#Return self
		#return self
		#</NotHook>

#</DefineClass>


```

<small>
View the Findoer sources on <a href="https://github.com/Ledoux/ShareYourSystem/tree/master/Pythonlogy/ShareYourSystem/Databasers/Findoer" target="_blank">Github</a>
</small>

