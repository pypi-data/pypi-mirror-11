

<!--
FrozenIsBool False
-->

#Grider

##Doc
----


>
> Grider instances
>
>

----

<small>
View the Grider notebook on [NbViewer](http://nbviewer.ipython.org/url/shareyour
system.ouvaton.org/Grider.ipynb)
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


Grider instances

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Storers.Storer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import itertools
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class GriderClass(BaseClass):

        #Definition
        RepresentingKeyStrsList=[
                                                'GridingScanTuplesList',
                                                'GridedGetKeyStrsList',
'GridedValueVariablesTuplesList',
'GridedComponentRetrieveListsList',
                                                'GridedScanRetrieveListsList'
                                        ]

        def default_init(
                        self,
                        _GridingScanTuplesList=None,
                        _GridedGetKeyStrsList=None,
                        _GridedValueVariablesTuplesList=None,
                        _GridedComponentRetrieveListsList=None,
                        _GridedScanRetrieveListsList=None,
                        **_KwargVariablesDict
                ):

                #Call the parent init method
                BaseClass.__init__(self,**_KwargVariablesDict)

        def do_grid(self):

                #just for init
                self.store(_InsertIsBool=False)

                #grid before in all the components
                self.GridedComponentRetrieveListsList=map(
                                lambda __DeriveGrider:
__DeriveGrider.grid().GridedScanRetrieveListsList,
self.OrganizedComponentCollectionOrderedDict.values()
                        )

                #debug
                self.debug(('self.',self,['GridedComponentRetrieveListsList']))

                #set the GridedGettingStrsList
                self.GridedGetKeyStrsList=SYS.unzip(
                        self.GridingScanTuplesList,[0]
                )

                #scan the values of this model
                self.GridedValueVariablesTuplesList=list(
                                itertools.product(
                                        *SYS.unzip(
                                                self.GridingScanTuplesList,[1]
                                        )
                                )
                )

                #set
                self.StoringInsertIsBool=True

                #map an update and a store for each combination
                self.GridedScanRetrieveListsList=map(
                                lambda __GridedValueVariablesTuple:
                                self.update(
                                        zip(
                                                self.GridedGetKeyStrsList,
                                                __GridedValueVariablesTuple
                                        )
                                ).store(
                                ).OrganizedTopDeriveDatabaserVariable.pick(
                                        ['TabledInt','RowedIndexInt']
                                ),
                                self.GridedValueVariablesTuplesList
                        )

                #debug
                '''
                self.debug(('self.',self,['GridedScanRetrieveListsList']))
                '''

                #Return self
                #return self

#</DefineClass>


```

<small>
View the Grider sources on <a href="https://github.com/Ledoux/ShareYourSystem/tr
ee/master/Pythonlogy/ShareYourSystem/Storers/Grider" target="_blank">Github</a>
</small>




<!---
FrozenIsBool True
-->

##Example

Now we do a grid that first grid in each sub components, get the retrive index
lists
and so do the scan in the upper layers with all the combiations of retrieve
lists.

```python
#ImportModules
import ShareYourSystem as SYS
from ShareYourSystem.Standards.Classors import Classer
from ShareYourSystem.Standards.Controllers import Grider
import numpy as np

#Define a Sumer class
@Classer.ClasserClass()
class SumerClass(Grider.GriderClass):

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
class FactorizerClass(Grider.GriderClass):

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
MyFactorizer=FactorizerClass().__setitem__(
    "Dis_<Component>",
    [
        [
            (
                'GridingScanTuplesList',
                [
                    ('SumingFirstInt',[1]),
                    ('SumingSecondInt',[2,4])
                ]
            ),
        ],
        [
            (
                'GridingScanTuplesList',
                [
                    ('SumingFirstInt',[0,1]),
                    ('SumingSecondInt',[3])
                ]
            ),
        ],
    ]
)

#grid
MyFactorizer.grid([('FactorizingPowerFloat',[1,2])])

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

                                    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                                    ////////////////////////////////
                                    Attentioner/__init__.py do_attention
                                    From Attentioner/__init__.py do_attention |
