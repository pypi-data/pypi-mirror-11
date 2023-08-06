

<!--
FrozenIsBool False
-->

#Rower

##Doc
----


>
> The Rower helps to set rowed lines in a Databaser from pointed attributes,
> ready then to be inserted in a table.
>
>

----

<small>
View the Rower notebook on [NbViewer](http://nbviewer.ipython.org/url/shareyours
ystem.ouvaton.org/Rower.ipynb)
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


The Rower helps to set rowed lines in a Databaser from pointed attributes,
ready then to be inserted in a table.

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Modelers.Tabler"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import collections
import copy

#</ImportSpecificModules>

#<DefineFunctions>
def getRowedDictsListWithTable(_Table):
        return map(
                        lambda __Row:
                        dict(
                                zip(
                                        _Table.colnames,
                                        map(
                                                lambda __ColumnStr:
                                                __Row[__ColumnStr],
                                                _Table.colnames
                                        )
                                )
                        ),
                        _Table.iterrows()
                )
#</DefineFunctions>


#<DefineClass>
@DecorationClass(
        #**{'ClassingSwitchMethodStrsList':["row"]}
)
class RowerClass(
                                        BaseClass
                                ):

        #Definition
        RepresentingKeyStrsList=[
'RowingKeyStrsList',
'RowedGetStrToColumnStrOrderedDict',
'RowedColumnStrsList',
'RowedPickOrderedDict',
'RowedIsBoolsList',
                                                                'RowedIsBool',
                                                                'RowedIndexInt'
                                                        ]

        def default_init(
                                        self,
                                        _RowingKeyStrsList={
'DefaultValueType':property,
'PropertyInitVariable':[],
                                                        'PropertyDocStr':''
                                        },
                                        _RowedGetStrToColumnStrOrderedDict=None,
                                        _RowedColumnStrsList=None,
                                        _RowedPickOrderedDict=None,
                                        _RowedIsBoolsList=None,
                                        _RowedIsBool=False,
                                        _RowedIndexInt=-1,
                                        **_KwargVariablesDict
                                ):

                #Call the parent init method
                BaseClass.__init__(self,**_KwargVariablesDict)

        def setModelingDescriptionTuplesList(self,_SettingValueVariable):

                #debug
                '''
                self.debug(
                                        [
                                                'Before setting
ModelingDescriptionTuplesList',
('self.',self,['ModelingDescriptionTuplesList']),
                                                '_SettingValueVariable is
'+str(_SettingValueVariable)
                                        ]
                                )
                '''

                #set
                self._ModelingDescriptionTuplesList=_SettingValueVariable

                #debug
                '''
                self.debug(
                                        [
                                                'After',
('self.',self,['ModelingDescriptionTuplesList']),
                                                'We bind with
RowedGetStrToColumnStrOrderedDict setting',
                                        ]
                                )
                '''

                #Bind with RowedGetStrToColumnStrOrderedDict setting
                self.RowedGetStrToColumnStrOrderedDict=collections.OrderedDict(
                                map(
                                        lambda _ModelingSealTuple:
(_ModelingSealTuple[0],_ModelingSealTuple[1]),
                                        self._ModelingDescriptionTuplesList
                                        )
                                )

                #debug
                '''
                self.debug(
                                        [
('self.',self,['RowedGetStrToColumnStrOrderedDict'])
                                        ]
                                )
                '''

        ModelingDescriptionTuplesList=property(
BaseClass.ModelingDescriptionTuplesList.fget,
setModelingDescriptionTuplesList,
BaseClass.ModelingDescriptionTuplesList.fdel,
BaseClass.ModelingDescriptionTuplesList.__doc__
                                                                )

        def setRowingKeyStrsList(self,_SettingValueVariable):

                #debug
                '''
                self.debug('_SettingValueVariable '+str(_SettingValueVariable))
                '''

                #set
                self._RowingKeyStrsList=_SettingValueVariable

                #debug
                '''
                self.debug(
                                                [
                                                        'bind with
RowedColumnStrsList setting',
('self.',self,['RowedGetStrToColumnStrOrderedDict'])
                                                ]
                                        )
                '''

                #Bind with
                self.RowedColumnStrsList=map(
                                lambda __RowingGetStr:
self.RowedGetStrToColumnStrOrderedDict[__RowingGetStr],
                                _SettingValueVariable
                        )

                #debug
                '''
                self.debug(('self.',self,['RowedColumnStrsList']))
                '''

        #@Alerter.AlerterClass()
        #@Hooker.HookerClass(**{'HookingBeforeVariablesList':[{'CallingMethodStr
