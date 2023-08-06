

<!--
FrozenIsBool False
-->

#Joiner

##Doc
----


> Joiner instances helps to insert in joined databases, get the corresponding
> RetrieveIndexesLists if it was already inserted, and then insert locally
> depending if it is a new row compared to all JoinedRetrieveIndexesListsList
>
>

----

<small>
View the Joiner notebook on [NbViewer](http://nbviewer.ipython.org/url/shareyour
system.ouvaton.org/Joiner.ipynb)
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

Joiner instances helps to insert in joined databases, get the corresponding
RetrieveIndexesLists if it was already inserted, and then insert locally
depending if it is a new row compared to all JoinedRetrieveIndexesListsList

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Modelers.Merger"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
Featurer=BaseModule
import collections
import tables
from ShareYourSystem.Standards.Modelers import Modeler
#</ImportSpecificModules>

#<DefineLocals>
JoinStr='__'
JoinDeepStr='/'
#</DefineLocals>

#<DefineFunctions>
def getJoinedRetrieveIndexesListWithInstanceVariableAndDeriveDatabaser(
        _InstanceVariable,_DeriveDatabaser):

        #Table
        _DeriveDatabaser.table().pick(['TabledInt',-1])

        #set the JoinedRetrieveIndexesListKeyStr
        return [_DeriveDatabaser.TabledInt,-1]
#<DefineFunctions>

#<DefineClass>
@DecorationClass(**{
        'ClassingSwitchMethodStrsList':[
                'model',
                'tabular',
                'join',
                'insert'
        ]
})
class JoinerClass(BaseClass):

        #Definition
        RepresentingKeyStrsList=[
'JoiningCollectionStr',
'JoiningCatchStr',
'JoiningAttentionStr',
'JoiningFindBeforeBool',
'JoinedCatchCollectionOrderedDict',
'JoinedCatchDeriveJoinersList',
'JoinedRetrieveIndexesListGetStrsList',
'JoinedRetrieveIndexesListColumnStrsList',
'JoinedInsertIndexIntsList'
                                                        ]

        def default_init(self,
                                                _JoiningCollectionStr="",
                                                _JoiningCatchStr="",
                                                _JoiningAttentionStr="",
                                                _JoiningFindBeforeBool=True,
_JoinedAttentionCollectionOrderedDict=None,
_JoinedCatchCollectionOrderedDict=None,
_JoinedCatchDeriveJoinersList=None,
_JoinedRetrieveIndexesListGetStrsList=None,
_JoinedRetrieveIndexesListColumnStrsList=None,
                                                _JoinedInsertIndexIntsList=None,
                                                **_KwargVariablesDict
                                        ):

                #Call the parent init method
                BaseClass.__init__(self,**_KwargVariablesDict)

        def mimic_model(self):

                #debug
                '''
                self.debug('We join first')
                '''

                #<NotHook>
                #join first
                self.join()
                #</NotHook>

                #debug
                '''
                self.debug('Add in the ModelingDescriptionTuplesList')
                '''

                #set
                if len(self.JoinedRetrieveIndexesListColumnStrsList)>0:
                        self.ModelingDescriptionTuplesList=map(
                                lambda
__JoinedRetrieveIndexesListGetStr,__JoinedRetrieveIndexesListColumnStr:
                                (
                                        __JoinedRetrieveIndexesListGetStr,
                                        __JoinedRetrieveIndexesListColumnStr,
                                        tables.Int64Col(shape=2)
                                ),
                                self.JoinedRetrieveIndexesListGetStrsList,
                                self.JoinedRetrieveIndexesListColumnStrsList
                        )+self.ModelingDescriptionTuplesList

                #debug
                '''
                self.debug(
                                        [
('self.',self,['ModelingDescriptionTuplesList']),
                                                'Now call the parent model
method'
                                        ]
                                )
                '''

                #<NotHook>
                #join and model first
                BaseClass.model(self)
                #</NotHook>

        def mimic_row(self):

                #debug
                '''
                self.debug('Maybe we have to join first')
                '''

                #<NotHook>
                #table and join first
                self.table()
                self.join()
                #</NotHook>

                #debug
                '''
                self.debug(
                                        [
                                                ("We are going to check if is
already inserted in the joined databases..."),
('self.',self,['JoinedCatchDeriveJoinersList'])
                                        ]
                                )
                '''

                #set
                self.JoinedInsertIndexIntsList=map(
                                        lambda __JoinedDeriveDatabaserPointer:
__JoinedDeriveDatabaserPointer.row().RowedIndexInt,
                                        self.JoinedCatchDeriveJoinersList
                                )

                #debug
                '''
                self.debug(('self.',self,[
'JoinedInsertIndexIntsList',
'JoinedRetrieveIndexesListGetStrsList'

                                                                ]))
                '''

                #set the modeled int in the retrieve tuples
                map(
                                lambda
__JoinedRetrieveIndexesListGetStr,__JoinedInsertIndexInt:
                                getattr(
                                        self.NodePointDeriveNoder,
                                        __JoinedRetrieveIndexesListGetStr
                                        ).__setitem__(
                                                1,
                                                __JoinedInsertIndexInt
                                ),
                                self.JoinedRetrieveIndexesListGetStrsList,
                                self.JoinedInsertIndexIntsList
                        )

                #debug
                '''
                self.debug([
                                                ('Before updating the
RowingKeyStrsList'),
#('self.',self,['NodePointDeriveNoder'])
                                                ('model first to set the
ModeledGetStrToColumStr')
                                        ]
                                )
                '''

                #Model first to set the ModeledGetStrToColumStr
                #self.model()

                #Add in the RowingKeyStrsList
                self.RowingKeyStrsList=self.JoinedRetrieveIndexesListGetStrsList
