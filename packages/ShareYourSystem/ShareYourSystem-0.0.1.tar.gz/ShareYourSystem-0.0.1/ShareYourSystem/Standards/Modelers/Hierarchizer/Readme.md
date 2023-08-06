

<!--
FrozenIsBool False
-->

#Hierarchizer

##Doc
----


>
> A Hierarchizer is a Joiner that taking care of the
> order of the joining connections between derived Joiners,
> whatever is the level of their setting in the hierarchy of
> their parent derived Storers.
>
>

----

<small>
View the Hierarchizer notebook on [NbViewer](http://nbviewer.ipython.org/url/sha
reyoursystem.ouvaton.org/Hierarchizer.ipynb)
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


A Hierarchizer is a Joiner that taking care of the
order of the joining connections between derived Joiners,
whatever is the level of their setting in the hierarchy of
their parent derived Storers.

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Modelers.Joiner"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import collections
import tables
from ShareYourSystem.Standards.Noders import Noder
Joiner=BaseModule
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass(**{
        'ClassingSwitchMethodStrsList':[
                'model',
                'tabular',
                'join',
                'insert'
        ]
})
class HierarchizerClass(BaseClass):

        #Definition
        RepresentingKeyStrsList=[
                                                        ]

        #@Hooker.HookerClass(**{'HookingAfterVariablesList':[{'CallingVariable':
BaseClass.__init__}]})
        def default_init(self,
                                                **_KwargVariablesDict
                                        ):

                #Call the parent init method
                BaseClass.__init__(self,**_KwargVariablesDict)

        def mimic_insert(self):

                #debug
                '''
                self.debug(
                                        [
                                                'we setSwitch first and insert',
                                                ('self.',self,[
'JoiningAttentionStr',
'JoiningCollectionStr'
                                                                        ])
                                        ]
                                )
                '''

                #<NotHook>
                #insert then
                BaseClass.insert(self)
                #</NotHook>

                #debug
                '''
                self.debug('we hierarchize now, self.hierarchize is
'+str(self.hierarchize))
                '''

                #call
                self.hierarchize()

                #switch first
                self.transmit(
                        [
                                ('setSwitch',{
'LiargVariablesList':[],
'KwargVariablesDict':
                                                                {
'_ClassVariable':'Hierarchizer',
'_DoStrsList':['Insert']
                                                                }
                                                        })
                        ],
                        [self.JoiningAttentionStr+self.JoiningCollectionStr],
                        #Self is not switched (if not it is circular !)
                        #False
                )

        def do_hierarchize(self):

                #debug
                '''
                self.debug(
                                        [
                                                'insert then in the joined
attention databasers',
('self.',self,['JoinedAttentionCollectionOrderedDict'])
                                        ]
                                )
                '''

                #map
                map(
                                lambda
__JoinedAttentionCollectionDeriveJoinerPointer:
__JoinedAttentionCollectionDeriveJoinerPointer.CatchToPointVariable.insert(),
self.JoinedAttentionCollectionOrderedDict.values()
                        )


#</DefineClass>


```

<small>
View the Hierarchizer sources on <a href="https://github.com/Ledoux/ShareYourSys
tem/tree/master/Pythonlogy/ShareYourSystem/Databasers/Hierarchizer"
target="_blank">Github</a>
</small>




<!---
FrozenIsBool True
-->

##Example

Let's do all at the same time :
Results-Parameters join and hierarchic joins.

```python
#ImportModules
import ShareYourSystem as SYS
from ShareYourSystem.Standards.Classors import Classer
from ShareYourSystem.Standards.Noders import Structurer
from ShareYourSystem.Standards.Modelers import Hierarchizer
import operator
import tables
import numpy as np

#Define a Sumer class
@Classer.ClasserClass()
class SumerClass(Structurer.StructurerClass):

    #Definition
    RepresentingKeyStrsList=[
                                    'SumingFirstInt',
                                    'SumingSecondInt',
                                    'SumedTotalInt'
                                ]

    def default_init(self,
                        _SumingFirstInt=0,
                        _SumingSecondInt=0,
                        _SumedTotalInt=0,
                        **_KwargVariablesDict
                    ):

        #Call the parent init method
        self.__class__.__bases__[0].__init__(self,**_KwargVariablesDict)

        #Set a parameters database
        self.collect(
                "Datome",
                "Parameters",
                Hierarchizer.HierarchizerClass().update(
                    [
                        (
                            'Attr_ModelingDescriptionTuplesList',
                            [
('SumingFirstInt','SumingFirstInt',tables.Int64Col()),
('SumingSecondInt','SumingSecondInt',tables.Int64Col())
                            ]
                        ),
('Attr_RowingKeyStrsList',['SumingFirstInt','SumingSecondInt'])
                    ]
                )
            )

        #Set a results database
        self.collect(
            "Datome",
            "Results",
            Hierarchizer.HierarchizerClass().update(
                [
                    (
                        'Attr_ModelingDescriptionTuplesList',
                        [
                            ('SumedTotalInt','SumedTotalInt',tables.Int64Col())
                        ]
                    ),
                    ('ConnectingGraspClueVariablesList',
                        [
'/NodePointDeriveNoder/<Datome>ParametersHierarchizer'
                        ]
                    ),
                    ('TagStr','Networked')
                ]
            )
        )

    def do_sum(self):

        #debug
        '''
        self.debug(('self.',self,['SumingFirstInt','SumingSecondInt']))
        '''

        #set the SumedTotalInt
        self.SumedTotalInt=self.SumingFirstInt+self.SumingSecondInt

