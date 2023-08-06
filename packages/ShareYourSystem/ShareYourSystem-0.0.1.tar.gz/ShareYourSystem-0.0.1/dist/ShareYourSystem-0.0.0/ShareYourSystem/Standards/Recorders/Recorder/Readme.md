

<!--
FrozenIsBool False
-->

#Simulater

##Doc
----


>
> A Simulater
>
>

----

<small>
View the Simulater notebook on [NbViewer](http://nbviewer.ipython.org/url/sharey
oursystem.ouvaton.org/Simulater.ipynb)
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


A Simulater

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Storers.Controller"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class SimulaterClass(BaseClass):

        #Definition
        RepresentingKeyStrsList=[
                'SimulatingStopTimeFloat',
                'SimulatingStepTimeFloat'
        ]

        #@Hooker.HookerClass(**{'HookingAfterVariablesList':[{'CallingVariable':
BaseClass.__init__}]})
        def default_init(self,
                                                _SimulatingStopTimeFloat=100.,
                                                _SimulatingStepTimeFloat=0.1,
                                                **_KwargVariablesDict
                                        ):

                #Call the parent __init__ method
                BaseClass.__init__(self,**_KwargVariablesDict)

        #@Hooker.HookerClass(**{'HookingAfterVariablesList':[{'CallingMethodStr'
:'hdformat'}]})
        #@Argumenter.ArgumenterClass()
        def do_simulate(
                                self,
                                **_KwargVariablesDict
                        ):

                #debug
                '''
                self.debug(('self.',self,[

                                        ]))
                '''
                #Return self
                #return self

#</DefineClass>

```

<small>
View the Simulater sources on <a href="https://github.com/Ledoux/ShareYourSystem
/tree/master/Pythonlogy/ShareYourSystem/Simulaters/Simulater"
target="_blank">Github</a>
</small>


