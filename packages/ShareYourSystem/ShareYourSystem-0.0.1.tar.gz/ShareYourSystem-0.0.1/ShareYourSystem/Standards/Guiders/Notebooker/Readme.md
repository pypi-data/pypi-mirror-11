

<!--
FrozenIsBool False
-->

#Notebooker

##Doc
----


>
> The Notebooker takes piece of .md,.py,.tex files for putting them in a IPython
Notebook
>
>

----

<small>
View the Notebooker notebook on [NbViewer](http://nbviewer.ipython.org/url/share
yoursystem.ouvaton.org/Notebooker.ipynb)
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


The Notebooker takes piece of .md,.py,.tex files for putting them in a IPython
Notebook

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
                                                lambda
__NotebookedTextStr,__NotebookedScriptStr,__IndexInt:
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
                                        lambda
__NotebookedPageStr,__PageIndexInt:
                                        'slide'
                                        if  __PageIndexInt==0
                                        else
                                        'subslide'
                                        if
self.NotebookedPageStrsList[__PageIndexInt-1]!=__NotebookedPageStr
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
View the Notebooker sources on <a href="https://github.com/Ledoux/ShareYourSyste
m/tree/master/Pythonlogy/ShareYourSystem/Guiders/Notebooker"
target="_blank">Github</a>
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
from ShareYourSystem.Guiders import Notebooker

#Definition a Notebooker
MyNotebooker=Notebooker.NotebookerClass(
    ).package(
        'ShareYourSystem.Standards.Objects.Concluder'
    ).scriptbook(
        **{
            'GuidingBookStr':'Doc'
        }
    ).notebook(
        'Presentation.ipynb'
)

