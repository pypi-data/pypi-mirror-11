

<!--
FrozenIsBool False
-->

#Organizer

##Doc
----


>
> Organizer instances
>
>

----

<small>
View the Organizer notebook on [NbViewer](http://nbviewer.ipython.org/url/sharey
oursystem.ouvaton.org/Organizer.ipynb)
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


Organizer instances

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Noders.Structurer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
from ShareYourSystem.Standards.Modelers import Modeler
from ShareYourSystem.Standards.Noders import Noder
import operator
#</ImportSpecificModules>

#<DefineLocals>
#</DefineLocals>

#<DefineClass>
@DecorationClass(**{
        'ClassingSwitchMethodStrsList':['organize']
})
class OrganizerClass(BaseClass):

        #Definition
        RepresentingKeyStrsList=[
'OrganizingModelsCollectionStr',
'OrganizingComponentsCollectionStr',
'OrganizingOutKeyStrsList',
'OrganizingInKeyStrsList',
'OrganizingOutStr',
'OrganizingInStr',
'OrganizedTopDeriveDatabaserVariable',
'OrganizedInstallIsBool',
'OrganizedDataGetStr',
'OrganizedComponentsGetStr',
'OrganizedDataGetStr',
'OrganizedComponentsGetStr',
'OrganizedInConnectAttentionGetStrsList',
'OrganizedOutConnectAttentionGetStrsList'
                                                        ]

        def default_init(self,
_OrganizingModelsCollectionStr="Data",
_OrganizingComponentsCollectionStr="Component",
                                                _OrganizingOutKeyStrsList=None,
                                                _OrganizingInKeyStrsList=None,
                                                _OrganizingOutStr="Results",
                                                _OrganizingInStr="Parameters",
_OrganizedTopDeriveDatabaserVariable=None,
                                                _OrganizedInstallIsBool=False,
                                                _OrganizedDataGetStr="",
                                                _OrganizedComponentsGetStr="",
_OrganizedInConnectAttentionGetStrsList=None,
_OrganizedOutConnectAttentionGetStrsList=None,
_OrganizedComponentCollectionOrderedDict=None,
                                                **_KwargVariablesDict
                                        ):

                #Call the parent init method
                BaseClass.__init__(self,**_KwargVariablesDict)

        def do_organize(self):

                #Check
                if len(self.OrganizingInKeyStrsList)==0:
                        self.OrganizingInKeyStrsList=self.__class__.DoingAttribu
teVariablesOrderedDict.keys()
                if len(self.OrganizingOutKeyStrsList)==0:
                        self.OrganizingOutKeyStrsList=self.__class__.DoneAttribu
teVariablesOrderedDict.keys()

                #set
                self.OrganizedDataGetStr=Noder.NodingPrefixGetStr+self.Organizin
gDataCollectionStr+Noder.NodingSuffixGetStr
                self.OrganizedComponentsGetStr=Noder.NodingPrefixGetStr+self.Orga
