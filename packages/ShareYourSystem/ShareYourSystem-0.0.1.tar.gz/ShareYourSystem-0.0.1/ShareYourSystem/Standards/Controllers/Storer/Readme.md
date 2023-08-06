

<!--
FrozenIsBool False
-->

#Storer

##Doc
----


>
> Storer instances
>
>

----

<small>
View the Storer notebook on [NbViewer](http://nbviewer.ipython.org/url/shareyour
system.ouvaton.org/Storer.ipynb)
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


Storer instances

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Noders.Organizer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
from ShareYourSystem.Standards.Modelers import Hierarchizer
from ShareYourSystem.Standards.Noders import Noder
import operator
#</ImportSpecificModules>

#<DefineLocals>
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class StorerClass(BaseClass):

        #Definition
        RepresentingKeyStrsList=[
'StoringOrganizeIsBool'
                                                        ]

        def default_init(self,
                                                _StoringOrganizeIsBool=False,
                                                _StoringInsertIsBool=True,
                                                **_KwargVariablesDict
                                        ):

                #Call the parent init method
                BaseClass.__init__(self,**_KwargVariablesDict)

        def do_store(self):

                #Check
                if self.StoringOrganizeIsBool==False:

                        #organize
                        self.organize()

                        #Walk
                        self.walk(
                                {
                                        'AfterUpdateList':[
('organize',{'LiargVariablesList':[]})
                                        ],
'GatherVariablesList':[self.OrganizedComponentsGetStr]
                                }
                        )

                        #structure
                        self.structure(
                                        [self.OrganizingComponentsCollectionStr]
                                )

                        #network
                        self.network(
                                        **{
                                                'VisitingCollectionStrsList':[
self.OrganizingModelsCollectionStr,
self.OrganizingComponentsCollectionStr
                                                ],
'RecruitingConcludeConditionVariable':[
                                                        (
'__class__.__mro__',
operator.contains,Hierarchizer.HierarchizerClass
                                                        )
                                                ]
                                        }
                                )

                        #set
                        self.StoringOrganizeIsBool=True

                #Check
                if self.StoringInsertIsBool:

                        #Walk
                        self.walk(
                                {
                                        'AfterUpdateList':[
('callDo',{'LiargVariablesList':[]})
                                        ],
'GatherVariablesList':[self.OrganizedComponentsGetStr]
                                }
                        )

                        #debug
                        '''
self.debug(('self.',self,['OrganizedTopDeriveDatabaserVariable']))
                        '''

                        #insert
                        self.OrganizedTopDeriveDatabaserVariable.insert()

#</DefineClass>


