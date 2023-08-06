
#Pather
 @Date : Fri Nov 14 13:20:38 2014

@Author : Erwan Ledoux



A Pather use its __setitem__ method for setting attributes in deeper levels
thanks to the PathPrefixStr





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
from ShareYourSystem.Standards.Objects import Pather

#Explicit expression
MyPather=Pather.PatherClass().__setitem__('MyStr','I am the parent')

#set with a deep short Str
MyPather.__setitem__('ChildPather',Pather.PatherClass()).__setitem__('/ChildPath
er/MyStr','I am the child')

#set with a deep deep short Str
MyPather.__setitem__('/ChildPather/GrandChildPather',Pather.PatherClass())

#Definition the AttestedStr
SYS._attest(
                    [
                        'MyPather is '+str(
                            Representer.represent(
                                MyPather,
                                **{
                                'RepresentingBaseKeyStrsListBool':False
                                }
                            )
                        )
                    ]
                )

#Print



```


```console
>>>


*****Start of the Attest *****

MyPather is < (PatherClass), 4507430032>
   /{
   /  '<New><Instance>ChildPather' : < (PatherClass), 4507614608>
   /   /{
   /   /  '<New><Instance>GrandChildPather' : < (PatherClass), 4507614736>
   /   /   /{
   /   /   /  '<Spe><Class>PathedKeyStrsList' : []
   /   /   /  '<Spe><Class>PathingKeyStr' :
   /   /   /}
   /   /  '<New><Instance>MyStr' : I am the child
   /   /  '<Spe><Instance>PathedKeyStrsList' : ['GrandChildPather']
   /   /  '<Spe><Instance>PathingKeyStr' : /GrandChildPather
   /   /}
   /  '<New><Instance>MyStr' : I am the parent
   /  '<Spe><Instance>PathedKeyStrsList' : ['ChildPather',
'GrandChildPather']
   /  '<Spe><Instance>PathingKeyStr' : /ChildPather/GrandChildPather
   /}

*****End of the Attest *****




```



<!--
FrozenIsBool False
-->

##More Descriptions at the level of the class

Special attributes of the PatherClass are :


```python



#ImportModules
import ShareYourSystem as SYS
from ShareYourSystem.Standards.Objects import Pather

#Definition the AttestedStr
SYS._attest(
    [
        'DefaultAttributeItemTuplesList is '+SYS._str(
            Pather.PatherClass.DefaultAttributeItemTuplesList,
            **{'RepresentingAlineaIsBool':False}
        )
    ]
)

#Print



```


```console
>>>


*****Start of the Attest *****

DefaultAttributeItemTuplesList is
   /[
   /  0 : ('PathingKeyStr', '')
   /  1 :
   /   /(
   /   /  0 : PathedKeyStrsList
   /   /  1 : []
   /   /)
   /  2 : ('PathedKeyStr', '')
   /  3 : ('PathedChildKeyStr', '')
   /  4 : ('PathedValueVariable', None)
   /]

*****End of the Attest *****




```



<!--
FrozenIsBool False
-->

##More Descriptions at the level of the instances

A default call of an instance gives :


```python



#ImportModules
from ShareYourSystem.Standards.Classors import Attester
from ShareYourSystem.Standards.Objects import Pather

#Definition the AttestedStr
SYS._attest(
    [
        Pather.PatherClass()
    ]
)

#Print




```


```console
>>>


*****Start of the Attest *****

< (PatherClass), 4582767760>
   /{
   /  '<Spe><Class>PathedKeyStrsList' : []
   /  '<Spe><Class>PathingKeyStr' :
   /}

*****End of the Attest *****




```

