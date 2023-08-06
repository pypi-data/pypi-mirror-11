

<!---
FrozenIsBool True
-->

##Example

We define here a MakerClass with some making and made attributes. Here is the
difference for a default instance
DefaultMaker that takes its values from the MakerClass.__dict__ and a special
one that sets in its __dict__

```python
#ImportModules
import ShareYourSystem as SYS

#Definition a FooClass decorated by the DefaultorClass
@SYS.DefaultorClass()
class FooClass(object):

    def default_init(self,
                        Int,
                        _MyFloat=1.,
                        _MyInt={
                                    'DefaultValueType':int
                                }
                ):
        #call the base method
        object.__init__(self)

        #Definition an attribute
        self.MyStr='I am a Foo with MyFloat equal to '+str(self.MyFloat)+' and
Int equal to '+str(Int)


#print
print("\n".join(
        [
        'FooClass.__init__ is '+str(FooClass.__init__),
        'FooClass has some special attributes',
        #'FooClass.InitInspectDict is '+SYS._str(FooClass.InitInspectDict),
        'FooClass.DefaultAttributeVariablesOrderedDict is '+SYS.indent(
            FooClass.DefaultAttributeVariablesOrderedDict),
        'FooClass.MyFloat is '+str(FooClass.MyFloat),
        'FooClass.MyInt is '+str(FooClass.MyInt),
        ]
    )
)

#Definition a default instance that will take its values from the default
classed attributes
DefaultFoo=FooClass(3)

#print
print("\n"+"\n".join(
    [
        'What are you saying DefaultFoo ?',
        'DefaultFoo.__dict__ is '+str(DefaultFoo.__dict__),
        'DefaultFoo.MyFloat is '+str(DefaultFoo.MyFloat),
        'DefaultFoo.MyInt is '+str(DefaultFoo.MyInt)
    ]
))

#Definition a special instance that sets in its __dict__
SpecialFoo=FooClass(
            3,
            **{'MyInt':5}
        )

#print
print("\n"+"\n".join(
    [
        'What are you saying SpecialFoo ?',
        'SpecialFoo.__dict__ is '+str(SpecialFoo.__dict__),
        'SpecialFoo.MyFloat is '+str(SpecialFoo.MyFloat),
        'SpecialFoo.MyInt is '+str(SpecialFoo.MyInt)
    ]
    )
)

#Change a classed attribute
FooClass.MyFloat=7.

#Add
print("\n"+"\n".join(
        [
        'After reset at the level of the class',
        'DefaultFoo.MyFloat is '+str(DefaultFoo.MyFloat),
        'SpecialFoo.MyFloat is '+str(SpecialFoo.MyFloat),
        ]
    )
)




```


```console
>>>
FooClass.__init__ is <unbound method FooClass.superDefault_init>
FooClass has some special attributes
FooClass.DefaultAttributeVariablesOrderedDict is {
  "MyInt": "0",
  "MyFloat": "1.0"
}
FooClass.MyFloat is 1.0
FooClass.MyInt is 0

What are you saying DefaultFoo ?
DefaultFoo.__dict__ is {'MyStr': 'I am a Foo with MyFloat equal to 1.0 and Int
equal to 3', 'DefaultInitBool': True}
DefaultFoo.MyFloat is 1.0
DefaultFoo.MyInt is 0

What are you saying SpecialFoo ?
SpecialFoo.__dict__ is {'MyStr': 'I am a Foo with MyFloat equal to 1.0 and Int
equal to 3', 'MyInt': 5, 'DefaultInitBool': True}
SpecialFoo.MyFloat is 1.0
SpecialFoo.MyInt is 5

After reset at the level of the class
DefaultFoo.MyFloat is 7.0
SpecialFoo.MyFloat is 7.0

```



<!---
FrozenIsBool True
-->

##Example

Particular case of the definition of mutable variables in the init method.
If you decide to initialize a mutable variable like a list with a
default empty value, this is rather to make it shared to all the instances.
On the other hand, if you want to declare a list that has to be unique for each
instance,
then set it to the default value None.

