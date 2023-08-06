

<!--
FrozenIsBool False
-->

#Pointer

##Doc
----


>
> A Pointer
>
>

----

<small>
View the Pointer notebook on [NbViewer](http://nbviewer.ipython.org/url/shareyou
rsystem.ouvaton.org/Pointer.ipynb)
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


A Pointer

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Applyiers.Updater"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
from ShareYourSystem.Standards.Itemizers import Pather
#</ImportSpecificModules>

#<DefineLocals>
PointPrefixStr=""
PointSuffixStr=""
PointBackStr="Back"
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class PointerClass(BaseClass):

        #Definition
        RepresentingKeyStrsList=[
'PointingGetVariable',
'PointingSetPathStr',
'PointingBackSetStr',
'PointedGetVariable',
'PointedPathBackVariable',
'PointedLocalSetStr',
'PointedBackSetStr'
                                                        ]

        def default_init(
                                        self,
                                        _PointingGetVariable=None,
                                        _PointingSetPathStr="",
                                        _PointingBackSetStr="",
                                        _PointedGetVariable=None,
                                        _PointedPathBackVariable="",
                                        _PointedPathBackStr="",
                                        _PointedLocalSetStr="",
                                        _PointedBackSetStr="",
                                        **_KwargVariablesDict
                                ):

                #Call the parent init method
                BaseClass.__init__(self,**_KwargVariablesDict)

        def do_point(self):

                #debug
                '''
                self.debug(('self.',self,[
'PointingGetVariable',
'PointingSetPathStr'
                                                                ]))
                '''

                #get
                if type(self.PointingGetVariable) in SYS.StrTypesList:
                        self.PointedGetVariable=self[self.PointingGetVariable]
                else:
                        self.PointedGetVariable=self.PointingGetVariable

                #debug
                '''
                self.debug(
                                        [
                                                'After getting',
                                                ('self.',self,[
'PointingGetVariable',
'PointedGetVariable'
]
                                                                        )
                                        ]
                                )
                '''

                #set
                self.PointedPathBackStr=Pather.getPathedBackGetStrWithGetStr(sel
f.PointingSetPathStr)

                #set
                self.PointedLocalSetStr=self.PointingSetPathStr.split(
                        self.PointedPathBackStr+Pather.PathPrefixStr)[-1]

                #debug
                '''
                self.debug(('self.',self,[
'PointingSetPathStr',
'PointedPathBackStr',
'PointedLocalSetStr'
                                                                ]))
                '''

                #set
                self.SettingKeyVariable=self.PointedPathBackStr+Pather.PathingPr
efixStr+PointPrefixStr+self.PointedLocalSetStr+PointSuffixStr

                #debug
                '''
                self.debug(('self.',self,['SettingKeyVariable']))
                '''

                #set the point variable
                self[
                                self.SettingKeyVariable
                        ]=self.PointedGetVariable

                #set a back pointer
                if self.PointingBackSetStr!="":

                        #debug
                        '''
                        self.debug(
                                                [
                                                        'We point back here',
                                                        ('self.',self,[
                'PointingSetPathStr',
                'PointingBackSetStr'
])
                                                ]
                                        )
                        '''

                        #Get
self.PointedPathBackVariable=Pather.getPathedBackVariableWithVariableAndGetStr(
                                self,
                                self.PointingSetPathStr
                        )

                        #debug
                        '''
                        self.debug(('self.',self,[
'PointedGetVariable',
'PointedPathBackVariable',
'PointingBackSetStr'
                                                                        ]))
                        '''

                        #link
                        self.PointedGetVariable[
                                self.PointingBackSetStr
                        ]=self.PointedPathBackVariable


#</DefineClass>


```

<small>
View the Pointer sources on <a href="https://github.com/Ledoux/ShareYourSystem/t
ree/master/Pythonlogy/ShareYourSystem/Itemizers/Pointer"
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
from ShareYourSystem.Standards.Itemizers import Pather,Pointer

#Explicit expression
MyPointer=Pointer.PointerClass().__setitem__(
        'ChildPather',
        Pather.PatherClass().__setitem__(
            'GrandChildPather',
            Pather.PatherClass()
        )
    ).point(
            '/',
            '/ChildPather/GrandChildPather/GrandParentPointer'
    )

#Return
SYS._attest(
    [
    'MyPointer is '+SYS._str(
            MyPointer,
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

MyPointer is < (PointerClass), 4554814160>
   /{
   /  '<New><Instance>ChildPather' : < (PatherClass), 4554817424>
   /   /{
   /   /  '<New><Instance>GrandChildPather' : < (PatherClass), 4554817488>
   /   /   /{
   /   /   /  '<New><Instance>IdInt' : 4554817488
   /   /   /  '<Spe><Class>PathedChildKeyStr' :
   /   /   /  '<Spe><Class>PathedGetKeyStr' :
   /   /   /  '<Spe><Class>PathedKeyStrsList' : None
   /   /   /  '<Spe><Class>PathingKeyStr' :
   /   /   /}
   /   /  '<New><Instance>GrandChildPather/GrandParentPointer' : {...}<
(PointerClass), 4554814160>
   /   /  '<New><Instance>IdInt' : 4554817424
   /   /  '<Spe><Class>PathedChildKeyStr' :
   /   /  '<Spe><Class>PathedGetKeyStr' :
   /   /  '<Spe><Class>PathedKeyStrsList' : None
   /   /  '<Spe><Class>PathingKeyStr' :
   /   /}
   /  '<New><Instance>IdInt' : 4554814160
   /  '<Spe><Class>PointedBackSetStr' :
   /  '<Spe><Class>PointedPathBackVariable' :
   /  '<Spe><Class>PointingBackSetStr' :
   /  '<Spe><Instance>PointedGetVariable' : {...}< (PointerClass), 4554814160>
   /  '<Spe><Instance>PointedLocalSetStr' : GrandParentPointer
   /  '<Spe><Instance>PointingGetVariable' : /
   /  '<Spe><Instance>PointingSetPathStr' :
/ChildPather/GrandChildPather/GrandParentPointer
   /}

*****End of the Attest *****



```

