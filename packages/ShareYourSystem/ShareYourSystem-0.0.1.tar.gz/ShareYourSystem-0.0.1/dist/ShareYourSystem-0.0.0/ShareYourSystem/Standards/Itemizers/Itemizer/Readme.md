

<!--
FrozenIsBool False
-->

#Itemizer

##Doc
----


>
> An Itemizer...
>
>

----

<small>
View the Itemizer notebook on [NbViewer](http://nbviewer.ipython.org/url/shareyo
ursystem.ouvaton.org/Itemizer.ipynb)
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


An Itemizer...

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Interfacers.Hdformater"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
#</ImportSpecificModules>

#<DefineLocals>
ItemizingPrefixStr="Item_"
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class ItemizerClass(BaseClass):

        pass

        """
        #Definition
        RepresentingKeyStrsList=[
'ItemizingKeyVariable',
'ItemizedKeyVariable'
                                                                ]

        #@SYS.HookerClass(**{'HookingAfterVariablesList':[{'CallingVariable':Bas
eClass.init}]})
        def default_init(self,
                                                _ItemizingKeyVariable=None,
                                                _ItemizedKeyVariable=None,
                                                **_KwargVariablesDict
                                        ):
                """ """

                #Call the parent init method
                BaseClass.__init__(self,**_KwargVariablesDict)

        def do_itemize(self):

                #Check
                if self.ItemizingKeyVariable.startswith(ItemizingPrefixStr):

                        #split
                        self.ItemizedKeyVariable=ItemizingPrefixStr.join(
                                self.ItemizingKeyVariable.split(
                                ItemizingPrefixStr)[1:]
                        )

                        #debug
                        self.debug(
                                                [
                                                        'go to a getitem get',
('self.',self,['ItemizingKeyVariable','ItemizedKeyVariable'])
                                                ]
                                        )

                        #return __getitem__
                        return self.__getitem__(self.ItemizedKeyVariable)

                else:

                        #debug
                        self.debug(
                                                [
                                                        'classic object
getattr...',
('self.',self,['ItemizingKeyVariable'])
                                                ]
                                        )

                        #Return default getattr
                        return
object.__getattribute__(self,self.ItemizingKeyVariable)

        def __getattribute__(self,_KeyVariable):

                #Itemize
                return self.itemize(_KeyVariable)
        """

#</DefineClass>



```

<small>
View the Itemizer sources on <a href="https://github.com/Ledoux/ShareYourSystem/
tree/master/Pythonlogy/ShareYourSystem/Itemizers/Itemizer"
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
from ShareYourSystem.Standards.Itemizers import Itemizer

class MakerClass(Itemizer.ItemizerClass):

    def __getitem__(self,_KeyVariable):

        #Debug
        print('_KeyVariable is ',_KeyVariable)
        print('')

        #return
        return object.__getattribute__(self,
                        'My'+str(_KeyVariable)+'Int'
                    )

#Definition of a derive maker itemizer class
MyMaker=MakerClass()
MyMaker.My1Int=1

#Definition the AttestedStr
SYS._attest(
    [
        'MyMaker is'+SYS._str(
            MyMaker,
            **{
                'RepresentingAlineaIsBool':False,
            }
        ),
        'MyMaker[1] is '+str(MyMaker[1]),
        #'MyMaker.Item_1 is '+str(MyMaker.Item_1),
    ]
)

#Print



```


```console
>>>
('_KeyVariable is ', 1)



*****Start of the Attest *****

MyMaker is< (MakerClass), 4540815632>
   /{
   /  '<New><Instance>IdInt' : 4540815632
   /  '<New><Instance>My1Int' : 1
   /}

------

MyMaker[1] is 1

*****End of the Attest *****



```

