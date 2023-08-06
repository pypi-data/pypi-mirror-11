

<!--
FrozenIsBool False
-->

#Retriever

##Doc
----


>
> Retriever instances can retrieve InsertedVariablesList given their
> IndexInt of their corresponding table and their RowInt
> (ie their index of their inserted line).
>
>

----

<small>
View the Retriever notebook on [NbViewer](http://nbviewer.ipython.org/url/sharey
oursystem.ouvaton.org/Retriever.ipynb)
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


Retriever instances can retrieve InsertedVariablesList given their
IndexInt of their corresponding table and their RowInt
(ie their index of their inserted line).

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Modelers.Inserter"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import collections
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class RetrieverClass(BaseClass):

        #Definition
        RepresentingKeyStrsList=[
'RetrievingIndexesList',
'RetrievedColumnStrToGetStrOrderedDict',
'RetrievedRowInt',
'RetrievedTable',
'RetrievedPickOrderedDict'
                                                                ]

        def default_init(self,
                                                _RetrievingIndexesList=None,
_RetrievedColumnStrToGetStrOrderedDict=None,
                                                _RetrievedRowInt=-1,
                                                _RetrievedTable=None,
                                                _RetrievedPickOrderedDict=None,
                                                **_KwargVariablesDict
                        ):

                #Call the parent init method
                BaseClass.__init__(self,**_KwargVariablesDict)

        def setModelingDescriptionTuplesList(self,_SettingValueVariable):

                #debug
                '''
                self.debug('Before we call the parent setModelingDescriptionTuplesList
method ')
                '''

                #Hook
                BaseClass.setModelingDescriptionTuplesList(self,_SettingValueVariable)

                #Bind with RetrievedColumnStrToGetStrOrderedDict setting
                if self.RetrievedColumnStrToGetStrOrderedDict==None:
self.RetrievedColumnStrToGetStrOrderedDict=collections.OrderedDict()
                map(
                        lambda __ModelingColumnTuple:
                        self.RetrievedColumnStrToGetStrOrderedDict.__setitem__(
                                __ModelingColumnTuple[1],
                                __ModelingColumnTuple[0]
                        ),
                        self.ModelingDescriptionTuplesList
                )

                #Init
                if self.RetrievedPickOrderedDict==None:
                        self.RetrievedPickOrderedDict=collections.OrderedDict()

                #debug
                '''
self.debug(('self.',self,['RetrievedColumnStrToGetStrOrderedDict']))
                '''

        ModelingDescriptionTuplesList=property(
BaseClass.ModelingDescriptionTuplesList.fget,
setModelingDescriptionTuplesList,
BaseClass.ModelingDescriptionTuplesList.fdel,
BaseClass.ModelingDescriptionTuplesList.__doc__
                                                                )

        #@Hooker.HookerClass(**{'HookingAfterVariablesList':[{"CallingMethodStr"
:"table"}]})
        def do_retrieve(self):

                #debug
                '''
                self.debug(
                                        [
                                                ('self.',self,[
'TabularedTableKeyStrsList',
'RetrievingIndexesList'
                                                                        ])
                                        ]
                                )
                '''

                #<NotHook>
                #table first
                self.table()
                #</NotHook>

                #debug
                '''
                self.debug(
                                        [
                                                ('Ok table is done'),
('self.',self,['TabularedTablesOrderedDict','TabularedTableKeyStrsList'])
                                        ]
                                )
                '''

                #set the RetrievedRowInt
                self.RetrievedRowInt=self.RetrievingIndexesList[1]

                #Definition the RetrievedTable
                self.RetrievedTable=self.TabularedTablesOrderedDict[
                        self.TabularedTableKeyStrsList[
                                self.RetrievingIndexesList[0]
                        ]
                ]

                #debug
                '''
self.debug(('self.',self,['RetrievedRowInt','RetrievedTable']))
                '''

                #Definition the RetrievedRowsList
                for __RetrievedRow in self.RetrievedTable.iterrows():
                        if __RetrievedRow['RowInt']==self.RetrievedRowInt:

                                #debug
                                '''
                                self.debug('self.RetrievedTable.colnames is
'+str(self.RetrievedTable.colnames))
                                '''

                                #Init
                                if self.RetrievedPickOrderedDict==None:
self.RetrievedPickOrderedDict=collections.OrderedDict()

                                #set
                                map(
                                        lambda __ColumnStr:
self.RetrievedPickOrderedDict.__setitem__(
self.RetrievedColumnStrToGetStrOrderedDict[__ColumnStr],
                                                __RetrievedRow[__ColumnStr]
                                                ) if __ColumnStr in
self.RetrievedColumnStrToGetStrOrderedDict else None
                                        ,
                                        self.RetrievedTable.colnames
                                )

                                #debug
                                '''
                                self.debug('RetrievedPickOrderedDict is setted')
                                '''

                #debug
                '''
                self.debug(
                                        [
('self.',self,['RetrievedPickOrderedDict'])
                                        ]
                                )
                '''

                #Update
                self.NodePointDeriveNoder.update(
                        self.RetrievedPickOrderedDict.items(),
                        **{'RestrictingIsBool':True}
                )
                self.NodePointDeriveNoder.RestrictingIsBool=False

                #debug
                '''
                self.debug('Update was done')
                '''

                #<NotHook>
                #Return self
                #return self
                #</NotHook>

#</DefineClass>

```

<small>
View the Retriever sources on <a href="https://github.com/Ledoux/ShareYourSystem
/tree/master/Pythonlogy/ShareYourSystem/Databasers/Retriever"
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
from ShareYourSystem.Standards.Noders import Structurer
from ShareYourSystem.Standards.Modelers import Retriever
import tables

#Definition of a Structurer instance with a noded datar
MyStructurer=Structurer.StructurerClass().collect(
    "Datome",
    "Things",
    Retriever.RetrieverClass().update(
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

MyStructurer.update(
            [
                ('MyInt',1),
                ('MyStr',"bonjour"),
                ('MyIntsList',[2,4,6])
            ]
).command(
    _UpdateList=[('insert',{'LiargVariablesList':[]})],
    **{'GatheringVariablesList':['<Datome>ThingsRetriever']}
).update(
            [
                ('MyInt',0),
                ('MyStr',"guten tag"),
                ('MyIntsList',[0,0,0])
            ]
).command(
    _UpdateList=[('insert',{'LiargVariablesList':[]})],
)


#Retrieve
MyStructurer['<Datome>ThingsRetriever'].__setitem__(
    'RetrievingIndexesList',(0,1)
).retrieve()

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

MyStructurer is < (StructurerClass), 4563994000>
   /{
   /  '<New><Instance>DatomeCollectionOrderedDict' :
   /   /{
   /   /  'ThingsRetriever' : < (RetrieverClass), 4559653840>
   /   /   /{
   /   /   /  '<New><Instance>IdInt' : 4559653840
   /   /   /  '<New><Instance>NewtorkAttentionStr' :
   /   /   /  '<New><Instance>NewtorkCatchStr' :
   /   /   /  '<New><Instance>NewtorkCollectionStr' :
   /   /   /  '<New><Instance>NodeCollectionStr' : Datome
   /   /   /  '<New><Instance>NodeIndexInt' : 0
   /   /   /  '<New><Instance>NodeKeyStr' : ThingsRetriever
   /   /   /  '<New><Instance>NodePointDeriveNoder' : {...}< (StructurerClass),
4563994000>
   /   /   /  '<New><Instance>NodePointOrderedDict' : {...}< (OrderedDict),
4561445536>
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
   /   /   /  '<Spe><Instance>RetrievedColumnStrToGetStrOrderedDict' :
   /   /   /   /{
   /   /   /   /  'MyInt' : MyInt
   /   /   /   /  'MyStr' : MyStr
   /   /   /   /  'MyIntsList' : MyIntsList
   /   /   /   /}
   /   /   /  '<Spe><Instance>RetrievedRowInt' : 1
   /   /   /  '<Spe><Instance>RetrievedPickOrderedDict' :
   /   /   /   /{
   /   /   /   /  'MyInt' : 0
   /   /   /   /  'MyIntsList' : array([0, 0, 0])
   /   /   /   /  'MyStr' : guten tag
   /   /   /   /}
   /   /   /  '<Spe><Instance>RetrievedTable' : /xx0xxThingsRetrieverTable
(Table(2,)) 'This is the ThingsRetrieverModelClass'
  description := {
  "RowInt": Int64Col(shape=(), dflt=0, pos=0),
  "MyInt": Int64Col(shape=(), dflt=0, pos=1),
  "MyIntsList": Int64Col(shape=(3,), dflt=0, pos=2),
  "MyStr": StringCol(itemsize=10, shape=(), dflt='', pos=3)}
  byteorder := 'little'
  chunkshape := (1310,)
   /   /   /  '<Spe><Instance>RetrievingIndexesList' : (0, 1)
   /   /   /}
   /   /}
   /  '<New><Instance>IdInt' : 4563994000
   /  '<New><Instance>MyInt' : 0
   /  '<New><Instance>MyIntsList' : {...}< (ndarray), 4563990288>
   /  '<New><Instance>MyStr' : guten tag
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