```python
#ImportModules
import ShareYourSystem as SYS
import numpy as np

#Definition a FooClass decorated by the DefaultorClass
@SYS.DefaultorClass()
class FooClass(object):

    def default_init(self,
                        _MyFirstList=[],
                        _MyArray=None,
                        _MySecondList=None,
                ):
        object.__init__(self)

#print
print("\n".join([
        'FooClass has some special attributes',
        #'FooClass.InitInspectDict is '+SYS._str(FooClass.InitInspectDict),
        'FooClass.DefaultAttributeVariablesOrderedDict is '+str(
            FooClass.DefaultAttributeVariablesOrderedDict),
        'FooClass.MyFirstList is '+str(FooClass.MyFirstList),
        'FooClass.MySecondList is '+str(FooClass.MySecondList),
        ]
    )
)

#Definition a default instance that will take its values from the default
classed attributes
DefaultFoo=FooClass()

#But it can touch at the mutable values defined in the class
DefaultFoo.MyFirstList.append('hello')

#Note: if you write DefaultFoo.MyFirstList=['hello'],
#then it will set it as a new list in the __dict__ of the DefaultFoo.

#print
print("\n"+"\n".join([
        'What are you saying DefaultFoo ?',
        'DefaultFoo.__dict__ is '+str(DefaultFoo.__dict__),
        'DefaultFoo.MyFirstList is '+str(DefaultFoo.MyFirstList),
        'DefaultFoo.MySecondList is '+str(DefaultFoo.MySecondList),
    ]
    )
)

#Definition a special instance that sets in its __dict__
SpecialFoo=FooClass(
            _MyArray=np.array([4]),
            _MySecondList=['bonjour'],
            **{'MyInt':3}
            )

#print
print("\n"+"\n".join([
        'What are you saying SpecialFoo ?',
        'SpecialFoo.__dict__ is '+str(SpecialFoo.__dict__),
        'SpecialFoo.MyFirstList is '+str(SpecialFoo.MyFirstList),
        'SpecialFoo.MySecondList is '+str(SpecialFoo.MySecondList),
        ]
    )
)




```


```console
>>>
FooClass has some special attributes
FooClass.DefaultAttributeVariablesOrderedDict is OrderedDict([('MyFirstList',
[]), ('MyArray', None), ('MySecondList', None)])
FooClass.MyFirstList is []
FooClass.MySecondList is None

What are you saying DefaultFoo ?
DefaultFoo.__dict__ is {'DefaultInitBool': True}
DefaultFoo.MyFirstList is ['hello']
DefaultFoo.MySecondList is None

What are you saying SpecialFoo ?
SpecialFoo.__dict__ is {'MySecondList': ['bonjour'], 'DefaultInitBool': True,
'MyArray': array([4])}
SpecialFoo.MyFirstList is ['hello']
SpecialFoo.MySecondList is ['bonjour']

```



<!---
FrozenIsBool True
-->

##Example

Defaultor can thus also share Objects if they are initiated at the level of the
class.

```python
#ImportModules
import ShareYourSystem as SYS

#Definition a FooClass decorated by the DefaultorClass
@SYS.DefaultorClass()
class FooClass(object):

    def default_init(self,
                        _ShareClassor=SYS.ClassorClass(),
                        _SpecificClassor=None
                ):
        object.__init__(self)

#Definition
FooClass.ShareClassor.MyInt=2
MyFirstFoo=FooClass()
MySecondFoo=FooClass()

#Definition the AttestedStr
print("\n".join(
    [
        'MyFirstFoo.ShareClassor.__dict__ is ',SYS.indent(
            MyFirstFoo.ShareClassor.__dict__),
        'MyFirstFoo.__dict__ is '+SYS.indent(MyFirstFoo.__dict__),
        'MyFirstFoo.SpecificClassor is '+str(MyFirstFoo.SpecificClassor)
    ]
    )
)




```


```console
>>>
MyFirstFoo.ShareClassor.__dict__ is
{
  "MyInt": "2"
}
MyFirstFoo.__dict__ is {
  "DefaultInitBool": "True"
}
MyFirstFoo.SpecificClassor is None

```



<!---
FrozenIsBool True
-->

##Example

It is possible to 'reset' an instance with the default value
defined at the level of the class.
Note that the mutable variables that are initiated at the level of the class
keeps
their ongoing value (as MyShareList). Also note that there is a
setDefaultMutable that
init all the mutables variables in the instance, if wanted.