+self.RowingKeyStrsList

                #debug
                '''
                self.debug('Now row with Featurer')
                '''

                #<NotHook>
                #row then
                BaseClass.row(self)
                #</NotHook>

                #debug
                '''
                self.debug('Ok row is over for joining')
                '''

        def mimic_insert(self):

                #<NotHook>
                #row first
                self.row()
                #</NotHook>

                #debug
                '''
                self.debug(
                                        [
                                                'First setSwitch and make insert
the catched databases',
                                                ('self.',self,[
        'JoiningCatchStr',
        'JoiningCollectionStr'
                                                                        ])
                                        ]
                                )
                '''

                #Insert the post joined databases
                self.JoinedInsertIndexIntsList=map(
                        lambda __JoinedCatchDeriveJoinerPointer:
                        __JoinedCatchDeriveJoinerPointer.CatchToPointVariable.insert(),
                        self.JoinedCatchCollectionOrderedDict.values(),
                )

                #switch first
                self.transmit(
                        [
                                ('setSwitch',{
                                                'LiargVariablesList':[],
                                                'KwargVariablesDict':
                                                {
'_ClassVariable':"Joiner",
                                                        '_DoStrsList':['Insert']
                                                }
                                        }
                                )
                        ],
                        [self.JoiningCatchStr+self.JoiningCollectionStr]
                )

                #debug
                '''
                self.debug('Now we can insert here')
                '''

                #<NotHook>
                #insert then
                BaseClass.insert(self)
                #</NotHook>

        def mimic_retrieve(self):

                #debug
                '''
                self.debug(('self.',self,['RetrievingIndexesList']))
                '''

                #<NotHook>
                #retrieve first
                BaseClass.retrieve(self)
                #</NotHook>

                #Retrieve in the joined databases
                self.JoinedInsertIndexIntsList=map(
                                        lambda
__JoinedRetrieveIndexesListGetStr,__JoinedDeriveDatabaserPointer:
                                        __JoinedDeriveDatabaserPointer.retrieve(
                                                getattr(
self.NodePointDeriveNoder,
__JoinedRetrieveIndexesListGetStr
                                                )
                                        ),
self.JoinedRetrieveIndexesListGetStrsList,
                                        self.JoinedCatchDeriveJoinersList
                                )

        def mimic_find(self):

                #<NotHook>
                #table first
                self.table()
                #</NotHook>

                #debug
                '''
                self.debug(('self.',self,['FindingConditionVariable']))
                '''

                #
                if self.JoiningFindBeforeBool:

                        #Find in the joined databases
                        JoinedFindFilterRowDictsListsList=map(
                                        lambda __JoinedDeriveDatabaserPointer:
__JoinedDeriveDatabaserPointer.find().FoundFilterRowDictsList,
                                        self.JoinedCatchDeriveJoinersList
                                )

                        #debug
                        '''
                        self.debug('JoinedFindFilterRowDictsListsList is
'+str(JoinedFindFilterRowDictsListsList))
                        '''

                        #Just keep the retrieve lists
                        JoinedFindFilterRetrieveListsList=map(
                                                lambda
__JoinedFindFilterRowDictsList:
                                                map(
                                                                lambda
__JoinedFindFilterRowDict:
                                                                [
__JoinedFindFilterRowDict['TabledInt']
                                                                        if
'TabledInt' in __JoinedFindFilterRowDict else 0,
__JoinedFindFilterRowDict['RowInt']
                                                                ],
__JoinedFindFilterRowDictsList
                                                        ),
JoinedFindFilterRowDictsListsList
                        )

                        #debug
                        '''
                        self.debug('JoinedFindFilterRetrieveListsList is
'+str(JoinedFindFilterRetrieveListsList))
                        '''

                        #Map
                        JoinedFindingConditionVariable=map(
                                        lambda
__JoinedRetrieveIndexesListColumnStr,__JoinedFindFilterRetrieveList:
                                        (
__JoinedRetrieveIndexesListColumnStr,
                                                (
                                                        SYS.getIsInListBool,
__JoinedFindFilterRetrieveList
                                                )
                                        ),
self.JoinedRetrieveIndexesListColumnStrsList,
                                        JoinedFindFilterRetrieveListsList
                                )

                        #debug
                        '''
                        self.debug('JoinedFindingConditionVariable is
'+str(JoinedFindingConditionVariable))
                        '''

                        #Add to the finding condition tuples
