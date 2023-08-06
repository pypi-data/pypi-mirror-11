

<!--
FrozenIsBool False
-->

#Inserter

##Doc
----


>
> Inserter instances can insert a RowedVariablesList into a table
> checking maybe before if this line is new in the table or not
> depending on identifying items.
>
>

----

<small>
View the Inserter notebook on [NbViewer](http://nbviewer.ipython.org/url/shareyou
rsystem.ouvaton.org/Inserter.ipynb)
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


Inserter instances can insert a RowedVariablesList into a table
checking maybe before if this line is new in the table or not
depending on identifying items.

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
import collections
BaseModuleStr="ShareYourSystem.Standards.Modelers.Rower"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class InserterClass(
                                        BaseClass,
                                ):

        #Definition
        RepresentingKeyStrsList=[
'InsertedNotRowGetStrsList',
'InsertedNotRowColumnStrsList',
'InsertedNotRowPickOrderedDict',
'InsertedIndexInt'
                                                                ]

        def default_init(self,
                                        _InsertedNotRowGetStrsList=None,
                                        _InsertedNotRowColumnStrsList=None,
                                        _InsertedNotRowPickOrderedDict=None,
                                        _InsertedIndexInt=-1,
                                        **_KwargVariablesDict
                                        ):

                #Call the parent init method
                BaseClass.__init__(self,**_KwargVariablesDict)

        def setRowingKeyStrsList(self,_SettingValueVariable):

                #Hook
                BaseClass.setRowingKeyStrsList(self,_SettingValueVariable)

                #Bind
                self.InsertedNotRowGetStrsList=list(set(SYS.unzip(
                        self.ModelingDescriptionTuplesList,[0]
                ))-set(self.RowingKeyStrsList))

                #set
                self.InsertedNotRowColumnStrsList=map(
                        lambda __NotRowGetStr:
                        self.RowedGetStrToColumnStrOrderedDict[__NotRowGetStr],
                        self.InsertedNotRowGetStrsList
                )
        RowingKeyStrsList=property(
BaseClass.RowingKeyStrsList.fget,
setRowingKeyStrsList,
BaseClass.RowingKeyStrsList.fdel,
BaseClass.RowingKeyStrsList.__doc__
                                                                )


        def do_insert(self):
                """ """

                #debug
                '''
                self.debug('row maybe before...')
                '''

                #<NotHook>
                #row first
                self.row()
                #</NotHook>

                #debug
                '''
                self.debug(
                                        ('self.',self,['RowedIsBool'])
                                )
                self.NodePointDeriveNoder.debug([
                                ('NOTE : ...ParentSpeaking...')
                        ])
                '''

                """
                map(
                                lambda __InitVariable:
                                setattr(
                                        self,
                                        __KeyStr,
SYS.getInitiatedVariableWithKeyStr(__KeyStr)
                                ) if __InitVariable==None else None,
                                map(
                                                lambda __KeyStr:
                                                (
                                                        __KeyStr,
                                                        getattr(self,__KeyStr)
                                                ),
                                                [
'InsertedNotRowPickOrderedDict',
'InsertedNotRowGetStrsList',
'InsertedNotRowGetStrsList',
'InsertedNotRowPickOrderedDict'
                                                ]
                                        )
                        )
                """

                #debug
                '''
                self.debug(('self.',self,['InsertedNotRowPickOrderedDict']))
                '''

                #Append and row if it is new
                if self.RowedIsBool==False:

                        #Check
                        if self.TabledTable!=None:

                                #debug
                                '''
                                self.debug('This is a new row')
                                '''

                                #Get the row
                                Row=None
                                Row=self.TabledTable.row

                                #debug
                                '''
self.debug(('self.',self,['InsertedNotRowPickOrderedDict']))
                                '''

                                #Pick and update
                                self.InsertedNotRowPickOrderedDict.update(
                                zip(
                                        self.InsertedNotRowColumnStrsList,
                                        self.NodePointDeriveNoder.pick(
                                                self.InsertedNotRowGetStrsList
                                                )
                                        )
                                )

                                #debug
                                '''
                                self.debug(('self.',self,[
        'RowedPickOrderedDict',
        'InsertedNotRowPickOrderedDict'
]))
                                '''

                                #Definition the InsertedItemTuplesList
                                InsertedItemTuplesList=[
('RowInt',self.RowedIndexInt)
]+self.RowedPickOrderedDict.items(
)+self.InsertedNotRowPickOrderedDict.items()

                                #import tables
                                #print(tables.tableextension.Row)

                                #debug
                                '''
                                self.debug(
                                                        [
                                                                'This is a new
row',
                                                                'Colnames are :
'+str(self.TabledTable.colnames),
'InsertedItemTuplesList is '+str(InsertedItemTuplesList),
'self.TabledTable is '+str(dir(self.TabledTable)),
'self.ModeledDescriptionClass is '+(str(self.ModeledDescriptionClass.columns) if
hasattr(self.ModeledDescriptionClass,'columns') else ""),
                                                                'Row is
'+str(dir(Row)),
                                                                'Row.table is
'+str(Row.table),
'TabularedTablesOrderedDict is '+str(self.TabularedTablesOrderedDict)
                                                        ]
                                                )
                                '''

                                #set
                                map(
                                                lambda __InsertingTuple:
Row.__setitem__(*__InsertingTuple),
                                                InsertedItemTuplesList
                                        )

                                #debug
                                '''
                                self.debug('The Row setting was good, so append
insert')
                                '''

                                #Append and Insert
                                Row.append()
                                self.TabledTable.insert()

                else:

                        #debug
                        '''
                        self.debug(
                                                [
                                                        'This is maybe not an
IdentifyingInserter',
                                                        'Or it is already
rowed',
                                                        'self.InsertedIsBoolsList
is '+str(self.InsertedIsBoolsList)
                                                ]
                                        )
                        '''
                        pass

                #<NotHook>
                #Return self
                #return self
                #</NotHook>

