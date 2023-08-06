

<!--
FrozenIsBool False
-->

#Celler

##Doc
----


>
> The Celler defines template of Mardown and Code Cells for readming a Module.
>
>

----

<small>
View the Celler notebook on [NbViewer](http://nbviewer.ipython.org/url/shareyour
system.ouvaton.org/Celler.ipynb)
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
                                                'metadata':
{'slideshow':{'slide_type':"slide"}},
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
                                                        'metadata':
{'slideshow':{'slide_type':"slide"}}
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

                                #Avoid the output of the corresponding NameStr
because it will do a circular effect...
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
                                                                lambda
__LineStr:
                                                                __LineStr+'\n',
self.CellingTextStr.replace(
"#FrozenIsBool True",""
                                                        ).replace(
                                                                "#FrozenIsBool
False",""
                                                        ).replace(
                                                                '\t',
                                                                '    '
                                                        ).replace('
\n','\n').split('\n')
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
View the Celler sources on [Github](https://github.com/Ledoux/ShareYourSystem/tr
ee/master/Pythonlogy/ShareYourSystem/Guiders/Celler)
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
from ShareYourSystem.Guiders import Celler

#Definition an instance
MyCeller=Celler.CellerClass().load(
    **{
        'FolderingPathVariable':
        SYS.ShareYourSystemLocalFolderPathStr+'Pythonlogy/ShareYourSystem/Object
s/Rebooter',
        'FilingKeyStr':'01_ExampleDoc.py'
    }
)
MyCeller.cell(MyCeller.LoadedReadVariable,'Python')

#Definition the AttestedStr
SYS._attest(
    [
        'MyCeller is '+SYS._str(
                MyCeller,
                **{
                'RepresentingBaseKeyStrsListBool':False,
                'RepresentingAlineaIsBool':False
                }
            )
    ]
)



```


```console
>>>


*****Start of the Attest *****

MyCeller is < (CellerClass), 4540557072>
   /{
   /  '<New><Instance>IdInt' : 4540557072
   /  '<New><Instance>_CapturingStopBool' : True
   /  '<Spe><Instance>CelledNoteDict' :
   /   /{
   /   /  'cell_type' : code
   /   /  'collapsed' : False
   /   /  'input' : ['#ImportModules\n', 'import ShareYourSystem as SYS\n',
'from ShareYourSystem.Standards.Classors import Classer\n', 'from ShareYourSystem.Standards.Objects
import Rebooter\n', '\n', '#Definition \n', '@Classer.ClasserClass(**\n', '{\n',
"    'ClassingSwitchMethodStrsList':['make']\n", '})\n', 'class
MakerClass(Rebooter.RebooterClass):\n', '\n', '    #Definition\n', '
RepresentingKeyStrsList=[\n', "
'MakingMyFloat',\n", "                                'MadeMyInt'\n", '
]\n', '\n', '    def default_init(self,\n', '
_MakingMyFloat=0.,\n', '                    _MadeMyInt=0,\n', '
**_KwarVariablesDict\n', '                ):\n', '
Rebooter.RebooterClass.__init__(self,**_KwarVariablesDict)\n', '\n', '    def
do_make(self):\n', '    \n', '        #print\n', "        print('I am in the
do_make of the Maker')\n", '\n', '        #cast\n', '
self.MadeMyInt=int(self.MakingMyFloat)\n', '\n', '#Definition\n',
'@Classer.ClasserClass(**{\n', '
\'ClassingSwitchMethodStrsList\':["make"]\n', '})\n', 'class
BuilderClass(MakerClass):\n', '\n', '    #Definition\n', '
RepresentingKeyStrsList=[\n', '                            ]\n', '\n', '    def
default_init(self,\n', '                    **_KwarVariablesDict\n', '
):\n', '        MakerClass.__init__(self,**_KwarVariablesDict)\n', '\n', '
def mimic_make(self):\n', '    \n', '        #print\n', "        print('I am in
the mimic_make of the Builder')\n", '\n', '        #call the parent method\n', '
MakerClass.make(self)\n', '\n', '        #cast\n', '
self.MadeMyInt+=10\n', '\n', '    def do_build(self):\n', '        pass\n',
'\n', '\n', '#Definition an instance\n', 'MyBuilder=BuilderClass()\n', '\n',
'#Print\n', "print('Before make, MyBuilder is ')\n",
'SYS._print(MyBuilder,**{\n', "    'RepresentingKeyStrsList':[\n", "
'MakingMyFloat',\n", "    'MadeMyInt',\n", '    ]\n', '})\n', '\n', '#make
once\n', 'MyBuilder.make(3.)\n', '\n', '#Print\n', "print('After the first make,
MyBuilder is ')\n", 'SYS._print(MyBuilder,**{\n', "
'RepresentingKeyStrsList':[\n", "    'MakingMyFloat',\n", "    'MadeMyInt',\n",
'    ]\n', '})\n', '\n', '#make again\n', 'MyBuilder.make(5.)\n', '\n',
'#Print\n', "print('After the second make, MyBuilder is ')\n",
'SYS._print(MyBuilder,**{\n', "    'RepresentingKeyStrsList':[\n", "
'MakingMyFloat',\n", "    'MadeMyInt',\n", '    ]\n', '})\n', '\n', '#make
again\n', "print('Now we reboot')\n", 'MyBuilder.reboot(\n', "
#_NameStrsList=['Maker','Builder'],\n", "
#_DoStrsList=['Make'],\n", '                    #_AllDoBool=True,\n', '
#_AllNameBool=True,\n', '                )\n', '\n', '#Print\n', "print('After
the reboot, MyBuilder is ')\n", 'SYS._print(MyBuilder,**{\n', "
'RepresentingKeyStrsList':[\n", "    'MakingMyFloat',\n", "    'MadeMyInt',\n",
'    ]\n', '})\n', '\n', '#make again\n', 'MyBuilder.make(8.)\n', '\n',
'#Definition the AttestedStr\n', 'SYS._attest(\n', '    [\n', "
'MyBuilder is '+SYS._str(\n", '        MyBuilder,\n', '        **{\n', "
'RepresentingAlineaIsBool':False,\n", "
'RepresentingKeyStrsList':[\n", "                'MakingMyFloat',\n", "
'MadeMyInt',\n", "                'RebootedWatchBoolKeyStrsList'\n", '
]\n', '            }\n', '        )\n', '    ]\n', ') \n']
   /   /  'language' : python
   /   /  'metadata' :
   /   /   /{
   /   /   /  'slideshow' :
   /   /   /   /{
   /   /   /   /  'slide_type' : slide
   /   /   /   /}
   /   /   /}
   /   /  'outputs' :
   /   /   /[
   /   /   /  0 :
   /   /   /   /{
   /   /   /   /  'output_type' : stream
   /   /   /   /  'stream' : stdout
   /   /   /   /  'text' : ['Before make, MyBuilder is \n', '< (BuilderClass),
4540177488>\n', '   /{ \n', "   /  '<Base><Class>MadeMyInt' : 0\n", "   /
'<Base><Class>MakingMyFloat' : 0.0\n", "   /  '<New><Instance>IdInt' :
4540177488\n", '   /}\n', 'I am in the mimic_make of the Builder\n', 'I am in
the do_make of the Maker\n', 'After the first make, MyBuilder is \n', '<
(BuilderClass), 4540177488>\n', '   /{ \n', "   /  '<New><Instance>IdInt' :
4540177488\n", "   /  '<Spe><Instance>MadeMyInt' : 13\n", "   /
'<Spe><Instance>MakingMyFloat' : 3.0\n", '   /}\n', 'After the second make,
MyBuilder is \n', '< (BuilderClass), 4540177488>\n', '   /{ \n', "   /
'<New><Instance>IdInt' : 4540177488\n", "   /  '<Spe><Instance>MadeMyInt' :
13\n", "   /  '<Spe><Instance>MakingMyFloat' : 3.0\n", '   /}\n', 'Now we
reboot\n', 'After the reboot, MyBuilder is \n', '< (BuilderClass),
4540177488>\n', '   /{ \n', "   /  '<New><Instance>IdInt' : 4540177488\n", "   /
'<Spe><Instance>MadeMyInt' : 0\n", "   /  '<Spe><Instance>MakingMyFloat' :
3.0\n", '   /}\n', 'I am in the mimic_make of the Builder\n', 'I am in the
do_make of the Maker\n', '\n', '\n', '*****Start of the Attest *****\n', '\n',
'MyBuilder is < (BuilderClass), 4540177488>\n', '   /{ \n', "   /
'<New><Instance>IdInt' : 4540177488\n", "   /  '<Spe><Instance>MadeMyInt' :
18\n", "   /  '<Spe><Instance>MakingMyFloat' : 8.0\n", "   /
'<Spe><Instance>RebootedWatchBoolKeyStrsList' : []\n", '   /}\n', '\n',
'*****End of the Attest *****\n', '\n', '\n']
   /   /   /   /}
   /   /   /]
   /   /  'prompt_number' : 0
   /   /}
   /  '<Spe><Instance>CelledOutputStr' : Before make, MyBuilder is
< (BuilderClass), 4540177488>
   /{
   /  '<Base><Class>MadeMyInt' : 0
   /  '<Base><Class>MakingMyFloat' : 0.0
   /  '<New><Instance>IdInt' : 4540177488
   /}
I am in the mimic_make of the Builder
I am in the do_make of the Maker
After the first make, MyBuilder is
< (BuilderClass), 4540177488>
   /{
   /  '<New><Instance>IdInt' : 4540177488
   /  '<Spe><Instance>MadeMyInt' : 13
   /  '<Spe><Instance>MakingMyFloat' : 3.0
   /}
After the second make, MyBuilder is
< (BuilderClass), 4540177488>
   /{
   /  '<New><Instance>IdInt' : 4540177488
   /  '<Spe><Instance>MadeMyInt' : 13
   /  '<Spe><Instance>MakingMyFloat' : 3.0
   /}
Now we reboot
After the reboot, MyBuilder is
< (BuilderClass), 4540177488>
   /{
   /  '<New><Instance>IdInt' : 4540177488
   /  '<Spe><Instance>MadeMyInt' : 0
   /  '<Spe><Instance>MakingMyFloat' : 3.0
   /}
I am in the mimic_make of the Builder
I am in the do_make of the Maker


*****Start of the Attest *****

MyBuilder is < (BuilderClass), 4540177488>
   /{
   /  '<New><Instance>IdInt' : 4540177488
   /  '<Spe><Instance>MadeMyInt' : 18
   /  '<Spe><Instance>MakingMyFloat' : 8.0
   /  '<Spe><Instance>RebootedWatchBoolKeyStrsList' : []
   /}

*****End of the Attest *****


   /  '<Spe><Instance>CellingScriptStr' : Python
   /  '<Spe><Instance>CellingTextStr' : #ImportModules
import ShareYourSystem as SYS
from ShareYourSystem.Standards.Classors import Classer
from ShareYourSystem.Standards.Objects import Rebooter

#Definition
@Classer.ClasserClass(**
{
        'ClassingSwitchMethodStrsList':['make']
})
class MakerClass(Rebooter.RebooterClass):

        #Definition
        RepresentingKeyStrsList=[
                                                                'MakingMyFloat',
                                                                'MadeMyInt'
                                                        ]

        def default_init(self,
                                        _MakingMyFloat=0.,
                                        _MadeMyInt=0,
                                        **_KwarVariablesDict
                                ):
                Rebooter.RebooterClass.__init__(self,**_KwarVariablesDict)

        def do_make(self):

                #print
                print('I am in the do_make of the Maker')

                #cast
                self.MadeMyInt=int(self.MakingMyFloat)

#Definition
@Classer.ClasserClass(**{
        'ClassingSwitchMethodStrsList':["make"]
})
class BuilderClass(MakerClass):

        #Definition
        RepresentingKeyStrsList=[
                                                        ]

        def default_init(self,
                                        **_KwarVariablesDict
                                ):
                MakerClass.__init__(self,**_KwarVariablesDict)

        def mimic_make(self):

                #print
                print('I am in the mimic_make of the Builder')

                #call the parent method
                MakerClass.make(self)

                #cast
                self.MadeMyInt+=10

        def do_build(self):
                pass


#Definition an instance
MyBuilder=BuilderClass()

#Print
print('Before make, MyBuilder is ')
SYS._print(MyBuilder,**{
        'RepresentingKeyStrsList':[
        'MakingMyFloat',
        'MadeMyInt',
        ]
})

#make once
MyBuilder.make(3.)

#Print
print('After the first make, MyBuilder is ')
SYS._print(MyBuilder,**{
        'RepresentingKeyStrsList':[
        'MakingMyFloat',
        'MadeMyInt',
        ]
})

#make again
MyBuilder.make(5.)

#Print
print('After the second make, MyBuilder is ')
SYS._print(MyBuilder,**{
        'RepresentingKeyStrsList':[
        'MakingMyFloat',
        'MadeMyInt',
        ]
})

#make again
print('Now we reboot')
MyBuilder.reboot(
                                        #_NameStrsList=['Maker','Builder'],
                                        #_DoStrsList=['Make'],
                                        #_AllDoBool=True,
                                        #_AllNameBool=True,
                                )

#Print
print('After the reboot, MyBuilder is ')
SYS._print(MyBuilder,**{
        'RepresentingKeyStrsList':[
        'MakingMyFloat',
        'MadeMyInt',
        ]
})

#make again
MyBuilder.make(8.)

#Definition the AttestedStr
SYS._attest(
        [
                'MyBuilder is '+SYS._str(
                MyBuilder,
                **{
                        'RepresentingAlineaIsBool':False,
                        'RepresentingKeyStrsList':[
                                'MakingMyFloat',
                                'MadeMyInt',
                                'RebootedWatchBoolKeyStrsList'
                        ]
                        }
                )
        ]
)
   /}

*****End of the Attest *****



```

