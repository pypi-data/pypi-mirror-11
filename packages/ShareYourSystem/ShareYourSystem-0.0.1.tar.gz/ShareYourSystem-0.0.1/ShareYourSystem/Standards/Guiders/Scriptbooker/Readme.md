

<!--
FrozenIsBool False
-->

#Scriptbooker

##Doc
----


>
> The Scriptbooker defines template of Mardown and Code Scriptbooks for readming
a Module.
>
>

----

<small>
View the Scriptbooker notebook on [NbViewer](http://nbviewer.ipython.org/url/sha
reyoursystem.ouvaton.org/Scriptbooker.ipynb)
</small>




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


The Scriptbooker defines template of Mardown and Code Scriptbooks for readming a
Module.

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Guiders.Guider"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import os
Guider=BaseModule
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class ScriptbookerClass(BaseClass):

        #Definition
        RepresentingKeyStrsList=[
'ScriptbookingGuideTuplesList',
'ScriptbookedFileKeyStrsList',
'ScriptbookedNewGuideTuplesList',
'ScriptbookedOldGuideTuplesList'
                                                        ]

        def default_init(self,
                                                _ScriptbookingGuideTuplesList=[
('001','Document','Markdown'),
('002','Github','Markdown'),
#('003','Ouvaton','Markdown')
                                                ],
_ScriptbookedFileKeyStrsList=None,
_ScriptbookedNewGuideTuplesList=None,
_ScriptbookedOldGuideTuplesList=None,
                                                **_KwargVariablesDict
                                        ):

                #Call the parent __init__ method
                BaseClass.__init__(self,**_KwargVariablesDict)

        def do_scriptbook(self):

                #debug
                '''
                self.debug(('self.',self,['FolderedDirKeyStrsList']))
                '''

                #Definition
                self.ScriptbookedFileKeyStrsList=SYS._filter(
                                lambda __DirKeyStr:
                                any(
                                        map(
                                                lambda __ExtensionStr:
                                                __DirKeyStr.endswith(
self.GuidingBookStr+__ExtensionStr
                                                ),
                                                ['.py','.md','.tex']
                                )),
                                self.FolderedDirKeyStrsList
                )

                #Definition
                ScriptbookedPageStrsList=map(
                                                                        lambda
__ScriptbookerScriptbookFileKeyStr:
Guider.GuidingSortStr.join(
__ScriptbookerScriptbookFileKeyStr.split(
        Guider.GuidingSortStr)[1:]
),
self.ScriptbookedFileKeyStrsList
                                                                )

                #set
                self.ScriptbookedSortDict=dict(
zip(ScriptbookedPageStrsList,self.ScriptbookedFileKeyStrsList)
                        )

                #debug
                '''
                self.debug(('self.',self,['ScriptbookedSortDict']))
                '''

                #Check
                if len(self.ScriptbookingGuideTuplesList)>0:

                        #map
                        ScriptbookedGuideTuplesList=map(
                                        lambda __ScriptbookingGuideTuple:
                                        list(__ScriptbookingGuideTuple)+[
__ScriptbookingGuideTuple[1]+self.GuidingBookStr+dict(
Guider.ScriptStrAndExtensionStrTuplesList
                                                )[
__ScriptbookingGuideTuple[2]
                                                ]
                                        ],
                                        self.ScriptbookingGuideTuplesList
                                )

                        #groupby
                        [
                                self.ScriptbookedNewGuideTuplesList,
                                self.ScriptbookedOldGuideTuplesList
                        ]=SYS.groupby(
                                lambda __ScriptbookedGuideTuple:
                                __ScriptbookedGuideTuple[3] not in
self.ScriptbookedSortDict,
                                ScriptbookedGuideTuplesList,
                        )

                        #debug
                        '''
                        self.debug(('self.',self,[
'ScriptbookedNewGuideTuplesList',
'ScriptbookedOldGuideTuplesList'
                                                ]))
                        '''

                        #map a guide for the news
                        map(
                                lambda __ScriptbookingNewGuideTuple:
                                self.guide(__ScriptbookingNewGuideTuple[0],
__ScriptbookingNewGuideTuple[1],
                                                        self.GuidingBookStr,
__ScriptbookingNewGuideTuple[2]),
                                self.ScriptbookedNewGuideTuplesList
                        )

                        #check if we rewrite for the olds
                        map(
                                lambda __ScriptbookingOldGuideTuple:
                                self.close()
                                if "#FrozenIsBool True" in self.load(
                                        _FormatStr='txt',
                                        **{
'FilingKeyStr':self.ScriptbookedSortDict[
                                                __ScriptbookingOldGuideTuple[3]
                                                ],
                                                'FilingModeStr':'r'
                                        }).LoadedReadVariable
                                else self.close().guide(
__ScriptbookingOldGuideTuple[0],
__ScriptbookingOldGuideTuple[1],
                                                        self.GuidingBookStr,
__ScriptbookingOldGuideTuple[2],
                                                ),
                                self.ScriptbookedOldGuideTuplesList
                        )

                #Return self
                #return self

#</DefineClass>


```

<small>
View the Scriptbooker sources on [Github](https://github.com/Ledoux/ShareYourSys
tem/tree/master/Pythonlogy/ShareYourSystem/Guiders/Scriptbooker)
</small>




<!---
FrozenIsBool True
-->

##Example

Let's create an empty class, which will automatically receive
special attributes from the decorating ClassorClass,
specially the NameStr, that should be the ClassStr
without the TypeStr in the end.

```python

#ImportModules
import ShareYourSystem as SYS
from ShareYourSystem.Guiders import Scriptbooker

#Definition of a Scriptbooker
MyScriptbooker=Scriptbooker.ScriptbookerClass(
    ).package(
        "ShareYourSystem.Standards.Objects.Object"
    ).scriptbook(
        **{
            'GuidingBookStr':'Doc'
        }
    )

#Definition the AttestedStr
SYS._attest(
    [
        'MyScriptbooker is '+SYS._str(
                MyScriptbooker,
                **{
                'RepresentingBaseKeyStrsListBool':False,
                'RepresentingAlineaIsBool':False
                }
        )
    ]
)

#Print



```


```console
>>>


*****Start of the Attest *****

MyScriptbooker is < (ScriptbookerClass), 4537302480>
   /{
   /  '<New><Instance>IdInt' : 4537302480
   /  '<New><Instance>ScriptbookedSortDict' :
   /   /{
   /   /  'DocumentDoc.md' : 001_DocumentDoc.md
   /   /  'ExampleDoc.md' : 00_ExampleDoc.md
   /   /  'ExampleDoc.py' : 01_ExampleDoc.py
   /   /  'GithubDoc.md' : 002_GithubDoc.md
   /   /}
   /  '<Spe><Class>ScriptbookingGuideTuplesList' :
   /   /[
   /   /  0 : ('001', 'Document', 'Markdown')
   /   /  1 : ('002', 'Github', 'Markdown')
   /   /]
   /  '<Spe><Instance>ScriptbookedFileKeyStrsList' : ['001_DocumentDoc.md',
'002_GithubDoc.md', '00_ExampleDoc.md', '01_ExampleDoc.py']
   /  '<Spe><Instance>ScriptbookedNewGuideTuplesList' : []
   /  '<Spe><Instance>ScriptbookedOldGuideTuplesList' :
   /   /[
   /   /  0 : ['001', 'Document', 'Markdown', 'DocumentDoc.md']
   /   /  1 : ['002', 'Github', 'Markdown', 'GithubDoc.md']
   /   /]
   /}

*****End of the Attest *****



```

