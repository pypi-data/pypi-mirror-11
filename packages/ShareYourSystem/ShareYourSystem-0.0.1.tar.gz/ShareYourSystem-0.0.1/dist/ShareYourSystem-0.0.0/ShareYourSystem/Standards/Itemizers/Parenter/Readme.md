

<!--
FrozenIsBool False
-->

#Parenter

##Doc
----


>
> A Parenter completes the list of grand-parent nodes that
> a child node could have. It acts only at one level.
>
>

----

<small>
View the Parenter notebook on [NbViewer](http://nbviewer.ipython.org/url/shareyo
ursystem.ouvaton.org/Parenter.ipynb)
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


A Parenter completes the list of grand-parent nodes that
a child node could have. It acts only at one level.

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Noders.Distinguisher"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import copy
from ShareYourSystem.Standards.Itemizers import Pather
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass(
        **{'ClassingSwitchMethodStrsList':['parent']}
)
class ParenterClass(BaseClass):

        #Definition
        RepresentingKeyStrsList=[
'ParentingWalkBool',
'ParentedDeriveParentersList',
'ParentedNodeCollectionStrsList',
'ParentedNodePathStr'
                                                        ]

        def default_init(self,
                                _ParentingWalkBool=True,
                                _ParentedDeriveParentersList=None,
                                _ParentedNodeCollectionStrsList=None,
                                _ParentedNodePathStr="",
                                **_KwargVariablesDict):

                #Call the parent init method
                BaseClass.__init__(self,**_KwargVariablesDict)

        def do_parent(self):

                #debug
                '''
self.debug(('self.',self,['ParentingNodeStr','NodePointDeriveNoder']))
                '''

                #Check of a parent pointer
                if self.NodePointDeriveNoder!=None:

                        #debug
                        '''
                        self.debug('We are going to node the parent pointer')
                        '''

                        #Parent the parent maybe
                        if self.ParentingWalkBool:

                                #parent the parent
                                self.NodePointDeriveNoder.parent()

                        #set
self.ParentedDeriveParentersList=[self.NodePointDeriveNoder
                        ]+self.NodePointDeriveNoder.ParentedDeriveParentersList

self.ParentedNodeCollectionStrsList=[self.NodedCollectionStr
]+self.NodePointDeriveNoder.ParentedNodeCollectionStrsList
                        self.ParentedNodeCollectionStrsList.reverse()

                        #definition
                        ParentedNodePathStrsList=map(
                                        lambda __ParentedDeriveParenter:
                                        __ParentedDeriveParenter.NodeKeyStr,
                                        self.ParentedDeriveParentersList
                                )
                        ParentedNodePathStrsList.reverse()

                        #Debug
                        '''
                        self.debug('ParentedNodePathStrsList is
'+str(ParentedNodePathStrsList))
                        '''

                        #set
self.ParentedNodePathStr=Pather.PathPrefixStr.join(ParentedNodePathStrsList)

                #Return self
                #return self

#</DefineClass>


```

<small>
View the Parenter sources on <a href="https://github.com/Ledoux/ShareYourSystem/
tree/master/Pythonlogy/ShareYourSystem/Noders/Parenter"
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
from ShareYourSystem.Standards.Noders import Parenter

#Short expression and set in the appended manner
MyParenter=Parenter.ParenterClass().__setitem__(
    '<Tree>ChildParenter',
    Parenter.ParenterClass().__setitem__(
        '<Tree>GrandChildParenter',
        Parenter.ParenterClass()
    )
)

#Parent for the children
#MyParenter['<Tree>ChildParenter'].parent('Tree')
MyParenter['<Tree>ChildParenter']['<Tree>GrandChildParenter'].parent()

#Definition the AttestedStr
SYS._attest(
    [
        'MyParenter is '+SYS._str(
        MyParenter,
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

MyParenter is < (ParenterClass), 4555207440>
   /{
   /  '<New><Instance>IdInt' : 4555207440
   /  '<New><Instance>NodeCollectionStr' : Globals
   /  '<New><Instance>NodeIndexInt' : -1
   /  '<New><Instance>NodeKeyStr' : TopParenter
   /  '<New><Instance>NodePointDeriveNoder' : None
   /  '<New><Instance>NodePointOrderedDict' : None
   /  '<New><Instance>TreeCollectionOrderedDict' :
   /   /{
   /   /  'ChildParenter' : < (ParenterClass), 4555206736>
   /   /   /{
   /   /   /  '<New><Instance>IdInt' : 4555206736
   /   /   /  '<New><Instance>NodeCollectionStr' : Tree
   /   /   /  '<New><Instance>NodeIndexInt' : 0
   /   /   /  '<New><Instance>NodeKeyStr' : ChildParenter
   /   /   /  '<New><Instance>NodePointDeriveNoder' : {...}< (ParenterClass),
4555207440>
   /   /   /  '<New><Instance>NodePointOrderedDict' : {...}< (OrderedDict),
4556379080>
   /   /   /  '<New><Instance>TreeCollectionOrderedDict' :
   /   /   /   /{
   /   /   /   /  'GrandChildParenter' : < (ParenterClass), 4555209552>
   /   /   /   /   /{
   /   /   /   /   /  '<New><Instance>IdInt' : 4555209552
   /   /   /   /   /  '<New><Instance>NodeCollectionStr' : Tree
   /   /   /   /   /  '<New><Instance>NodeIndexInt' : 0
   /   /   /   /   /  '<New><Instance>NodeKeyStr' : GrandChildParenter
   /   /   /   /   /  '<New><Instance>NodePointDeriveNoder' : {...}<
(ParenterClass), 4555206736>
   /   /   /   /   /  '<New><Instance>NodePointOrderedDict' : {...}<
(OrderedDict), 4556378784>
   /   /   /   /   /  '<Spe><Class>ParentingWalkBool' : True
   /   /   /   /   /  '<Spe><Instance>ParentedDeriveParentersList' :
   /   /   /   /   /   /[
   /   /   /   /   /   /  0 : {...}< (ParenterClass), 4555206736>
   /   /   /   /   /   /  1 : {...}< (ParenterClass), 4555207440>
   /   /   /   /   /   /]
   /   /   /   /   /  '<Spe><Instance>ParentedNodeCollectionStrsList' : ['', '']
   /   /   /   /   /  '<Spe><Instance>ParentedNodePathStr' :
TopParenter/ChildParenter
   /   /   /   /   /}
   /   /   /   /}
   /   /   /  '<Spe><Class>ParentingWalkBool' : True
   /   /   /  '<Spe><Instance>ParentedDeriveParentersList' :
   /   /   /   /[
   /   /   /   /  0 : {...}< (ParenterClass), 4555207440>
   /   /   /   /]
   /   /   /  '<Spe><Instance>ParentedNodeCollectionStrsList' : ['']
   /   /   /  '<Spe><Instance>ParentedNodePathStr' : TopParenter
   /   /   /}
   /   /}
   /  '<Spe><Class>ParentedNodePathStr' :
   /  '<Spe><Class>ParentingWalkBool' : True
   /  '<Spe><Instance>ParentedDeriveParentersList' : []
   /  '<Spe><Instance>ParentedNodeCollectionStrsList' : []
   /}

*****End of the Attest *****



```

