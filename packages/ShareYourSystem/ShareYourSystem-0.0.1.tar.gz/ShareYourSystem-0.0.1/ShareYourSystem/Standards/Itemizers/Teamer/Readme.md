

<!--
FrozenIsBool False
-->

#Noder

##Doc
----


>
> A Noder defines Child ordered dicts with <DoStr> as KeyStr.
> The items inside are automatically setted with Noded<DoStr><TypeStr> and have
> a Pointer to the parent InstanceVariable. This is the beginning for buiding
high
> arborescent and (possibly circular) structures of objects.
>
>

----

<small>
View the Noder notebook on [NbViewer](http://nbviewer.ipython.org/url/shareyours
ystem.ouvaton.org/Noder.ipynb)
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


A Noder defines Child ordered dicts with <DoStr> as KeyStr.
The items inside are automatically setted with Noded<DoStr><TypeStr> and have
a Pointer to the parent InstanceVariable. This is the beginning for buiding high
arborescent and (possibly circular) structures of objects.

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Applyiers.Filterer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import collections
from ShareYourSystem.Standards.Itemizers import Pather
#</ImportSpecificModules>

#<DefineLocals>
NodingPrefixGetStr='<'
NodingSuffixGetStr='>'
NodingCollectionPrefixStr="Node"
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class NoderClass(BaseClass):

        #Definition
        RepresentingKeyStrsList=[
'NodingCollectionStr',
'NodedCollectionOrderedDict',
'NodedCollectionStr',
'NodedKeyStr',
'NodedCollectionIndexInt'
                                                                ]

        def default_init(self,
                                _NodingCollectionStr="",
                                _NodedCollectionOrderedDict=None,
                                _NodedCollectionStr="",
                                _NodedKeyStr="",
                                _NodedCollectionIndexInt=-1,
                                **_KwargVariablesDict
                                ):

                #Call the parent init method
                BaseClass.__init__(self,**_KwargVariablesDict)

                #global
                global NodingCollectionPrefixStr

                NodedMethodStr='__setattr__'
                NodedMethod=getattr(self,NodedMethodStr)

                #Int and Set Child attributes
                NodedMethod(
                        NodingCollectionPrefixStr+'CollectionStr',
                        "Globals"
                )
                NodedMethod(
                        NodingCollectionPrefixStr+'IndexInt',
                        -1
                )
                """
                NodedMethod(
                        NodingCollectionPrefixStr+'KeyStr',
                        SYS._filter(
                                lambda __ListedVariable:
                                id(__ListedVariable)==self.IdStr,
                                sys.modules['__main__'].globals().values()
                        )
                )
                """
                NodedMethod(
                        NodingCollectionPrefixStr+'KeyStr',
                        'Top'+self.__class__.NameStr
                )
                self.point(
                                None,
                                NodingCollectionPrefixStr+'PointOrderedDict'
                        )
                self.point(
                                None,
                                NodingCollectionPrefixStr+'PointDeriveNoder'
                        )

        def do_node(self):

                #debug
                '''
                self.debug(("self.",self,['NodingCollectionStr']))
                '''

                #Get the NodedStr
                if self.NodingCollectionStr!="":

                        #set the Noded OrderedDict and KeyStr
                        NodedCollectionOrderedSetTagStr=self.NodingCollectionSt
r+'CollectionOrderedDict'
                        #self.NodeKeyStrKeyStr=self.NodedPrefixStr+'KeyStr'

                        try:
self.NodedCollectionOrderedDict=getattr(self,NodedCollectionOrderedSetTagStr)
                        except AttributeError:
                                self.__setattr__(
NodedCollectionOrderedSetTagStr,
collections.OrderedDict()
                                                                )
self.NodedCollectionOrderedDict=getattr(self,NodedCollectionOrderedSetTagStr)

        def mimic_get(self):

                #debug
                '''
                self.debug(("self.",self,['GettingKeyVariable']))
                '''

                #Definition
                OutputDict={'HookingIsBool':True}

                #Appending set
                if self.GettingKeyVariable.startswith(NodingPrefixGetStr):

                        #Definition the SplittedStrsList