#Define a Factorizer class
@Classer.ClasserClass()
class FactorizerClass(Structurer.StructurerClass):

    #Definition
    RepresentingKeyStrsList=[
                                'FactorizingPowerFloat',
                                'FactorizedTotalFloat'
                            ]

    def default_init(self,
                        _FactorizingPowerFloat=1.,
                        _FactorizedTotalFloat=0.,
                        **_KwargVariablesDict
                    ):

        #Call the parent init method
        self.__class__.__bases__[0].__init__(self,**_KwargVariablesDict)

        #Build the output hierarchy
        self.update(
                        [
                            ('<Component>XSumer',SumerClass()),
                            ('<Component>YSumer',SumerClass())
                        ]
                    )

        #Set a parameters database
        self.collect(
                    "Datome",
                    "Parameters",
                    Hierarchizer.HierarchizerClass().update(
                        [
                            (
                                'Attr_ModelingDescriptionTuplesList',
                                [
('FactorizingPowerFloat','FactorizingPowerFloat',tables.Float64Col())
                                ]
                            ),
('Attr_RowingKeyStrsList',['FactorizingPowerFloat']),
                            ('ConnectingGraspClueVariablesList',
                                [
'/NodePointDeriveNoder/<Component>XSumer/<Datome>ParametersHierarchizer',
'/NodePointDeriveNoder/<Component>YSumer/<Datome>ParametersHierarchizer'
                                ]
                            )
                        ]
                    )
                )

        #Set a results database
        self.collect(
            "Datome",
            "Results",
            Hierarchizer.HierarchizerClass().update(
                [
                    (
                        'Attr_ModelingDescriptionTuplesList',
                        [
('FactorizedTotalFloat','FactorizedTotalFloat',tables.Float64Col())
                        ]
                    ),
                    ('ConnectingGraspClueVariablesList',
                        [
'/NodePointDeriveNoder/<Datome>ParametersHierarchizer'
                        ]
                    ),
                    ('TagStr','Networked')
                ]
            )
        )

    def do_factorize(self):

        #debug
        self.debug('We factorize here')

        #set the FactorizedTotalFloat
        self.FactorizedTotalFloat=np.power(
            sum(
                map(
                    lambda __DeriveSumer:
                    __DeriveSumer.SumedTotalInt,
                    self['<Component>']
                )
            ),
            self.FactorizingPowerFloat
        )

#Definition of a Factorizer instance, structure and network
MyFactorizer=FactorizerClass().structure(
    ['Component']
).network(
    **{
        'VisitingCollectionStrsList':['Datome','Component'],
        'RecruitingConcludeConditionVariable':[
            (
                '__class__.__mro__',
                operator.contains,Hierarchizer.HierarchizerClass
            )
        ]
    }
)

#Update transmit the do method and insert in the results
MyFactorizer.__setitem__(
    "Dis_<Component>",
    [
        [
            ('SumingFirstInt',1),
            ('SumingSecondInt',2)
        ],
        [
            ('SumingFirstInt',1),
            ('SumingSecondInt',3)
        ]
    ]
).walk(
    {
        'AfterUpdateList':[
            ('callDo',{'LiargVariablesList':[]})
        ],
        'GatherVariablesList':['<Component>']
    }
)['<Datome>ResultsHierarchizer'].insert()

#Update and insert in the results
MyFactorizer.__setitem__(
    "Dis_<Component>",
    [
        [
            ('SumingFirstInt',2)
        ],
        [
            ('SumingSecondInt',4)
        ]
    ]
).walk(
    {
        'AfterUpdateList':[
            ('callDo',{'LiargVariablesList':[]})
        ],
        'GatherVariablesList':['<Component>']
    }
)['<Datome>ResultsHierarchizer'].insert()