nizingComponentCollectionStr+Noder.NodingSuffixGetStr

                #Make the hierarchical joins for the ins
                self.OrganizedInConnectAttentionGetStrsList=map(
                                lambda __DeriveNoder:
                                '/NodePointDeriveNoder/'+self.OrganizedComponent
GetStr+__DeriveNoder.NodeKeyStr+'/'+self.OrganizedDataGetStr+self.OrganizingInSt
r+'Hierarchizer',
                                self[self.OrganizedComponentsGetStr]
                        )

                #Set
                self.OrganizedComponentCollectionOrderedDict=getattr(
                        self,
self.OrganizingComponentsCollectionStr+'CollectionOrderedDict'
                )

                #map
                self.OrganizedOutConnectAttentionGetStrsList=[
                                '/NodePointDeriveNoder/'+self.OrganizedDataGetSt
r+self.OrganizingInStr+'Hierarchizer'
                ]

                #debug
                '''
                self.debug(
                                        ('self.',self,[
'OrganizedInConnectAttentionGetStrsList',
'OrganizedOutConnectAttentionGetStrsList'
                                                                ])
                        )
                '''

                #import
                from ShareYourSystem.Standards.Modelers import Hierarchizer

                #Set a parameters and a results database
                self.push(
                                [
                                        (
                                                self.OrganizingInStr,
Hierarchizer.HierarchizerClass().update(
                                                        [
                                                                (
'Attr_ModelingDescriptionTuplesList',
                                                                        map(
Modeler.getModelingColumnTupleWithGetKeyStr,
self.OrganizingInKeyStrsList
                                                                        )
                                                                ),
                                                                (
'Attr_RowingKeyStrsList',
self.__class__.DoingAttributeVariablesOrderedDict.keys()
                                                                ),
                                                                (
'ConnectingGraspClueVariablesList',
self.OrganizedInConnectAttentionGetStrsList
                                                                )
                                                        ]
                                                )
                                        ),
                                        (
                                                self.OrganizingOutStr,
Hierarchizer.HierarchizerClass().update(
                                                        [
                                                                (
'Attr_ModelingDescriptionTuplesList',
                                                                        map(
Modeler.getModelingColumnTupleWithGetKeyStr,
self.OrganizingOutKeyStrsList
                                                                        )
                                                                ),
                                                                (
'ConnectingGraspClueVariablesList',
self.OrganizedOutConnectAttentionGetStrsList
                                                                ),
('TagStr','Networked')
                                                        ]
                                                )
                                        )
                                ],
**{'CollectingCollectionStr':self.OrganizingModelsCollectionStr}
                )

                #set
                self.OrganizedTopDeriveDatabaserVariable=getattr(
                                self,
self.OrganizingModelsCollectionStr+'CollectionOrderedDict'
                        ).values()[-1]
#</DefineClass>