self.FindingConditionVariable+=JoinedFindingConditionVariable

                        #Call the parent method
                        Featurer.FeaturerClass.find(self)

                else:

                        #Call the parent method
                        BaseClass.find(self).FoundFilterRowDictsList

        def do_join(
                                self
                        ):

                #<NotHook>
                #database first
                self.database()
                #</NotHook>

                #Check
                if self.JoiningCollectionStr=="":
                        self.JoiningCollectionStr=self.NetworkCollectionStr
                if self.JoiningCatchStr=="":
                        self.JoiningCatchStr=self.NetworkCatchStr
                if self.JoiningAttentionStr=="":
                        self.JoiningAttentionStr=self.NetworkAttentionStr

                #debug
                '''
                self.debug(
                                        ('self.',self,[
'JoiningCollectionStr',
'JoiningCatchStr',
'JoiningAttentionStr'
                                                                ])
                                )
                '''
                #set
                JoinedAttentionCollectionOrderedSetTagStr=self.JoiningAttention
Str+self.JoiningCollectionStr+"CollectionOrderedDict"

                #check
                if hasattr(
                        self,
                        JoinedAttentionCollectionOrderedSetTagStr
                ):

                        #get
                        self.JoinedAttentionCollectionOrderedDict=getattr(
                                self,
                                JoinedAttentionCollectionOrderedSetTagStr
                        )

                #set
                JoinedCatchCollectionOrderedSetTagStr=self.JoiningCatchStr+self
.JoiningCollectionStr+"CollectionOrderedDict"

                #check
                if hasattr(self,JoinedCatchCollectionOrderedSetTagStr):

                        #get
                        self.JoinedCatchCollectionOrderedDict=getattr(
                                self,
                                JoinedCatchCollectionOrderedSetTagStr
                        )

                        #model and link all the catched joiners
                        self.JoinedCatchDeriveJoinersList=map(
                                        lambda __JoinedCatchDeriveJoiner:
                                        #__JoinedCatchDeriveJoiner.__setitem__(
                                        #       'InsertIsBool',
                                        #       False
                                        #).CatchToPointVariable.model(
                                        #),
__JoinedCatchDeriveJoiner.CatchToPointVariable.model(),
self.JoinedCatchCollectionOrderedDict.values()
                                )

                        #debug
                        '''
self.debug(('self.',self,['JoinedCatchCollectionOrderedDict']))
                        '''

                        #set
                        self.JoinedRetrieveIndexesListColumnStrsList=map(
                                        lambda __JoinedCatchDeriveJoiner:
                                        "Join"+''.join(
                                                [
__JoinedCatchDeriveJoiner.ModelDeriveControllerVariable.NodeKeyStr
                                                        if
__JoinedCatchDeriveJoiner.ModelDeriveControllerVariable.NodeKeyStr!=""
                                                        else 'Top'+__JoinedCatch
DeriveJoiner.ModelDeriveControllerVariable.__class__.NameStr,
__JoinedCatchDeriveJoiner.ModeledSuffixStr
                                                ]
                                        )+"RetrieveIndexesList",
                                        self.JoinedCatchDeriveJoinersList,
                                )

                        #debug
                        '''
self.debug(('self.',self,['JoinedRetrieveIndexesListColumnStrsList']))
                        '''

                        #set
                        self.JoinedRetrieveIndexesListGetStrsList=map(
                                        lambda __JoinedCatchDeriveJoiner:
                                        "Joined"+''.join(
                                                [
self.ModelDeriveControllerVariable.NodeKeyStr
                                                        if
self.ModelDeriveControllerVariable.NodeKeyStr!=""
                                                        else
'Top'+self.ModelDeriveControllerVariable.__class__.NameStr,
                                                        self.ModeledSuffixStr,
                                                        'To',
__JoinedCatchDeriveJoiner.ModelDeriveControllerVariable.NodeKeyStr
                                                        if
__JoinedCatchDeriveJoiner.ModelDeriveControllerVariable.NodeKeyStr!=""
                                                        else 'Top'+__JoinedCatch
DeriveJoiner.ModelDeriveControllerVariable.__class__.NameStr,
__JoinedCatchDeriveJoiner.ModeledSuffixStr
                                                ]
                                        )+"RetrieveIndexesList",
                                        self.JoinedCatchDeriveJoinersList,
                                )

                        #debug
                        '''
                        self.debug(
                                                [
('self.',self,['JoinedRetrieveIndexesListGetStrsList']),
                                                        'Table the joined
databases'
                                                ]
                                        )
                        '''

                        #Table all the joined databasers and init the
corresponding JoinedRetrieveIndexesList in the NodePointDeriveNoder
                        self.ModelDeriveControllerVariable.update(
                                zip(
self.JoinedRetrieveIndexesListGetStrsList,
                                                map(
                                                        lambda
__JoinedCatchDeriveJoiner:
                                                        [
__JoinedCatchDeriveJoiner.table()['TabledInt'],
                                                                -1
                                                        ],
self.JoinedCatchDeriveJoinersList
                                                )
                                        )
                        )

                        #debug
                        '''
                        self.debug(
                                                ('self.',self,[
'JoinedRetrieveIndexesListColumnStrsList',
'JoinedRetrieveIndexesListGetStrsList'
                                                                        ])
                        )
                        '''
#</DefineClass>


