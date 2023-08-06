

<!---
FrozenIsBool True
-->

##Example

Let's create an empty class, which will automatically receive special attributes
from the decorating ClassorClass specially the NameStr, that should be the
ClassStr without the TypeStr in the end.

```python
#ImportModules
import ShareYourSystem as SYS
import json

#Definition a FooClass decorated by the ClassorClass
@SYS.ClassorClass()
class FooClass(object):
    pass

#print
print('FooClass.__dict__ is ')
print(
    json.dumps(
        dict(
            zip(
                FooClass.__dict__.keys(),
                map(
                    str,
                    FooClass.__dict__.values()
                )
            )
        ),
        indent=2
    )
)

```


```console
>>>
FooClass.__dict__ is
{
  "ConceptModuleStr": "",
  "__module__": "__builtin__",
  "getClass": "<function getClass at 0x109338500>",
  "DeriveClassor": "<ShareYourSystem.Standards.Classors.Classor.ClassorClass
object at 0x10bf58050>",
  "SelfClass": "<class 'FooClass'>",
  "MroClassesDict": "{'FooClass': <class 'FooClass'>, 'object': <type
'object'>}",
  "MroClassesList": "(<class 'FooClass'>, <type 'object'>)",
  "Module": "<module '__builtin__' (built-in)>",
  "__doc__": "None",
  "InspectMethodDict": "MethodDict([('callAllMro', <unbound method
FooClass.callAllMro>), ('getClass', <unbound method FooClass.getClass>)])",
  "KeyStrsList": "['ConceptModuleStr', 'DeriveClassor', 'SelfClass',
'MroClassesDict', 'MroClassesList', 'Module', 'InspectMethodDict', 'NameStr',
'InspectInspectDict', 'KeyStrsList']",
  "__dict__": "<attribute '__dict__' of 'FooClass' objects>",
  "NameStr": "Foo",
  "InspectInspectDict": "{'getClass': InspectDict([('DefaultIndexInt', 1),
('InputKeyStrsList', ['_InstanceVariable', '_ClassVariable']),
('LiargVariablesListKeyStr', ''), ('KwargVariablesSetTagStr', ''),
('DefaultOrderedDict', OrderedDict([('_ClassVariable', None)])),
('FunctionNameStr', 'getClass')]), 'callAllMro':
InspectDict([('DefaultIndexInt', 2), ('InputKeyStrsList', ['_InstanceVariable',
'_MethodStr']), ('LiargVariablesListKeyStr', '_LiargVariablesList'),
('KwargVariablesSetTagStr', '_KwargVariablesDict'), ('DefaultOrderedDict',
OrderedDict()), ('FunctionNameStr', 'callAllMro')])}",
  "__weakref__": "<attribute '__weakref__' of 'FooClass' objects>",
  "callAllMro": "<function callAllMro at 0x109338578>"
}

```



<!--
FrozenIsBool False
-->

Classor gives information to the base classes that derive classes exists


```python

#ImportModules
import ShareYourSystem as SYS

#Definition of a MakerClass decorated by a DoerClass instance
@SYS.ClassorClass()
class MakerClass(object):
    pass

#Definition of a derived BuilderClass decorated by a Deriver
@SYS.ClassorClass()
class BuilderClass(MakerClass):
    pass

#Print
#print('MakerClass.DerivedClassesList is '+str(MakerClass.DerivedClassesList))

#Definition the AttestedStr
print('MakerClass.DeriveClassesList is '+str(MakerClass.DeriveClassesList))



```


```console
>>>
MakerClass.DeriveClassesList is [<class 'BuilderClass'>]

```



<!---
FrozenIsBool True
-->

We can inspect a classor decorated class

```python
#ImportModules
import ShareYourSystem as SYS

#define
@SYS.ClassorClass()
class MakerClass(object):

    def default_init(self,
            _MakingMyStr,
            _MakingMyInt=0,
            **_KwargVariablesDict
        ):
        object.__init__(self,**_KwargVariablesDict)

    def do_make(self):

        #str
        self.MadeMyStr=str(self.MakingMyStr)

#print
print('MakerClass.InspectInspectDict is ')
print(SYS.indent(
        MakerClass.InspectInspectDict
    )
)




```


```console
>>>
MakerClass.InspectInspectDict is
{
  "default_init": "InspectDict([('DefaultIndexInt', 2), ('InputKeyStrsList',
['self', '_MakingMyStr', '_MakingMyInt']), ('LiargVariablesListKeyStr', ''),
('KwargVariablesSetTagStr', '_KwargVariablesDict'), ('DefaultOrderedDict',
OrderedDict([('_MakingMyInt', 0)])), ('FunctionNameStr', 'default_init')])",
  "getClass": "InspectDict([('DefaultIndexInt', 1), ('InputKeyStrsList',
['_InstanceVariable', '_ClassVariable']), ('LiargVariablesListKeyStr', ''),
('KwargVariablesSetTagStr', ''), ('DefaultOrderedDict',
OrderedDict([('_ClassVariable', None)])), ('FunctionNameStr', 'getClass')])",
  "callAllMro": "InspectDict([('DefaultIndexInt', 2), ('InputKeyStrsList',
['_InstanceVariable', '_MethodStr']), ('LiargVariablesListKeyStr',
'_LiargVariablesList'), ('KwargVariablesSetTagStr', '_KwargVariablesDict'),
('DefaultOrderedDict', OrderedDict()), ('FunctionNameStr', 'callAllMro')])",
  "do_make": "InspectDict([('DefaultIndexInt', 1), ('InputKeyStrsList',
['self']), ('LiargVariablesListKeyStr', ''), ('KwargVariablesSetTagStr', ''),
('DefaultOrderedDict', OrderedDict()), ('FunctionNameStr', 'do_make')])"
}

```

