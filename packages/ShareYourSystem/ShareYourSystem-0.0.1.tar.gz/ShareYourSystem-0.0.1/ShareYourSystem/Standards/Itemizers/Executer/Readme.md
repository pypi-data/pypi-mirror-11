

<!--
FrozenIsBool False
-->

#Executer

##Doc
----


>
> An Executer can exec commands with the six.exec_ function
>

----

<small>
View the Executer notebook on [NbViewer](http://nbviewer.ipython.org/url/shareyo
ursystem.ouvaton.org/Executer.ipynb)
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


An Executer can exec commands with the six.exec_ function
"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Itemizers.Sharer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import six
#</ImportSpecificModules>

#<DefineLocals>
ExecutionPrefixStr="Exec_"
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class ExecuterClass(BaseClass):

        #Definition
        RepresentingKeyStrsList=[
'ExecutionPrefixStr'
                                                                ]

        def default_init(self,
                                _ExecutionPrefixStr="" ,
                                **_KwargVariablesDict):

                #Call the parent __init__ method
                BaseClass.__init__(self,**_KwargVariablesDict)

#<Hook>@Hooker.HookerClass(**{'HookingBeforeCallingDictsList':[BaseClass.get]})
        #@Imitater.ImitaterClass()
        def mimic_get(self):

                #Check
                if self.GettingKeyVariable.startswith(ExecutionPrefixStr):

                        #Definition the ExecStr
                        self.ExecutionPrefixStr=ExecutionPrefixStr.join(
self.GettingKeyVariable.split(ExecutionPrefixStr)[1:])

                        #debug
                        '''
                        self.debug(('self.',self,['ExecutionPrefixStr']))
                        '''

                        #Put the output in a local Local Variable
                        self.execute()

                #debug
                '''
                self.debug('BaseClass.get is '+str(BaseClass.get))
                '''

                #Call the parent get method
                return BaseClass.get(self)

#<Hook>@Hooker.HookerClass(**{'HookingBeforeCallingDictsList':[BaseClass.set]})
        #@Imitater.ImitaterClass()
        def mimic_set(self):

                #Check
                if type(self.SettingValueVariable
                        ) in SYS.StrTypesList and
self.SettingValueVariable.startswith(
                        ExecutionPrefixStr):

                        #Definition the ExecStr
                        self.ExecutionPrefixStr=ExecutionPrefixStr.join(
self.SettingValueVariable.split(ExecutionPrefixStr)[1:])

                        #debug
                        '''
self.debug(('self.',self,['ExecutionPrefixStr',"SettingValueVariable"]))
                        '''

                        #Put the output in a local Local Variable
                        self.execute()

                        #debug
                        '''
self.debug(('self.',self,['ExecutionPrefixStr',"SettingValueVariable"]))
                        '''

                #Call the parent get method
                BaseClass.set(self)


        def do_execute(self):

                #Execute
                six.exec_(self.ExecutionPrefixStr,locals())

                #Return self
                #return self

#</DefineClass>

```

<small>
View the Executer sources on <a href="https://github.com/Ledoux/ShareYourSystem/
tree/master/Pythonlogy/ShareYourSystem/Itemizers/Executer"
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
from ShareYourSystem.Standards.Itemizers import Executer

#Definition and update with an exec Str
MyExecuter=Executer.ExecuterClass()

MySecondInt=MyExecuter.__setitem__(
    'MySecondInt',
    'Exec_self.SettingValueVariable=1+1'
).MySecondInt

#Exec is also possible in a getting
GettedValueVariable=MyExecuter['Exec_self.GettedValueVariable=self.MySecondInt-1
']

#Definition the AttestedStr
SYS._attest(
    [
        'MySecondInt is  '+str(MySecondInt),
        'GettedValueVariable is '+str(GettedValueVariable)
    ]
)

#Print



```


```console
>>>


*****Start of the Attest *****

MySecondInt is  2

------

GettedValueVariable is None

*****End of the Attest *****



```