':"table"}]})
        def do_row(self):
                """"""

                #<NotHook>
                #table then
                self.table()
                #</NotHook>

                #Check
                if self.NodePointDeriveNoder!=None:

                        #debug
                        '''
                        self.NodePointDeriveNoder.debug('ParentSpeaking...')
                        '''

                        #Update
                        self.RowedPickOrderedDict.update(
                                zip(
                                        self.RowedColumnStrsList,
self.NodePointDeriveNoder.pick(self.RowingKeyStrsList)
                                )
                        )

                        #debug
                        '''
                        self.debug(('self.',self,[
'RowedPickOrderedDict',
'TabledTable'
                                                                ]))
                        '''

                        #Check if it was already rowed
                        self.RowedIsBoolsList=map(
                                        lambda __Row:
                                        all(
                                                map(
                                                                lambda
__RowedItemTuple:
SYS.getIsEqualBool(
                        __Row[__RowedItemTuple[0]],
                        __RowedItemTuple[1]
                ),
self.RowedPickOrderedDict.items()
                                                        )
                                                ),
                                        self.TabledTable.iterrows()
                                )

                        #debug
                        '''
                        self.debug(('self.',self,['RowedIsBoolsList']))
                        '''

                        #set
                        if len(self.RowedIsBoolsList)==0:
                                self.RowedIsBool=False
                        else:
                                self.RowedIsBool=any(self.RowedIsBoolsList)

                        #Init to the len of the table
                        self.RowedIndexInt=self.TabledTable.nrows

                        #But maybe find a last index
                        if self.RowedIsBool:
                                if len(self.RowedIsBoolsList)>0:
self.RowedIndexInt=self.RowedIsBoolsList.index(True)

                        #debug
                        '''
self.debug(('self.',self,['RowedIsBool','RowedIndexInt']))
                        '''

                #<NotHook>
                #Return self
                #return self
                #</NotHook>

#</DefineClass>

```

<small>
View the Rower sources on <a href="https://github.com/Ledoux/ShareYourSystem/tre
e/master/Pythonlogy/ShareYourSystem/Databasers/Rower" target="_blank">Github</a>
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
import tables
import ShareYourSystem as SYS
from ShareYourSystem.Standards.Noders import Structurer
from ShareYourSystem.Standards.Modelers import Rower

#Definition of a Structurer instance with a noded datar
MyStructurer=Structurer.StructurerClass().collect(
    "Datome",
    "Things",
    Rower.RowerClass().update(
        [
            (
                'Attr_ModelingDescriptionTuplesList',
                [
                    #GetStr #ColumnStr #Col
                    ('MyInt','MyInt',tables.Int64Col()),
                    ('MyStr','MyStr',tables.StringCol(10)),
                    ('MyIntsList','MyIntsList',(tables.Int64Col(shape=3)))
                ]
            ),
            ('Attr_RowingKeyStrsList',['MyInt'])
        ]
    )
)

#Tabular in it
MyStructurer.update(
[
    ('MyInt',0),
    ('MyStr',"hello"),
    ('MyIntsList',[2,4,1])
])['<Datome>ThingsRower'].row()

#Definition the AttestedStr
SYS._attest(
    [
        'MyStructurer is '+SYS._str(
        MyStructurer,
        **{
            'RepresentingBaseKeyStrsListBool':False,
            'RepresentingAlineaIsBool':False
        }
        ),
        'hdf5 file is : '+MyStructurer.hdfview().hdfclose().HdformatedConsoleStr
    ]
)

#Print



```


