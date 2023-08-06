

<!--
FrozenIsBool False
-->

#Findoer

##Doc
----


>
> Findoer (sorry Finder is already an important module in python standards, so
just to be sure to not override...)
> instances helps to find in a hdf5 table RowedVariablesList corresponding to
the FindingConditionVariable.
>
>

----

<small>
View the Findoer notebook on [NbViewer](http://nbviewer.ipython.org/url/shareyou
rsystem.ouvaton.org/Findoer.ipynb)
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


Findoer (sorry Finder is already an important module in python standards, so
just to be sure to not override...)
instances helps to find in a hdf5 table RowedVariablesList corresponding to the
FindingConditionVariable.

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Modelers.Retriever"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>

#from ShareYourSystem.Functers import Argumenter,Hooker
from ShareYourSystem.Standards.Modelers import Rower
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class FindoerClass(BaseClass):

        #Definition
        RepresentingKeyStrsList=[
'FindingConditionVariable',
'FoundRowDictsList',
'FoundFilterRowDictsList'
                                                                ]

        def default_init(self,
                                        _FindingConditionVariable=None,
                                        _FoundRowDictsList=None,
                                        _FoundFilterRowDictsList=None,
                                        _FoundIsBool=False,
                                        **_KwargVariablesDict
                                ):

                #Call the parent init method
                BaseClass.__init__(self,**_KwargVariablesDict)

        #@Hooker.HookerClass(**{'HookingAfterVariablesList':[{'CallingMethodStr'
:"table"}]})
        #@Argumenter.ArgumenterClass()
        def do_find(self):

                #debug
                '''
self.debug(("self.",self,['ModeledKeyStr','FindingConditionVariable']))
                '''

                #<NotHook>
                #table first
                self.table()
                #</NotHook>

                #If the FoundRowedTuplesList was not yet setted
                if self.FoundIsBool==False:

                        #debug
                        '''
                        self.debug('FoundRowDictsList was not yet setted')
                        '''

                        #Take the first one in the list
                        self.FoundRowDictsList=Rower.getRowedDictsListWithTable(
                self.TabularedGroupVariable._f_getChild(
                        self.TabularedTableKeyStrsList[0]
                )
        )

                        #set
                        self.FoundIsBool=True

                #debug
                '''
                self.debug(
                                                [
("self.",self,['FoundRowDictsList'])
                                                ]
                                )
                '''

                #Now find really !
                self.FoundFilterRowDictsList=SYS.filterNone(
                                                                SYS.where(
        self.FoundRowDictsList,
        self.FindingConditionVariable
                                                                )
                                                        )

                #debug
                '''
                self.debug(
                                        [
                                                'The where is over now',
("self.",self,['FoundFilterRowDictsList'])
                                        ]

                                )
                '''

                #<NotHook>
                #Return self
                #return self
                #</NotHook>

#</DefineClass>