```

<small>
View the Joiner sources on <a href="https://github.com/Ledoux/ShareYourSystem/tr
ee/master/Pythonlogy/ShareYourSystem/Databasers/Joiner"
target="_blank">Github</a>
</small>




<!---
FrozenIsBool True
-->

##Example

Let's do a hierarchic components join

```python
#ImportModules
import ShareYourSystem as SYS
from ShareYourSystem.Standards.Classors import Classer
from ShareYourSystem.Standards.Noders import Structurer
from ShareYourSystem.Standards.Modelers import Joiner
import operator
import tables
import numpy as np

#Define a Multiplier class
@Classer.ClasserClass()
class MultiplierClass(Structurer.StructurerClass):

    #Definition
    RepresentingKeyStrsList=[
                                    'MultiplyingFirstInt',
                                    'MultiplyingSecondInt'
                                ]

    def default_init(self,
                        _MultiplyingFirstInt=0,
                        _MultiplyingSecondInt=0,
                        **_KwargVariablesDict
                    ):

        #Call the parent init method
        self.__class__.__bases__[0].__init__(self,**_KwargVariablesDict)

        #Set a parameters database
        self.collect(
                        "Datome",
                        "Parameters",
                        Joiner.JoinerClass().update(
                            [
                                (
                                    'Attr_ModelingDescriptionTuplesList',
                                    [
('MultiplyingFirstInt','MultiplyingFirstInt',tables.Int64Col()),
('MultiplyingSecondInt','MultiplyingSecondInt',tables.Int64Col())
                                    ]
                                ),
('Attr_RowingKeyStrsList',['MultiplyingFirstInt','MultiplyingSecondInt'])
                            ]
                        )
                )

#Define a Modulizer class
@Classer.ClasserClass()
class ModulizerClass(Structurer.StructurerClass):

    #Definition
    RepresentingKeyStrsList=[
                                    'ModulizingPowerFloat',
                                    'ModulizedTotalFloat'
                                ]

    def default_init(self,
                        _ModulizingPowerFloat=1.,
                        _ModulizedTotalFloat=0.,
                        **_KwargVariablesDict
                    ):

        #Call the parent init method
        self.__class__.__bases__[0].__init__(self,**_KwargVariablesDict)

        #Build the output hierarchy
        self.update(
                        [
                            ('<Component>RealMultiplier',MultiplierClass()),
                            ('<Component>ImageMultiplier',MultiplierClass())
                        ]
                    )

        #Set a parameters database
        self.collect(
                    "Datome",
                    "Parameters",
                    Joiner.JoinerClass().update(
                        [
                            (
                                'Attr_ModelingDescriptionTuplesList',
                                [
('ModulizingPowerFloat','ModulizingPowerFloat',tables.Float64Col())
                                ]
                            ),
                            ('Attr_RowingKeyStrsList',['ModulizingPowerFloat']),
                            ('ConnectingGraspClueVariablesList',
                                [
'/NodePointDeriveNoder/<Component>RealMultiplier/<Datome>ParametersJoiner',
'/NodePointDeriveNoder/<Component>ImageMultiplier/<Datome>ParametersJoiner'
                                ]
                            )
                        ]
                    )
                )


#Definition of a Modulizer instance, structure and network
MyModulizer=ModulizerClass().structure(
    ['Component']
).network(
    **{
        'VisitingCollectionStrsList':['Datome','Component'],
        'RecruitingConcludeConditionVariable':[
            (
                '__class__.__mro__',
                operator.contains,Joiner.JoinerClass
            )
        ]
    }
)

#Update and insert in the results
MyModulizer.__setitem__(
    "Dis_<Component>",
    [
        [
            ('MultiplyingFirstInt',1),
            ('MultiplyingSecondInt',2)
        ],
        [
            ('MultiplyingFirstInt',1),
            ('MultiplyingSecondInt',3)
        ]
    ]
)['<Datome>ParametersJoiner'].insert()

#Update and insert in the results
MyModulizer.__setitem__(
    "Dis_<Component>",
    [
        [
            ('MultiplyingFirstInt',2)
        ],
        [
            ('MultiplyingSecondInt',4)
        ]
    ]
)['<Datome>ParametersJoiner'].insert()


#Definition the AttestedStr
SYS._attest(
    [
        'MyModulizer is '+SYS._str(
        MyModulizer,
        **{
            'RepresentingBaseKeyStrsListBool':False,
            'RepresentingAlineaIsBool':False
        }
        ),
        'hdf5 file is : '+MyModulizer.hdfview().hdfclose().HdformatedConsoleStr
    ]
)

#Print



```


```console
>>>

                            xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                            ////////////////////////////////
                            Attentioner/__init__.py do_attention
                            From Attentioner/__init__.py do_attention |
Connecter/__init__.py do_connect | Networker/__init__.py do_network | site-
packages/six.py exec_ | Celler/__init__.py do_cell | Notebooker/__init__.py
do_notebook | Documenter/__init__.py do_inform | inform.py <module>
                            ////////////////////////////////

                            l.60 :
                            *****
                            I am with [('NodeKeyStr', 'ParametersJoiner')]
                            *****
                            self.AttentioningCollectionStr is PreConnectome
                            self.GraspingClueVariable is