SplittedStrsList=self.GettingKeyVariable.split(NodingSuffixGetStr)

                        #Definition the NodingCollectionStr
                        NodingCollectionStr=NodingPrefixGetStr.join(
SplittedStrsList[0].split(NodingPrefixGetStr)[1:])

                        #debug
                        '''
                        self.debug(
                                                [
                                                        'NodingCollectionStr is
'+NodingCollectionStr,
                                                        'We are going to node'
                                                ]
                                        )
                        '''

                        #Nodify
                        self.node(
                                                NodingCollectionStr,
                                                #**{'IsNoderBool':False}
                                        )

                        #Definition of the KeyStr
                        GetKeyStr=NodingSuffixGetStr.join(SplittedStrsList[1:])

                        #debug
                        '''
                        self.debug(
                                                        [
                                                                'node is done',
                                                                'GetKeyStr is
'+GetKeyStr,
'self.NodedCollectionOrderedDict is '+str(self.NodedCollectionOrderedDict)
                                                        ]
                                )
                        '''

                        #Get with a digited KeyStr case
                        if GetKeyStr.isdigit():

                                #Definition the GetInt
                                GetInt=(int)(GetKeyStr)

                                #Check if the size is ok
                                if GetInt<len(self.NodedCollectionOrderedDict):

                                        #Get the GettedVariable
                                        self.GettedValueVariable=SYS.get(
                                                self.NodedCollectionOrderedDict,
                                                'values',
                                                GetInt
                                        )

                                        #Return
                                        OutputDict['HookingIsBool']=False
                                        #<Hook>return OutputDict

                        #Get in the ValueVariablesList
                        elif GetKeyStr=="":

                                #Get the GettedVariable
self.GettedValueVariable=self.NodedCollectionOrderedDict.values()

                                #Return
                                OutputDict['HookingIsBool']=False
                                #<Hook>return OutputDict

                        elif GetKeyStr in self.NodedCollectionOrderedDict:

                                #Get the GettedVariable
self.GettedValueVariable=self.NodedCollectionOrderedDict[GetKeyStr]

                                #Return
                                OutputDict['HookingIsBool']=False
                                #<Hook>return OutputDict



                #Call the parent get method
                if OutputDict['HookingIsBool']:

                        #debug
                        '''
                        self.debug(
                                                [
('self.',self,['GettingKeyVariable']),
                                                        'BaseClass.get is
'+str(BaseClass.get)
                                                ]
                                        )
                        '''

                        #Call
                        return BaseClass.get(self)

                else:

                        #return
                        return OutputDict

#<Hook>@Hooker.HookerClass(**{'HookingAfterVariablesList':[BaseClass.set]})
        #@Imitater.ImitaterClass()
        def mimic_set(self):
                """ """

                #debug
                '''
                self.debug(('self.',self,[
                                                'SettingKeyVariable',
                                                #'SettingValueVariable'
                                                ]))
                '''

                #Definition
                OutputDict={'HookingIsBool':True}

                #Appending set
                if self.SettingKeyVariable.startswith(NodingPrefixGetStr):

                        #Definition the SplittedStrsList
SplittedStrsList=self.SettingKeyVariable.split(NodingSuffixGetStr)

                        #Definition the NodingCollectionStr
                        NodingCollectionStr=NodingPrefixGetStr.join(
SplittedStrsList[0].split(NodingPrefixGetStr)[1:])

                        #Check if it is an append of Nodes
                        IsNoderBool='NoderClass' in map(
        lambda __Class:
        __Class.__name__,
        type(self.SettingValueVariable).__mro__
        )

                        #debug
                        '''
                        self.debug(('vars
',vars(),['NodingCollectionStr','IsNoderBool']))
                        '''

                        #Nodify
                        self.node(
                                                NodingCollectionStr,
                                                #**{'IsNoderBool':IsNoderBool}
                                        )

                        #Definition the KeyStr
                        SetTagStr=NodingSuffixGetStr.join(SplittedStrsList[1:])

                        #debug
                        '''
                        self.debug('SetTagStr is '+SetTagStr)
                        '''

                        #Append (or set if it is already in)
                        Pather.setWithPathVariableAndKeyVariable(
                                self.NodedCollectionOrderedDict,
                                Pather.PathPrefixStr+SetTagStr,
                                self.SettingValueVariable
                        )

                        if Pather.PathPrefixStr not in SetTagStr:

                                #debug
                                '''
self.debug(('self.',self,['SettingValueVariable']))
                                '''

                                #If it is an object
                                if IsNoderBool:

                                        #global
                                        global NodingCollectionPrefixStr

                                        NodedMethodStr='__setattr__'
