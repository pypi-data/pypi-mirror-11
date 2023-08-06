
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


Retriever instances can retrieve InsertedVariablesList given their 
IndexInt of their corresponding table and their RowInt 
(ie their index of their inserted line).

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Modelers.Inserter"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import collections
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class RetrieverClass(BaseClass):
	
	#Definition
	RepresentingKeyStrsList=[
									'RetrievingIndexesList',
									'RetrievedColumnStrToGetStrOrderedDict',
									'RetrievedRowInt',			
									'RetrievedTable', 			
									'RetrievedPickOrderedDict'
								]

	def default_init(self,
						_RetrievingIndexesList=None,
						_RetrievedColumnStrToGetStrOrderedDict=None,
						_RetrievedRowInt=-1,			
						_RetrievedTable=None, 			
						_RetrievedPickOrderedDict=None,		
						**_KwargVariablesDict
			):

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def setModelingDescriptionTuplesList(self,_SettingValueVariable):

		#debug
		'''
		self.debug('Before we call the parent setModelingDescriptionTuplesList method ')
		'''

		#Hook
		BaseClass.setModelingDescriptionTuplesList(self,_SettingValueVariable)

		#Bind with RetrievedColumnStrToGetStrOrderedDict setting
		if self.RetrievedColumnStrToGetStrOrderedDict==None:
			self.RetrievedColumnStrToGetStrOrderedDict=collections.OrderedDict()
		map(
			lambda __ModelingColumnTuple:
			self.RetrievedColumnStrToGetStrOrderedDict.__setitem__(
				__ModelingColumnTuple[1],
				__ModelingColumnTuple[0]
			),
			self.ModelingDescriptionTuplesList
		)

		#Init
		if self.RetrievedPickOrderedDict==None:
			self.RetrievedPickOrderedDict=collections.OrderedDict()

		#debug
		'''
		self.debug(('self.',self,['RetrievedColumnStrToGetStrOrderedDict']))
		'''
		
	ModelingDescriptionTuplesList=property(
									BaseClass.ModelingDescriptionTuplesList.fget,
									setModelingDescriptionTuplesList,
									BaseClass.ModelingDescriptionTuplesList.fdel,
									BaseClass.ModelingDescriptionTuplesList.__doc__
								)
	
	#@Hooker.HookerClass(**{'HookingAfterVariablesList':[{"CallingMethodStr":"table"}]})
	def do_retrieve(self):

		#debug
		'''
		self.debug(
					[
						('self.',self,[
										'TabularedTableKeyStrsList',
										'RetrievingIndexesList'
									])
					]
				)
		'''

		#<NotHook>
		#table first
		self.table()
		#</NotHook>

		#debug
		'''
		self.debug(
					[
						('Ok table is done'),
						('self.',self,['TabularedTablesOrderedDict','TabularedTableKeyStrsList'])
					]
				)
		'''

		#set the RetrievedRowInt
		self.RetrievedRowInt=self.RetrievingIndexesList[1]

		#Definition the RetrievedTable
		self.RetrievedTable=self.TabularedTablesOrderedDict[
			self.TabularedTableKeyStrsList[
				self.RetrievingIndexesList[0]
			]
		]

		#debug
		'''
		self.debug(('self.',self,['RetrievedRowInt','RetrievedTable']))
		'''

		#Definition the RetrievedRowsList
		for __RetrievedRow in self.RetrievedTable.iterrows():
			if __RetrievedRow['RowInt']==self.RetrievedRowInt:

				#debug
				'''
				self.debug('self.RetrievedTable.colnames is '+str(self.RetrievedTable.colnames))
				'''

				#Init
				if self.RetrievedPickOrderedDict==None:
					self.RetrievedPickOrderedDict=collections.OrderedDict()

				#set
				map(
					lambda __ColumnStr:
					self.RetrievedPickOrderedDict.__setitem__(
						self.RetrievedColumnStrToGetStrOrderedDict[__ColumnStr],
						__RetrievedRow[__ColumnStr]
						) if __ColumnStr in self.RetrievedColumnStrToGetStrOrderedDict else None
					,
					self.RetrievedTable.colnames
				)

				#debug
				'''
				self.debug('RetrievedPickOrderedDict is setted')
				'''

		#debug
		'''
		self.debug(
					[
						('self.',self,['RetrievedPickOrderedDict'])
					]
				)
		'''

		#Update
		self.NodePointDeriveNoder.update(
			self.RetrievedPickOrderedDict.items(),
			**{'RestrictingIsBool':True}
		)
		self.NodePointDeriveNoder.RestrictingIsBool=False

		#debug
		'''
		self.debug('Update was done')
		'''

		#<NotHook>
		#Return self
		#return self
		#</NotHook>

#</DefineClass>

```

<small>
View the Retriever sources on <a href="https://github.com/Ledoux/ShareYourSystem/tree/master/Pythonlogy/ShareYourSystem/Databasers/Retriever" target="_blank">Github</a>
</small>

