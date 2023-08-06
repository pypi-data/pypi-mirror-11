

<!--
FrozenIsBool False
-->

#Conditioner

##Doc
----


>
> The Conditioner
>
>

----

<small>
View the Conditioner notebook on [NbViewer](http://nbviewer.ipython.org/url/shar
eyoursystem.ouvaton.org/Conditioner.ipynb)
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


The Conditioner

"""


#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Objects.Debugger"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Representer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
Representer=DecorationModule
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class ConditionerClass(BaseClass):

        #Definition
        RepresentingKeyStrsList=[
'ConditioningTestGetVariable',
'ConditioningGetBoolFunction',
'ConditionedIsBool'
                                                                ]

        def default_init(self,
                                                _ConditioningTestGetVariable=None,
_ConditioningGetBoolFunction=None,
_ConditioningAttestGetVariable=None,
                                                _ConditionedIsBool=True,
                                                **_KwargVariablesDict
                                        ):

                #Call the parent init method
                BaseClass.__init__(self,**_KwargVariablesDict)

        #<DefineDoMethod>
        def do_condition(self):

                #debug
                '''
                self.debug(('self.',self,[
'ConditioningTestGetVariable',
'ConditioningAttestGetVariable'
                                                                ]))
                '''

                #call
                self.ConditionedIsBool=self.ConditioningGetBoolFunction(
                        self.ConditioningTestGetVariable,
                        self.ConditioningAttestGetVariable
                )

                #debug
                '''
                self.debug(('self.',self,['ConditionedIsBool']))
                '''

#</DefineClass>


```

<small>
View the Conditioner sources on <a href="https://github.com/Ledoux/ShareYourSyst
em/tree/master/Pythonlogy/ShareYourSystem/Objects/Conditioner"
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
from ShareYourSystem.Standards.Classors import Attester
from ShareYourSystem.Standards.Objects import Conditioner

#Definition of an instance Conditioner and make it print hello
MyConditioner=Conditioner.ConditionerClass(**{
        'ConditioningGetBoolFunction':lambda
_TestVariable,_AttestVariable:_TestVariable==_AttestVariable,
        'ConditioningAttestGetVariable':2
    })
MyConditioner.condition(3).ConditionedIsBool

#Definition the AttestedStr
SYS._attest(
                    [
                        'MyConditioner.condition(3).ConditionedIsBool is '+str(
                            MyConditioner.condition(3).ConditionedIsBool),
                        'MyConditioner.condition(2).ConditionedIsBool is '+str(
                            MyConditioner.condition(2).ConditionedIsBool)
                    ]
                )

#Print



```


```console
>>>


*****Start of the Attest *****

MyConditioner.condition(3).ConditionedIsBool is False

------

MyConditioner.condition(2).ConditionedIsBool is True

*****End of the Attest *****



```

