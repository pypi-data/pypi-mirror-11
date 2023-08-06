

<!--
FrozenIsBool False
-->

#Capturer

##Doc
----


>
> The Capturer
>
>

----

<small>
View the Capturer notebook on [NbViewer](http://nbviewer.ipython.org/url/shareyo
ursystem.ouvaton.org/Capturer.ipynb)
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


The Capturer

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Interfacers.Hdformater"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
from cStringIO import StringIO
import sys
import copy
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class CapturerClass(BaseClass):

        #Definition
        RepresentingKeyStrsList=[
'CapturingStopBool',
'CapturedStdoutVariable',
'CapturedPrintStrsList'
                                                        ]

        def default_init(self,
                                                _CapturingStopBool={
'DefaultValueType':property,
'PropertyInitVariable':False,
'PropertyDocStr':''
                                                },
_CapturedStdoutVariable=sys.stdout,
                                                _CapturedPrintStrsList=None,
                                                **_KwargVariablesDict
                                        ):

                #Call the parent __init__ method
                BaseClass.__init__(self,**_KwargVariablesDict)

        def setCapturingStopBool(self,_SettingValueVariable):

                #set
                self._CapturingStopBool=_SettingValueVariable

                #reset the CapturedStrsList
                if _SettingValueVariable:

                        #Check
                        if self.CapturedPrintStrsList!=None:

                                if hasattr(sys.stdout,'getvalue'):

                                        #extend
                                        self.CapturedPrintStrsList.extend(
sys.stdout.getvalue().splitlines()
                                        )

                        #reset
                sys.stdout = self.CapturedStdoutVariable

        def do_capture(self):

                #debug
                '''
                self.debug('We capture here ')
                '''

                #set
                self.CapturedStdoutVariable = sys.stdout

                #init
                sys.stdout = StringIO()

                #Return self
                #return self

#</DefineClass>

```

<small>
View the Capturer sources on <a href="https://github.com/Ledoux/ShareYourSystem/
tree/master/Pythonlogy/ShareYourSystem/Interfacers/Capturer"
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
from ShareYourSystem.Standards.Interfacers import Capturer

#Definition a Capturer
MyCapturer=Capturer.CapturerClass().capture()
print('Hello !')
print('Bonjour !')
MyCapturer.CapturingStopBool=True
print('Y a quelqu un?')

#Definition the AttestedStr
SYS._attest(
    [
        'MyCapturer is '+SYS._str(
        MyCapturer,
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
Y a quelqu un?


*****Start of the Attest *****

MyCapturer is < (CapturerClass), 4551821200>
   /{
   /  '<New><Instance>IdInt' : 4551821200
   /  '<New><Instance>_CapturingStopBool' : True
   /  '<Spe><Class>CapturingStopBool' : True
   /  '<Spe><Instance>CapturedPrintStrsList' : ['Hello !', 'Bonjour !']
   /  '<Spe><Instance>CapturedStdoutVariable' : <cStringIO.StringO object at
0x10f4f79d0>
   /}

*****End of the Attest *****



```

