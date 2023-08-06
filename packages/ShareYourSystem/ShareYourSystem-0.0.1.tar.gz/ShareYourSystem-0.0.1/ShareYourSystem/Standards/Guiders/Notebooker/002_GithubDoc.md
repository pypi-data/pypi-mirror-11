
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


The Notebooker takes piece of .md,.py,.tex files for putting them in a IPython Notebook

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Guiders.Celler"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import copy
import os
import sys

from ShareYourSystem.Standards.Interfacers import Filer,Loader
from ShareYourSystem.Guiders import Guider
import importlib
Celler=BaseModule
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class NotebookerClass(BaseClass):
	
	#Definition
	RepresentingKeyStrsList=[
								'NotebookingFileKeyStr',
								'NotebookingWriteBool',
								'NotebookedTextStrsList',
								'NotebookedCodeDict',
								'NotebookedPageStrsList',
								'NotebookedSubslideStrsList'
							]

	def default_init(self,
						_NotebookingFileKeyStr="",
						_NotebookingWriteBool=True,
						_NotebookedTextStrsList=None,
						_NotebookedCodeDict=None,
						_NotebookedPageStrsList=None,
						_NotebookedSubslideStrsList=None,
						**_KwargVariablesDict
					):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_notebook(self):
		
		#debug
		'''
		self.debug(('self.',self,['NotebookingFileKeyStr']))
		'''

		#Check
		if self.NotebookingFileKeyStr!="":
			
			#debug
			'''
			self.debug(('self.',self,['ScriptbookedSortDict']))
			'''

			#map
			self.NotebookedTextStrsList=map(
					lambda __ScriptbookedFileKeyStr:
					self.load(**{
									'FilingKeyStr':__ScriptbookedFileKeyStr
								}
					).LoadedReadVariable,
					sorted(self.ScriptbookedSortDict.values())
				)

			#map
			self.NotebookedScriptStrsList=map(
					lambda __ScriptbookedFileKeyStr:
					SYS.flip(
						dict(
									Guider.ScriptStrAndExtensionStrTuplesList
							)
					)[
						'.'+__ScriptbookedFileKeyStr.split('.')[-1]
					],
					sorted(self.ScriptbookedSortDict.values())
				)

			#debug
			'''
			self.debug(('self.',self,[
					'NotebookedTextStrsList',
					'NotebookedScriptStrsList'
				]))
			'''

			#Update
			self.LoadingFormatStr='json'

			#file first
			self.file(
						self.NotebookingFileKeyStr,
						'w'
					)

			#Copy
			self.NotebookedCodeDict=copy.copy(Celler.CellingInitDict)

			#Fill the cells
			self.NotebookedCodeDict['worksheets']=[
				{
					'cells':map(
						lambda __NotebookedTextStr,__NotebookedScriptStr,__IndexInt:
							dict(
								self.cell(
									__NotebookedTextStr,
									__NotebookedScriptStr
								).CelledNoteDict,
								**{
									'prompt_number':__IndexInt,
								}
							),
							self.NotebookedTextStrsList,
							self.NotebookedScriptStrsList,
							xrange(len(self.NotebookedTextStrsList))
						)
				}
			]

			#map
			self.NotebookedPageStrsList=map(
					lambda __FileKeyStr:
					Guider.GuidingSortStr.join(
						__FileKeyStr.split('.')[0].split(
							Guider.GuidingSortStr
						)[1:]
					),
					sorted(self.ScriptbookedSortDict.values())
				)

			#map
			self.NotebookedSubslideStrsList=map(
					lambda __NotebookedPageStr,__PageIndexInt:
					'slide'
					if  __PageIndexInt==0
					else
					'subslide' 
					if self.NotebookedPageStrsList[__PageIndexInt-1]!=__NotebookedPageStr
					else '-',
					self.NotebookedPageStrsList,
					xrange(len(self.NotebookedPageStrsList))
				)

			#debug
			'''
			self.debug(
				[
					('self.',self,['NotebookedSubslideStrsList']),
					"self.NotebookedCodeDict['worksheets'][0]['cells'] is "+SYS._str(
						self.NotebookedCodeDict['worksheets'][0]['cells'])
				]
			)
			'''

			#Specify the page/slide
			map(
				lambda __CellDict,__NotebookedSubslideStr:
				__CellDict['metadata']['slideshow'].__setitem__(
						"slide_type",
						__NotebookedSubslideStr
					)
				,
				self.NotebookedCodeDict['worksheets'][0]['cells'],
				self.NotebookedSubslideStrsList
			)

			#debug
			'''
			self.debug(
				[
					"self.NotebookedCodeDict['worksheets'][0]['cells'] is "+SYS._str(
						self.NotebookedCodeDict['worksheets'][0]['cells'])
				]
			)
			'''

			#debug
			'''
			self.debug(
						('self.',self,[
											'NotebookingWriteBool',
											'NotebookedCodeDict',
										])
					)
			'''

			#Check
			if self.NotebookingWriteBool:

				#debug
				'''
				self.debug(
							('self.',self,[
												'FolderingPathVariable',
												'FilingKeyStr',
												'LoadingFormatStr'
											])
						)
				'''

				#Write
				self.write(self.NotebookedCodeDict)

				#Close
				self.FiledHardVariable.close()


		#Return self
		#return self
	
#</DefineClass>


```

<small>
View the Notebooker sources on <a href="https://github.com/Ledoux/ShareYourSystem/tree/master/Pythonlogy/ShareYourSystem/Guiders/Notebooker" target="_blank">Github</a>
</small>

