
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


The Celler defines template of Mardown and Code Cells for readming a Module.

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Guiders.Scriptbooker"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import os
import six
import copy

#</ImportSpecificModules>

#<DefineLocals>
CellingInitDict={
				'metadata': {
								'name': "",
								'signature': ""
							},
				'nbformat': 3,
				'nbformat_minor': 0,
				'worksheets': []
			}

CellingCodeCellDict={
						'cell_type':'code',
						'collapsed': False,
						'input':[],
						'language': "python",
						'metadata': {'slideshow':{'slide_type':"slide"}},
						'prompt_number':0
					}

CellingOutputDict={
						'output_type': "stream",
						'stream': "stdout",
						'text': [														
								]
					}

CellingMarkdownCellDict={
							'source': "", 
							'cell_type': 'markdown', 
							'metadata': {'slideshow':{'slide_type':"slide"}}
						} 
#</DefineLocals>


#<DefineClass>
@DecorationClass()
class CellerClass(BaseClass):
	
	#Definition
	RepresentingKeyStrsList=[
								'CellingTextStr',
								'CellingScriptStr',
								'CelledOutputStr',
								'CelledNoteDict'
							]
						
	def default_init(self,
						_CellingTextStr="",
						_CellingScriptStr="",
						_CelledOutputStr="",
						_CelledNoteDict=None,
						**_KwargVariablesDict
					):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_cell(self):

		#Debug
		'''
		self.debug(
					('self.',self,[
						'FolderingPathVariable',
						#'CellingTextStr'
						]
					)
				)
		'''
		
		#Check Code case
		if self.CellingScriptStr=='Python':
			
			#folder first
			self.folder()

			#Definition the self.CelledOutputStr
			if self.FolderingPathVariable!=os.getcwd()+'/':		
		
				#capture and six method
				self.CapturedPrintStrsList=[]
				self.capture()
				six.exec_(self.CellingTextStr,vars())
				self.CapturingStopBool=True
				self.CelledOutputStr='\n'.join(self.CapturedPrintStrsList)

			else:

				#Avoid the output of the corresponding NameStr because it will do a circular effect...
				self.CelledOutputStr=""


			#Debug
			'''
			self.debug(('self.',self,['CelledOutputStr']))
			'''

			#Return 
			self.CelledNoteDict=dict(
				copy.deepcopy(CellingCodeCellDict),
				**{
					'input':map(	
								lambda __LineStr:
								__LineStr+'\n',
								self.CellingTextStr.replace(
									"#FrozenIsBool True",""
							).replace(
								"#FrozenIsBool False",""
							).replace(
								'\t',
								'    '
							).replace('    \n','\n').split('\n')
						),
						"outputs":[
						dict(
							copy.copy(CellingOutputDict),
								**
								{
									"text":map(	
											lambda __LineStr:
											__LineStr+'\n',
											self.CelledOutputStr.split('\n')
										)
								}
							)
						]
				}
			)

		#Check Markdown case
		elif self.CellingScriptStr=='Markdown':

			self.CelledNoteDict=dict(
				copy.deepcopy(CellingMarkdownCellDict),
				**{
						'source':self.CellingTextStr
				}
			)
	
#</DefineClass>


```

<small>
View the Celler sources on [Github](https://github.com/Ledoux/ShareYourSystem/tree/master/Pythonlogy/ShareYourSystem/Guiders/Celler)
</small>

