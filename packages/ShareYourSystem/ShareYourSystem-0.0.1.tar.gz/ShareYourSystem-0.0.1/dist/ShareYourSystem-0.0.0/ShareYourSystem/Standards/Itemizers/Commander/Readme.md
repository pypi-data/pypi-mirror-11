

<!--
FrozenIsBool False
-->

#Commander

##Doc
----


>
> A Commander gather Variables to set them with an UpdateList.
> The command process can be AllSetsForEach (ie a map of the update succesively
for each)
> or a EachSetForAll (ie each set is a map of each).
>
>

----

<small>
View the Commander notebook on [NbViewer](http://nbviewer.ipython.org/url/sharey
oursystem.ouvaton.org/Commander.ipynb)
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


A Commander gather Variables to set them with an UpdateList.
The command process can be AllSetsForEach (ie a map of the update succesively
for each)
or a EachSetForAll (ie each set is a map of each).

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Noders.Attentioner"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class CommanderClass(BaseClass):

        #Definition
        RepresentingKeyStrsList=[
                                                        #'CommandingUpdateList',
#'CommandingVariablesList',
                                                        'CommandingOrderStr',
                                                        'CommandingGatherIsBool'
                                                ]

        def default_init(self,
                                _CommandingUpdateList=None,
                                _CommandingVariablesList=None,
                                _CommandingOrderStr="AllSetsForEach",
                                _CommandingGatherIsBool=True,
                                **_KwargVariablesDict
                                ):

                #Call the parent __init__ method
                BaseClass.__init__(self,**_KwargVariablesDict)

        def do_command(self):
                """Collect with _GatheringKeyVariablesList and do a all sets for
each with _UpdatingItemVariable"""

                #Check
                if self.CommandingGatherIsBool:

                        #Get the GatheredVariablesList
                        self.gather()

                        #debug
                        '''
                        self.debug(
                                                        ('self.',self,[
'CommandingUpdateList',
'GatheringVariablesList',
'GatheredVariablesList'
                                                                        ]
                                                        )
                                                )
                        '''

                        #Check
                        if len(self.GatheredVariablesList)>0:

                                #Just keep the values
self.CommandingVariablesList=SYS.flat(SYS.unzip(self.GatheredVariablesList,[1]))

                #debug
                '''
                self.debug(("self.",self,['CommandingVariablesList']))
                '''

                #Check for the order
                if self.CommandingOrderStr=="AllSetsForEach":

                        #For each __GatheredVariable it is updating with
_UpdatingItemVariable
                        map(
                                        lambda __CommandedVariable:
__CommandedVariable.update(self.CommandingUpdateList),
                                        self.CommandingVariablesList
                                )

                elif self.CommandingOrderStr=="EachSetForAll":

                        #For each SettingTuple it is setted in
_GatheredVariablesList
                        map(
                                        lambda __SettingVariableTuple:
                                        map(
                                                lambda __CommandedVariable:
__CommandedVariable.__setitem__(*__SettingVariableTuple),
                                                self.CommandingVariablesList
                                                ),
                                        self.CommandingUpdateList.items()
                                        if
hasattr(self.CommandingUpdateList,'items')
                                        else self.CommandingUpdateList
                                )

                #Return self
                #return self
#</DefineClass>