```python
#ImportModules
import ShareYourSystem as SYS

#Definition a FooClass decorated by the DefaultorClass
@SYS.DefaultorClass()
class FooClass(object):

    def default_init(self,
                        _MyFloat=1.,
                        _MyShareList=[],
                        _MyFirstSpecificList=None,
                        _MySecondSpecificList=None,
                        _MyInt={
                                    'DefaultValueType':int
                                }
                ):
        object.__init__(self)

#Definition
MyFoo=FooClass(**{'MyFloat':5.,'MyInt':9})
MyFoo.MyShareList.append(7)
MyFoo.MyFirstSpecificList=['hello']

#Before default
print('Before setDefault MyFoo.__dict__ is')
print(SYS.indent(MyFoo.__dict__))

#default
MyFoo.setDefault(
    #ClassVariable
    #it can be a Class, ClassKeyStr or [Class]
    FooClass,
    #AttributeKeyStrsList
    #it can be just a KeyStr a [<KeyStr>] and if None it is all the KeyStr from
all the Classes
    ['MyFloat','MyFirstSpecificList']
)

#After default
print('\nAfter setDefault MyFoo.__dict__ is')
print(SYS.indent(MyFoo.__dict__))

#default
MyFoo.setDefaultMutable(
    #ClassVariable
    #it can be a Class, ClassKeyStr or [Class]
    FooClass,
    #AttributeKeyStrsList
    #it can be just a KeyStr a [<KeyStr>] and if None it is all the KeyStr from
all the Classes
    ['MyFirstSpecificList']
)

#After default
print('\nAfter setDefaultMutable MyFoo.__dict__ is')
print(SYS.indent(MyFoo.__dict__))

#append to the share list
MyFoo.MyShareList.append(8)

#After default
print('\nAfter setDefault MyFoo.__dict__ is')
print(SYS.indent(MyFoo.__dict__))

#define
print('\nFooClass.DefaultAttributeVariablesOrderedDict is '+SYS.indent(
            FooClass.DefaultAttributeVariablesOrderedDict)
)

#print
print('\nMyFoo.__dict__ is ')
print(SYS.indent(MyFoo.__dict__))





```


```console
>>>
Before setDefault MyFoo.__dict__ is
{
  "DefaultInitBool": "True",
  "MyFirstSpecificList": "['hello']",
  "MyInt": "9",
  "MyFloat": "5.0"
}

After setDefault MyFoo.__dict__ is
{
  "DefaultInitBool": "True",
  "MyFirstSpecificList": "None",
  "MyInt": "9",
  "MyFloat": "1.0"
}

After setDefaultMutable MyFoo.__dict__ is
{
  "DefaultInitBool": "True",
  "MyFirstSpecificList": "[]",
  "MyInt": "9",
  "MyFloat": "1.0"
}

After setDefault MyFoo.__dict__ is
{
  "DefaultInitBool": "True",
  "MyFirstSpecificList": "[]",
  "MyInt": "9",
  "MyFloat": "1.0"
}

FooClass.DefaultAttributeVariablesOrderedDict is {
  "MyInt": "0",
  "MySecondSpecificList": "None",
  "MyFirstSpecificList": "None",
  "MyShareList": "[7, 8]",
  "MyFloat": "1.0"
}

MyFoo.__dict__ is
{
  "DefaultInitBool": "True",
  "MyFirstSpecificList": "[]",
  "MyInt": "9",
  "MyFloat": "1.0"
}

```



<!---
FrozenIsBool True
-->

##Example

And we can reset at the same time several Mro attributes.
Also here we show that there is the option DefaultMutableBool to directly init
the mutables variables.


```python
#ImportModules
import ShareYourSystem as SYS

#Definition a FooClass decorated by the DefaultorClass
@SYS.DefaultorClass()
class FooClass(object):

    def default_init(self,
                        _MyFloat=1.,
                        _MyShareList=[],
                        _MyFirstSpecificList=None,
                        _MySecondSpecificList=None,
                        _MyInt={
                                    'DefaultValueType':int
                                }
                ):
        object.__init__(self)

#Definition a FeeClass decorated by the DefaultorClass
@SYS.DefaultorClass()
class FeeClass(FooClass):

    def default_init(self,
                        _MyBool=True,
                ):
        FooClass.__init__(self)

#put in the SYS scope
SYS.FeeClass=FeeClass

#Definition
MyFee=FeeClass(**{
    'MyFloat':5.,
    'MyInt':9,
    'MyBool':False
})

#Before default
print('Before setDefault MyFee.__dict__ is')
print(SYS.indent(MyFee.__dict__))

#default and also init the mutable variables
MyFee.setDefault(
    #ClassVariable,
    [FooClass,'FeeClass'],
    **{'DefaultMutableBool':True}
)

#print
print('\nMyFee.__dict__ is ')
print(SYS.indent(MyFee.__dict__))





```


```console
>>>
Before setDefault MyFee.__dict__ is
{
  "DefaultInitBool": "True"
}

MyFee.__dict__ is
{
  "MyBool": "True",
  "MySecondSpecificList": "[]",
  "MyFloat": "1.0",
  "MyFirstSpecificList": "[]",
  "MyShareList": "[]",
  "MyInt": "0",
  "DefaultInitBool": "True"
}

```