#</DefineClass>

```

<small>
View the Inserter sources on <a href="https://github.com/Ledoux/ShareYourSystem/t
ree/master/Pythonlogy/ShareYourSystem/Databasers/Inserter"
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
import tables
import ShareYourSystem as SYS
from ShareYourSystem.Standards.Noders import Structurer
from ShareYourSystem.Standards.Modelers import Inserter

#Definition of a Structurer instance with a noded datar
MyStructurer=Structurer.StructurerClass().collect(
    "Datome",
    "Things",
    Inserter.InserterClass().update(
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

#Definition a structure with a db
MyStructurer.update(
            [
                ('MyInt',1),
                ('MyStr',"bonjour"),
                ('MyIntsList',[2,4,6])
            ]
).command(
    _UpdateList=[('insert',{'LiargVariablesList':[]})],
    **{'GatheringVariablesList':['<Datome>ThingsInserter']}
).update(
            [
                ('MyInt',0),
                ('MyStr',"hello"),
                ('MyIntsList',[0,0,0])
            ]
).command(
    _UpdateList=[('insert',{'LiargVariablesList':[]})],
)

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

MyStructurer is < (StructurerClass), 4563962256>
   /{
   /  '<New><Instance>DatomeCollectionOrderedDict' :
   /   /{
   /   /  'ThingsInserter' : < (InserterClass), 4563961296>
   /   /   /{
   /   /   /  '<New><Instance>IdInt' : 4563961296
   /   /   /  '<New><Instance>NewtorkAttentionStr' :
   /   /   /  '<New><Instance>NewtorkCatchStr' :
   /   /   /  '<New><Instance>NewtorkCollectionStr' :
   /   /   /  '<New><Instance>NodeCollectionStr' : Datome
   /   /   /  '<New><Instance>NodeIndexInt' : 0
   /   /   /  '<New><Instance>NodeKeyStr' : ThingsInserter
   /   /   /  '<New><Instance>NodePointDeriveNoder' : {...}< (StructurerClass),
4563962256>
   /   /   /  '<New><Instance>NodePointOrderedDict' : {...}< (OrderedDict),
4563687232>
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
   /   /   /  '<Spe><Class>InsertedIndexInt' : -1
   /   /   /  '<Spe><Instance>InsertedNotRowColumnStrsList' : ['MyStr',
'MyIntsList']
   /   /   /  '<Spe><Instance>InsertedNotRowGetStrsList' : ['MyStr',
'MyIntsList']
   /   /   /  '<Spe><Instance>InsertedNotRowPickOrderedDict' :
   /   /   /   /{
   /   /   /   /}
   /   /   /}
   /   /}
   /  '<New><Instance>IdInt' : 4563962256
   /  '<New><Instance>MyInt' : 0
   /  '<New><Instance>MyIntsList' : [0, 0, 0]
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