```

<small>
View the Commander sources on <a href="https://github.com/Ledoux/ShareYourSystem
/tree/master/Pythonlogy/ShareYourSystem/Applyiers/Commander"
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
from ShareYourSystem.Applyiers import Commander
import copy

#Definition a structure of Commanders.
MyFirstCommander=Commander.CommanderClass().__add__(
    [
        Commander.CommanderClass().update(
            [
                ('NodeCollectionStr','Commandome'),
                ('NodeKeyStr',str(Int1))
            ]) for Int1 in xrange(2)
    ]
)

#Definition a structure of Commanders.
MySecondCommander=Commander.CommanderClass().__add__(
    [
        Commander.CommanderClass().update(
            [
                ('NodeCollectionStr','Commandome'),
                ('NodeKeyStr',str(Int1))
            ]) for Int1 in xrange(2)
    ]
)


#Definition an CommandingUpdateList to be commanded
CommandingUpdateList=[
    (
        'MyCountingInt',
        ';'.join([
'Exec_self.SettingValueVariable=self.__class__.MyCountingInt',
                    'self.__class__.MyCountingInt+=1'
                ])
    ),
    (
        'MyCountingInt',
        ';'.join([
'Exec_self.SettingValueVariable=self.__class__.MyCountingInt',
                    'self.__class__.MyCountingInt+=1'
                ])
    )
]

#Definition GatheringVariablesList
GatheringVariablesList=[
        ['/'],
        '<Commandome>'
]

#Now command with a AllSetsForEach protocol
MyFirstCommander.execute('self.__class__.MyCountingInt=0').command(
        _UpdateList=CommandingUpdateList,
        **{
            'GatheringVariablesList': GatheringVariablesList
            }
        )

#Command with a EachSetForAll protocol
MySecondCommander.execute('self.__class__.MyCountingInt=0').command(
        CommandingUpdateList,
        _OrderStr='EachSetForAll',
        **{
            'GatheringVariablesList': GatheringVariablesList
        }
)

#Definition the AttestedStr
SYS._attest(
    [
        'MyFirstCommander is '+SYS._str(
        MyFirstCommander,
        **{
            'RepresentingBaseKeyStrsListBool':False,
            'RepresentingAlineaIsBool':False
        }
        ),
        'MySecondCommander is '+SYS._str(
        MySecondCommander,
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

                                            xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                                            ////////////////////////////////
                                            Appender/__init__.py do_append
                                            From Appender/__init__.py do_append
| Instancer/__init__.py mimic_append | Mimicker/__init__.py mimic |
Applyier/__init__.py do_apply | Mapper/__init__.py do_map | Adder/__init__.py
do_add | Adder/__init__.py __add__ | site-packages/six.py exec_ |
Celler/__init__.py do_cell | Notebooker/__init__.py do_notebook |
Documenter/__init__.py do_inform | inform.py <module>
                                            ////////////////////////////////

                                            l.138 :
                                            *****
                                            I am with [('NodeKeyStr',
'TopCommander')]
                                            *****
                                            self.AppendedNodeCollectionStr is
Commandome
                                            self.AppendedNodeKeyStr is 0

                                            xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


                                            xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                                            ////////////////////////////////
                                            Appender/__init__.py do_append
                                            From Appender/__init__.py do_append
| Instancer/__init__.py mimic_append | Mimicker/__init__.py mimic |
Applyier/__init__.py do_apply | Mapper/__init__.py do_map | Adder/__init__.py
do_add | Adder/__init__.py __add__ | site-packages/six.py exec_ |
Celler/__init__.py do_cell | Notebooker/__init__.py do_notebook |
Documenter/__init__.py do_inform | inform.py <module>
                                            ////////////////////////////////

                                            l.138 :
                                            *****
                                            I am with [('NodeKeyStr',
'TopCommander')]
                                            *****
                                            self.AppendedNodeCollectionStr is
Commandome
                                            self.AppendedNodeKeyStr is 1

                                            xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


                                            xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                                            ////////////////////////////////
                                            Appender/__init__.py do_append
                                            From Appender/__init__.py do_append
| Instancer/__init__.py mimic_append | Mimicker/__init__.py mimic |
Applyier/__init__.py do_apply | Mapper/__init__.py do_map | Adder/__init__.py
do_add | Adder/__init__.py __add__ | site-packages/six.py exec_ |
Celler/__init__.py do_cell | Notebooker/__init__.py do_notebook |
Documenter/__init__.py do_inform | inform.py <module>
                                            ////////////////////////////////

                                            l.138 :
                                            *****
                                            I am with [('NodeKeyStr',
'TopCommander')]
                                            *****
                                            self.AppendedNodeCollectionStr is
Commandome
                                            self.AppendedNodeKeyStr is 0

                                            xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


                                            xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                                            ////////////////////////////////
                                            Appender/__init__.py do_append
                                            From Appender/__init__.py do_append
| Instancer/__init__.py mimic_append | Mimicker/__init__.py mimic |
Applyier/__init__.py do_apply | Mapper/__init__.py do_map | Adder/__init__.py
do_add | Adder/__init__.py __add__ | site-packages/six.py exec_ |
Celler/__init__.py do_cell | Notebooker/__init__.py do_notebook |
Documenter/__init__.py do_inform | inform.py <module>
                                            ////////////////////////////////

                                            l.138 :
                                            *****
                                            I am with [('NodeKeyStr',
'TopCommander')]
                                            *****
                                            self.AppendedNodeCollectionStr is
Commandome
                                            self.AppendedNodeKeyStr is 1

                                            xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx



*****Start of the Attest *****

MyFirstCommander is < (CommanderClass), 4555039568>
   /{
   /  '<New><Instance>CommandomeCollectionOrderedDict' :
   /   /{
   /   /  '0' : < (CommanderClass), 4555133968>
   /   /   /{
   /   /   /  '<New><Instance>IdInt' : 4555133968
   /   /   /  '<New><Instance>MyCountingInt' : 3
   /   /   /  '<New><Instance>NodeCollectionStr' : Commandome
   /   /   /  '<New><Instance>NodeIndexInt' : 0
   /   /   /  '<New><Instance>NodeKeyStr' : 0
   /   /   /  '<New><Instance>NodePointDeriveNoder' : {...}< (CommanderClass),
4555039568>
   /   /   /  '<New><Instance>NodePointOrderedDict' : {...}< (OrderedDict),
4555109320>
   /   /   /  '<Spe><Class>CommandingGatherIsBool' : True
   /   /   /  '<Spe><Class>CommandingOrderStr' : AllSetsForEach
   /   /   /}
   /   /  '1' : < (CommanderClass), 4555134096>
   /   /   /{
   /   /   /  '<New><Instance>IdInt' : 4555134096
   /   /   /  '<New><Instance>MyCountingInt' : 5
   /   /   /  '<New><Instance>NodeCollectionStr' : Commandome
   /   /   /  '<New><Instance>NodeIndexInt' : 1
   /   /   /  '<New><Instance>NodeKeyStr' : 1
   /   /   /  '<New><Instance>NodePointDeriveNoder' : {...}< (CommanderClass),
4555039568>
   /   /   /  '<New><Instance>NodePointOrderedDict' : {...}< (OrderedDict),
4555109320>
   /   /   /  '<Spe><Class>CommandingGatherIsBool' : True
   /   /   /  '<Spe><Class>CommandingOrderStr' : AllSetsForEach
   /   /   /}
   /   /}
   /  '<New><Instance>IdInt' : 4555039568
   /  '<New><Instance>MyCountingInt' : 1
   /  '<New><Instance>NodeCollectionStr' : Globals
   /  '<New><Instance>NodeIndexInt' : -1
   /  '<New><Instance>NodeKeyStr' : TopCommander
   /  '<New><Instance>NodePointDeriveNoder' : None
   /  '<New><Instance>NodePointOrderedDict' : None
   /  '<Spe><Class>CommandingGatherIsBool' : True
   /  '<Spe><Class>CommandingOrderStr' : AllSetsForEach
   /}

------

MySecondCommander is < (CommanderClass), 4555134416>
   /{
   /  '<New><Instance>CommandomeCollectionOrderedDict' :
   /   /{
   /   /  '0' : < (CommanderClass), 4555135184>
   /   /   /{
   /   /   /  '<New><Instance>IdInt' : 4555135184
   /   /   /  '<New><Instance>MyCountingInt' : 4
   /   /   /  '<New><Instance>NodeCollectionStr' : Commandome
   /   /   /  '<New><Instance>NodeIndexInt' : 0
   /   /   /  '<New><Instance>NodeKeyStr' : 0
   /   /   /  '<New><Instance>NodePointDeriveNoder' : {...}< (CommanderClass),
4555134416>
   /   /   /  '<New><Instance>NodePointOrderedDict' : {...}< (OrderedDict),
4555109616>
   /   /   /  '<Spe><Class>CommandingGatherIsBool' : True
   /   /   /  '<Spe><Class>CommandingOrderStr' : AllSetsForEach
   /   /   /}
   /   /  '1' : < (CommanderClass), 4555134928>
   /   /   /{
   /   /   /  '<New><Instance>IdInt' : 4555134928
   /   /   /  '<New><Instance>MyCountingInt' : 5
   /   /   /  '<New><Instance>NodeCollectionStr' : Commandome
   /   /   /  '<New><Instance>NodeIndexInt' : 1
   /   /   /  '<New><Instance>NodeKeyStr' : 1
   /   /   /  '<New><Instance>NodePointDeriveNoder' : {...}< (CommanderClass),
4555134416>
   /   /   /  '<New><Instance>NodePointOrderedDict' : {...}< (OrderedDict),
4555109616>
   /   /   /  '<Spe><Class>CommandingGatherIsBool' : True
   /   /   /  '<Spe><Class>CommandingOrderStr' : AllSetsForEach
   /   /   /}
   /   /}
   /  '<New><Instance>IdInt' : 4555134416
   /  '<New><Instance>MyCountingInt' : 3
   /  '<New><Instance>NodeCollectionStr' : Globals
   /  '<New><Instance>NodeIndexInt' : -1
   /  '<New><Instance>NodeKeyStr' : TopCommander
   /  '<New><Instance>NodePointDeriveNoder' : None
   /  '<New><Instance>NodePointOrderedDict' : None
   /  '<Spe><Class>CommandingGatherIsBool' : True
   /  '<Spe><Instance>CommandingOrderStr' : EachSetForAll
   /}

*****End of the Attest *****



```

