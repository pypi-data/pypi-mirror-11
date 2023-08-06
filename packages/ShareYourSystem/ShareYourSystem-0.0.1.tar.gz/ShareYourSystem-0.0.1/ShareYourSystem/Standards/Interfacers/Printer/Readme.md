

<!--
FrozenIsBool False
-->

#Printer

##Doc
----


>
> The Printer is an object that can directly print
> Strs in the Representer context.
>
>

----

<small>
View the Printer notebook on [NbViewer](http://nbviewer.ipython.org/url/shareyou
rsystem.ouvaton.org/Printer.ipynb)
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


The Printer is an object that can directly print
Strs in the Representer context.

"""


#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Objects.Initiator"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Representer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
Representer=DecorationModule
#</ImportSpecificModules>


#<DefineClass>
@DecorationClass()
class PrinterClass(BaseClass):

        #Definition
        RepresentingKeyStrsList=[
'PrintingCopyVariable'
                                                                ]

        def default_init(self,
                                                _PrintingCopyVariable=None,
                                                **_KwargVariablesDict
                                        ):

                #Call the parent init method
                BaseClass.__init__(self,**_KwargVariablesDict)

        #<DefineDoMethod>
        def do__print(self,**_KwargVariablesDict):

                #debug
                '''
                print('self.PrintingCopyVariable is ',self.PrintingCopyVariable)
                print('')
                '''

                #print
                print(
                        Representer.getRepresentedStrWithVariable(
                                self.PrintingCopyVariable,
                                **_KwargVariablesDict
                                )
                )

#</DefineClass>


```

<small>
View the Printer sources on <a href="https://github.com/Ledoux/ShareYourSystem/t
ree/master/Pythonlogy/ShareYourSystem/Objects/Printer"
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
from ShareYourSystem.Standards.Interfacers import Printer

#Definition of an instance Printer and make it print hello
MyPrinter=Printer.PrinterClass()._print('hello')

#Definition the AttestedStr
SYS._attest(
    [
        'MyPrinter is '+SYS._str(MyPrinter)
    ]
)

#Print



```


```console
>>>
hello


*****Start of the Attest *****

MyPrinter is < (PrinterClass), 4536927888>
   /{
   /  '<New><Instance>IdInt' : 4536927888
   /  '<Spe><Instance>PrintingCopyVariable' : hello
   /}

*****End of the Attest *****



```