Connecter/__init__.py do_connect | Networker/__init__.py do_network |
Storer/__init__.py do_store | Grider/__init__.py do_grid | site-packages/six.py
exec_ | Celler/__init__.py do_cell | Notebooker/__init__.py do_notebook |
Documenter/__init__.py do_inform | inform.py <module>
                                    ////////////////////////////////

                                    l.60 :
                                    *****
                                    I am with [('NodeKeyStr',
'ParametersHierarchizer')]
                                    *****
                                    self.AttentioningCollectionStr is
PreConnectome
                                    self.GraspingClueVariable is
/NodePointDeriveNoder/<Component>XSumer/<Data>ParametersHierarchizer

                                    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


                                    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                                    ////////////////////////////////
                                    Attentioner/__init__.py do_attention
                                    From Attentioner/__init__.py do_attention |
Connecter/__init__.py do_connect | Networker/__init__.py do_network |
Storer/__init__.py do_store | Grider/__init__.py do_grid | site-packages/six.py
exec_ | Celler/__init__.py do_cell | Notebooker/__init__.py do_notebook |
Documenter/__init__.py do_inform | inform.py <module>
                                    ////////////////////////////////

                                    l.60 :
                                    *****
                                    I am with [('NodeKeyStr',
'ParametersHierarchizer')]
                                    *****
                                    self.AttentioningCollectionStr is
PreConnectome
                                    self.GraspingClueVariable is
/NodePointDeriveNoder/<Component>YSumer/<Data>ParametersHierarchizer

                                    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


                                    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                                    ////////////////////////////////
                                    Attentioner/__init__.py do_attention
                                    From Attentioner/__init__.py do_attention |
Connecter/__init__.py do_connect | Networker/__init__.py do_network |
Storer/__init__.py do_store | Grider/__init__.py do_grid | site-packages/six.py
exec_ | Celler/__init__.py do_cell | Notebooker/__init__.py do_notebook |
Documenter/__init__.py do_inform | inform.py <module>
                                    ////////////////////////////////

                                    l.60 :
                                    *****
                                    I am with [('NodeKeyStr',
'ResultsHierarchizer')]
                                    *****
                                    self.AttentioningCollectionStr is
PreConnectome
                                    self.GraspingClueVariable is
/NodePointDeriveNoder/<Data>ParametersHierarchizer

                                    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


                                    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                                    ////////////////////////////////
                                    Attentioner/__init__.py do_attention
                                    From Attentioner/__init__.py do_attention |
Connecter/__init__.py do_connect | Networker/__init__.py do_network |
Storer/__init__.py do_store | Grider/__init__.py do_grid | site-packages/six.py
exec_ | Celler/__init__.py do_cell | Notebooker/__init__.py do_notebook |
Documenter/__init__.py do_inform | inform.py <module>
                                    ////////////////////////////////

                                    l.60 :
                                    *****
                                    I am with [('NodeKeyStr',
'ResultsHierarchizer')]
                                    *****
                                    self.AttentioningCollectionStr is
PreConnectome
                                    self.GraspingClueVariable is
/NodePointDeriveNoder/<Data>ParametersHierarchizer

                                    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


                                    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                                    ////////////////////////////////
                                    Attentioner/__init__.py do_attention
                                    From Attentioner/__init__.py do_attention |
Connecter/__init__.py do_connect | Networker/__init__.py do_network |
Storer/__init__.py do_store | Grider/__init__.py do_grid | site-packages/six.py
exec_ | Celler/__init__.py do_cell | Notebooker/__init__.py do_notebook |
Documenter/__init__.py do_inform | inform.py <module>
                                    ////////////////////////////////

                                    l.60 :
                                    *****
                                    I am with [('NodeKeyStr',
'ResultsHierarchizer')]
                                    *****
                                    self.AttentioningCollectionStr is
PreConnectome
                                    self.GraspingClueVariable is
/NodePointDeriveNoder/<Data>ParametersHierarchizer

                                    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


                                        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                                        ////////////////////////////////
                                        Attentioner/__init__.py do_attention
                                        From Attentioner/__init__.py