/NodePointDeriveNoder/<Component>RealMultiplier/<Datome>ParametersJoiner

                            xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


                            xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                            ////////////////////////////////
                            Attentioner/__init__.py do_attention
                            From Attentioner/__init__.py do_attention |
Connecter/__init__.py do_connect | Networker/__init__.py do_network | site-
packages/six.py exec_ | Celler/__init__.py do_cell | Notebooker/__init__.py
do_notebook | Documenter/__init__.py do_inform | inform.py <module>
                            ////////////////////////////////

                            l.60 :
                            *****
                            I am with [('NodeKeyStr', 'ParametersJoiner')]
                            *****
                            self.AttentioningCollectionStr is PreConnectome
                            self.GraspingClueVariable is
/NodePointDeriveNoder/<Component>ImageMultiplier/<Datome>ParametersJoiner

                            xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx



*****Start of the Attest *****

MyModulizer is < (ModulizerClass), 4565315408>
   /{
   /  '<New><Instance>ComponentCollectionOrderedDict' :
   /   /{
   /   /  'RealMultiplier' : < (MultiplierClass), 4565314896>
   /   /   /{
   /   /   /  '<New><Instance>ComponentCollectionOrderedDict' :
   /   /   /   /{
   /   /   /   /}
   /   /   /  '<New><Instance>DatomeCollectionOrderedDict' :
   /   /   /   /{
   /   /   /   /  'ParametersJoiner' : < (JoinerClass), 4564992336>
   /   /   /   /   /{
   /   /   /   /   /  '<New><Instance>ComponentCollectionOrderedDict' :
   /   /   /   /   /   /{
   /   /   /   /   /   /}
   /   /   /   /   /  '<New><Instance>DatomeCollectionOrderedDict' :
   /   /   /   /   /   /{
   /   /   /   /   /   /}
   /   /   /   /   /  '<New><Instance>IdInt' : 4564992336
   /   /   /   /   /  '<New><Instance>NetworkAttentionStr' : Pre
   /   /   /   /   /  '<New><Instance>NetworkCatchStr' : Post
   /   /   /   /   /  '<New><Instance>NetworkCollectionStr' : Connectome
   /   /   /   /   /  '<New><Instance>NewtorkAttentionStr' :
   /   /   /   /   /  '<New><Instance>NewtorkCatchStr' :
   /   /   /   /   /  '<New><Instance>NewtorkCollectionStr' :
   /   /   /   /   /  '<New><Instance>NodeCollectionStr' : Datome
   /   /   /   /   /  '<New><Instance>NodeIndexInt' : 0
   /   /   /   /   /  '<New><Instance>NodeKeyStr' : ParametersJoiner
   /   /   /   /   /  '<New><Instance>NodePointDeriveNoder' : {...}<
(MultiplierClass), 4565314896>
   /   /   /   /   /  '<New><Instance>NodePointOrderedDict' : {...}<
(OrderedDict), 4565048880>
   /   /   /   /   /  '<New><Instance>PreConnectomeCollectionOrderedDict' :
   /   /   /   /   /   /{
   /   /   /   /   /   /
'ParametersJoiner_RealMultiplier>TopModulizer<ParametersJoinerPointer' : <
(PointerClass), 4563977744>
   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4563977744
   /   /   /   /   /   /   /  '<New><Instance>CatchToPointVariable' : < (JoinerClass),
4563943504>
   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /
'<New><Instance>ComponentCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /  '<New><Instance>DatomeCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4563943504
   /   /   /   /   /   /   /   /  '<New><Instance>NetworkAttentionStr' : Pre
   /   /   /   /   /   /   /   /  '<New><Instance>NetworkCatchStr' : Post
   /   /   /   /   /   /   /   /  '<New><Instance>NetworkCollectionStr' :
Connectome
   /   /   /   /   /   /   /   /  '<New><Instance>NewtorkAttentionStr' :
   /   /   /   /   /   /   /   /  '<New><Instance>NewtorkCatchStr' :
   /   /   /   /   /   /   /   /  '<New><Instance>NewtorkCollectionStr' :
   /   /   /   /   /   /   /   /  '<New><Instance>NodeCollectionStr' : Datome
   /   /   /   /   /   /   /   /  '<New><Instance>NodeIndexInt' : 0
   /   /   /   /   /   /   /   /  '<New><Instance>NodeKeyStr' : ParametersJoiner
   /   /   /   /   /   /   /   /  '<New><Instance>NodePointDeriveNoder' : {...}<
(ModulizerClass), 4565315408>
   /   /   /   /   /   /   /   /  '<New><Instance>NodePointOrderedDict' :
   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /  'ParametersJoiner' : {...}< (JoinerClass),
4563943504>
   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /
'<New><Instance>PostConnectomeCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /  '_NodePointDeriveNoder_<Component>RealMult
iplier_<Datome>ParametersJoinerPointer' : < (PointerClass), 4563945104>
   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4563945104
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>CatchToPointVariable' :
{...}< (JoinerClass), 4564992336>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /   /   /   /  '<Spe><Class>PointedPathBackVariable'
:
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointedGetVariable' :
{...}< (JoinerClass), 4564992336>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointedLocalSetStr' :
CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingGetVariable' :
{...}< (JoinerClass), 4564992336>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingSetPathStr' :
CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /  '_NodePointDeriveNoder_<Component>ImageMul
tiplier_<Datome>ParametersJoinerPointer' : < (PointerClass), 4563945040>
   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4563945040
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>CatchToPointVariable' : <
(JoinerClass), 4564992784>
   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>ComponentCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>DatomeCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' :
4564992784
   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NetworkAttentionStr' : Pre
   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>NetworkCatchStr' :
Post
   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NetworkCollectionStr' : Connectome
   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NewtorkAttentionStr' :
   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>NewtorkCatchStr' :
   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NewtorkCollectionStr' :
   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>NodeCollectionStr'
: Datome
   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>NodeIndexInt' : 0
   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>NodeKeyStr' :
ParametersJoiner
   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NodePointDeriveNoder' : < (MultiplierClass), 4564993168>
   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>ComponentCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>DatomeCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /  'ParametersJoiner' :
{...}< (JoinerClass), 4564992784>
   /   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' :
4564993168
   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NewtorkAttentionStr' :
   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NewtorkCatchStr' :
   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NewtorkCollectionStr' :
   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NodeCollectionStr' : Component
   /   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>NodeIndexInt'
: 1
   /   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>NodeKeyStr' :
ImageMultiplier
   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NodePointDeriveNoder' : {...}< (ModulizerClass), 4565315408>
   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NodePointOrderedDict' : {...}< (OrderedDict), 4565116144>
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>MultiplyingFirstInt' : 1
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>MultiplyingSecondInt' : 4
   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NodePointOrderedDict' : {...}< (OrderedDict), 4565115848>
   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>PreConnectomeCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /
'ParametersJoiner_ImageMultiplier>TopModulizer<ParametersJoinerPointer' : <
(PointerClass), 4563980112>
   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' :
4563980112
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>CatchToPointVariable' : {...}< (JoinerClass), 4563943504>
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedPathBackVariable' :
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedGetVariable' : {...}< (JoinerClass), 4563943504>
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedLocalSetStr' : CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingGetVariable' : {...}< (JoinerClass), 4563943504>
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingSetPathStr' : CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>_ModelingDescriptionTuplesList' :
   /   /   /   /   /   /   /   /   /   /   /   /[
   /   /   /   /   /   /   /   /   /   /   /   /  0 :
   /   /   /   /   /   /   /   /   /   /   /   /   /(
   /   /   /   /   /   /   /   /   /   /   /   /   /  0 : MultiplyingFirstInt
   /   /   /   /   /   /   /   /   /   /   /   /   /  1 : MultiplyingFirstInt
   /   /   /   /   /   /   /   /   /   /   /   /   /  2 : Int64Col(shape=(),
dflt=0, pos=None)
   /   /   /   /   /   /   /   /   /   /   /   /   /)
   /   /   /   /   /   /   /   /   /   /   /   /  1 :
   /   /   /   /   /   /   /   /   /   /   /   /   /(
   /   /   /   /   /   /   /   /   /   /   /   /   /  0 : MultiplyingSecondInt
   /   /   /   /   /   /   /   /   /   /   /   /   /  1 : MultiplyingSecondInt
   /   /   /   /   /   /   /   /   /   /   /   /   /  2 : Int64Col(shape=(),
dflt=0, pos=None)
   /   /   /   /   /   /   /   /   /   /   /   /   /)
   /   /   /   /   /   /   /   /   /   /   /   /]
   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>_RowingKeyStrsList' : ['MultiplyingFirstInt',
'MultiplyingSecondInt']
   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>JoiningFindBeforeBool' : True
   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>JoinedCatchCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>JoinedCatchDeriveJoinersList' : []
   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>JoinedInsertIndexIntsList' : []
   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>JoinedRetrieveIndexesListColumnStrsList' : []
   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>JoinedRetrieveIndexesListGetStrsList' : []
   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>JoiningAttentionStr' : Pre
   /   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>JoiningCatchStr' :
Post
   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>JoiningCollectionStr' : Connectome
   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /  '<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /   /   /   /  '<Spe><Class>PointedPathBackVariable'
:
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointedGetVariable' :
{...}< (JoinerClass), 4564992784>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointedLocalSetStr' :
CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingGetVariable' :
{...}< (JoinerClass), 4564992784>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingSetPathStr' :
CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /  '<New><Instance>_ModelingDescriptionTuplesList' :
   /   /   /   /   /   /   /   /   /[
   /   /   /   /   /   /   /   /   /  0 :
   /   /   /   /   /   /   /   /   /   /(
   /   /   /   /   /   /   /   /   /   /  0 : JoinedTopModulizerParametersJoiner
ModelToRealMultiplierParametersJoinerModelRetrieveIndexesList
   /   /   /   /   /   /   /   /   /   /  1 :
JoinRealMultiplierParametersJoinerModelRetrieveIndexesList
   /   /   /   /   /   /   /   /   /   /  2 : Int64Col(shape=(2,), dflt=0,
pos=None)
   /   /   /   /   /   /   /   /   /   /)
   /   /   /   /   /   /   /   /   /  1 :
   /   /   /   /   /   /   /   /   /   /(
   /   /   /   /   /   /   /   /   /   /  0 : JoinedTopModulizerParametersJoiner
ModelToImageMultiplierParametersJoinerModelRetrieveIndexesList
   /   /   /   /   /   /   /   /   /   /  1 :
JoinImageMultiplierParametersJoinerModelRetrieveIndexesList
   /   /   /   /   /   /   /   /   /   /  2 : Int64Col(shape=(2,), dflt=0,
pos=None)
   /   /   /   /   /   /   /   /   /   /)
   /   /   /   /   /   /   /   /   /  2 :
   /   /   /   /   /   /   /   /   /   /(
   /   /   /   /   /   /   /   /   /   /  0 : ModulizingPowerFloat
   /   /   /   /   /   /   /   /   /   /  1 : ModulizingPowerFloat
   /   /   /   /   /   /   /   /   /   /  2 : Float64Col(shape=(), dflt=0.0,
pos=None)
   /   /   /   /   /   /   /   /   /   /)
   /   /   /   /   /   /   /   /   /]
   /   /   /   /   /   /   /   /  '<New><Instance>_RowingKeyStrsList' : ['Joined
TopModulizerParametersJoinerModelToRealMultiplierParametersJoinerModelRetrieveIn
dexesList', 'JoinedTopModulizerParametersJoinerModelToImageMultiplierParametersJ
oinerModelRetrieveIndexesList', 'JoinedTopModulizerParametersJoinerModelToRealMu
ltiplierParametersJoinerModelRetrieveIndexesList', 'JoinedTopModulizerParameters
JoinerModelToImageMultiplierParametersJoinerModelRetrieveIndexesList', 'JoinedTo
pModulizerParametersJoinerModelToRealMultiplierParametersJoinerModelRetrieveInde
xesList', 'JoinedTopModulizerParametersJoinerModelToImageMultiplierParametersJoi
nerModelRetrieveIndexesList', 'JoinedTopModulizerParametersJoinerModelToRealMult
iplierParametersJoinerModelRetrieveIndexesList', 'JoinedTopModulizerParametersJo
inerModelToImageMultiplierParametersJoinerModelRetrieveIndexesList',
'ModulizingPowerFloat']
   /   /   /   /   /   /   /   /  '<Spe><Class>JoiningFindBeforeBool' : True
   /   /   /   /   /   /   /   /
'<Spe><Instance>JoinedCatchCollectionOrderedDict' : {...}< (OrderedDict),
4565117328>
   /   /   /   /   /   /   /   /  '<Spe><Instance>JoinedCatchDeriveJoinersList'
:
   /   /   /   /   /   /   /   /   /[
   /   /   /   /   /   /   /   /   /  0 : {...}< (JoinerClass), 4564992336>
   /   /   /   /   /   /   /   /   /  1 : {...}< (JoinerClass), 4564992784>
   /   /   /   /   /   /   /   /   /]
   /   /   /   /   /   /   /   /  '<Spe><Instance>JoinedInsertIndexIntsList' :
[1, 1]
   /   /   /   /   /   /   /   /
'<Spe><Instance>JoinedRetrieveIndexesListColumnStrsList' :
['JoinRealMultiplierParametersJoinerModelRetrieveIndexesList',
'JoinImageMultiplierParametersJoinerModelRetrieveIndexesList']
   /   /   /   /   /   /   /   /
'<Spe><Instance>JoinedRetrieveIndexesListGetStrsList' : ['JoinedTopModulizerPara
metersJoinerModelToRealMultiplierParametersJoinerModelRetrieveIndexesList', 'Joi
nedTopModulizerParametersJoinerModelToImageMultiplierParametersJoinerModelRetrie
veIndexesList']
   /   /   /   /   /   /   /   /  '<Spe><Instance>JoiningAttentionStr' : Pre
   /   /   /   /   /   /   /   /  '<Spe><Instance>JoiningCatchStr' : Post
   /   /   /   /   /   /   /   /  '<Spe><Instance>JoiningCollectionStr' :
Connectome
   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /  '<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /  '<Spe><Class>PointedPathBackVariable' :
   /   /   /   /   /   /   /  '<Spe><Instance>PointedGetVariable' : {...}<
(JoinerClass), 4563943504>
   /   /   /   /   /   /   /  '<Spe><Instance>PointedLocalSetStr' :
CatchToPointVariable
   /   /   /   /   /   /   /  '<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /  '<Spe><Instance>PointingGetVariable' : {...}<
(JoinerClass), 4563943504>
   /   /   /   /   /   /   /  '<Spe><Instance>PointingSetPathStr' :
CatchToPointVariable
   /   /   /   /   /   /   /}
   /   /   /   /   /   /}
   /   /   /   /   /  '<New><Instance>_ModelingDescriptionTuplesList' :
   /   /   /   /   /   /[
   /   /   /   /   /   /  0 :
   /   /   /   /   /   /   /(
   /   /   /   /   /   /   /  0 : MultiplyingFirstInt
   /   /   /   /   /   /   /  1 : MultiplyingFirstInt
   /   /   /   /   /   /   /  2 : Int64Col(shape=(), dflt=0, pos=None)
   /   /   /   /   /   /   /)
   /   /   /   /   /   /  1 :
   /   /   /   /   /   /   /(
   /   /   /   /   /   /   /  0 : MultiplyingSecondInt
   /   /   /   /   /   /   /  1 : MultiplyingSecondInt
   /   /   /   /   /   /   /  2 : Int64Col(shape=(), dflt=0, pos=None)
   /   /   /   /   /   /   /)
   /   /   /   /   /   /]
   /   /   /   /   /  '<New><Instance>_RowingKeyStrsList' :
['MultiplyingFirstInt', 'MultiplyingSecondInt']
   /   /   /   /   /  '<Spe><Class>JoiningFindBeforeBool' : True
   /   /   /   /   /  '<Spe><Instance>JoinedCatchCollectionOrderedDict' :
   /   /   /   /   /   /{
   /   /   /   /   /   /}
   /   /   /   /   /  '<Spe><Instance>JoinedCatchDeriveJoinersList' : []
   /   /   /   /   /  '<Spe><Instance>JoinedInsertIndexIntsList' : []
   /   /   /   /   /  '<Spe><Instance>JoinedRetrieveIndexesListColumnStrsList' :
[]
   /   /   /   /   /  '<Spe><Instance>JoinedRetrieveIndexesListGetStrsList' : []
   /   /   /   /   /  '<Spe><Instance>JoiningAttentionStr' : Pre
   /   /   /   /   /  '<Spe><Instance>JoiningCatchStr' : Post
   /   /   /   /   /  '<Spe><Instance>JoiningCollectionStr' : Connectome
   /   /   /   /   /}
   /   /   /   /}
   /   /   /  '<New><Instance>IdInt' : 4565314896
   /   /   /  '<New><Instance>NewtorkAttentionStr' :
   /   /   /  '<New><Instance>NewtorkCatchStr' :
   /   /   /  '<New><Instance>NewtorkCollectionStr' :
   /   /   /  '<New><Instance>NodeCollectionStr' : Component
   /   /   /  '<New><Instance>NodeIndexInt' : 0
   /   /   /  '<New><Instance>NodeKeyStr' : RealMultiplier
   /   /   /  '<New><Instance>NodePointDeriveNoder' : {...}< (ModulizerClass),
4565315408>
   /   /   /  '<New><Instance>NodePointOrderedDict' : {...}< (OrderedDict),
4565116144>
   /   /   /  '<Spe><Instance>MultiplyingFirstInt' : 2
   /   /   /  '<Spe><Instance>MultiplyingSecondInt' : 2
   /   /   /}
   /   /  'ImageMultiplier' : {...}< (MultiplierClass), 4564993168>
   /   /}
   /  '<New><Instance>DatomeCollectionOrderedDict' : {...}< (OrderedDict),
