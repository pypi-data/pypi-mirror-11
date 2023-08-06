

<!--
FrozenIsBool False
-->

#Controller

##Doc
----


>
> A Controller
>
>

----

<small>
View the Controller notebook on [NbViewer](http://nbviewer.ipython.org/url/share
yoursystem.ouvaton.org/Controller.ipynb)
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


A Controller

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Storers.Grider"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class ControllerClass(BaseClass):

        #Definition
        RepresentingKeyStrsList=[
                                                                ]

        def default_init(self,
                                **_KwargVariablesDict):

                #Call the parent init method
                BaseClass.__init__(self,**_KwargVariablesDict)

        #@Argumenter.ArgumenterClass()
        def do_control(self):
                pass

#</DefineClass>


```

<small>
View the Controller sources on <a href="https://github.com/Ledoux/ShareYourSyste
m/tree/master/Pythonlogy/ShareYourSystem/Storers/Controller"
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
from ShareYourSystem.Standards.Controllers import Controller

#Short expression and set in the appended manner
MyController=Controller.ControllerClass()

#Definition the AttestedStr
SYS._attest(
    [
        'MyController is '+SYS._str(
        MyController,
        **{
            'RepresentingBaseKeyStrsListBool':False
        }
        )
    ]
)

#Print



```


```console
>>>


*****Start of the Attest *****

MyController is < (ControllerClass), 4555038992>
   /{
   /  '<New><Instance>IdInt' : 4555038992
   /  '<New><Instance>NewtorkAttentionStr' :
   /  '<New><Instance>NewtorkCatchStr' :
   /  '<New><Instance>NewtorkCollectionStr' :
   /  '<New><Instance>NodeCollectionStr' : Globals
   /  '<New><Instance>NodeIndexInt' : -1
   /  '<New><Instance>NodeKeyStr' : TopController
   /  '<New><Instance>NodePointDeriveNoder' : None
   /  '<New><Instance>NodePointOrderedDict' : None
   /}

*****End of the Attest *****



```