do_attention | Connecter/__init__.py do_connect | Networker/__init__.py
do_network | Storer/__init__.py do_store | Grider/__init__.py do_grid |
Grider/__init__.py do_grid | site-packages/six.py exec_ | Celler/__init__.py
do_cell | Notebooker/__init__.py do_notebook | Documenter/__init__.py do_inform |
inform.py <module>
                                        ////////////////////////////////

                                        l.60 :
                                        *****
                                        I am with [('NodeKeyStr',
'ResultsHierarchizer')]
                                        *****
                                        self.AttentioningCollectionStr is
PreConnectome
                                        self.GraspingClueVariable is
/NodePointDeriveNoder/<Data>ParametersHierarchizer

                                        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


                        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                        ////////////////////////////////
                        Grider/__init__.py do_grid
                        From Grider/__init__.py do_grid | Grider/__init__.py
do_grid | site-packages/six.py exec_ | Celler/__init__.py do_cell |
Notebooker/__init__.py do_notebook | Documenter/__init__.py do_inform | inform.py
<module>
                        ////////////////////////////////

                        l.65 :
                        *****
                        I am with [('NodeKeyStr', 'XSumer')]
                        *****
                        self.GridedComponentRetrieveListsList is []

                        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


                                        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                                        ////////////////////////////////
                                        Attentioner/__init__.py do_attention
                                        From Attentioner/__init__.py
do_attention | Connecter/__init__.py do_connect | Networker/__init__.py
do_network | Storer/__init__.py do_store | Grider/__init__.py do_grid |
Grider/__init__.py do_grid | site-packages/six.py exec_ | Celler/__init__.py
do_cell | Notebooker/__init__.py do_notebook | Documenter/__init__.py do_inform |
inform.py <module>
                                        ////////////////////////////////

                                        l.60 :
                                        *****
                                        I am with [('ModelingKeyStr',
'ParametersHierarchizer'), ('NodeKeyStr', 'ParametersHierarchizer')]
                                        *****
                                        self.AttentioningCollectionStr is
PreConnectome
                                        self.GraspingClueVariable is
/NodePointDeriveNoder/<Component>XSumer/<Data>ParametersHierarchizer

                                        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


                                        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                                        ////////////////////////////////
                                        Attentioner/__init__.py do_attention
                                        From Attentioner/__init__.py
do_attention | Connecter/__init__.py do_connect | Networker/__init__.py
do_network | Storer/__init__.py do_store | Grider/__init__.py do_grid |
Grider/__init__.py do_grid | site-packages/six.py exec_ | Celler/__init__.py
do_cell | Notebooker/__init__.py do_notebook | Documenter/__init__.py do_inform |
inform.py <module>
                                        ////////////////////////////////

                                        l.60 :
                                        *****
                                        I am with [('ModelingKeyStr',
'ParametersHierarchizer'), ('NodeKeyStr', 'ParametersHierarchizer')]
                                        *****
                                        self.AttentioningCollectionStr is
PreConnectome
                                        self.GraspingClueVariable is
/NodePointDeriveNoder/<Component>YSumer/<Data>ParametersHierarchizer

                                        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


                                        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                                        ////////////////////////////////
                                        Attentioner/__init__.py do_attention
                                        From Attentioner/__init__.py
do_attention | Connecter/__init__.py do_connect | Networker/__init__.py
do_network | Storer/__init__.py do_store | Grider/__init__.py do_grid |
Grider/__init__.py do_grid | site-packages/six.py exec_ | Celler/__init__.py
do_cell | Notebooker/__init__.py do_notebook | Documenter/__init__.py do_inform |
inform.py <module>
                                        ////////////////////////////////

                                        l.60 :
                                        *****
                                        I am with [('ModelingKeyStr',
'ResultsHierarchizer'), ('NodeKeyStr', 'ResultsHierarchizer')]
                                        *****
                                        self.AttentioningCollectionStr is
PreConnectome
                                        self.GraspingClueVariable is