#Definition the AttestedStr
SYS._attest(
    [
        'MyFactorizer is '+SYS._str(
        MyFactorizer,
        **{
            'RepresentingBaseKeyStrsListBool':False,
            'RepresentingAlineaIsBool':False
        }
        ),
        'hdf5 file is : '+MyFactorizer.hdfview().hdfclose().HdformatedConsoleStr
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
                            I am with [('NodeKeyStr', 'ParametersHierarchizer')]
                            *****
                            self.AttentioningCollectionStr is PreConnectome
                            self.GraspingClueVariable is
/NodePointDeriveNoder/<Component>XSumer/<Datome>ParametersHierarchizer

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
                            I am with [('NodeKeyStr', 'ParametersHierarchizer')]
                            *****
                            self.AttentioningCollectionStr is PreConnectome
                            self.GraspingClueVariable is
/NodePointDeriveNoder/<Component>YSumer/<Datome>ParametersHierarchizer

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
                            I am with [('NodeKeyStr', 'ResultsHierarchizer')]
                            *****
                            self.AttentioningCollectionStr is PreConnectome
                            self.GraspingClueVariable is
/NodePointDeriveNoder/<Datome>ParametersHierarchizer

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
                            I am with [('NodeKeyStr', 'ResultsHierarchizer')]
                            *****
                            self.AttentioningCollectionStr is PreConnectome
                            self.GraspingClueVariable is
/NodePointDeriveNoder/<Datome>ParametersHierarchizer

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
                            I am with [('NodeKeyStr', 'ResultsHierarchizer')]
                            *****
                            self.AttentioningCollectionStr is PreConnectome
                            self.GraspingClueVariable is
/NodePointDeriveNoder/<Datome>ParametersHierarchizer

                            xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


                                                                    xxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
////////////////////////////////
Doer/__init__.py callDo
                                                                    From
Doer/__init__.py callDo | Applyier/__init__.py do_apply | Applyier/__init__.py
mimic_set | Mimicker/__init__.py mimic | Noder/__init__.py mimic_set |
Mimicker/__init__.py mimic | Distinguisher/__init__.py mimic_set |
Mimicker/__init__.py mimic | Setter/__init__.py __setitem__ |
Applyier/__init__.py do_apply | Mapper/__init__.py do_map | Updater/__init__.py
do_update | Walker/__init__.py do_walk | site-packages/six.py exec_ |
Celler/__init__.py do_cell | Notebooker/__init__.py do_notebook |
Documenter/__init__.py do_inform | inform.py <module>
////////////////////////////////

                                                                    l.49 :
                                                                    *****
                                                                    I am with
[('NodeKeyStr', 'TopFactorizer')]
                                                                    *****
                                                                    We factorize
here
                                                                    xxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


                                                                    xxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
////////////////////////////////
Doer/__init__.py callDo
                                                                    From
Doer/__init__.py callDo | Applyier/__init__.py do_apply | Applyier/__init__.py
mimic_set | Mimicker/__init__.py mimic | Noder/__init__.py mimic_set |
Mimicker/__init__.py mimic | Distinguisher/__init__.py mimic_set |
Mimicker/__init__.py mimic | Setter/__init__.py __setitem__ |
Applyier/__init__.py do_apply | Mapper/__init__.py do_map | Updater/__init__.py
do_update | Walker/__init__.py do_walk | site-packages/six.py exec_ |
Celler/__init__.py do_cell | Notebooker/__init__.py do_notebook |
Documenter/__init__.py do_inform | inform.py <module>
////////////////////////////////

                                                                    l.49 :
                                                                    *****
                                                                    I am with
[('NodeKeyStr', 'TopFactorizer')]
                                                                    *****
                                                                    We factorize
here
                                                                    xxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx



*****Start of the Attest *****

MyFactorizer is < (FactorizerClass), 4564993232>
   /{
   /  '<New><Instance>ComponentCollectionOrderedDict' :
   /   /{
   /   /  'XSumer' : < (SumerClass), 4564995920>
   /   /   /{
   /   /   /  '<New><Instance>ComponentCollectionOrderedDict' :
   /   /   /   /{
   /   /   /   /}
   /   /   /  '<New><Instance>DatomeCollectionOrderedDict' :
   /   /   /   /{
   /   /   /   /  'ParametersHierarchizer' : < (HierarchizerClass), 4563962896>
   /   /   /   /   /{
   /   /   /   /   /  '<New><Instance>ComponentCollectionOrderedDict' :
   /   /   /   /   /   /{
   /   /   /   /   /   /}
   /   /   /   /   /  '<New><Instance>DatomeCollectionOrderedDict' :
   /   /   /   /   /   /{
   /   /   /   /   /   /}
   /   /   /   /   /  '<New><Instance>IdInt' : 4563962896
   /   /   /   /   /  '<New><Instance>NetworkAttentionStr' : Pre
   /   /   /   /   /  '<New><Instance>NetworkCatchStr' : Post
   /   /   /   /   /  '<New><Instance>NetworkCollectionStr' : Connectome
   /   /   /   /   /  '<New><Instance>NewtorkAttentionStr' :
   /   /   /   /   /  '<New><Instance>NewtorkCatchStr' :
   /   /   /   /   /  '<New><Instance>NewtorkCollectionStr' :
   /   /   /   /   /  '<New><Instance>NodeCollectionStr' : Datome
   /   /   /   /   /  '<New><Instance>NodeIndexInt' : 0
   /   /   /   /   /  '<New><Instance>NodeKeyStr' : ParametersHierarchizer
   /   /   /   /   /  '<New><Instance>NodePointDeriveNoder' : {...}<
(SumerClass), 4564995920>
   /   /   /   /   /  '<New><Instance>NodePointOrderedDict' : {...}<
(OrderedDict), 4564832632>
   /   /   /   /   /  '<New><Instance>PreConnectomeCollectionOrderedDict' :
   /   /   /   /   /   /{
   /   /   /   /   /   /
'ParametersHierarchizer_XSumer>TopFactorizer<ParametersHierarchizerPointer' : <
(PointerClass), 4565077840>
   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4565077840
   /   /   /   /   /   /   /  '<New><Instance>CatchToPointVariable' : <
(HierarchizerClass), 4565313168>
   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /
'<New><Instance>ComponentCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /  '<New><Instance>DatomeCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4565313168
   /   /   /   /   /   /   /   /  '<New><Instance>NetworkAttentionStr' : Pre
   /   /   /   /   /   /   /   /  '<New><Instance>NetworkCatchStr' : Post
   /   /   /   /   /   /   /   /  '<New><Instance>NetworkCollectionStr' :
Connectome
   /   /   /   /   /   /   /   /  '<New><Instance>NewtorkAttentionStr' :
   /   /   /   /   /   /   /   /  '<New><Instance>NewtorkCatchStr' :
   /   /   /   /   /   /   /   /  '<New><Instance>NewtorkCollectionStr' :
   /   /   /   /   /   /   /   /  '<New><Instance>NodeCollectionStr' : Datome
   /   /   /   /   /   /   /   /  '<New><Instance>NodeIndexInt' : 0
   /   /   /   /   /   /   /   /  '<New><Instance>NodeKeyStr' :
ParametersHierarchizer
   /   /   /   /   /   /   /   /  '<New><Instance>NodePointDeriveNoder' : {...}<
(FactorizerClass), 4564993232>
   /   /   /   /   /   /   /   /  '<New><Instance>NodePointOrderedDict' :
   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /  'ParametersHierarchizer' : {...}<
(HierarchizerClass), 4565313168>
   /   /   /   /   /   /   /   /   /  'ResultsHierarchizer' : <
(HierarchizerClass), 4565076240>
   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /
'<New><Instance>ComponentCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /
'<New><Instance>DatomeCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4565076240
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>NetworkAttentionStr' :
Pre
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>NetworkCatchStr' :
Post
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>NetworkCollectionStr'
: Connectome
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>NewtorkAttentionStr' :
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>NewtorkCatchStr' :
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>NewtorkCollectionStr'
:
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>NodeCollectionStr' :
Datome
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>NodeIndexInt' : 1
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>NodeKeyStr' :
ResultsHierarchizer
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>NodePointDeriveNoder'
: {...}< (FactorizerClass), 4564993232>
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>NodePointOrderedDict'
: {...}< (OrderedDict), 4564931232>
   /   /   /   /   /   /   /   /   /   /
'<New><Instance>PostConnectomeCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /
'_NodePointDeriveNoder_<Datome>ParametersHierarchizerPointer' : <
(PointerClass), 4564993424>
   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' :
4564993424
   /   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>CatchToPointVariable'
: {...}< (HierarchizerClass), 4565313168>
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedPathBackVariable' :
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedGetVariable' : {...}< (HierarchizerClass), 4565313168>
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedLocalSetStr' : CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingGetVariable' : {...}< (HierarchizerClass), 4565313168>
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingSetPathStr' : CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>TagStr' : Networked
   /   /   /   /   /   /   /   /   /   /
'<New><Instance>_ModelingDescriptionTuplesList' :
   /   /   /   /   /   /   /   /   /   /   /[
   /   /   /   /   /   /   /   /   /   /   /  0 :
   /   /   /   /   /   /   /   /   /   /   /   /(
   /   /   /   /   /   /   /   /   /   /   /   /  0 : JoinedTopFactorizerResults
HierarchizerModelToTopFactorizerParametersHierarchizerModelRetrieveIndexesList
   /   /   /   /   /   /   /   /   /   /   /   /  1 :
JoinTopFactorizerParametersHierarchizerModelRetrieveIndexesList
   /   /   /   /   /   /   /   /   /   /   /   /  2 : Int64Col(shape=(2,),
dflt=0, pos=None)
   /   /   /   /   /   /   /   /   /   /   /   /)
   /   /   /   /   /   /   /   /   /   /   /  1 :
   /   /   /   /   /   /   /   /   /   /   /   /(
   /   /   /   /   /   /   /   /   /   /   /   /  0 : FactorizedTotalFloat
   /   /   /   /   /   /   /   /   /   /   /   /  1 : FactorizedTotalFloat
   /   /   /   /   /   /   /   /   /   /   /   /  2 : Float64Col(shape=(),
dflt=0.0, pos=None)
   /   /   /   /   /   /   /   /   /   /   /   /)
   /   /   /   /   /   /   /   /   /   /   /]
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>_RowingKeyStrsList' : 
['JoinedTopFactorizerResultsHierarchizerModelToTopFactorizerParametersHierarchiz
erModelRetrieveIndexesList', 'JoinedTopFactorizerResultsHierarchizerModelToTopFa
ctorizerParametersHierarchizerModelRetrieveIndexesList', 'JoinedTopFactorizerRes
ultsHierarchizerModelToTopFactorizerParametersHierarchizerModelRetrieveIndexesLi
st', 'JoinedTopFactorizerResultsHierarchizerModelToTopFactorizerParametersHierar
chizerModelRetrieveIndexesList']
   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /
'<New><Instance>PostConnectomeCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /
'_NodePointDeriveNoder_<Component>XSumer_<Datome>ParametersHierarchizerPointer'
: < (PointerClass), 4563979536>
   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4563979536
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>CatchToPointVariable' :
{...}< (HierarchizerClass), 4563962896>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /   /   /   /  '<Spe><Class>PointedPathBackVariable'
:
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointedGetVariable' :
{...}< (HierarchizerClass), 4563962896>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointedLocalSetStr' :
CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingGetVariable' :
{...}< (HierarchizerClass), 4563962896>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingSetPathStr' :
CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /
'_NodePointDeriveNoder_<Component>YSumer_<Datome>ParametersHierarchizerPointer'
: < (PointerClass), 4565075344>
   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4565075344
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>CatchToPointVariable' : <
(HierarchizerClass), 4563977808>
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
4563977808
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
ParametersHierarchizer
   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NodePointDeriveNoder' : < (SumerClass), 4563979152>
   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>ComponentCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>DatomeCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /  'ParametersHierarchizer' :
{...}< (HierarchizerClass), 4563977808>
   /   /   /   /   /   /   /   /   /   /   /   /   /  'ResultsHierarchizer' : <
(HierarchizerClass), 4565074832>
   /   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>ComponentCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>DatomeCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt'
: 4565074832
   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NetworkAttentionStr' : Pre
   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NetworkCatchStr' : Post
   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NetworkCollectionStr' : Connectome
   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NewtorkAttentionStr' :
   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NewtorkCatchStr' :
   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NewtorkCollectionStr' :
   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NodeCollectionStr' : Datome
   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NodeIndexInt' : 1
   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NodeKeyStr' : ResultsHierarchizer
   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NodePointDeriveNoder' : {...}< (SumerClass), 4563979152>
   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NodePointOrderedDict' : {...}< (OrderedDict), 4564834704>
   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>PostConnectomeCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'_NodePointDeriveNoder_<Datome>ParametersHierarchizerPointer' : <
(PointerClass), 4564956048>
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>IdInt' : 4564956048
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>CatchToPointVariable' : {...}< (HierarchizerClass), 4563977808>
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedPathBackVariable' :
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedGetVariable' : {...}< (HierarchizerClass), 4563977808>
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedLocalSetStr' : CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingGetVariable' : {...}< (HierarchizerClass), 4563977808>
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingSetPathStr' : CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>TagStr' : Networked
   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>_ModelingDescriptionTuplesList' :
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /[
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /  0 :
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /(
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /  0 : JoinedYSum
erResultsHierarchizerModelToYSumerParametersHierarchizerModelRetrieveIndexesList
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /  1 :
JoinYSumerParametersHierarchizerModelRetrieveIndexesList
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /  2 :
Int64Col(shape=(2,), dflt=0, pos=None)
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /)
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /  1 :
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /(
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /  0 :
SumedTotalInt
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /  1 :
SumedTotalInt
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /  2 :
Int64Col(shape=(), dflt=0, pos=None)
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /)
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /]
   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>_RowingKeyStrsList' : ['JoinedYSumerResultsHierarchizerModelToYS
umerParametersHierarchizerModelRetrieveIndexesList', 'JoinedYSumerResultsHierarc
hizerModelToYSumerParametersHierarchizerModelRetrieveIndexesList', 'JoinedYSumer
ResultsHierarchizerModelToYSumerParametersHierarchizerModelRetrieveIndexesList',
'JoinedYSumerResultsHierarchizerModelToYSumerParametersHierarchizerModelRetrieve
IndexesList']
   /   /   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' :
4563979152
   /   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>JoinedYSumerRe
sultsHierarchizerModelToYSumerParametersHierarchizerModelRetrieveIndexesList' :
[0, 1]
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
YSumer
   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NodePointDeriveNoder' : {...}< (FactorizerClass), 4564993232>
   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NodePointOrderedDict' : {...}< (OrderedDict), 4564835888>
   /   /   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>SumedTotalInt'
: 5
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>SumingFirstInt' : 1
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>SumingSecondInt' : 4
   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NodePointOrderedDict' : {...}< (OrderedDict), 4564834704>
   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>PreConnectomeCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /
'ParametersHierarchizer_YSumer>TopFactorizer<ParametersHierarchizerPointer' : <
(PointerClass), 4564955344>
   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' :
4564955344
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>CatchToPointVariable' : {...}< (HierarchizerClass), 4565313168>
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedPathBackVariable' :
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedGetVariable' : {...}< (HierarchizerClass), 4565313168>
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedLocalSetStr' : CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingGetVariable' : {...}< (HierarchizerClass), 4565313168>
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingSetPathStr' : CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /   /
'ParametersHierarchizer_YSumer>TopFactorizer<YSumer_ResultsHierarchizerPointer'
: < (PointerClass), 4564955216>
   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' :
4564955216
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>CatchToPointVariable' : {...}< (HierarchizerClass), 4565074832>
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedPathBackVariable' :
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedGetVariable' : {...}< (HierarchizerClass), 4565074832>
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedLocalSetStr' : CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingGetVariable' : {...}< (HierarchizerClass), 4565074832>
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingSetPathStr' : CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>_ModelingDescriptionTuplesList' :
   /   /   /   /   /   /   /   /   /   /   /   /[
   /   /   /   /   /   /   /   /   /   /   /   /  0 :
   /   /   /   /   /   /   /   /   /   /   /   /   /(
   /   /   /   /   /   /   /   /   /   /   /   /   /  0 : SumingFirstInt
   /   /   /   /   /   /   /   /   /   /   /   /   /  1 : SumingFirstInt
   /   /   /   /   /   /   /   /   /   /   /   /   /  2 : Int64Col(shape=(),
dflt=0, pos=None)
   /   /   /   /   /   /   /   /   /   /   /   /   /)
   /   /   /   /   /   /   /   /   /   /   /   /  1 :
   /   /   /   /   /   /   /   /   /   /   /   /   /(
   /   /   /   /   /   /   /   /   /   /   /   /   /  0 : SumingSecondInt
   /   /   /   /   /   /   /   /   /   /   /   /   /  1 : SumingSecondInt
   /   /   /   /   /   /   /   /   /   /   /   /   /  2 : Int64Col(shape=(),
dflt=0, pos=None)
   /   /   /   /   /   /   /   /   /   /   /   /   /)
   /   /   /   /   /   /   /   /   /   /   /   /]
   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>_RowingKeyStrsList' : ['SumingFirstInt', 'SumingSecondInt']
   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /  '<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /   /   /   /  '<Spe><Class>PointedPathBackVariable'
:
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointedGetVariable' :
{...}< (HierarchizerClass), 4563977808>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointedLocalSetStr' :
CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingGetVariable' :
{...}< (HierarchizerClass), 4563977808>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingSetPathStr' :
CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /
'<New><Instance>PreConnectomeCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /
'ParametersHierarchizer>TopFactorizer<ResultsHierarchizerPointer' : <
(PointerClass), 4564955856>
   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4564955856
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>CatchToPointVariable' :
{...}< (HierarchizerClass), 4565076240>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /   /   /   /  '<Spe><Class>PointedPathBackVariable'
:
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointedGetVariable' :
{...}< (HierarchizerClass), 4565076240>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointedLocalSetStr' :
CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingGetVariable' :
{...}< (HierarchizerClass), 4565076240>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingSetPathStr' :
CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /  '<New><Instance>_ModelingDescriptionTuplesList' :
   /   /   /   /   /   /   /   /   /[
   /   /   /   /   /   /   /   /   /  0 :
   /   /   /   /   /   /   /   /   /   /(
   /   /   /   /   /   /   /   /   /   /  0 : JoinedTopFactorizerParametersHiera
rchizerModelToXSumerParametersHierarchizerModelRetrieveIndexesList
   /   /   /   /   /   /   /   /   /   /  1 :
JoinXSumerParametersHierarchizerModelRetrieveIndexesList
   /   /   /   /   /   /   /   /   /   /  2 : Int64Col(shape=(2,), dflt=0,
pos=None)
   /   /   /   /   /   /   /   /   /   /)
   /   /   /   /   /   /   /   /   /  1 :
   /   /   /   /   /   /   /   /   /   /(
   /   /   /   /   /   /   /   /   /   /  0 : JoinedTopFactorizerParametersHiera
rchizerModelToYSumerParametersHierarchizerModelRetrieveIndexesList
   /   /   /   /   /   /   /   /   /   /  1 :
JoinYSumerParametersHierarchizerModelRetrieveIndexesList
   /   /   /   /   /   /   /   /   /   /  2 : Int64Col(shape=(2,), dflt=0,
pos=None)
   /   /   /   /   /   /   /   /   /   /)
   /   /   /   /   /   /   /   /   /  2 :
   /   /   /   /   /   /   /   /   /   /(
   /   /   /   /   /   /   /   /   /   /  0 : FactorizingPowerFloat
   /   /   /   /   /   /   /   /   /   /  1 : FactorizingPowerFloat
   /   /   /   /   /   /   /   /   /   /  2 : Float64Col(shape=(), dflt=0.0,
pos=None)
   /   /   /   /   /   /   /   /   /   /)
   /   /   /   /   /   /   /   /   /]
   /   /   /   /   /   /   /   /  '<New><Instance>_RowingKeyStrsList' : ['Joined
TopFactorizerParametersHierarchizerModelToXSumerParametersHierarchizerModelRetri
eveIndexesList', 'JoinedTopFactorizerParametersHierarchizerModelToYSumerParamete
rsHierarchizerModelRetrieveIndexesList', 'JoinedTopFactorizerParametersHierarchi
zerModelToXSumerParametersHierarchizerModelRetrieveIndexesList', 'JoinedTopFacto
rizerParametersHierarchizerModelToYSumerParametersHierarchizerModelRetrieveIndex
esList', 'JoinedTopFactorizerParametersHierarchizerModelToXSumerParametersHierar
chizerModelRetrieveIndexesList', 'JoinedTopFactorizerParametersHierarchizerModel
ToYSumerParametersHierarchizerModelRetrieveIndexesList', 'JoinedTopFactorizerPar
ametersHierarchizerModelToXSumerParametersHierarchizerModelRetrieveIndexesList',
'JoinedTopFactorizerParametersHierarchizerModelToYSumerParametersHierarchizerMod
elRetrieveIndexesList', 'JoinedTopFactorizerParametersHierarchizerModelToXSumerP
arametersHierarchizerModelRetrieveIndexesList', 'JoinedTopFactorizerParametersHi
erarchizerModelToYSumerParametersHierarchizerModelRetrieveIndexesList', 'JoinedT
opFactorizerParametersHierarchizerModelToXSumerParametersHierarchizerModelRetrie
veIndexesList', 'JoinedTopFactorizerParametersHierarchizerModelToYSumerParameter
sHierarchizerModelRetrieveIndexesList', 'JoinedTopFactorizerParametersHierarchiz
erModelToXSumerParametersHierarchizerModelRetrieveIndexesList', 'JoinedTopFactor
izerParametersHierarchizerModelToYSumerParametersHierarchizerModelRetrieveIndexe
sList', 'JoinedTopFactorizerParametersHierarchizerModelToXSumerParametersHierarc
hizerModelRetrieveIndexesList', 'JoinedTopFactorizerParametersHierarchizerModelT
oYSumerParametersHierarchizerModelRetrieveIndexesList', 'FactorizingPowerFloat']
   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /  '<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /  '<Spe><Class>PointedPathBackVariable' :
   /   /   /   /   /   /   /  '<Spe><Instance>PointedGetVariable' : {...}<
(HierarchizerClass), 4565313168>
   /   /   /   /   /   /   /  '<Spe><Instance>PointedLocalSetStr' :
CatchToPointVariable
   /   /   /   /   /   /   /  '<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /  '<Spe><Instance>PointingGetVariable' : {...}<
(HierarchizerClass), 4565313168>
   /   /   /   /   /   /   /  '<Spe><Instance>PointingSetPathStr' :
CatchToPointVariable
   /   /   /   /   /   /   /}
   /   /   /   /   /   /
'ParametersHierarchizer_XSumer>TopFactorizer<XSumer_ResultsHierarchizerPointer'
: < (PointerClass), 4564955792>
   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4564955792
   /   /   /   /   /   /   /  '<New><Instance>CatchToPointVariable' : <
(HierarchizerClass), 4565312912>{...}< (dict), 4563706776>
   /   /   /   /   /   /   /  '<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /  '<Spe><Class>PointedPathBackVariable' :
   /   /   /   /   /   /   /  '<Spe><Instance>PointedGetVariable' : {...}<
(HierarchizerClass), 4565312912>
   /   /   /   /   /   /   /  '<Spe><Instance>PointedLocalSetStr' :
CatchToPointVariable
   /   /   /   /   /   /   /  '<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /  '<Spe><Instance>PointingGetVariable' : {...}<
(HierarchizerClass), 4565312912>
   /   /   /   /   /   /   /  '<Spe><Instance>PointingSetPathStr' :
CatchToPointVariable
   /   /   /   /   /   /   /}
   /   /   /   /   /   /}
   /   /   /   /   /  '<New><Instance>_ModelingDescriptionTuplesList' :
   /   /   /   /   /   /[
   /   /   /   /   /   /  0 :
   /   /   /   /   /   /   /(
   /   /   /   /   /   /   /  0 : SumingFirstInt
   /   /   /   /   /   /   /  1 : SumingFirstInt
   /   /   /   /   /   /   /  2 : Int64Col(shape=(), dflt=0, pos=None)
   /   /   /   /   /   /   /)
   /   /   /   /   /   /  1 :
   /   /   /   /   /   /   /(
   /   /   /   /   /   /   /  0 : SumingSecondInt
   /   /   /   /   /   /   /  1 : SumingSecondInt
   /   /   /   /   /   /   /  2 : Int64Col(shape=(), dflt=0, pos=None)
   /   /   /   /   /   /   /)
   /   /   /   /   /   /]
   /   /   /   /   /  '<New><Instance>_RowingKeyStrsList' : ['SumingFirstInt',
'SumingSecondInt']
   /   /   /   /   /}
   /   /   /   /  'ResultsHierarchizer' : {...}< (HierarchizerClass),
4565312912>
   /   /   /   /}
   /   /   /  '<New><Instance>IdInt' : 4564995920
   /   /   /  '<New><Instance>JoinedXSumerResultsHierarchizerModelToXSumerParame
tersHierarchizerModelRetrieveIndexesList' : [0, 1]
   /   /   /  '<New><Instance>NewtorkAttentionStr' :
   /   /   /  '<New><Instance>NewtorkCatchStr' :
   /   /   /  '<New><Instance>NewtorkCollectionStr' :
   /   /   /  '<New><Instance>NodeCollectionStr' : Component
   /   /   /  '<New><Instance>NodeIndexInt' : 0
   /   /   /  '<New><Instance>NodeKeyStr' : XSumer
   /   /   /  '<New><Instance>NodePointDeriveNoder' : {...}< (FactorizerClass),
4564993232>
   /   /   /  '<New><Instance>NodePointOrderedDict' : {...}< (OrderedDict),
4564835888>
   /   /   /  '<Spe><Instance>SumedTotalInt' : 4
   /   /   /  '<Spe><Instance>SumingFirstInt' : 2
   /   /   /  '<Spe><Instance>SumingSecondInt' : 2
   /   /   /}
   /   /  'YSumer' : {...}< (SumerClass), 4563979152>
   /   /}
   /  '<New><Instance>DatomeCollectionOrderedDict' : {...}< (OrderedDict),
4564931232>
   /  '<New><Instance>IdInt' : 4564993232
   /  '<New><Instance>JoinedTopFactorizerParametersHierarchizerModelToXSumerPara
metersHierarchizerModelRetrieveIndexesList' : [0, 1]
   /  '<New><Instance>JoinedTopFactorizerParametersHierarchizerModelToYSumerPara
metersHierarchizerModelRetrieveIndexesList' : [0, 1]
   /  '<New><Instance>JoinedTopFactorizerResultsHierarchizerModelToTopFactorizer
ParametersHierarchizerModelRetrieveIndexesList' : [0, 1]
   /  '<New><Instance>NewtorkAttentionStr' :
   /  '<New><Instance>NewtorkCatchStr' :
   /  '<New><Instance>NewtorkCollectionStr' :
   /  '<New><Instance>NodeCollectionStr' : Globals
   /  '<New><Instance>NodeIndexInt' : -1
   /  '<New><Instance>NodeKeyStr' : TopFactorizer
   /  '<New><Instance>NodePointDeriveNoder' : None
   /  '<New><Instance>NodePointOrderedDict' : None
   /  '<Spe><Class>FactorizingPowerFloat' : 1.0
   /  '<Spe><Instance>FactorizedTotalFloat' : 9.0
   /}

------

hdf5 file is : /                        Group
/TopFactorizer           Group
/TopFactorizer/XSumer    Group
/TopFactorizer/XSumer/xx0xxParametersHierarchizerTable Dataset {3/Inf}
    Data:
        (0) {RowInt=0, SumingFirstInt=1, SumingSecondInt=2},
        (1) {RowInt=1, SumingFirstInt=2, SumingSecondInt=2},
        (2) {RowInt=2, SumingFirstInt=1, SumingSecondInt=4}
/TopFactorizer/XSumer/xx0xxResultsHierarchizerTable Dataset {3/Inf}
    Data:
        (0) {JoinXSumerParametersHierarchizerModelRetrieveIndexesList=[0,0],
        (0)  RowInt=0, SumedTotalInt=3},
        (1) {JoinXSumerParametersHierarchizerModelRetrieveIndexesList=[0,1],
        (1)  RowInt=1, SumedTotalInt=4},
        (2) {JoinXSumerParametersHierarchizerModelRetrieveIndexesList=[0,2],
        (2)  RowInt=2, SumedTotalInt=5}
/TopFactorizer/YSumer    Group
/TopFactorizer/YSumer/xx0xxParametersHierarchizerTable Dataset {4/Inf}
    Data:
        (0) {RowInt=0, SumingFirstInt=1, SumingSecondInt=3},
        (1) {RowInt=1, SumingFirstInt=1, SumingSecondInt=4},
        (2) {RowInt=2, SumingFirstInt=0, SumingSecondInt=0},
        (3) {RowInt=3, SumingFirstInt=0, SumingSecondInt=3}
/TopFactorizer/YSumer/xx0xxResultsHierarchizerTable Dataset {4/Inf}
    Data:
        (0) {JoinYSumerParametersHierarchizerModelRetrieveIndexesList=[0,0],
        (0)  RowInt=0, SumedTotalInt=4},
        (1) {JoinYSumerParametersHierarchizerModelRetrieveIndexesList=[0,1],
        (1)  RowInt=1, SumedTotalInt=5},
        (2) {JoinYSumerParametersHierarchizerModelRetrieveIndexesList=[0,2],
        (2)  RowInt=2, SumedTotalInt=0},
        (3) {JoinYSumerParametersHierarchizerModelRetrieveIndexesList=[0,3],
        (3)  RowInt=3, SumedTotalInt=3}
/xx0xxParametersHierarchizerTable Dataset {7/Inf}
    Data:
        (0) {FactorizingPowerFloat=1,
        (0)  JoinXSumerParametersHierarchizerModelRetrieveIndexesList=[0,0],
        (0)  JoinYSumerParametersHierarchizerModelRetrieveIndexesList=[0,0],
        (0)  RowInt=0},
        (1) {FactorizingPowerFloat=1,
        (1)  JoinXSumerParametersHierarchizerModelRetrieveIndexesList=[0,1],
        (1)  JoinYSumerParametersHierarchizerModelRetrieveIndexesList=[0,1],
        (1)  RowInt=1},
        (2) {FactorizingPowerFloat=1,
        (2)  JoinXSumerParametersHierarchizerModelRetrieveIndexesList=[0,0],
        (2)  JoinYSumerParametersHierarchizerModelRetrieveIndexesList=[0,2],
        (2)  RowInt=2},
        (3) {FactorizingPowerFloat=1,
        (3)  JoinXSumerParametersHierarchizerModelRetrieveIndexesList=[0,2],
        (3)  JoinYSumerParametersHierarchizerModelRetrieveIndexesList=[0,2],
        (3)  RowInt=3},
        (4) {FactorizingPowerFloat=1,
        (4)  JoinXSumerParametersHierarchizerModelRetrieveIndexesList=[0,2],
        (4)  JoinYSumerParametersHierarchizerModelRetrieveIndexesList=[0,3],
        (4)  RowInt=4},
        (5) {FactorizingPowerFloat=1,
        (5)  JoinXSumerParametersHierarchizerModelRetrieveIndexesList=[0,2],
        (5)  JoinYSumerParametersHierarchizerModelRetrieveIndexesList=[0,0],
        (5)  RowInt=5},
        (6) {FactorizingPowerFloat=2,
        (6)  JoinXSumerParametersHierarchizerModelRetrieveIndexesList=[0,2],
        (6)  JoinYSumerParametersHierarchizerModelRetrieveIndexesList=[0,0],
        (6)  RowInt=6}
/xx0xxResultsHierarchizerTable Dataset {7/Inf}
    Data:
        (0) {FactorizedTotalFloat=7,
        (0)  JoinTopFactorizerParametersHierarchizerModelRetrieveIndexesList=[0,
        (0)  0], RowInt=0},
        (1) {FactorizedTotalFloat=9,
        (1)  JoinTopFactorizerParametersHierarchizerModelRetrieveIndexesList=[0,
        (1)  1], RowInt=1},
        (2) {FactorizedTotalFloat=0,
        (2)  JoinTopFactorizerParametersHierarchizerModelRetrieveIndexesList=[0,
        (2)  2], RowInt=2},
        (3) {FactorizedTotalFloat=0,
        (3)  JoinTopFactorizerParametersHierarchizerModelRetrieveIndexesList=[0,
        (3)  3], RowInt=3},
        (4) {FactorizedTotalFloat=0,
        (4)  JoinTopFactorizerParametersHierarchizerModelRetrieveIndexesList=[0,
        (4)  4], RowInt=4},
        (5) {FactorizedTotalFloat=0,
        (5)  JoinTopFactorizerParametersHierarchizerModelRetrieveIndexesList=[0,
        (5)  5], RowInt=5},
        (6) {FactorizedTotalFloat=81,
        (6)  JoinTopFactorizerParametersHierarchizerModelRetrieveIndexesList=[0,
        (6)  6], RowInt=6}


*****End of the Attest *****



```