```console
>>>


*****Start of the Attest *****

MyStructurer is < (StructurerClass), 4563969424>
   /{
   /  '<New><Instance>DatomeCollectionOrderedDict' :
   /   /{
   /   /  'ThingsRower' : < (RowerClass), 4563968592>
   /   /   /{
   /   /   /  '<New><Instance>IdInt' : 4563968592
   /   /   /  '<New><Instance>NewtorkAttentionStr' :
   /   /   /  '<New><Instance>NewtorkCatchStr' :
   /   /   /  '<New><Instance>NewtorkCollectionStr' :
   /   /   /  '<New><Instance>NodeCollectionStr' : Datome
   /   /   /  '<New><Instance>NodeIndexInt' : 0
   /   /   /  '<New><Instance>NodeKeyStr' : ThingsRower
   /   /   /  '<New><Instance>NodePointDeriveNoder' : {...}< (StructurerClass),
4563969424>
   /   /   /  '<New><Instance>NodePointOrderedDict' : {...}< (OrderedDict),
4563600032>
   /   /   /  '<New><Instance>_ModelingDescriptionTuplesList' :
   /   /   /   /[
   /   /   /   /  0 :
   /   /   /   /   /(
   /   /   /   /   /  0 : MyInt
   /   /   /   /   /  1 : MyInt
   /   /   /   /   /  2 : Int64Col(shape=(), dflt=0, pos=None)
   /   /   /   /   /)
   /   /   /   /  1 :
   /   /   /   /   /(
   /   /   /   /   /  0 : MyStr
   /   /   /   /   /  1 : MyStr
   /   /   /   /   /  2 : StringCol(itemsize=10, shape=(), dflt='', pos=None)
   /   /   /   /   /)
   /   /   /   /  2 :
   /   /   /   /   /(
   /   /   /   /   /  0 : MyIntsList
   /   /   /   /   /  1 : MyIntsList
   /   /   /   /   /  2 : Int64Col(shape=(3,), dflt=0, pos=None)
   /   /   /   /   /)
   /   /   /   /]
   /   /   /  '<New><Instance>_RowingKeyStrsList' : ['MyInt']
   /   /   /  '<Spe><Class>RowingKeyStrsList' : {...}< (list), 4561768600>
   /   /   /  '<Spe><Instance>RowedColumnStrsList' : ['MyInt']
   /   /   /  '<Spe><Instance>RowedGetStrToColumnStrOrderedDict' :
   /   /   /   /{
   /   /   /   /  'MyInt' : MyInt
   /   /   /   /  'MyStr' : MyStr
   /   /   /   /  'MyIntsList' : MyIntsList
   /   /   /   /}
   /   /   /  '<Spe><Instance>RowedIndexInt' : 0
   /   /   /  '<Spe><Instance>RowedIsBool' : False
   /   /   /  '<Spe><Instance>RowedIsBoolsList' : []
   /   /   /  '<Spe><Instance>RowedPickOrderedDict' :
   /   /   /   /{
   /   /   /   /  'MyInt' : 0
   /   /   /   /}
   /   /   /}
   /   /}
   /  '<New><Instance>IdInt' : 4563969424
   /  '<New><Instance>MyInt' : 0
   /  '<New><Instance>MyIntsList' : [2, 4, 1]
   /  '<New><Instance>MyStr' : hello
   /  '<New><Instance>NewtorkAttentionStr' :
   /  '<New><Instance>NewtorkCatchStr' :
   /  '<New><Instance>NewtorkCollectionStr' :
   /  '<New><Instance>NodeCollectionStr' : Globals
   /  '<New><Instance>NodeIndexInt' : -1
   /  '<New><Instance>NodeKeyStr' : TopStructurer
   /  '<New><Instance>NodePointDeriveNoder' : None
   /  '<New><Instance>NodePointOrderedDict' : None
   /  '<Spe><Class>StructuringBeforeUpdateList' : None
   /  '<Spe><Class>StructuringNodeCollectionStrsList' : []
   /}

------

hdf5 file is : /                        Group
/TopStructurer           Group
/TopStructurer/FirstChildStructurer Group
/TopStructurer/FirstChildStructurer/GrandChildStructurer Group
/TopStructurer/SecondChildStructurer Group
/TopStructurer/SecondChildStructurer/OtherGrandChildStructurer Group
/xx0xxThingsFindoerTable Dataset {3/Inf}
    Data:
        (0) {RowInt=0, MyInt=1, MyIntsList=[0,0,1], MyStr="bonjour"},
        (1) {RowInt=1, MyInt=0, MyIntsList=[0,0,1], MyStr="guten tag"},
        (2) {RowInt=2, MyInt=1, MyIntsList=[0,0,0], MyStr="bonjour"}
/xx0xxThingsInserterTable Dataset {2/Inf}
    Data:
        (0) {RowInt=0, MyInt=1, MyIntsList=[2,4,6], MyStr="bonjour"},
        (1) {RowInt=1, MyInt=0, MyIntsList=[0,0,0], MyStr="hello"}
/xx0xxThingsRecovererTable Dataset {3/Inf}
    Data:
        (0) {RowInt=0, MyInt=1, MyIntsList=[0,0,1], MyStr="bonjour"},
        (1) {RowInt=1, MyInt=0, MyIntsList=[0,0,1], MyStr="guten tag"},
        (2) {RowInt=2, MyInt=1, MyIntsList=[0,0,0], MyStr="bonjour"}
/xx0xxThingsRetrieverTable Dataset {2/Inf}
    Data:
        (0) {RowInt=0, MyInt=1, MyIntsList=[2,4,6], MyStr="bonjour"},
        (1) {RowInt=1, MyInt=0, MyIntsList=[0,0,0], MyStr="guten tag"}
/xx0xxThingsRowerTable   Dataset {0/Inf}
    Data:

/xx0xxThingsTablerTable  Dataset {0/Inf}
    Data:

/xx0xx__UnitsInt_3__ThingsMergerTable Dataset {2/Inf}
    Data:
        (0) {RowInt=0, MyInt=0, MyIntsList=[0,0,1], MyStr="hello"},
        (1) {RowInt=1, MyInt=1, MyIntsList=[0,0,1], MyStr="bonjour"}
/xx0xx__UnitsInt_3__ThingsShaperTable Dataset {2/Inf}
    Data:
        (0) {RowInt=0, MyInt=0, MyIntsList=[0,0,1], MyStr="hello"},
        (1) {RowInt=1, MyInt=1, MyIntsList=[0,0,1], MyStr="bonjour"}
/xx1xx__UnitsInt_2__ThingsMergerTable Dataset {1/Inf}
    Data:
        (0) {RowInt=0, MyInt=0, MyIntsList=[0,0], MyStr=""}
/xx1xx__UnitsInt_2__ThingsShaperTable Dataset {1/Inf}
    Data:
        (0) {RowInt=0, MyInt=0, MyIntsList=[0,0], MyStr=""}


*****End of the Attest *****



```

