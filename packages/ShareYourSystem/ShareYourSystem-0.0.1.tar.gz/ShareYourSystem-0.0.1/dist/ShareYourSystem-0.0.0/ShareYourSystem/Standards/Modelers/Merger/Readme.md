

<!--
FrozenIsBool False
-->

#Merger

##Doc
----


>
> Merger instances help for reloading rowed variables from
> different tables but with different shaping variables.
> The results is a list of rowed items from merged tables.
>
>

----

<small>
View the Merger notebook on [NbViewer](http://nbviewer.ipython.org/url/shareyour
system.ouvaton.org/Merger.ipynb)
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


Merger instances help for reloading rowed variables from
different tables but with different shaping variables.
The results is a list of rowed items from merged tables.

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Modelers.Shaper"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import operator
Shaper=BaseModule
from ShareYourSystem.Standards.Modelers import Tabler,Rower,Recoverer
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class MergerClass(BaseClass):

        #Definition
        RepresentingKeyStrsList=[
'MergingConditionVariable',
'MergedRowedDictsList'
                                                                ]

        def default_init(self,
                                        _MergingConditionVariable=None,
                                        _MergedRowedDictsList=None,
                                        **_KwargVariablesDict
                                ):

                #Call the parent init method
                BaseClass.__init__(self,**_KwargVariablesDict)

        def mimic_find(self):

                #<NotHook>
                #merge first
                self.merge()
                #</NotHook>

                #Bound the FoundRowDictsList with the MergedRowedDictsList one
                self.FoundRowDictsList=self.MergedRowedDictsList

                #<NotHook>
                #find then
                BaseClass.find(self)
                #</NotHook>

        def do_merge(self):

                #debug
                '''
                self.debug(
                                        ('self.',self,[
'ModeledKeyStr',
'MergingConditionVariable',
'TabularedTableKeyStrsList'
                                                                        ])
                                )
                '''

                #Debug
                '''
                print(

                                map(
                                                        lambda
__TabularedKeyStr:
__TabularedKeyStr.split(Shaper.ShapingJoiningStr),
                                                self.TabularedTableKeyStrsList
                                        )
                        )
                '''

                #Bind with MergedShapingDictsList setting
                MergedShapingDictsList=map(
                                                                lambda
__StrsList:
                                                                dict(
                                                                        map(
        lambda __ShapingStr:
        SYS.getUnSerializedTuple(
                self.NodePointDeriveNoder,
                __ShapingStr.split(
                        Shaper.ShapingTuplingStr
                )
        )
        #Remove the suffix and the prefix
        ,__StrsList[1:-1] if len(__StrsList)>2 else []
)
                                                                ),
                                                                map(
                                                                        lambda
__TabularedKeyStr:
__TabularedKeyStr.split(Shaper.ShapingJoiningStr),
self.TabularedTableKeyStrsList
                                                                )
                                                )

                #debug
                '''
                self.debug('MergedShapingDictsList is
'+str(MergedShapingDictsList))
                '''

                #Bind with MergedFilteredShapingDictsList
                MergedFilteredShapingDictsList=SYS.where(
MergedShapingDictsList,
self.MergingConditionVariable
                                                                        )

                #debug
                '''
                self.debug('MergedFilteredShapingDictsList is
'+str(MergedFilteredShapingDictsList))
                '''

                #Bind with MergedTablesList setting
                MergedTablesList=SYS.filterNone(
                                                                        map(
        lambda __Table,__MergedFilteredShapingDict:
        __Table
        if __MergedFilteredShapingDict!=None
        else None,
        self.TabularedTablesOrderedDict.values(),
        MergedFilteredShapingDictsList
                                                                        ))

                MergedRowedDictsListsList=map(
                                lambda __MergedTable:
                                map(
                                                lambda __RowedDict:
                                                dict(__RowedDict,**{
                                                                'TabledInt':int(
                __MergedTable.name.split(Tabler.TablingOrderStr)[1]
        )
                                                        }
                                                ),
Rower.getRowedDictsListWithTable(__MergedTable)
                                        ),
                                MergedTablesList
                        )

                #debug
                '''
                self.debug('MergedRowedDictsListsList is
'+str(MergedRowedDictsListsList))
                '''

                #Reduce
                if len(MergedRowedDictsListsList)>0:
self.MergedRowedDictsList=reduce(operator.__add__,MergedRowedDictsListsList)

#</DefineClass>