NodedMethod=getattr(self.SettingValueVariable,NodedMethodStr)

                                        #Int and Set Child attributes
                                        NodedMethod(
NodingCollectionPrefixStr+'CollectionStr',
                                                self.NodingCollectionStr
                                        )
                                        NodedMethod(
NodingCollectionPrefixStr+'IndexInt',
len(self.NodedCollectionOrderedDict)-1
                                        )
                                        NodedMethod(
NodingCollectionPrefixStr+'KeyStr',
                                                SetTagStr
                                        )
                                        self.SettingValueVariable.point(
self.NodedCollectionOrderedDict,
NodingCollectionPrefixStr+'PointOrderedDict'
                                                )
                                        self.SettingValueVariable.point(
                                                        self,
NodingCollectionPrefixStr+'PointDeriveNoder'
                                                )

                        #set
                        OutputDict['HookingIsBool']=False

                        #return
                        return OutputDict

                #Call the parent get method
                if OutputDict['HookingIsBool']:
                        return BaseClass.set(self)

#</DefineClass>


```

<small>
View the Noder sources on <a href="https://github.com/Ledoux/ShareYourSystem/tre
e/master/Pythonlogy/ShareYourSystem/Noders/Noder" target="_blank">Github</a>
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
from ShareYourSystem.Standards.Noders import Noder

#Definition of a Noder instance
MyNoder=Noder.NoderClass()

#Short expression for setting in the appended manner a structured object
MyNoder['<Nodome>FirstChildNoder']=Noder.NoderClass()

#Short expression for setting in the appended manner a structured object
MyNoder['<Nodome>SecondChildNoder']=Noder.NoderClass()

#Definition the AttestedStr
SYS._attest(
    [
        'MyNoder is '+SYS._str(
                MyNoder,
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

MyNoder is < (NoderClass), 4555208528>
   /{
   /  '<New><Instance>IdInt' : 4555208528
   /  '<New><Instance>NodeCollectionStr' : Globals
   /  '<New><Instance>NodeIndexInt' : -1
   /  '<New><Instance>NodeKeyStr' : TopNoder
   /  '<New><Instance>NodePointDeriveNoder' : None
   /  '<New><Instance>NodePointOrderedDict' : None
   /  '<New><Instance>NodomeCollectionOrderedDict' :
   /   /{
   /   /  'FirstChildNoder' : < (NoderClass), 4555208592>
   /   /   /{
   /   /   /  '<New><Instance>IdInt' : 4555208592
   /   /   /  '<New><Instance>NodeCollectionStr' : Nodome
   /   /   /  '<New><Instance>NodeIndexInt' : 0
   /   /   /  '<New><Instance>NodeKeyStr' : FirstChildNoder
   /   /   /  '<New><Instance>NodePointDeriveNoder' : {...}< (NoderClass),
4555208528>
   /   /   /  '<New><Instance>NodePointOrderedDict' : {...}< (OrderedDict),
4556316208>
   /   /   /  '<Spe><Class>NodedCollectionIndexInt' : -1
   /   /   /  '<Spe><Class>NodedCollectionOrderedDict' : None
   /   /   /  '<Spe><Class>NodedCollectionStr' :
   /   /   /  '<Spe><Class>NodedKeyStr' :
   /   /   /  '<Spe><Class>NodingCollectionStr' :
   /   /   /}
   /   /  'SecondChildNoder' : < (NoderClass), 4555209424>
   /   /   /{
   /   /   /  '<New><Instance>IdInt' : 4555209424
   /   /   /  '<New><Instance>NodeCollectionStr' : Nodome
   /   /   /  '<New><Instance>NodeIndexInt' : 1
   /   /   /  '<New><Instance>NodeKeyStr' : SecondChildNoder
   /   /   /  '<New><Instance>NodePointDeriveNoder' : {...}< (NoderClass),
4555208528>
   /   /   /  '<New><Instance>NodePointOrderedDict' : {...}< (OrderedDict),
4556316208>
   /   /   /  '<Spe><Class>NodedCollectionIndexInt' : -1
   /   /   /  '<Spe><Class>NodedCollectionOrderedDict' : None
   /   /   /  '<Spe><Class>NodedCollectionStr' :
   /   /   /  '<Spe><Class>NodedKeyStr' :
   /   /   /  '<Spe><Class>NodingCollectionStr' :
   /   /   /}
   /   /}
   /  '<Spe><Class>NodedCollectionIndexInt' : -1
   /  '<Spe><Class>NodedCollectionStr' :
   /  '<Spe><Class>NodedKeyStr' :
   /  '<Spe><Instance>NodedCollectionOrderedDict' : {...}< (OrderedDict),
4556316208>
   /  '<Spe><Instance>NodingCollectionStr' : Nodome
   /}

*****End of the Attest *****



```

