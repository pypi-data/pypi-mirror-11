

<!--
FrozenIsBool False
-->

#Setter

##Doc
----


>
> A Setter has a __setitem__ method for setting things in the
<InstanceVariable>.__dict__
>
>

----

<small>
View the Setter notebook on [NbViewer](http://nbviewer.ipython.org/url/shareyour
system.ouvaton.org/Setter.ipynb)
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


A Setter has a __setitem__ method for setting things in the
<InstanceVariable>.__dict__

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Itemizers.Getter"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass(**{'DoingGetBool':True})
class SetterClass(BaseClass):

        #Definition
        RepresentingKeyStrsList=[
'SettingKeyVariable',
'SettingValueVariable'
                                                                ]

        def default_init(self,
                                                _SettingKeyVariable=None,
                                                _SettingValueVariable=None,
                                                **_KwargVariablesDict
                                        ):
                """ """

                #Call the parent init method
                BaseClass.__init__(self,**_KwargVariablesDict)

        #@Argumenter.ArgumenterClass(**{'ArgumentingDoStr':'Set'})
        def __setitem__(self,_KeyVariable,_ValueVariable):
                """ """

                #debug
                '''
                self.debug(
                                        [
                                                ('locals()[\'',locals(),[
'_KeyVariable',
'_ValueVariable']
,'\']'),
                                                ('self.',self,[
'SettingKeyVariable',
#'SettingValueVariable'
                                                                        ])
                                        ])
                '''

                #set (and set before argument to facilitate switch triggers (see
later...)
                self.SettingKeyVariable=_KeyVariable
                self.SettingValueVariable=_ValueVariable
                self.set()

                #set
                return self

        def do_set(self):
                """ """

                #debug
                '''
self.debug(("self.",self,['SettingKeyVariable','SettingValueVariable']))
                '''

                #__setitem__ in the __dict__, this is an utility set
                self.__dict__[self.SettingKeyVariable]=self.SettingValueVariable

                #Return
                return {'HookingIsBool':False}

#</DefineClass>

```

<small>
View the Setter sources on <a href="https://github.com/Ledoux/ShareYourSystem/tr
ee/master/Pythonlogy/ShareYourSystem/Itemizers/Setter"
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
from ShareYourSystem.Standards.Itemizers import Setter

#Definition a Setter and set with the __setitem__
MySetter=Setter.SetterClass().__setitem__('MyInt',0)

#Definition the AttestedStr
SYS._attest(
    [
    'MySetter is '+SYS._str(
            MySetter,
            **{
            'RepresentingBaseKeyStrsListBool':False,
            'RepresentingAlineaIsBool':False
            }
        )
    ]
)

#Print



```


```console
>>>


*****Start of the Attest *****

MySetter is < (SetterClass), 4540815888>
   /{
   /  '<New><Instance>IdInt' : 4540815888
   /  '<New><Instance>MyInt' : 0
   /  '<Spe><Instance>SettingKeyVariable' : MyInt
   /  '<Spe><Instance>SettingValueVariable' : 0
   /}

*****End of the Attest *****



```

