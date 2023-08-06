

<!--
FrozenIsBool False
-->

#Folderer

##Doc
----


>
> The Folderer is a quick object helping for getting the FolderedDirKeyStrsList
> at a specified directory or in the current one by default
>
>

----

<small>
View the Folderer notebook on [NbViewer](http://nbviewer.ipython.org/url/shareyo
ursystem.ouvaton.org/Folderer.ipynb)
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


The Folderer is a quick object helping for getting the FolderedDirKeyStrsList
at a specified directory or in the current one by default

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Interfacers.Interfacer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import collections
import json
import os
import sys
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class FoldererClass(BaseClass):
        """
                FoldererClass ...

        """

        #Definition
        RepresentingKeyStrsList=[
'FolderingPathVariable',
'FolderingMkdirBool',
'FolderedDirKeyStrsList',
'FolderedModuleStr',
'FolderedParentModuleStr',
'FolderedNameStr'
                                                                ]

        def default_init(self,
                                                _FolderingPathVariable="",
                                                _FolderingMkdirBool=False,
                                                _FolderedDirKeyStrsList=None,
                                                _FolderedModuleStr="",
                                                _FolderedParentModuleStr="",
                                                _FolderedNameStr="",
                                                **_KwargVariablesDict
                                        ):

                #Call the parent __init__ method
                BaseClass.__init__(self,**_KwargVariablesDict)

        def do_folder(self,**_KwargVariablesDict):

                #Get the current
                FolderedCurrentPathStr=os.getcwd()

                #set
                if self.FolderingPathVariable=="":
                        self.FolderingPathVariable=FolderedCurrentPathStr+'/'

                #debug
                '''
                print('self.FolderingPathVariable is '+self.FolderingPathVariable)
                print('FolderedCurrentPathStr is '+FolderedCurrentPathStr)
                print('')
                '''

                #Check
                if self.FolderingPathVariable!="":

                        #Add the '/' if not in the end
                        if self.FolderingPathVariable[-1]!="/":
                                self.FolderingPathVariable+="/"

                        #Build intermediar pathes
                        if os.path.isdir(self.FolderingPathVariable)==False:

                                #Check
                                if self.FolderingMkdirBool:

                                        #debug
                                        '''
                                        print('We are going to build the
intermediar folder')
                                        print('self.FolderingPathVariable is
',self.FolderingPathVariable)
                                        print('')
                                        '''

                                        #Definition
FolderingPathVariablesList=self.FolderingPathVariable.split('/')
FolderedRootPathStr=FolderingPathVariablesList[0]
                                        for _PathStr in
FolderingPathVariablesList[1:]:

                                                #debug
                                                '''
                                                print('FolderedRootPathStr is
',FolderedRootPathStr)
                                                print('')
                                                '''

                                                #Mkdir if it doesn't exist
                                                if FolderedRootPathStr!="" and
os.path.isdir(FolderedRootPathStr)==False:
                                                        os.popen('mkdir
'+FolderedRootPathStr)

                                                #Add the following
FolderedRootPathStr+='/'+_PathStr

                                        #Mkdir if it doesn't exist
                                        if
os.path.isdir(FolderedRootPathStr)==False:
                                                os.popen('mkdir
'+FolderedRootPathStr)

                #Recheck
                if os.path.isdir(self.FolderingPathVariable):

                        #set
self.FolderedDirKeyStrsList=os.listdir(self.FolderingPathVariable)

                        #Check
                        if '__init__.py' in self.FolderedDirKeyStrsList:

                                #set maybe FolderedModuleStr and
FolderedParentModuleStr if we are located in the SYS path
                                if 'ShareYourSystem' in self.FolderingPathVariable:

                                        #set
self.FolderedModuleStr='ShareYourSystem'+self.FolderingPathVariable.split(
'ShareYourSystem')[-1].replace('/','.')

                                        #Remove the ossibly last dot
                                        if self.FolderedModuleStr[-1]=='.':
self.FolderedModuleStr=self.FolderedModuleStr[:-1]

                                        #set
                                        if '.' in self.FolderedModuleStr:

                                                #set
self.FolderedNameStr=self.FolderedModuleStr.split('.')[-1]

                                                #debug
                                                '''
self.debug(('self.',self,['FolderingPathVariable','FolderedNameStr']))
                                                '''

                                                #set the parent
self.FolderedParentModuleStr=self.FolderedNameStr.join(
self.FolderedModuleStr.split(self.FolderedNameStr)[:-1]
                                                )
                                                if
len(self.FolderedParentModuleStr
                                                        )>0 and
self.FolderedParentModuleStr[-1]=='.':
self.FolderedParentModuleStr=self.FolderedParentModuleStr[:-1]
                                        else:
self.FolderedModuleStr=self.FolderedModuleStr

                        else:

                                #set
                                self.FolderedModuleStr=""
                                self.FolderedParentModuleStr=""

                #Return self
                #return self

#</DefineClass>

```

<small>
View the Folderer sources on <a href="https://github.com/Ledoux/ShareYourSystem/
tree/master/Pythonlogy/ShareYourSystem/Interfacers/Folderer"
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
from ShareYourSystem.Standards.Interfacers import Folderer

#Definition of an instance Folderer and make it find the current dir
MyFolderer=Folderer.FoldererClass(
    ).folder(
        Folderer.LocalFolderPathStr
    )

#If you don't have these folder, MyFolderer is going to create them for you
MyFolderer=Folderer.FoldererClass(
    ).folder(
        MyFolderer.FolderingPathVariable+'TestFolder1/TestFolder2/',
        True
    )

#Definition the AttestedStr
SYS._attest(
    [
        'MyFolderer is '+SYS._str(MyFolderer,
        **{'RepresentingAlineaIsBool':False})
    ]
)

#Print


```


```console
>>>


*****Start of the Attest *****

MyFolderer is < (FoldererClass), 4540265104>
   /{
   /  '<New><Instance>IdInt' : 4540265104
   /  '<Spe><Class>FolderedNameStr' :
   /  '<Spe><Instance>FolderedDirKeyStrsList' : []
   /  '<Spe><Instance>FolderedModuleStr' :
   /  '<Spe><Instance>FolderedParentModuleStr' :
   /  '<Spe><Instance>FolderingMkdirBool' : True
   /  '<Spe><Instance>FolderingPathVariable' : /Users/ledoux/Documents/ShareYourSyste
m/Pythonlogy/ShareYourSystem/Interfacers/Folderer/TestFolder1/TestFolder2/
   /}

*****End of the Attest *****



```