/NodePointDeriveNoder/<Data>ParametersHierarchizer

                                        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


                                        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                                        ////////////////////////////////
                                        Attentioner/__init__.py do_attention
                                        From Attentioner/__init__.py
do_attention | Connecter/__init__.py do_connect | Networker/__init__.py
do_network | Storer/__init__.py do_store | Grider/__init__.py do_grid |
Grider/__init__.py do_grid | site-packages/six.py exec_ | Celler/__init__.py
do_cell | Notebooker/__init__.py do_notebook | Documenter/__init__.py do_inform |
inform.py <module>
                                        ////////////////////////////////

                                        l.60 :
                                        *****
                                        I am with [('ModelingKeyStr',
'ResultsHierarchizer'), ('NodeKeyStr', 'ResultsHierarchizer')]
                                        *****
                                        self.AttentioningCollectionStr is
PreConnectome
                                        self.GraspingClueVariable is
/NodePointDeriveNoder/<Data>ParametersHierarchizer

                                        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


                                        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                                        ////////////////////////////////
                                        Attentioner/__init__.py do_attention
                                        From Attentioner/__init__.py
do_attention | Connecter/__init__.py do_connect | Networker/__init__.py
do_network | Storer/__init__.py do_store | Grider/__init__.py do_grid |
Grider/__init__.py do_grid | site-packages/six.py exec_ | Celler/__init__.py
do_cell | Notebooker/__init__.py do_notebook | Documenter/__init__.py do_inform |
inform.py <module>
                                        ////////////////////////////////

                                        l.60 :
                                        *****
                                        I am with [('ModelingKeyStr',
'ResultsHierarchizer'), ('NodeKeyStr', 'ResultsHierarchizer')]
                                        *****
                                        self.AttentioningCollectionStr is
PreConnectome
                                        self.GraspingClueVariable is
/NodePointDeriveNoder/<Data>ParametersHierarchizer

                                        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


                        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                        ////////////////////////////////
                        Grider/__init__.py do_grid
                        From Grider/__init__.py do_grid | Grider/__init__.py
do_grid | site-packages/six.py exec_ | Celler/__init__.py do_cell |
Notebooker/__init__.py do_notebook | Documenter/__init__.py do_inform | inform.py
<module>
                        ////////////////////////////////

                        l.65 :
                        *****
                        I am with [('NodeKeyStr', 'YSumer')]
                        *****
                        self.GridedComponentRetrieveListsList is []

                        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


                    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                    ////////////////////////////////
                    Grider/__init__.py do_grid
                    From Grider/__init__.py do_grid | site-packages/six.py exec_
| Celler/__init__.py do_cell | Notebooker/__init__.py do_notebook |
Documenter/__init__.py do_inform | inform.py <module>
                    ////////////////////////////////

                    l.65 :
                    *****
                    I am with [('NodeKeyStr', 'TopFactorizer')]
                    *****
                    self.GridedComponentRetrieveListsList is
                       /[
                       /  0 :
                       /   /[
                       /   /  0 : [0, 0]
                       /   /  1 : [0, 2]
                       /   /]
                       /  1 :
                       /   /[
                       /   /  0 : [0, 3]
                       /   /  1 : [0, 0]
                       /   /]
                       /]

                    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx



*****Start of the Attest *****