```

<small>
View the Merger sources on <a href="https://github.com/Ledoux/ShareYourSystem/tr
ee/master/Pythonlogy/ShareYourSystem/Databasers/Merger"
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
import operator,tables
import ShareYourSystem as SYS
from ShareYourSystem.Standards.Noders import Structurer
from ShareYourSystem.Standards.Modelers import Merger

#Definition a structure
MyStructurer=Structurer.StructurerClass().collect(
    "Datome",
    "Things",
    Merger.MergerClass().update(
        [
            ('Attr_ModelingDescriptionTuplesList',
                [
                    ('MyInt','MyInt',tables.Int64Col()),
                    ('MyStr','MyStr',tables.StringCol(10)),
                    ('MyIntsList','MyIntsList',tables.Int64Col(shape=[3]))
                ]
            ),
            ('Attr_RowingKeyStrsList',
                ['MyInt','MyStr']
            ),
            ('ShapingDimensionTuplesList',
                [
                    ('MyIntsList',['UnitsInt'])
                ]
            )
        ]
    )
)

MyStructurer.update(
    [
        ('MyInt',0),
        ('MyStr',"hello"),
        ('UnitsInt',3),
        ('MyIntsList',[0,0,1])
    ]
)['<Datome>ThingsMerger'].insert()

MyStructurer.update(
    [
        ('MyInt',1),
        ('MyStr',"bonjour"),
        ('MyIntsList',[0,0,1])
    ]
)['<Datome>ThingsMerger'].insert()

MyStructurer.update(
    [
        ('MyInt',1),
        ('MyStr',"ola"),
        ('MyIntsList',[0,1])
    ]
)['<Datome>ThingsMerger'].insert()

#Merge
MyStructurer['<Datome>ThingsMerger'].merge(
            [
                ('UnitsInt',(operator.gt,2))
            ]
)

#Definition the AttestedStr
SYS._attest(
    [
        'MyStructurer is '+SYS._str(
        MyStructurer,
        **{
            'RepresentingAlineaIsBool':False,
            'RepresentingBaseKeyStrsListBool':False
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

MyStructurer is < (StructurerClass), 4564328080>
   /{
   /  '<New><Instance>DatomeCollectionOrderedDict' :
   /   /{
   /   /  'ThingsMerger' : < (MergerClass), 4564328144>
   /   /   /{
   /   /   /  '<New><Instance>IdInt' : 4564328144
   /   /   /  '<New><Instance>NewtorkAttentionStr' :
   /   /   /  '<New><Instance>NewtorkCatchStr' :
   /   /   /  '<New><Instance>NewtorkCollectionStr' :
   /   /   /  '<New><Instance>NodeCollectionStr' : Datome
   /   /   /  '<New><Instance>NodeIndexInt' : 0
   /   /   /  '<New><Instance>NodeKeyStr' : ThingsMerger
   /   /   /  '<New><Instance>NodePointDeriveNoder' : {...}< (StructurerClass),
4564328080>
   /   /   /  '<New><Instance>NodePointOrderedDict' : {...}< (OrderedDict),
4563600032>
   /   /   /  '<New><Instance>ShapedErrorBool' : True
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
   /   /   /   /   /  2 : Int64Col(shape=(2,), dflt=0, pos=None)
   /   /   /   /   /)
   /   /   /   /]
   /   /   /  '<New><Instance>_RowingKeyStrsList' : ['MyInt', 'MyStr']
   /   /   /  '<Spe><Instance>MergedRowedDictsList' :
   /   /   /   /[
   /   /   /   /  0 :
   /   /   /   /   /{
   /   /   /   /   /  'RowInt' : 0
   /   /   /   /   /  'MyInt' : 0
   /   /   /   /   /  'MyIntsList' : array([0, 0, 1])
   /   /   /   /   /  'MyStr' : hello
   /   /   /   /   /  'TabledInt' : 0
   /   /   /   /   /}
   /   /   /   /  1 :
   /   /   /   /   /{
   /   /   /   /   /  'RowInt' : 1
   /   /   /   /   /  'MyInt' : 1
   /   /   /   /   /  'MyIntsList' : array([0, 0, 1])
   /   /   /   /   /  'MyStr' : bonjour
   /   /   /   /   /  'TabledInt' : 0
   /   /   /   /   /}
   /   /   /   /]
   /   /   /  '<Spe><Instance>MergingConditionVariable' :
   /   /   /   /[
   /   /   /   /  0 :
   /   /   /   /   /(
   /   /   /   /   /  0 : UnitsInt
   /   /   /   /   /  1 :
   /   /   /   /   /   /(
   /   /   /   /   /   /  0 : <built-in function gt>
   /   /   /   /   /   /  1 : 2
   /   /   /   /   /   /)
   /   /   /   /   /)
   /   /   /   /]
   /   /   /}
   /   /}
   /  '<New><Instance>IdInt' : 4564328080
   /  '<New><Instance>MyInt' : 1
   /  '<New><Instance>MyIntsList' : [0, 1]
   /  '<New><Instance>MyStr' : ola
   /  '<New><Instance>NewtorkAttentionStr' :
   /  '<New><Instance>NewtorkCatchStr' :
   /  '<New><Instance>NewtorkCollectionStr' :
   /  '<New><Instance>NodeCollectionStr' : Globals
   /  '<New><Instance>NodeIndexInt' : -1
   /  '<New><Instance>NodeKeyStr' : TopStructurer
   /  '<New><Instance>NodePointDeriveNoder' : None
   /  '<New><Instance>NodePointOrderedDict' : None
   /  '<New><Instance>UnitsInt' : 2
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

