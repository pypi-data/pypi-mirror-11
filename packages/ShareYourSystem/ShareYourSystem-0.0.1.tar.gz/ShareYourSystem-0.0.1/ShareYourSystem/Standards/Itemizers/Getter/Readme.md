

<!--
FrozenIsBool False
-->

#Getter

##Doc
----


>
> A Getter helps for getting attributes safely in
> an instance. Through the __getitem__ method, It looks first in the
\_\_dict\_\_ to
> check if there is the corresponding GettingKeyStr.
>
>

----

<small>
View the Getter notebook on [NbViewer](http://nbviewer.ipython.org/url/shareyour
system.ouvaton.org/Getter.ipynb)
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


A Getter helps for getting attributes safely in
an instance. Through the __getitem__ method, It looks first in the \_\_dict\_\_
to
check if there is the corresponding GettingKeyStr.

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Itemizers.Itemizer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
from ShareYourSystem.Functers import Argumenter
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass(**{'DoingGetBool':True})
class GetterClass(BaseClass):

        #Definition
        RepresentingKeyStrsList=[
'GettingKeyVariable',
'GettedValueVariable'
                                                                ]

        #@SYS.HookerClass(**{'HookingAfterVariablesList':[{'CallingVariable':Bas
eClass.init}]})
        def default_init(self,
                                                _GettingKeyVariable=None,
                                                _GettedValueVariable=None,
                                                **_KwargVariablesDict
                                        ):
                """ """

                #Call the parent init method
                BaseClass.__init__(self,**_KwargVariablesDict)

        #@Argumenter.ArgumenterClass(**{'ArgumentingDoStr':'Get'})
        def __getitem__(self,_KeyVariable):
                """ """

                #Debug
                '''
                print('l.53 __getitem__ Getter')
                print('self.get is ',self.get.im_func)
                print('_KeyVariables is ',_KeyVariable)
                print('')
                '''

                #get
                self.get(_KeyVariable)

                #Debug
                '''
                self.debug(('self.',self,['GettedValueVariable']))
                '''

                #return
                return self.GettedValueVariable

        def do_get(self):
                """ """

                #debug
                '''
                self.debug(("self.",self,['GettingKeyVariable']))
                '''

                #Check
                if type(self.GettingKeyVariable) in [str,unicode]:

                        #Get safely the Value
                        if self.GettingKeyVariable in self.__dict__:

                                #__getitem__ in the __dict__
self.GettedValueVariable=self.__dict__[self.GettingKeyVariable]

                                #debug
                                '''
                                self.debug(
                                                        [
                                                                'This is a Spe
in Instance',
('self.',self,['GettedValueVariable'])
                                                        ]
                                                )
                                '''

                                #Stop the getting
                                return {"HookingIsBool":False}

                        elif self.GettingKeyVariable in self.__class__.__dict__:

                                #__getitem__ in the __class__
self.GettedValueVariable=self.__class__.__dict__[self.GettingKeyVariable]

                                #debug
                                '''
                                self.debug(
                                                        [
                                                                'This is in the
__class__',
('self.',self,['GettedValueVariable'])
                                                        ]
                                                )
                                '''

                                #Stop the getting
                                return {"HookingIsBool":False}

                #set
                self.GettedValueVariable=None

                #debug
                '''
                self.debug(
                                        [
                                                'Not found here so set it to
None',
('self.',self,['GettedValueVariable'])
                                        ]
                                )
                '''
                #Return an output dict
                return {"HookingIsBool":True}

#</DefineClass>



```

<small>
View the Getter sources on <a href="https://github.com/Ledoux/ShareYourSystem/tr
ee/master/Pythonlogy/ShareYourSystem/Itemizers/Getter"
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
from ShareYourSystem.Standards.Itemizers import Getter

#Definition a Getter
MyGetter=Getter.GetterClass()
MyGetter.MyInt=1

#Definition the AttestedStr
SYS._attest(
    [
        'Get the MyInt returns '+str(MyGetter['MyInt']),
        'Get the MyStr returns '+str(MyGetter['MyStr'])
    ]
)

#Print



```


```console
>>>


*****Start of the Attest *****

Get the MyInt returns 1

------

Get the MyStr returns None

*****End of the Attest *****



```