MyFactorizer is < (FactorizerClass), 4555535056>
   /{
   /  '<New><Instance>ComponentCollectionOrderedDict' :
   /   /{
   /   /  'XSumer' : < (SumerClass), 4559652816>
   /   /   /{
   /   /   /  '<New><Instance>ComponentCollectionOrderedDict' :
   /   /   /   /{
   /   /   /   /}
   /   /   /  '<New><Instance>DataCollectionOrderedDict' :
   /   /   /   /{
   /   /   /   /  'ParametersHierarchizer' : < (HierarchizerClass), 4559811280>
   /   /   /   /   /{
   /   /   /   /   /  '<New><Instance>ComponentCollectionOrderedDict' :
   /   /   /   /   /   /{
   /   /   /   /   /   /}
   /   /   /   /   /  '<New><Instance>DataCollectionOrderedDict' :
   /   /   /   /   /   /{
   /   /   /   /   /   /}
   /   /   /   /   /  '<New><Instance>IdInt' : 4559811280
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
(SumerClass), 4559652816>
   /   /   /   /   /  '<New><Instance>NodePointOrderedDict' : {...}<
(OrderedDict), 4560020128>
   /   /   /   /   /  '<New><Instance>PreConnectomeCollectionOrderedDict' :
   /   /   /   /   /   /{
   /   /   /   /   /   /
'ParametersHierarchizer_XSumer>TopFactorizer<ParametersHierarchizerPointer' : <
(PointerClass), 4559510928>
   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4559510928
   /   /   /   /   /   /   /  '<New><Instance>CatchToPointVariable' : <
(HierarchizerClass), 4555535760>
   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /
'<New><Instance>ComponentCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /  '<New><Instance>DataCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4555535760
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
(FactorizerClass), 4555535056>
   /   /   /   /   /   /   /   /  '<New><Instance>NodePointOrderedDict' :
   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /  'ParametersHierarchizer' : {...}<
(HierarchizerClass), 4555535760>
   /   /   /   /   /   /   /   /   /  'ResultsHierarchizer' : <
(HierarchizerClass), 4559653968>
   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /
'<New><Instance>ComponentCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /
'<New><Instance>DataCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4559653968
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
: {...}< (FactorizerClass), 4555535056>
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>NodePointOrderedDict'
: {...}< (OrderedDict), 4557626928>
   /   /   /   /   /   /   /   /   /   /
'<New><Instance>PostConnectomeCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /
'_NodePointDeriveNoder_<Data>ParametersHierarchizerPointer' : < (PointerClass),
4559510544>
   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' :
4559510544
   /   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>CatchToPointVariable'
: {...}< (HierarchizerClass), 4555535760>
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedPathBackVariable' :
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedGetVariable' : {...}< (HierarchizerClass), 4555535760>
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedLocalSetStr' : CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingGetVariable' : {...}< (HierarchizerClass), 4555535760>
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
chizerModelRetrieveIndexesList', 'JoinedTopFactorizerResultsHierarchizerModelToT
opFactorizerParametersHierarchizerModelRetrieveIndexesList', 'JoinedTopFactorize
rResultsHierarchizerModelToTopFactorizerParametersHierarchizerModelRetrieveIndex
esList', 'JoinedTopFactorizerResultsHierarchizerModelToTopFactorizerParametersHi
erarchizerModelRetrieveIndexesList', 'JoinedTopFactorizerResultsHierarchizerMode
lToTopFactorizerParametersHierarchizerModelRetrieveIndexesList', 'JoinedTopFacto
rizerResultsHierarchizerModelToTopFactorizerParametersHierarchizerModelRetrieveI
ndexesList', 'JoinedTopFactorizerResultsHierarchizerModelToTopFactorizerParamete
rsHierarchizerModelRetrieveIndexesList', 'JoinedTopFactorizerResultsHierarchizer
ModelToTopFactorizerParametersHierarchizerModelRetrieveIndexesList', 'JoinedTopF
actorizerResultsHierarchizerModelToTopFactorizerParametersHierarchizerModelRetri
eveIndexesList']
   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /
'<New><Instance>PostConnectomeCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /
'_NodePointDeriveNoder_<Component>XSumer_<Data>ParametersHierarchizerPointer' :
< (PointerClass), 4559510800>
   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4559510800
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>CatchToPointVariable' :
{...}< (HierarchizerClass), 4559811280>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /   /   /   /  '<Spe><Class>PointedPathBackVariable'
:
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointedGetVariable' :
{...}< (HierarchizerClass), 4559811280>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointedLocalSetStr' :
CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingGetVariable' :
{...}< (HierarchizerClass), 4559811280>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingSetPathStr' :
CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /
'_NodePointDeriveNoder_<Component>YSumer_<Data>ParametersHierarchizerPointer' :
< (PointerClass), 4556651856>
   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4556651856
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>CatchToPointVariable' : <
(HierarchizerClass), 4559705488>
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
4559705488
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
'<New><Instance>NodePointDeriveNoder' : < (SumerClass), 4559653776>
   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>ComponentCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>DataCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /  'ParametersHierarchizer' :
{...}< (HierarchizerClass), 4559705488>
   /   /   /   /   /   /   /   /   /   /   /   /   /  'ResultsHierarchizer' : <
(HierarchizerClass), 4559707152>
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
: 4559707152
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
'<New><Instance>NodePointDeriveNoder' : {...}< (SumerClass), 4559653776>
   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NodePointOrderedDict' : {...}< (OrderedDict), 4560022792>
   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>PostConnectomeCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'_NodePointDeriveNoder_<Data>ParametersHierarchizerPointer' : < (PointerClass),
4559511056>
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>IdInt' : 4559511056
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>CatchToPointVariable' : {...}< (HierarchizerClass), 4559705488>
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedPathBackVariable' :
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedGetVariable' : {...}< (HierarchizerClass), 4559705488>
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedLocalSetStr' : CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingGetVariable' : {...}< (HierarchizerClass), 4559705488>
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
IndexesList', 'JoinedYSumerResultsHierarchizerModelToYSumerParametersHierarchize
rModelRetrieveIndexesList', 'JoinedYSumerResultsHierarchizerModelToYSumerParamet
ersHierarchizerModelRetrieveIndexesList', 'JoinedYSumerResultsHierarchizerModelT
oYSumerParametersHierarchizerModelRetrieveIndexesList', 'JoinedYSumerResultsHier
archizerModelToYSumerParametersHierarchizerModelRetrieveIndexesList', 'JoinedYSu
merResultsHierarchizerModelToYSumerParametersHierarchizerModelRetrieveIndexesLis
t', 'JoinedYSumerResultsHierarchizerModelToYSumerParametersHierarchizerModelRetr
ieveIndexesList', 'JoinedYSumerResultsHierarchizerModelToYSumerParametersHierarc
hizerModelRetrieveIndexesList', 'JoinedYSumerResultsHierarchizerModelToYSumerPar
ametersHierarchizerModelRetrieveIndexesList', 'JoinedYSumerResultsHierarchizerMo
delToYSumerParametersHierarchizerModelRetrieveIndexesList', 'JoinedYSumerResults
HierarchizerModelToYSumerParametersHierarchizerModelRetrieveIndexesList', 'Joine
dYSumerResultsHierarchizerModelToYSumerParametersHierarchizerModelRetrieveIndexe
sList', 'JoinedYSumerResultsHierarchizerModelToYSumerParametersHierarchizerModel
RetrieveIndexesList']
   /   /   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' :
4559653776
   /   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>JoinedYSumerRe
sultsHierarchizerModelToYSumerParametersHierarchizerModelRetrieveIndexesList' :
[0, 0]
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
'<New><Instance>NodePointDeriveNoder' : {...}< (FactorizerClass), 4555535056>
   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NodePointOrderedDict' : {...}< (OrderedDict), 4537425456>
   /   /   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>SumedTotalInt'
: 4
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>SumingFirstInt' : 1
   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>SumingSecondInt' : 3
   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>NodePointOrderedDict' : {...}< (OrderedDict), 4560022792>
   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>PreConnectomeCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /
'ParametersHierarchizer_YSumer>TopFactorizer<ParametersHierarchizerPointer' : <
(PointerClass), 4559510352>
   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' :
4559510352
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>CatchToPointVariable' : {...}< (HierarchizerClass), 4555535760>
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedPathBackVariable' :
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedGetVariable' : {...}< (HierarchizerClass), 4555535760>
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedLocalSetStr' : CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingGetVariable' : {...}< (HierarchizerClass), 4555535760>
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingSetPathStr' : CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /   /   /   /
'ParametersHierarchizer_YSumer>TopFactorizer<YSumer_ResultsHierarchizerPointer'
: < (PointerClass), 4559511440>
   /   /   /   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' :
4559511440
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<New><Instance>CatchToPointVariable' : {...}< (HierarchizerClass), 4559707152>
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Class>PointedPathBackVariable' :
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedGetVariable' : {...}< (HierarchizerClass), 4559707152>
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointedLocalSetStr' : CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /   /   /   /
'<Spe><Instance>PointingGetVariable' : {...}< (HierarchizerClass), 4559707152>
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
{...}< (HierarchizerClass), 4559705488>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointedLocalSetStr' :
CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingGetVariable' :
{...}< (HierarchizerClass), 4559705488>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingSetPathStr' :
CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /   /
'<New><Instance>PreConnectomeCollectionOrderedDict' :
   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /
'ParametersHierarchizer>TopFactorizer<ResultsHierarchizerPointer' : <
(PointerClass), 4559509136>
   /   /   /   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4559509136
   /   /   /   /   /   /   /   /   /   /  '<New><Instance>CatchToPointVariable' :
{...}< (HierarchizerClass), 4559653968>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /   /   /   /  '<Spe><Class>PointedPathBackVariable'
:
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointedGetVariable' :
{...}< (HierarchizerClass), 4559653968>
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointedLocalSetStr' :
CatchToPointVariable
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /   /   /   /  '<Spe><Instance>PointingGetVariable' :
{...}< (HierarchizerClass), 4559653968>
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
oYSumerParametersHierarchizerModelRetrieveIndexesList', 'JoinedTopFactorizerPara
metersHierarchizerModelToXSumerParametersHierarchizerModelRetrieveIndexesList', 
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
oYSumerParametersHierarchizerModelRetrieveIndexesList', 'JoinedTopFactorizerPara
metersHierarchizerModelToXSumerParametersHierarchizerModelRetrieveIndexesList', 
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
oYSumerParametersHierarchizerModelRetrieveIndexesList', 'JoinedTopFactorizerPara
metersHierarchizerModelToXSumerParametersHierarchizerModelRetrieveIndexesList', 
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
oYSumerParametersHierarchizerModelRetrieveIndexesList', 'JoinedTopFactorizerPara
metersHierarchizerModelToXSumerParametersHierarchizerModelRetrieveIndexesList', 
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
oYSumerParametersHierarchizerModelRetrieveIndexesList', 'JoinedTopFactorizerPara
metersHierarchizerModelToXSumerParametersHierarchizerModelRetrieveIndexesList', 
'JoinedTopFactorizerParametersHierarchizerModelToYSumerParametersHierarchizerMod
elRetrieveIndexesList', 'JoinedTopFactorizerParametersHierarchizerModelToXSumerP
arametersHierarchizerModelRetrieveIndexesList', 'JoinedTopFactorizerParametersHi
erarchizerModelToYSumerParametersHierarchizerModelRetrieveIndexesList', 'JoinedT
opFactorizerParametersHierarchizerModelToXSumerParametersHierarchizerModelRetrie
veIndexesList', 'JoinedTopFactorizerParametersHierarchizerModelToYSumerParameter
sHierarchizerModelRetrieveIndexesList', 'JoinedTopFactorizerParametersHierarchiz
erModelToXSumerParametersHierarchizerModelRetrieveIndexesList', 'JoinedTopFactor
izerParametersHierarchizerModelToYSumerParametersHierarchizerModelRetrieveIndexe
sList', 'FactorizingPowerFloat']
   /   /   /   /   /   /   /   /}
   /   /   /   /   /   /   /  '<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /  '<Spe><Class>PointedPathBackVariable' :
   /   /   /   /   /   /   /  '<Spe><Instance>PointedGetVariable' : {...}<
(HierarchizerClass), 4555535760>
   /   /   /   /   /   /   /  '<Spe><Instance>PointedLocalSetStr' :
CatchToPointVariable
   /   /   /   /   /   /   /  '<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /  '<Spe><Instance>PointingGetVariable' : {...}<
(HierarchizerClass), 4555535760>
   /   /   /   /   /   /   /  '<Spe><Instance>PointingSetPathStr' :
CatchToPointVariable
   /   /   /   /   /   /   /}
   /   /   /   /   /   /
'ParametersHierarchizer_XSumer>TopFactorizer<XSumer_ResultsHierarchizerPointer'
: < (PointerClass), 4555498960>
   /   /   /   /   /   /   /{
   /   /   /   /   /   /   /  '<New><Instance>IdInt' : 4555498960
   /   /   /   /   /   /   /  '<New><Instance>CatchToPointVariable' : <
(HierarchizerClass), 4559812112>{...}< (dict), 4540826240>
   /   /   /   /   /   /   /  '<Spe><Class>PointedBackSetStr' :
   /   /   /   /   /   /   /  '<Spe><Class>PointedPathBackVariable' :
   /   /   /   /   /   /   /  '<Spe><Instance>PointedGetVariable' : {...}<
(HierarchizerClass), 4559812112>
   /   /   /   /   /   /   /  '<Spe><Instance>PointedLocalSetStr' :
CatchToPointVariable
   /   /   /   /   /   /   /  '<Spe><Instance>PointingBackSetStr' :
   /   /   /   /   /   /   /  '<Spe><Instance>PointingGetVariable' : {...}<
(HierarchizerClass), 4559812112>
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
4559812112>
   /   /   /   /}
   /   /   /  '<New><Instance>IdInt' : 4559652816
   /   /   /  '<New><Instance>JoinedXSumerResultsHierarchizerModelToXSumerParame
tersHierarchizerModelRetrieveIndexesList' : [0, 2]
   /   /   /  '<New><Instance>NewtorkAttentionStr' :
   /   /   /  '<New><Instance>NewtorkCatchStr' :
   /   /   /  '<New><Instance>NewtorkCollectionStr' :
   /   /   /  '<New><Instance>NodeCollectionStr' : Component
   /   /   /  '<New><Instance>NodeIndexInt' : 0
   /   /   /  '<New><Instance>NodeKeyStr' : XSumer
   /   /   /  '<New><Instance>NodePointDeriveNoder' : {...}< (FactorizerClass),
4555535056>
   /   /   /  '<New><Instance>NodePointOrderedDict' : {...}< (OrderedDict),
4537425456>
   /   /   /  '<Spe><Instance>SumedTotalInt' : 5
   /   /   /  '<Spe><Instance>SumingFirstInt' : 1
   /   /   /  '<Spe><Instance>SumingSecondInt' : 4
   /   /   /}
   /   /  'YSumer' : {...}< (SumerClass), 4559653776>
   /   /}
   /  '<New><Instance>DataCollectionOrderedDict' : {...}< (OrderedDict),
4557626928>
   /  '<New><Instance>IdInt' : 4555535056
   /  '<New><Instance>JoinedTopFactorizerParametersHierarchizerModelToXSumerPara
metersHierarchizerModelRetrieveIndexesList' : [0, 2]
   /  '<New><Instance>JoinedTopFactorizerParametersHierarchizerModelToYSumerPara
metersHierarchizerModelRetrieveIndexesList' : [0, 0]
   /  '<New><Instance>JoinedTopFactorizerResultsHierarchizerModelToTopFactorizer
ParametersHierarchizerModelRetrieveIndexesList' : [0, 6]
   /  '<New><Instance>NewtorkAttentionStr' :
   /  '<New><Instance>NewtorkCatchStr' :
   /  '<New><Instance>NewtorkCollectionStr' :
   /  '<New><Instance>NodeCollectionStr' : Globals
   /  '<New><Instance>NodeIndexInt' : -1
   /  '<New><Instance>NodeKeyStr' : TopFactorizer
   /  '<New><Instance>NodePointDeriveNoder' : None
   /  '<New><Instance>NodePointOrderedDict' : None
   /  '<Spe><Instance>FactorizedTotalFloat' : 81
   /  '<Spe><Instance>FactorizingPowerFloat' : 2
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