```

<small>
View the Storer sources on <a href="https://github.com/Ledoux/ShareYourSystem/tr
ee/master/Pythonlogy/ShareYourSystem/Storers/Storer" target="_blank">Github</a>
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
from ShareYourSystem.Standards.Controllers import Storer
import numpy as np

#Define a Sumer class
@Classer.ClasserClass()
class SumerClass(Storer.StorerClass):

    #Definition
    RepresentingKeyStrsList=[
                                'SumingFirstInt',
                                'SumingSecondInt',
                                'SumedTotalInt'
                            ]

    def default_init(self,
                        _SumingFirstInt=0,
                        _SumingSecondInt=0,
                        _SumedTotalInt=0
                    ):

        #Call the parent init method
        self.__class__.__bases__[0].__init__(self)

    def do_sum(self):

        #set the SumedTotalInt
        self.SumedTotalInt=self.SumingFirstInt+self.SumingSecondInt

#Define a Factorizer class
@Classer.ClasserClass()
class FactorizerClass(Storer.StorerClass):

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
                    self[self.OrganizedComponentsGetStr]
                )
            ),
            self.FactorizingPowerFloat
        )

#Definition of a Factorizer
MyFactorizer=FactorizerClass()

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
).store()

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
).store()

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

                                xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                                ////////////////////////////////
                                Attentioner/__init__.py do_attention
                                From Attentioner/__init__.py do_attention |
Connecter/__init__.py do_connect | Networker/__init__.py do_network |
Storer/__init__.py do_store | site-packages/six.py exec_ | Celler/__init__.py
do_cell | Notebooker/__init__.py do_notebook | Documenter/__init__.py do_inform |
inform.py <module>
                                ////////////////////////////////

                                l.60 :
                                *****
                                I am with [('NodeKeyStr',
'ParametersHierarchizer')]
                                *****
                                self.AttentioningCollectionStr is PreConnectome
                                self.GraspingClueVariable is
/NodePointDeriveNoder/<Component>XSumer/<Data>ParametersHierarchizer

                                xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


                                xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                                ////////////////////////////////
                                Attentioner/__init__.py do_attention
                                From Attentioner/__init__.py do_attention |
Connecter/__init__.py do_connect | Networker/__init__.py do_network |
Storer/__init__.py do_store | site-packages/six.py exec_ | Celler/__init__.py
do_cell | Notebooker/__init__.py do_notebook | Documenter/__init__.py do_inform |
inform.py <module>
                                ////////////////////////////////

                                l.60 :
                                *****
                                I am with [('NodeKeyStr',
'ParametersHierarchizer')]
                                *****
                                self.AttentioningCollectionStr is PreConnectome
                                self.GraspingClueVariable is
/NodePointDeriveNoder/<Component>YSumer/<Data>ParametersHierarchizer

                                xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


                                xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                                ////////////////////////////////
                                Attentioner/__init__.py do_attention
                                From Attentioner/__init__.py do_attention |
Connecter/__init__.py do_connect | Networker/__init__.py do_network |
Storer/__init__.py do_store | site-packages/six.py exec_ | Celler/__init__.py
do_cell | Notebooker/__init__.py do_notebook | Documenter/__init__.py do_inform |
inform.py <module>
                                ////////////////////////////////

                                l.60 :
                                *****
                                I am with [('NodeKeyStr',
'ResultsHierarchizer')]
                                *****
                                self.AttentioningCollectionStr is PreConnectome
                                self.GraspingClueVariable is
/NodePointDeriveNoder/<Data>ParametersHierarchizer

                                xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


                                xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                                ////////////////////////////////
                                Attentioner/__init__.py do_attention
                                From Attentioner/__init__.py do_attention |
Connecter/__init__.py do_connect | Networker/__init__.py do_network |
Storer/__init__.py do_store | site-packages/six.py exec_ | Celler/__init__.py
do_cell | Notebooker/__init__.py do_notebook | Documenter/__init__.py do_inform |
inform.py <module>
                                ////////////////////////////////

                                l.60 :
                                *****
                                I am with [('NodeKeyStr',
'ResultsHierarchizer')]
                                *****
                                self.AttentioningCollectionStr is PreConnectome
                                self.GraspingClueVariable is
/NodePointDeriveNoder/<Data>ParametersHierarchizer

                                xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


                                xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                                ////////////////////////////////
                                Attentioner/__init__.py do_attention
                                From Attentioner/__init__.py do_attention |
Connecter/__init__.py do_connect | Networker/__init__.py do_network |
Storer/__init__.py do_store | site-packages/six.py exec_ | Celler/__init__.py
do_cell | Notebooker/__init__.py do_notebook | Documenter/__init__.py do_inform |
inform.py <module>
                                ////////////////////////////////

                                l.60 :
                                *****
                                I am with [('NodeKeyStr',
'ResultsHierarchizer')]
                                *****
                                self.AttentioningCollectionStr is PreConnectome
                                self.GraspingClueVariable is
/NodePointDeriveNoder/<Data>ParametersHierarchizer

                                xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx



*****Start of the Attest *****

MyFactorizer is < (FactorizerClass), 4557707536>
   /{
   /  '<New><Instance>ComponentCollectionOrderedDict' :
   /   /{
   /   /  'XSumer' : < (SumerClass), 4559399504>
   /   /   /{
   /   /   /  '<New><Instance>ComponentCollectionOrderedDict' :
   /   /   /   /{
   /   /   /   /}
   /   /   /  '<New><Instance>DataCollectionOrderedDict' :
   /   /   /   /{
   /   /   /   /  'ParametersHierarchizer' : < (HierarchizerClass), 4559445968>
   /   /   /   /   /{
   /   /   /   /   /  '<New><Instance>ComponentCollectionOrderedDict' :
   /   /   /   /   /   /{
   /   /   /   /   /   /}
   /   /   /   /   /  '<New><Instance>DataCollectionOrderedDict' :
   /   /   /   /   /   /{
   /   /   /   /   /   /}
   /   /   /   /   /  '<New><Instance>IdInt' : 4559445968
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
(SumerClass), 4559399504>
   /   /   /   /   /  '<New><Instance>NodePointOrderedDict' : {...}<
(OrderedDict), 4559449648>
   /   /   /   /   /  '<New><Instance>PreConnectomeCollectionOrderedDict' :
   /   /   /   /   /   /{
   /   /   /   /   /   /
'ParametersHierarchizer_XSumer>TopFactorizer<ParametersHierarchizerPointer' : <
(PointerClass), 4559813776>
   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4559813776
   /   /   /   /   /   /   /  '<New><Instance>CatchToPointVariable' : <
(HierarchizerClass), 4559400464>
   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /
'<New><Instance>ComponentCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /  '<New><Instance>DataCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4559400464
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
(FactorizerClass), 4557707536>
   /   /   /   /   /   /   /   /  '<New><Instance>NodePointOrderedDict' :
   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /  'ParametersHierarchizer' : {...}<
(HierarchizerClass), 4559400464>
   /   /   /   /   /   /   /   /   /  'ResultsHierarchizer' : <
(HierarchizerClass), 4559444176>
   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /
'<New><Instance>ComponentCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /
'<New><Instance>DataCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4559444176
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
: {...}< (FactorizerClass), 4557707536>
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>NodePointOrderedDict'
: {...}< (OrderedDict), 4559446392>
   /   /   /   /   /   /   /   /   /   /
'<New><Instance>PostConnectomeCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /
'_NodePointDeriveNoder_<Data>ParametersHierarchizerPointer' : < (PointerClass),
4559814032>
   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' :
4559814032
   /   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>CatchToPointVariable'
: {...}< (HierarchizerClass), 4559400464>
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedPathBackVariable' :
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedGetVariable' : {...}< (HierarchizerClass), 4559400464>
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedLocalSetStr' : CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingGetVariable' : {...}< (HierarchizerClass), 4559400464>
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
< (PointerClass), 4559494608>
   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4559494608
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>CatchToPointVariable' :
{...}< (HierarchizerClass), 4559445968>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /   /   /   /  '<Spe><Class>PointedPathBackVariable'
:
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointedGetVariable' :
{...}< (HierarchizerClass), 4559445968>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointedLocalSetStr' :
CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingGetVariable' :
{...}< (HierarchizerClass), 4559445968>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingSetPathStr' :
CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /
'_NodePointDeriveNoder_<Component>YSumer_<Data>ParametersHierarchizerPointer' :
< (PointerClass), 4559444752>
   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4559444752
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>CatchToPointVariable' : <
(HierarchizerClass), 4559444496>
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
4559444496
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
'<New><Instance>NodePointDeriveNoder' : < (SumerClass), 4559400400>
   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>ComponentCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>DataCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /  'ParametersHierarchizer' :
{...}< (HierarchizerClass), 4559444496>
   /   /   /   /   /   /   /   /   /   /   /   /   /  'ResultsHierarchizer' : <
(HierarchizerClass), 4559507728>
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
: 4559507728
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
'<New><Instance>NodePointDeriveNoder' : {...}< (SumerClass), 4559400400>
   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NodePointOrderedDict' : {...}< (OrderedDict), 4559530384>
   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>PostConnectomeCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'_NodePointDeriveNoder_<Data>ParametersHierarchizerPointer' : < (PointerClass),
4559814544>
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>IdInt' : 4559814544
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>CatchToPointVariable' : {...}< (HierarchizerClass), 4559444496>
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedPathBackVariable' :
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedGetVariable' : {...}< (HierarchizerClass), 4559444496>
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedLocalSetStr' : CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingGetVariable' : {...}< (HierarchizerClass), 4559444496>
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
4559400400
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
'<New><Instance>NodePointDeriveNoder' : {...}< (FactorizerClass), 4557707536>
   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NodePointOrderedDict' : {...}< (OrderedDict), 4559407504>
   /   /   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>SumedTotalInt'
: 5
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>SumingFirstInt' : 1
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>SumingSecondInt' : 4
   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NodePointOrderedDict' : {...}< (OrderedDict), 4559530384>
   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>PreConnectomeCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /
'ParametersHierarchizer_YSumer>TopFactorizer<ParametersHierarchizerPointer' : <
(PointerClass), 4559813264>
   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' :
4559813264
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>CatchToPointVariable' : {...}< (HierarchizerClass), 4559400464>
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedPathBackVariable' :
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedGetVariable' : {...}< (HierarchizerClass), 4559400464>
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedLocalSetStr' : CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingGetVariable' : {...}< (HierarchizerClass), 4559400464>
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingSetPathStr' : CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /   /
'ParametersHierarchizer_YSumer>TopFactorizer<YSumer_ResultsHierarchizerPointer'
: < (PointerClass), 4559812688>
   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' :
4559812688
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>CatchToPointVariable' : {...}< (HierarchizerClass), 4559507728>
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedPathBackVariable' :
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedGetVariable' : {...}< (HierarchizerClass), 4559507728>
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedLocalSetStr' : CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingGetVariable' : {...}< (HierarchizerClass), 4559507728>
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
{...}< (HierarchizerClass), 4559444496>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointedLocalSetStr' :
CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingGetVariable' :
{...}< (HierarchizerClass), 4559444496>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingSetPathStr' :
CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /
'<New><Instance>PreConnectomeCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /
'ParametersHierarchizer>TopFactorizer<ResultsHierarchizerPointer' : <
(PointerClass), 4559812304>
   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4559812304
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>CatchToPointVariable' :
{...}< (HierarchizerClass), 4559444176>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /   /   /   /  '<Spe><Class>PointedPathBackVariable'
:
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointedGetVariable' :
{...}< (HierarchizerClass), 4559444176>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointedLocalSetStr' :
CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingGetVariable' :
{...}< (HierarchizerClass), 4559444176>
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
(HierarchizerClass), 4559400464>
   /   /   /   /   /   /   /  '<Spe><Instance>PointedLocalSetStr' :
CatchToPointVariable
   /   /   /   /   /   /   /  '<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /  '<Spe><Instance>PointingGetVariable' : {...}<
(HierarchizerClass), 4559400464>
   /   /   /   /   /   /   /  '<Spe><Instance>PointingSetPathStr' :
CatchToPointVariable
   /   /   /   /   /   /   /}
   /   /   /   /   /   /
'ParametersHierarchizer_XSumer>TopFactorizer<XSumer_ResultsHierarchizerPointer'
: < (PointerClass), 4559812432>
   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4559812432
   /   /   /   /   /   /   /  '<New><Instance>CatchToPointVariable' : <
(HierarchizerClass), 4559494032>{...}< (dict), 4555069992>
   /   /   /   /   /   /   /  '<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /  '<Spe><Class>PointedPathBackVariable' :
   /   /   /   /   /   /   /  '<Spe><Instance>PointedGetVariable' : {...}<
(HierarchizerClass), 4559494032>
   /   /   /   /   /   /   /  '<Spe><Instance>PointedLocalSetStr' :
CatchToPointVariable
   /   /   /   /   /   /   /  '<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /  '<Spe><Instance>PointingGetVariable' : {...}<
(HierarchizerClass), 4559494032>
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
4559494032>
   /   /   /   /}
   /   /   /  '<New><Instance>IdInt' : 4559399504
   /   /   /  '<New><Instance>JoinedXSumerResultsHierarchizerModelToXSumerParame
tersHierarchizerModelRetrieveIndexesList' : [0, 1]
   /   /   /  '<New><Instance>NewtorkAttentionStr' :
   /   /   /  '<New><Instance>NewtorkCatchStr' :
   /   /   /  '<New><Instance>NewtorkCollectionStr' :
   /   /   /  '<New><Instance>NodeCollectionStr' : Component
   /   /   /  '<New><Instance>NodeIndexInt' : 0
   /   /   /  '<New><Instance>NodeKeyStr' : XSumer
   /   /   /  '<New><Instance>NodePointDeriveNoder' : {...}< (FactorizerClass),
4557707536>
   /   /   /  '<New><Instance>NodePointOrderedDict' : {...}< (OrderedDict),
4559407504>
   /   /   /  '<Spe><Instance>SumedTotalInt' : 4
   /   /   /  '<Spe><Instance>SumingFirstInt' : 2
   /   /   /  '<Spe><Instance>SumingSecondInt' : 2
   /   /   /}
   /   /  'YSumer' : {...}< (SumerClass), 4559400400>
   /   /}
   /  '<New><Instance>DataCollectionOrderedDict' : {...}< (OrderedDict),
4559446392>
   /  '<New><Instance>IdInt' : 4557707536
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