```

<small>
View the Organizer sources on <a href="https://github.com/Ledoux/ShareYourSystem
/tree/master/Pythonlogy/ShareYourSystem/Noders/Organizer"
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
from ShareYourSystem.Standards.Modelers import Hierarchizer
from ShareYourSystem.Standards.Noders import Organizer
import numpy as np
import operator

#Define a Sumer class
@Classer.ClasserClass()
class SumerClass(Organizer.OrganizerClass):

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
                    ):

        #Call the parent init method
        self.__class__.__bases__[0].__init__(self)

    def do_sum(self):

        #debug
        '''
        self.debug(('self.',self,['SumingFirstInt','SumingSecondInt']))
        '''

        #set the SumedTotalInt
        self.SumedTotalInt=self.SumingFirstInt+self.SumingSecondInt

#Define a Factorizer class
@Classer.ClasserClass()
class FactorizerClass(Organizer.OrganizerClass):

    #Definition
    RepresentingKeyStrsList=[
                                'FactorizingPowerFloat',
                                'FactorizedTotalFloat'
                            ]

    def default_init(self,
                        _FactorizingPowerFloat=1.,
                        _FactorizedTotalFloat=0.
                    ):

        #Call the parent init method
        self.__class__.__bases__[0].__init__(self)

        #Build the output hierarchy
        self.produce(
                ['X','Y'],
                SumerClass,
**{'CollectingCollectionStr':self.OrganizingComponentsCollectionStr}
            )

    def do_factorize(self):

        #debug
        '''
        self.debug('We factorize here')
        '''

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

#Definition of a Factorizer instance, organize structure and network
MyFactorizer=FactorizerClass().walk(
                {
                    'AfterUpdateList':[
                        ('organize',{'LiargVariablesList':[]})
                    ],
                    'GatherVariablesList':['<Component>']
                }
            ).structure(
                ['Component']
            ).network(
                **{
                    'VisitingCollectionStrsList':[
                        'Data','Component'
                    ],
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
)['<Data>ResultsHierarchizer'].insert()

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
)['<Data>ResultsHierarchizer'].insert()

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
/NodePointDeriveNoder/<Component>XSumer/<Data>ParametersHierarchizer

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
/NodePointDeriveNoder/<Component>YSumer/<Data>ParametersHierarchizer

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
/NodePointDeriveNoder/<Data>ParametersHierarchizer

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
/NodePointDeriveNoder/<Data>ParametersHierarchizer

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
/NodePointDeriveNoder/<Data>ParametersHierarchizer

                            xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx



*****Start of the Attest *****

MyFactorizer is < (FactorizerClass), 4557352528>
   /{
   /  '<New><Instance>ComponentCollectionOrderedDict' :
   /   /{
   /   /  'XSumer' : < (SumerClass), 4556883216>
   /   /   /{
   /   /   /  '<New><Instance>ComponentCollectionOrderedDict' :
   /   /   /   /{
   /   /   /   /}
   /   /   /  '<New><Instance>DataCollectionOrderedDict' :
   /   /   /   /{
   /   /   /   /  'ParametersHierarchizer' : < (HierarchizerClass), 4556885392>
   /   /   /   /   /{
   /   /   /   /   /  '<New><Instance>ComponentCollectionOrderedDict' :
   /   /   /   /   /   /{
   /   /   /   /   /   /}
   /   /   /   /   /  '<New><Instance>DataCollectionOrderedDict' :
   /   /   /   /   /   /{
   /   /   /   /   /   /}
   /   /   /   /   /  '<New><Instance>IdInt' : 4556885392
   /   /   /   /   /  '<New><Instance>NetworkAttentionStr' : Pre
   /   /   /   /   /  '<New><Instance>NetworkCatchStr' : Post
   /   /   /   /   /  '<New><Instance>NetworkCollectionStr' : Connectome
   /   /   /   /   /  '<New><Instance>NewtorkAttentionStr' :
   /   /   /   /   /  '<New><Instance>NewtorkCatchStr' :
   /   /   /   /   /  '<New><Instance>NewtorkCollectionStr' :
   /   /   /   /   /  '<New><Instance>NodeCollectionStr' : Data
   /   /   /   /   /  '<New><Instance>NodeIndexInt' : 0
   /   /   /   /   /  '<New><Instance>NodeKeyStr' : ParametersHierarchizer
   /   /   /   /   /  '<New><Instance>NodePointDeriveNoder' : {...}<
(SumerClass), 4556883216>
   /   /   /   /   /  '<New><Instance>NodePointOrderedDict' : {...}<
(OrderedDict), 4557341048>
   /   /   /   /   /  '<New><Instance>PreConnectomeCollectionOrderedDict' :
   /   /   /   /   /   /{
   /   /   /   /   /   /
'ParametersHierarchizer_XSumer>TopFactorizer<ParametersHierarchizerPointer' : <
(PointerClass), 4556355344>
   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4556355344
   /   /   /   /   /   /   /  '<New><Instance>CatchToPointVariable' : <
(HierarchizerClass), 4556884880>
   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /
'<New><Instance>ComponentCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /  '<New><Instance>DataCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4556884880
   /   /   /   /   /   /   /   /  '<New><Instance>NetworkAttentionStr' : Pre
   /   /   /   /   /   /   /   /  '<New><Instance>NetworkCatchStr' : Post
   /   /   /   /   /   /   /   /  '<New><Instance>NetworkCollectionStr' :
Connectome
   /   /   /   /   /   /   /   /  '<New><Instance>NewtorkAttentionStr' :
   /   /   /   /   /   /   /   /  '<New><Instance>NewtorkCatchStr' :
   /   /   /   /   /   /   /   /  '<New><Instance>NewtorkCollectionStr' :
   /   /   /   /   /   /   /   /  '<New><Instance>NodeCollectionStr' : Data
   /   /   /   /   /   /   /   /  '<New><Instance>NodeIndexInt' : 0
   /   /   /   /   /   /   /   /  '<New><Instance>NodeKeyStr' :
ParametersHierarchizer
   /   /   /   /   /   /   /   /  '<New><Instance>NodePointDeriveNoder' : {...}<
(FactorizerClass), 4557352528>
   /   /   /   /   /   /   /   /  '<New><Instance>NodePointOrderedDict' :
   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /  'ParametersHierarchizer' : {...}<
(HierarchizerClass), 4556884880>
   /   /   /   /   /   /   /   /   /  'ResultsHierarchizer' : <
(HierarchizerClass), 4556885136>
   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /
'<New><Instance>ComponentCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /
'<New><Instance>DataCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4556885136
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
Data
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>NodeIndexInt' : 1
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>NodeKeyStr' :
ResultsHierarchizer
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>NodePointDeriveNoder'
: {...}< (FactorizerClass), 4557352528>
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>NodePointOrderedDict'
: {...}< (OrderedDict), 4556907760>
   /   /   /   /   /   /   /   /   /   /
'<New><Instance>PostConnectomeCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /
'_NodePointDeriveNoder_<Data>ParametersHierarchizerPointer' : < (PointerClass),
4556354960>
   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' :
4556354960
   /   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>CatchToPointVariable'
: {...}< (HierarchizerClass), 4556884880>
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedPathBackVariable' :
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedGetVariable' : {...}< (HierarchizerClass), 4556884880>
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedLocalSetStr' : CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingGetVariable' : {...}< (HierarchizerClass), 4556884880>
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
'_NodePointDeriveNoder_<Component>XSumer_<Data>ParametersHierarchizerPointer' :
< (PointerClass), 4556885264>
   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4556885264
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>CatchToPointVariable' :
{...}< (HierarchizerClass), 4556885392>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /   /   /   /  '<Spe><Class>PointedPathBackVariable'
:
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointedGetVariable' :
{...}< (HierarchizerClass), 4556885392>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointedLocalSetStr' :
CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingGetVariable' :
{...}< (HierarchizerClass), 4556885392>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingSetPathStr' :
CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /
'_NodePointDeriveNoder_<Component>YSumer_<Data>ParametersHierarchizerPointer' :
< (PointerClass), 4556883280>
   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4556883280
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>CatchToPointVariable' : <
(HierarchizerClass), 4556969104>
   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>ComponentCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>DataCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' :
4556969104
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
: Data
   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>NodeIndexInt' : 0
   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>NodeKeyStr' :
ParametersHierarchizer
   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NodePointDeriveNoder' : < (SumerClass), 4556884176>
   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>ComponentCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>DataCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /  'ParametersHierarchizer' :
{...}< (HierarchizerClass), 4556969104>
   /   /   /   /   /   /   /   /   /   /   /   /   /  'ResultsHierarchizer' : <
(HierarchizerClass), 4556968592>
   /   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>ComponentCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>DataCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt'
: 4556968592
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
'<New><Instance>NodeCollectionStr' : Data
   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NodeIndexInt' : 1
   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NodeKeyStr' : ResultsHierarchizer
   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NodePointDeriveNoder' : {...}< (SumerClass), 4556884176>
   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NodePointOrderedDict' : {...}< (OrderedDict), 4557343712>
   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>PostConnectomeCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'_NodePointDeriveNoder_<Data>ParametersHierarchizerPointer' : < (PointerClass),
4555497744>
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>IdInt' : 4555497744
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>CatchToPointVariable' : {...}< (HierarchizerClass), 4556969104>
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedPathBackVariable' :
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedGetVariable' : {...}< (HierarchizerClass), 4556969104>
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedLocalSetStr' : CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingGetVariable' : {...}< (HierarchizerClass), 4556969104>
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
Int32Col(shape=(), dflt=0, pos=None)
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
4556884176
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
'<New><Instance>NodePointDeriveNoder' : {...}< (FactorizerClass), 4557352528>
   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NodePointOrderedDict' : {...}< (OrderedDict), 4556821744>
   /   /   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>SumedTotalInt'
: 5
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>SumingFirstInt' : 1
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>SumingSecondInt' : 4
   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NodePointOrderedDict' : {...}< (OrderedDict), 4557343712>
   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>PreConnectomeCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /
'ParametersHierarchizer_YSumer>TopFactorizer<ParametersHierarchizerPointer' : <
(PointerClass), 4556356432>
   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' :
4556356432
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>CatchToPointVariable' : {...}< (HierarchizerClass), 4556884880>
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedPathBackVariable' :
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedGetVariable' : {...}< (HierarchizerClass), 4556884880>
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedLocalSetStr' : CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingGetVariable' : {...}< (HierarchizerClass), 4556884880>
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingSetPathStr' : CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /   /
'ParametersHierarchizer_YSumer>TopFactorizer<YSumer_ResultsHierarchizerPointer'
: < (PointerClass), 4556365648>
   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' :
4556365648
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>CatchToPointVariable' : {...}< (HierarchizerClass), 4556968592>
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedPathBackVariable' :
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedGetVariable' : {...}< (HierarchizerClass), 4556968592>
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedLocalSetStr' : CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingGetVariable' : {...}< (HierarchizerClass), 4556968592>
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
   /   /   /   /   /   /   /   /   /   /   /   /   /  2 : Int32Col(shape=(),
dflt=0, pos=None)
   /   /   /   /   /   /   /   /   /   /   /   /   /)
   /   /   /   /   /   /   /   /   /   /   /   /  1 :
   /   /   /   /   /   /   /   /   /   /   /   /   /(
   /   /   /   /   /   /   /   /   /   /   /   /   /  0 : SumingSecondInt
   /   /   /   /   /   /   /   /   /   /   /   /   /  1 : SumingSecondInt
   /   /   /   /   /   /   /   /   /   /   /   /   /  2 : Int32Col(shape=(),
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
{...}< (HierarchizerClass), 4556969104>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointedLocalSetStr' :
CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingGetVariable' :
{...}< (HierarchizerClass), 4556969104>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingSetPathStr' :
CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /
'<New><Instance>PreConnectomeCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /
'ParametersHierarchizer>TopFactorizer<ResultsHierarchizerPointer' : <
(PointerClass), 4555579152>
   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4555579152
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>CatchToPointVariable' :
{...}< (HierarchizerClass), 4556885136>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /   /   /   /  '<Spe><Class>PointedPathBackVariable'
:
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointedGetVariable' :
{...}< (HierarchizerClass), 4556885136>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointedLocalSetStr' :
CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingGetVariable' :
{...}< (HierarchizerClass), 4556885136>
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
(HierarchizerClass), 4556884880>
   /   /   /   /   /   /   /  '<Spe><Instance>PointedLocalSetStr' :
CatchToPointVariable
   /   /   /   /   /   /   /  '<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /  '<Spe><Instance>PointingGetVariable' : {...}<
(HierarchizerClass), 4556884880>
   /   /   /   /   /   /   /  '<Spe><Instance>PointingSetPathStr' :
CatchToPointVariable
   /   /   /   /   /   /   /}
   /   /   /   /   /   /
'ParametersHierarchizer_XSumer>TopFactorizer<XSumer_ResultsHierarchizerPointer'
: < (PointerClass), 4555497680>
   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4555497680
   /   /   /   /   /   /   /  '<New><Instance>CatchToPointVariable' : <
(HierarchizerClass), 4556968272>
   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /
'<New><Instance>ComponentCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /  '<New><Instance>DataCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4556968272
   /   /   /   /   /   /   /   /  '<New><Instance>NetworkAttentionStr' : Pre
   /   /   /   /   /   /   /   /  '<New><Instance>NetworkCatchStr' : Post
   /   /   /   /   /   /   /   /  '<New><Instance>NetworkCollectionStr' :
Connectome
   /   /   /   /   /   /   /   /  '<New><Instance>NewtorkAttentionStr' :
   /   /   /   /   /   /   /   /  '<New><Instance>NewtorkCatchStr' :
   /   /   /   /   /   /   /   /  '<New><Instance>NewtorkCollectionStr' :
   /   /   /   /   /   /   /   /  '<New><Instance>NodeCollectionStr' : Data
   /   /   /   /   /   /   /   /  '<New><Instance>NodeIndexInt' : 1
   /   /   /   /   /   /   /   /  '<New><Instance>NodeKeyStr' :
ResultsHierarchizer
   /   /   /   /   /   /   /   /  '<New><Instance>NodePointDeriveNoder' : {...}<
(SumerClass), 4556883216>
   /   /   /   /   /   /   /   /  '<New><Instance>NodePointOrderedDict' : {...}<
(OrderedDict), 4557341048>
   /   /   /   /   /   /   /   /
'<New><Instance>PostConnectomeCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /
'_NodePointDeriveNoder_<Data>ParametersHierarchizerPointer' : < (PointerClass),
4556356944>
   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4556356944
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>CatchToPointVariable' :
{...}< (HierarchizerClass), 4556885392>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /   /   /   /  '<Spe><Class>PointedPathBackVariable'
:
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointedGetVariable' :
{...}< (HierarchizerClass), 4556885392>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointedLocalSetStr' :
CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingGetVariable' :
{...}< (HierarchizerClass), 4556885392>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingSetPathStr' :
CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /  '<New><Instance>TagStr' : Networked
   /   /   /   /   /   /   /   /  '<New><Instance>_ModelingDescriptionTuplesList' :
   /   /   /   /   /   /   /   /   /[
   /   /   /   /   /   /   /   /   /  0 :
   /   /   /   /   /   /   /   /   /   /(
   /   /   /   /   /   /   /   /   /   /  0 : JoinedXSumerResultsHierarchizerMod
elToXSumerParametersHierarchizerModelRetrieveIndexesList
   /   /   /   /   /   /   /   /   /   /  1 :
JoinXSumerParametersHierarchizerModelRetrieveIndexesList
   /   /   /   /   /   /   /   /   /   /  2 : Int64Col(shape=(2,), dflt=0,
pos=None)
   /   /   /   /   /   /   /   /   /   /)
   /   /   /   /   /   /   /   /   /  1 :
   /   /   /   /   /   /   /   /   /   /(
   /   /   /   /   /   /   /   /   /   /  0 : SumedTotalInt
   /   /   /   /   /   /   /   /   /   /  1 : SumedTotalInt
   /   /   /   /   /   /   /   /   /   /  2 : Int32Col(shape=(), dflt=0,
pos=None)
   /   /   /   /   /   /   /   /   /   /)
   /   /   /   /   /   /   /   /   /]
   /   /   /   /   /   /   /   /  '<New><Instance>_RowingKeyStrsList' : ['Joined
XSumerResultsHierarchizerModelToXSumerParametersHierarchizerModelRetrieveIndexes
List', 'JoinedXSumerResultsHierarchizerModelToXSumerParametersHierarchizerModelR
etrieveIndexesList', 'JoinedXSumerResultsHierarchizerModelToXSumerParametersHier
archizerModelRetrieveIndexesList', 'JoinedXSumerResultsHierarchizerModelToXSumer
ParametersHierarchizerModelRetrieveIndexesList']
   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /  '<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /  '<Spe><Class>PointedPathBackVariable' :
   /   /   /   /   /   /   /  '<Spe><Instance>PointedGetVariable' : {...}<
(HierarchizerClass), 4556968272>
   /   /   /   /   /   /   /  '<Spe><Instance>PointedLocalSetStr' :
CatchToPointVariable
   /   /   /   /   /   /   /  '<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /  '<Spe><Instance>PointingGetVariable' : {...}<
(HierarchizerClass), 4556968272>
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
   /   /   /   /   /   /   /  2 : Int32Col(shape=(), dflt=0, pos=None)
   /   /   /   /   /   /   /)
   /   /   /   /   /   /  1 :
   /   /   /   /   /   /   /(
   /   /   /   /   /   /   /  0 : SumingSecondInt
   /   /   /   /   /   /   /  1 : SumingSecondInt
   /   /   /   /   /   /   /  2 : Int32Col(shape=(), dflt=0, pos=None)
   /   /   /   /   /   /   /)
   /   /   /   /   /   /]
   /   /   /   /   /  '<New><Instance>_RowingKeyStrsList' : ['SumingFirstInt',
'SumingSecondInt']
   /   /   /   /   /}
   /   /   /   /  'ResultsHierarchizer' : {...}< (HierarchizerClass),
4556968272>
   /   /   /   /}
   /   /   /  '<New><Instance>IdInt' : 4556883216
   /   /   /  '<New><Instance>JoinedXSumerResultsHierarchizerModelToXSumerParame
tersHierarchizerModelRetrieveIndexesList' : [0, 1]
   /   /   /  '<New><Instance>NewtorkAttentionStr' :
   /   /   /  '<New><Instance>NewtorkCatchStr' :
   /   /   /  '<New><Instance>NewtorkCollectionStr' :
   /   /   /  '<New><Instance>NodeCollectionStr' : Component
   /   /   /  '<New><Instance>NodeIndexInt' : 0
   /   /   /  '<New><Instance>NodeKeyStr' : XSumer
   /   /   /  '<New><Instance>NodePointDeriveNoder' : {...}< (FactorizerClass),
4557352528>
   /   /   /  '<New><Instance>NodePointOrderedDict' : {...}< (OrderedDict),
4556821744>
   /   /   /  '<Spe><Instance>SumedTotalInt' : 4
   /   /   /  '<Spe><Instance>SumingFirstInt' : 2
   /   /   /  '<Spe><Instance>SumingSecondInt' : 2
   /   /   /}
   /   /  'YSumer' : {...}< (SumerClass), 4556884176>
   /   /}
   /  '<New><Instance>DataCollectionOrderedDict' : {...}< (OrderedDict),
4556907760>
   /  '<New><Instance>IdInt' : 4557352528
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

