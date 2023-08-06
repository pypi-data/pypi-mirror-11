

<!--
FrozenIsBool False
-->

#Interfacer

##Doc
----


>
> The Interfacer
>
>

----

<small>
View the Interfacer notebook on [NbViewer](http://nbviewer.ipython.org/url/share
yoursystem.ouvaton.org/Interfacer.ipynb)
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


The Interfacer

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Objects.Rebooter"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import os
#</ImportSpecificModules>

#<DefineLocals>
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class InterfacerClass(BaseClass):

        #Definition
        RepresentingKeyStrsList=[
                                                                ]


        def default_init(self,
                                                **_KwargVariablesDict
                                        ):

                #Call the parent __init__ method
                BaseClass.__init__(self,**_KwargVariablesDict)

        #@Argumenter.ArgumenterClass()
        def do_interface(self,**_KwargVariablesDict):

                pass

                #Return self
                #return self

#</DefineClass>


```

<small>
View the Interfacer sources on <a href="https://github.com/Ledoux/ShareYourSyste
m/tree/master/Pythonlogy/ShareYourSystem/Interfacers/Interfacer"
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
from ShareYourSystem.Standards.Interfacers import Interfacer

#Definition
MyInterfacer=Interfacer.InterfacerClass()

#Definition the AttestedStr
SYS._attest(
    [
        'MyInterfacer is '+SYS._str(
            MyInterfacer,
            **{
            'RepresentingAlineaIsBool':False
            })
    ]
)

#Print



```


```console
>>>


*****Start of the Attest *****

MyInterfacer is < (InterfacerClass), 4540175632>
   /{
   /  '<New><Instance>IdInt' : 4540175632
   /}

*****End of the Attest *****



```