```

<small>
View the Findoer sources on <a href="https://github.com/Ledoux/ShareYourSystem/t
ree/master/Pythonlogy/ShareYourSystem/Databasers/Findoer"
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
import tables,operator

import ShareYourSystem as SYS
from ShareYourSystem.Standards.Noders import Structurer
from ShareYourSystem.Standards.Modelers import Findoer

#Definition of a Structurer instance with a noded datar
MyStructurer=Structurer.StructurerClass().collect(
    "Datome",
    "Things",
    Findoer.FindoerClass().update(
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
            ('Attr_RowingKeyStrsList',['MyInt','MyStr','MyIntsList'])
        ]
    )
)

MyStructurer.update(
            [
                ('MyInt',1),
                ('MyStr',"bonjour"),
                ('MyIntsList',[0,0,1])
            ]
)['<Datome>ThingsFindoer'].insert()

MyStructurer.update(
            [
                ('MyInt',0),
                ('MyStr',"guten tag"),
                ('MyIntsList',[0,0,1])
            ]
)['<Datome>ThingsFindoer'].insert()

MyStructurer.update(
            [
                ('MyInt',1),
                ('MyStr',"bonjour"),
                ('MyIntsList',[0,0,0])
            ]
)['<Datome>ThingsFindoer'].insert()

#Retrieve
MyStructurer['<Datome>ThingsFindoer'].find(
                                        [
                                            ('MyInt',(operator.eq,1)),
('MyIntsList',(SYS.getIsEqualBool,[0,0,1]))
                                        ]
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

MyStructurer is < (StructurerClass), 4559346064>
   /{
   /  '<New><Instance>DatomeCollectionOrderedDict' :
   /   /{
   /   /  'ThingsFindoer' : < (FindoerClass), 4563943952>
   /   /   /{
   /   /   /  '<New><Instance>IdInt' : 4563943952
   /   /   /  '<New><Instance>NewtorkAttentionStr' :
   /   /   /  '<New><Instance>NewtorkCatchStr' :
   /   /   /  '<New><Instance>NewtorkCollectionStr' :
   /   /   /  '<New><Instance>NodeCollectionStr' : Datome
   /   /   /  '<New><Instance>NodeIndexInt' : 0
   /   /   /  '<New><Instance>NodeKeyStr' : ThingsFindoer
   /   /   /  '<New><Instance>NodePointDeriveNoder' : {...}< (StructurerClass),
4559346064>
   /   /   /  '<New><Instance>NodePointOrderedDict' : {...}< (OrderedDict),
4563689008>
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
   /   /   /  '<New><Instance>_RowingKeyStrsList' : ['MyInt', 'MyStr',
'MyIntsList']
   /   /   /  '<Spe><Instance>FindingConditionVariable' :
   /   /   /   /[
   /   /   /   /  0 :
   /   /   /   /   /(
   /   /   /   /   /  0 : MyInt
   /   /   /   /   /  1 :
   /   /   /   /   /   /(
   /   /   /   /   /   /  0 : <built-in function eq>
   /   /   /   /   /   /  1 : 1
   /   /   /   /   /   /)
   /   /   /   /   /)
   /   /   /   /  1 :
   /   /   /   /   /(
   /   /   /   /   /  0 : MyIntsList
   /   /   /   /   /  1 :
   /   /   /   /   /   /(
   /   /   /   /   /   /  0 : <function getIsEqualBool at 0x10dae4de8>
   /   /   /   /   /   /  1 : [0, 0, 1]
   /   /   /   /   /   /)
   /   /   /   /   /)
   /   /   /   /]
   /   /   /  '<Spe><Instance>FoundFilterRowDictsList' :
   /   /   /   /[
   /   /   /   /  0 :
   /   /   /   /   /{
   /   /   /   /   /  'RowInt' : 0
   /   /   /   /   /  'MyInt' : 1
   /   /   /   /   /  'MyIntsList' : array([0, 0, 1])
   /   /   /   /   /  'MyStr' : bonjour
   /   /   /   /   /}
   /   /   /   /]
   /   /   /  '<Spe><Instance>FoundRowDictsList' :
   /   /   /   /[
   /   /   /   /  0 : {...}< (dict), 4561836304>
   /   /   /   /  1 :
   /   /   /   /   /{
   /   /   /   /   /  'RowInt' : 1
   /   /   /   /   /  'MyInt' : 0
   /   /   /   /   /  'MyIntsList' : array([0, 0, 1])
   /   /   /   /   /  'MyStr' : guten tag
   /   /   /   /   /}
   /   /   /   /  2 :
   /   /   /   /   /{
   /   /   /   /   /  'RowInt' : 2
   /   /   /   /   /  'MyInt' : 1
   /   /   /   /   /  'MyIntsList' : array([0, 0, 0])
   /   /   /   /   /  'MyStr' : bonjour
   /   /   /   /   /}
   /   /   /   /]
   /   /   /}
   /   /}
   /  '<New><Instance>IdInt' : 4559346064
   /  '<New><Instance>MyInt' : 1
   /  '<New><Instance>MyIntsList' : [0, 0, 0]
   /  '<New><Instance>MyStr' : bonjour
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