4565117032>
   /  '<New><Instance>IdInt' : 4565315408
   /  '<New><Instance>JoinedTopModulizerParametersJoinerModelToImageMultiplierPa
rametersJoinerModelRetrieveIndexesList' : [0, 1]
   /  '<New><Instance>JoinedTopModulizerParametersJoinerModelToRealMultiplierPar
ametersJoinerModelRetrieveIndexesList' : [0, 1]
   /  '<New><Instance>NewtorkAttentionStr' :
   /  '<New><Instance>NewtorkCatchStr' :
   /  '<New><Instance>NewtorkCollectionStr' :
   /  '<New><Instance>NodeCollectionStr' : Globals
   /  '<New><Instance>NodeIndexInt' : -1
   /  '<New><Instance>NodeKeyStr' : TopModulizer
   /  '<New><Instance>NodePointDeriveNoder' : None
   /  '<New><Instance>NodePointOrderedDict' : None
   /  '<Spe><Class>ModulizedTotalFloat' : 0.0
   /  '<Spe><Class>ModulizingPowerFloat' : 1.0
   /}

------

hdf5 file is : /                        Group
/TopModulizer            Group
/TopModulizer/ImageMultiplier Group
/TopModulizer/ImageMultiplier/xx0xxParametersJoinerTable Dataset {2/Inf}
    Data:
        (0) {RowInt=0, MultiplyingFirstInt=1, MultiplyingSecondInt=3},
        (1) {RowInt=1, MultiplyingFirstInt=1, MultiplyingSecondInt=4}
/TopModulizer/RealMultiplier Group
/TopModulizer/RealMultiplier/xx0xxParametersJoinerTable Dataset {2/Inf}
    Data:
        (0) {RowInt=0, MultiplyingFirstInt=1, MultiplyingSecondInt=2},
        (1) {RowInt=1, MultiplyingFirstInt=2, MultiplyingSecondInt=2}
/xx0xxParametersJoinerTable Dataset {2/Inf}
    Data:
        (0) {JoinImageMultiplierParametersJoinerModelRetrieveIndexesList=[0,
        (0)  0], JoinRealMultiplierParametersJoinerModelRetrieveIndexesList=[0,
        (0)  0], RowInt=0, ModulizingPowerFloat=1},
        (1) {JoinImageMultiplierParametersJoinerModelRetrieveIndexesList=[0,
        (1)  1], JoinRealMultiplierParametersJoinerModelRetrieveIndexesList=[0,
        (1)  1], RowInt=1, ModulizingPowerFloat=1}


*****End of the Attest *****



```