#Definition the AttestedStr
SYS._attest(
    [
        'MyNotebooker is '+SYS._str(
        MyNotebooker,
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

MyNotebooker is < (NotebookerClass), 4540557456>
   /{
   /  '<New><Instance>IdInt' : 4540557456
   /  '<New><Instance>NotebookedScriptStrsList' : ['Markdown', 'Markdown',
'Markdown', 'Python']
   /  '<New><Instance>ScriptbookedSortDict' :
   /   /{
   /   /  'DocumentDoc.md' : 001_DocumentDoc.md
   /   /  'ExampleDoc.md' : 00_ExampleDoc.md
   /   /  'ExampleDoc.py' : 01_ExampleDoc.py
   /   /  'GithubDoc.md' : 002_GithubDoc.md
   /   /}
   /  '<New><Instance>_CapturingStopBool' : True
   /  '<Spe><Class>NotebookingWriteBool' : True
   /  '<Spe><Instance>NotebookedCodeDict' :
   /   /{
   /   /  'metadata' :
   /   /   /{
   /   /   /  'name' :
   /   /   /  'signature' :
   /   /   /}
   /   /  'nbformat' : 3
   /   /  'nbformat_minor' : 0
   /   /  'worksheets' :
   /   /   /[
   /   /   /  0 :
   /   /   /   /{
   /   /   /   /  'cells' :
   /   /   /   /   /[
   /   /   /   /   /  0 :
   /   /   /   /   /   /{
   /   /   /   /   /   /  'cell_type' : markdown
   /   /   /   /   /   /  'metadata' :
   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /  'slideshow' :
   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /  'slide_type' : slide
   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /}
   /   /   /   /   /   /  'prompt_number' : 0
   /   /   /   /   /   /  'source' :
<!--
FrozenIsBool False
-->

#Concluder

##Doc
----


>
> A Concluder
>
>

----

<small>
View the Concluder notebook on [NbViewer](http://nbviewer.ipython.org/url/sharey
oursystem.ouvaton.org/Concluder.ipynb)
</small>


   /   /   /   /   /   /}
   /   /   /   /   /  1 :
   /   /   /   /   /   /{
   /   /   /   /   /   /  'cell_type' : markdown
   /   /   /   /   /   /  'metadata' :
   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /  'slideshow' :
   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /  'slide_type' : subslide
   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /}
   /   /   /   /   /   /  'prompt_number' : 1
   /   /   /   /   /   /  'source' :
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


A Concluder

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Objects.Conditioner"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Tester"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class ConcluderClass(BaseClass):

        #Definition
        RepresentingKeyStrsList=[
'ConcludingTestVariable',
'ConcludingConditionVariable',
'ConcludedConditionIsBoolsList',
'ConcludedIsBool'
                                                                ]

        def default_init(self,
                                _ConcludingTestVariable=None,
                                _ConcludingConditionVariable=None,
                                _ConcludedConditionIsBoolsList=None,
                                _ConcludedIsBool=True,
                                **_KwargVariablesDict
                                ):

                #Call the parent init method
                BaseClass.__init__(self,**_KwargVariablesDict)

        def do_conclude(self):
                """ """

                #debug
                '''
                self.debug(('self.',self,['ConcludingConditionVariable']))
                '''

                #Apply __getitem__
                self.ConcludedConditionIsBoolsList=map(
                                lambda __ConcludingConditionTuple:
                                self.condition(
                                                self.ConcludingTestVariable[
__ConcludingConditionTuple[0]
                                                ] if type(
__ConcludingConditionTuple[0])
                                                in SYS.StrTypesList else
__ConcludingConditionTuple[0],
                                                __ConcludingConditionTuple[1],
                                                __ConcludingConditionTuple[2]
                                        ).ConditionedIsBool,
                                self.ConcludingConditionVariable
                        )

                #all
                self.ConcludedIsBool=all(self.ConcludedConditionIsBoolsList)

                #Return self
                #return self
#</DefineClass>

```

<small>
View the Concluder sources on <a href="https://github.com/Ledoux/ShareYourSystem
/tree/master/Pythonlogy/ShareYourSystem/Objects/Concluder"
target="_blank">Github</a>
</small>


   /   /   /   /   /   /}
   /   /   /   /   /  2 :
   /   /   /   /   /   /{
   /   /   /   /   /   /  'cell_type' : markdown
   /   /   /   /   /   /  'metadata' :
   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /  'slideshow' :
   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /  'slide_type' : subslide
   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /}
   /   /   /   /   /   /  'prompt_number' : 2
   /   /   /   /   /   /  'source' :
<!---
FrozenIsBool True
-->

##Example

Let's do a simple conclude call
   /   /   /   /   /   /}
   /   /   /   /   /  3 :
   /   /   /   /   /   /{
   /   /   /   /   /   /  'cell_type' : code
   /   /   /   /   /   /  'collapsed' : False
   /   /   /   /   /   /  'input' : ['\n', '#ImportModules\n', 'import
ShareYourSystem as SYS\n', 'from ShareYourSystem.Standards.Objects import Concluder\n',
'import operator\n', '\n', '#Definition of an instance Concluder and make it
print hello\n', 'MyConcluder=Concluder.ConcluderClass().conclude(\n', "
{'MyColorStr':'Black','MySuperInt':6},\n", '    [\n', '
(\'MyColorStr\',operator.eq,"Black"),\n', "
('MySuperInt',operator.gt,3),\n", '        (1,operator.eq,1)\n', '    ]\n',
')\n', '    \n', '#Definition the AttestedStr\n', 'SYS._attest(\n', '    [\n', "
'MyConcluder is '+SYS._str(\n", '        MyConcluder,\n', '        **{\n', "
'RepresentingBaseKeyStrsListBool':False,\n", "
'RepresentingAlineaIsBool':False\n", '            }\n', '        ),\n', '
]\n', ') \n', '\n', '#Print\n', '\n', '\n', '\n', '\n', '\n']
   /   /   /   /   /   /  'language' : python
   /   /   /   /   /   /  'metadata' :
   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /  'slideshow' :
   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /  'slide_type' : -
   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /}
   /   /   /   /   /   /  'outputs' :
   /   /   /   /   /   /   /[
   /   /   /   /   /   /   /  0 :
   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /  'output_type' : stream
   /   /   /   /   /   /   /   /  'stream' : stdout
   /   /   /   /   /   /   /   /  'text' : ['\n', '\n', '*****Start of the
Attest *****\n', '\n', 'MyConcluder is < (ConcluderClass), 4540622864>\n', '
/{ \n', "   /  '<New><Instance>IdInt' : 4540622864\n", "   /
'<Spe><Instance>ConcludedConditionIsBoolsList' : \n", '   /   /[\n', '   /   /
0 : True\n', '   /   /  1 : True\n', '   /   /  2 : True\n', '   /   /]\n', "
/  '<Spe><Instance>ConcludedIsBool' : True\n", "   /
'<Spe><Instance>ConcludingConditionVariable' : \n", '   /   /[\n', '   /   /
0 : \n', '   /   /   /(\n', '   /   /   /  0 : MyColorStr\n', '   /   /   /  1 :
<built-in function eq>\n', '   /   /   /  2 : Black\n', '   /   /   /)\n', '   /
/  1 : \n', '   /   /   /(\n', '   /   /   /  0 : MySuperInt\n', '   /   /   /
1 : <built-in function gt>\n', '   /   /   /  2 : 3\n', '   /   /   /)\n', '   /
/  2 : \n', '   /   /   /(\n', '   /   /   /  0 : 1\n', '   /   /   /  1 :
{...}< (builtin_function_or_method), 4522748384>\n', '   /   /   /  2 : 1\n', '
/   /   /)\n', '   /   /]\n', "   /  '<Spe><Instance>ConcludingTestVariable' :
\n", '   /   /{ \n', "   /   /  'MyColorStr' : Black\n", "   /   /  'MySuperInt'
: 6\n", '   /   /}\n', '   /}\n', '\n', '*****End of the Attest *****\n', '\n',
'\n']
   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /]
   /   /   /   /   /   /  'prompt_number' : 3
   /   /   /   /   /   /}
   /   /   /   /   /]
   /   /   /   /}
   /   /   /]
   /   /}
   /  '<Spe><Instance>NotebookedPageStrsList' : ['DocumentDoc', 'GithubDoc',
'ExampleDoc', 'ExampleDoc']
   /  '<Spe><Instance>NotebookedSubslideStrsList' : ['slide', 'subslide',
'subslide', '-']
   /  '<Spe><Instance>NotebookedTextStrsList' : ['\n<!--\nFrozenIsBool
False\n-->\n\n#Concluder\n\n##Doc\n----\n\n\n> \n> A Concluder\n> \n>
\n\n----\n\n<small>\nView the Concluder notebook on [NbViewer](http://nbviewer.i
python.org/url/shareyoursystem.ouvaton.org/Concluder.ipynb)\n</small>\n\n',
'\n<!--\nFrozenIsBool
False\n-->\n\n##Code\n\n----\n\n<ClassDocStr>\n\n----\n\n```python\n# -*-
coding: utf-8 -*-\n"""\n\n\n<DefineSource>\n@Date : Fri Nov 14 13:20:38 2014
\\n\n@Author : Erwan Ledoux \\n\\n\n</DefineSource>\n\n\nA
Concluder\n\n"""\n\n#<DefineAugmentation>\nimport ShareYourSystem as SYS\nBaseMo
duleStr="ShareYourSystem.Standards.Objects.Conditioner"\nDecorationModuleStr="ShareYourSys
tem.Classors.Tester"\nSYS.setSubModule(globals())\n#</DefineAugmentation>\n\n#<I
mportSpecificModules>\n#</ImportSpecificModules>\n\n#<DefineClass>\n@DecorationC
lass()\nclass ConcluderClass(BaseClass):\n\t\n\t#Definition\n\tRepresentingKeySt
rsList=[\n\t\t\t\t\t\t\t\t\t\'ConcludingTestVariable\',\n\t\t\t\t\t\t\t\t\t\'Con
cludingConditionVariable\',\n\t\t\t\t\t\t\t\t\t\'ConcludedConditionIsBoolsList
\',\n\t\t\t\t\t\t\t\t\t\'ConcludedIsBool\'\n\t\t\t\t\t\t\t\t]\n\n\tdef default_i
nit(self,\n\t\t\t\t_ConcludingTestVariable=None,\n\t\t\t\t_ConcludingConditionTu
plesList=None,\n\t\t\t\t_ConcludedConditionIsBoolsList=None,\n\t\t\t\t_Concluded
IsBool=True,\n\t\t\t\t**_KwargVariablesDict\n\t\t\t\t):\n\n\t\t#Call the parent
init method\n\t\tBaseClass.__init__(self,**_KwargVariablesDict)\n\n\tdef
do_conclude(self):\n\t\t""" """\n\n\t\t#debug\n\t\t\'\'\'\n\t\tself.debug((\'sel
f.\',self,[\'ConcludingConditionVariable\']))\n\t\t\'\'\'\n\t\t\n\t\t#Apply
__getitem__\n\t\tself.ConcludedConditionIsBoolsList=map(\n\t\t\t\tlambda __Concl
udingConditionTuple:\n\t\t\t\tself.condition(\n\t\t\t\t\t\tself.ConcludingTestVa
riable[\n\t\t\t\t\t\t\t__ConcludingConditionTuple[0]\n\t\t\t\t\t\t] if
type(\n\t\t\t\t\t\t\t__ConcludingConditionTuple[0])\n\t\t\t\t\t\tin
SYS.StrTypesList else __ConcludingConditionTuple[0],\n\t\t\t\t\t\t__ConcludingCo
nditionTuple[1],\n\t\t\t\t\t\t__ConcludingConditionTuple[2]\n\t\t\t\t\t).Conditi
onedIsBool,\n\t\t\t\tself.ConcludingConditionVariable\n\t\t\t)\n\n\t\t#all\n\t
\tself.ConcludedIsBool=all(self.ConcludedConditionIsBoolsList)\n\n\t\t#Return
self\n\t\t#return self\n#</DefineClass>\n\n```\n\n<small>\nView the Concluder
sources on <a href="https://github.com/Ledoux/ShareYourSystem/tree/master/Python
logy/ShareYourSystem/Objects/Concluder"
target="_blank">Github</a>\n</small>\n\n', "\n<!---\nFrozenIsBool
True\n-->\n\n##Example\n\nLet's do a simple conclude call",
'\n#ImportModules\nimport ShareYourSystem as SYS\nfrom ShareYourSystem.Standards.Objects
import Concluder\nimport operator\n\n#Definition of an instance Concluder and
make it print hello\nMyConcluder=Concluder.ConcluderClass().conclude(\n\t{\'MyCo
lorStr\':\'Black\',\'MySuperInt\':6},\n\t[\n\t\t(\'MyColorStr\',operator.eq,"Bla
ck"),\n\t\t(\'MySuperInt\',operator.gt,3),\n\t\t(1,operator.eq,1)\n\t]\n)\n\t\t\
n#Definition the AttestedStr\nSYS._attest(\n\t[\n\t\t\'MyConcluder is \'+SYS._st
r(\n\t\tMyConcluder,\n\t\t**{\n\t\t\t\'RepresentingBaseKeyStrsListBool\':False,\
n\t\t\t\'RepresentingAlineaIsBool\':False\n\t\t\t}\n\t\t),\n\t]\n)
\n\n#Print\n\n\n\t\n\n']
   /  '<Spe><Instance>NotebookingFileKeyStr' : Presentation.ipynb
   /}

*****End of the Attest *****



```

