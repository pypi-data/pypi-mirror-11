
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


Organizer instances

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Noders.Structurer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
from ShareYourSystem.Standards.Modelers import Modeler
from ShareYourSystem.Standards.Noders import Noder
import operator
#</ImportSpecificModules>

#<DefineLocals>
#</DefineLocals>

#<DefineClass>
@DecorationClass(**{
	'ClassingSwitchMethodStrsList':['organize']
})
class OrganizerClass(BaseClass):
	
	#Definition
	RepresentingKeyStrsList=[
								'OrganizingModelsCollectionStr',
								'OrganizingComponentsCollectionStr',
								'OrganizingOutKeyStrsList',
								'OrganizingInKeyStrsList',
								'OrganizingOutStr',
								'OrganizingInStr',
								'OrganizedTopDeriveDatabaserVariable',
								'OrganizedInstallIsBool',
								'OrganizedDataGetStr',
								'OrganizedComponentsGetStr',
								'OrganizedDataGetStr',
								'OrganizedComponentsGetStr',
								'OrganizedInConnectAttentionGetStrsList',
								'OrganizedOutConnectAttentionGetStrsList'
							]

	def default_init(self,
						_OrganizingModelsCollectionStr="Data",
						_OrganizingComponentsCollectionStr="Component",
						_OrganizingOutKeyStrsList=None,
						_OrganizingInKeyStrsList=None,
						_OrganizingOutStr="Results",
						_OrganizingInStr="Parameters",
						_OrganizedTopDeriveDatabaserVariable=None,
						_OrganizedInstallIsBool=False,
						_OrganizedDataGetStr="",
						_OrganizedComponentsGetStr="",
						_OrganizedInConnectAttentionGetStrsList=None,
						_OrganizedOutConnectAttentionGetStrsList=None,
						_OrganizedComponentCollectionOrderedDict=None,
						**_KwargVariablesDict
					):

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_organize(self):

		#Check
		if len(self.OrganizingInKeyStrsList)==0:
			self.OrganizingInKeyStrsList=self.__class__.DoingAttributeVariablesOrderedDict.keys()
		if len(self.OrganizingOutKeyStrsList)==0:
			self.OrganizingOutKeyStrsList=self.__class__.DoneAttributeVariablesOrderedDict.keys()

		#set
		self.OrganizedDataGetStr=Noder.NodingPrefixGetStr+self.OrganizingModelsCollectionStr+Noder.NodingSuffixGetStr
		self.OrganizedComponentsGetStr=Noder.NodingPrefixGetStr+self.OrganizingComponentsCollectionStr+Noder.NodingSuffixGetStr

		#Make the hierarchical joins for the ins 
		self.OrganizedInConnectAttentionGetStrsList=map(
				lambda __DeriveNoder:
				'/NodePointDeriveNoder/'+self.OrganizedComponentsGetStr+__DeriveNoder.NodeKeyStr+'/'+self.OrganizedDataGetStr+self.OrganizingInStr+'Hierarchizer',
				self[self.OrganizedComponentsGetStr]
			)

		#Set
		self.OrganizedComponentCollectionOrderedDict=getattr(
			self,
			self.OrganizingComponentsCollectionStr+'CollectionOrderedDict'
		)

		#map
		self.OrganizedOutConnectAttentionGetStrsList=[
				'/NodePointDeriveNoder/'+self.OrganizedDataGetStr+self.OrganizingInStr+'Hierarchizer'
		]

		#debug
		'''
		self.debug(
					('self.',self,[
									'OrganizedInConnectAttentionGetStrsList',
									'OrganizedOutConnectAttentionGetStrsList'
								])
			)
		'''

		#import
		from ShareYourSystem.Standards.Modelers import Hierarchizer

		#Set a parameters and a results database
		self.push(
				[
					(
						self.OrganizingInStr,
						Hierarchizer.HierarchizerClass().update(
							[
								(
									'Attr_ModelingDescriptionTuplesList',
									map(
										Modeler.getModelingColumnTupleWithGetKeyStr,
										self.OrganizingInKeyStrsList
									)
								),
								(
									'Attr_RowingKeyStrsList',
									self.__class__.DoingAttributeVariablesOrderedDict.keys()
								),
								(
									'ConnectingGraspClueVariablesList',
									self.OrganizedInConnectAttentionGetStrsList
								)
							]
						)
					),
					(
						self.OrganizingOutStr,
						Hierarchizer.HierarchizerClass().update(
							[
								(
									'Attr_ModelingDescriptionTuplesList',
									map(
										Modeler.getModelingColumnTupleWithGetKeyStr,
										self.OrganizingOutKeyStrsList
									)
								),
								(
									'ConnectingGraspClueVariablesList',
									self.OrganizedOutConnectAttentionGetStrsList
								),
								('TagStr','Networked')
							]
						)
					)
				],
			**{'CollectingCollectionStr':self.OrganizingModelsCollectionStr}
		)

		#set
		self.OrganizedTopDeriveDatabaserVariable=getattr(
				self,
				self.OrganizingModelsCollectionStr+'CollectionOrderedDict'
			).values()[-1]
#</DefineClass>


```

<small>
View the Organizer sources on <a href="https://github.com/Ledoux/ShareYourSystem/tree/master/Pythonlogy/ShareYourSystem/Noders/Organizer" target="_blank">Github</a>
</small>

