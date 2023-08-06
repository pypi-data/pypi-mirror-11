

<!--
FrozenIsBool False
-->

#Propertiser

##Doc
----


>
> The Propertiser is an augmented Defaultor because it will set defaults
attributes
> possibly in properties for the new-style decorated classes. This can set
objects
> with high controlling features thanks to the binding
>
>

----

<small>
View the Propertiser notebook on [NbViewer](http://nbviewer.ipython.org/url/shar
eyoursystem.ouvaton.org/Propertiser.ipynb)
</small>




<!---
FrozenIsBool True
-->

##Example

Let's create a class with one property value.
By default the class has also a _<PropertyKeyStr> value that is the init value.

```python
#ImportModules
import ShareYourSystem as SYS

#Define
@SYS.PropertiserClass()
class MakerClass(SYS.PrinterClass):

    def default_init(self,
            _MakingMyFloat={
                            'DefaultValueType':property,
                            'PropertyInitVariable':3.,
                            'PropertyDocStr':'I am doing the thing here'
                            }
        ):
        SYS.PrinterClass.__init__(self)

#Print and show that the class has already propertize_(get,set,del)MakingMyFloat
# a default _MakingMyFloat value and the MakingMyFloat prop
print('SYS.MakerClass.__dict__ is')
print(SYS.indent(SYS.MakerClass.__dict__))

#Define
MyMaker=SYS.MakerClass()

#print the __dict__, there is no things related to the
#MakingMyFloat property
print('MyMaker.__dict__ before set is ')
SYS._print(MyMaker.__dict__)

#set
MyMaker.MakingMyFloat=7.

#print the __dict__, now there is the hidden attribute
print('MyMaker.__dict__ after set is ')
SYS._print(MyMaker.__dict__)

#Define
MyMaker=SYS.MakerClass()

#print the repr : the instance just show the MakingMyFloat key
#that is actually the get of _MakingMyFloat in the class
print('MyMaker before set is ')
SYS._print(MyMaker)

#set
MyMaker.MakingMyFloat=7.

#print the repr : now the instance shows the _MakingMyFloat
#value that is particulat for the instance
print('MyMaker after set is ')
SYS._print(MyMaker)

```


```console
>>>
SYS.MakerClass.__dict__ is
{
  "__module__": "__builtin__",
  "DoneAttributeVariablesOrderedDict": "OrderedDict()",
  "MakingMyFloat": "<property object at 0x10bf55310>",
  "DoneStr": "Made",
  "DoMakerExecStr": "def superDo_make(_InstanceVariable,_MyFloat=None,*_LiargVar
iablesList,**_KwargVariablesDict):\n\t\n\tif type(_MyFloat)!=None.__class__:\n\t
\t_InstanceVariable.MakingMyFloat=_MyFloat;\n",
  "__init__": "<function superDefault_init at 0x10a9ce758>",
  "DoerStr": "Maker",
  "ConceptModuleStr": "",
  "DeriveClassor":
"<ShareYourSystem.Standards.Classors.Propertiser.PropertiserClass object at
0x10bfc3790>",
  "SelfClass": "<class 'MakerClass'>",
  "default_init": "<function default_init at 0x10bfb6398>",
  "make": "<function superDo_make at 0x10a458410>",
  "DefaultBaseKeyStrsList": "['PrintIdInt', 'PrintStr', 'PrintingCopyVariable',
'PrintingInstanceSkipKeyStrsList', 'PrintingInstanceForceKeyStrsList',
'PrintingClassSkipKeyStrsList', 'PrintingClassForceKeyStrsList',
'PrintingBaseBool', 'PrintingNewInstanceBool', 'PrintingNewClassBool',
'PrintingOutBool', 'PrintingSelfBool', 'PrintingInfoStr',
'PrintingInstanceForceBaseKeyStrsList']",
  "superDefault_init": "<function superDefault_init at 0x10a9ce758>",
  "PropertizedDefaultTuplesList": "[('MakingMyFloat', <property object at
0x10bf55310>)]",
  "DoingAttributeVariablesOrderedDict": "OrderedDict([('MakingMyFloat',
{'PropertyDocStr': 'I am doing the thing here', 'PropertyInitVariable': 3.0,
'DefaultValueType': <type 'property'>})])",
  "KeyStrsList": "['ConceptModuleStr', 'DeriveClassor', 'SelfClass',
'MroClassesDict', 'MroClassesList', 'Module', 'InspectMethodDict', 'NameStr',
'InspectInspectDict', 'KeyStrsList', 'DefaultInitBool',
'DefaultAttributeVariablesOrderedDict', 'InitInspectDict',
'DefaultBaseKeyStrsList', 'DefaultSpecificKeyStrsList', 'MakingMyFloat',
'DoerStr', 'DoStr', 'DoneStr', 'DoingStr', 'DoneAttributeVariablesOrderedDict',
'DoingAttributeVariablesOrderedDict', 'DoingDeprefixAttributeStrsList',
'DoMethodStr', 'DoHistoryOrderedDict', 'DoMakerExecStr', 'DoingGetBool',
'DoTempAttributeItemTuplesList', 'DoTempNotAttributeItemTupleItemsList',
'DoMethodStrsList', 'MroDoerClassesList', 'PropertyMethodsDict',
'PropertizedDefaultTuplesList']",
  "PropertyMethodsDict": "{'propertize_getMakingMyFloat': <function
propertize_getMakingMyFloat at 0x10bf9ce60>, 'propertize_delMakingMyFloat':
<function propertize_delMakingMyFloat at 0x10bf9cc80>,
'propertize_setMakingMyFloat': <function propertize_setMakingMyFloat at
0x10bf9ced8>}",
  "DoStr": "Make",
  "__doc__": "None",
  "DoMethodStrsList": "['interface', '_print', 'make']",
  "propertize_getMakingMyFloat": "<function propertize_getMakingMyFloat at
0x10bf9ce60>",
  "DoingDeprefixAttributeStrsList": "['_MyFloat']",
  "DoingStr": "Making",
  "InitInspectDict": "InspectDict([('DefaultIndexInt', 1), ('InputKeyStrsList',
['self', '_MakingMyFloat']), ('LiargVariablesListKeyStr', ''),
('KwargVariablesSetTagStr', ''), ('DefaultOrderedDict',
OrderedDict([('_MakingMyFloat', {'PropertyDocStr': 'I am doing the thing here',
'PropertyInitVariable': 3.0, 'DefaultValueType': <type 'property'>})])),
('FunctionNameStr', 'default_init')])",
  "InspectInspectDict": "{'getClass': InspectDict([('DefaultIndexInt', 1),
('InputKeyStrsList', ['_InstanceVariable', '_ClassVariable']),
('LiargVariablesListKeyStr', ''), ('KwargVariablesSetTagStr', ''),
('DefaultOrderedDict', OrderedDict([('_ClassVariable', None)])),
('FunctionNameStr', 'getClass')]), 'callDo': InspectDict([('DefaultIndexInt',
1), ('InputKeyStrsList', ['_InstanceVariable']), ('LiargVariablesListKeyStr',
''), ('KwargVariablesSetTagStr', ''), ('DefaultOrderedDict', OrderedDict()),
('FunctionNameStr', 'callDo')]), '_print': InspectDict([('DefaultIndexInt', 1),
('InputKeyStrsList', ['_InstanceVariable', '_CopyVariable',
'_InstanceSkipKeyStrsList', '_InstanceForceKeyStrsList',
'_ClassSkipKeyStrsList', '_ClassForceKeyStrsList', '_BaseBool',
'_NewInstanceBool', '_NewClassBool', '_OutBool', '_SelfBool', '_InfoStr',
'_InstanceForceBaseKeyStrsList']), ('LiargVariablesListKeyStr',
'_LiargVariablesList'), ('KwargVariablesSetTagStr', '_KwargVariablesDict'),
('DefaultOrderedDict', OrderedDict([('_CopyVariable', None),
('_InstanceSkipKeyStrsList', None), ('_InstanceForceKeyStrsList', None),
('_ClassSkipKeyStrsList', None), ('_ClassForceKeyStrsList', None), ('_BaseBool',
None), ('_NewInstanceBool', None), ('_NewClassBool', None), ('_OutBool', None),
('_SelfBool', None), ('_InfoStr', None), ('_InstanceForceBaseKeyStrsList',
None)])), ('FunctionNameStr', 'superDo__print')]), 'forcePrint':
InspectDict([('DefaultIndexInt', 3), ('InputKeyStrsList', ['self',
'_KeyStrsList', '_ClassStr']), ('LiargVariablesListKeyStr', ''),
('KwargVariablesSetTagStr', ''), ('DefaultOrderedDict', OrderedDict()),
('FunctionNameStr', 'forcePrint')]), 'callAllMro':
InspectDict([('DefaultIndexInt', 2), ('InputKeyStrsList', ['_InstanceVariable',
'_MethodStr']), ('LiargVariablesListKeyStr', '_LiargVariablesList'),
('KwargVariablesSetTagStr', '_KwargVariablesDict'), ('DefaultOrderedDict',
OrderedDict()), ('FunctionNameStr', 'callAllMro')]), '__init__':
InspectDict([('DefaultIndexInt', 1), ('InputKeyStrsList',
['_InstanceVariable']), ('LiargVariablesListKeyStr', '_LiargVariablesList'),
('KwargVariablesSetTagStr', '_KwargVariablesDict'), ('DefaultOrderedDict',
OrderedDict()), ('FunctionNameStr', 'superDefault_init')]), 'setDo':
InspectDict([('DefaultIndexInt', 1), ('InputKeyStrsList', ['_InstanceVariable',
'_DoClassVariable']), ('LiargVariablesListKeyStr', ''),
('KwargVariablesSetTagStr', '_KwargVariablesDict'), ('DefaultOrderedDict',
OrderedDict([('_DoClassVariable', None)])), ('FunctionNameStr', 'setDo')]),
'getDoing': InspectDict([('DefaultIndexInt', 1), ('InputKeyStrsList',
['_InstanceVariable', '_DoClassVariable']), ('LiargVariablesListKeyStr', ''),
('KwargVariablesSetTagStr', ''), ('DefaultOrderedDict',
OrderedDict([('_DoClassVariable', None)])), ('FunctionNameStr', 'getDoing')]),
'getReprStr': InspectDict([('DefaultIndexInt', 1), ('InputKeyStrsList',
['self']), ('LiargVariablesListKeyStr', ''), ('KwargVariablesSetTagStr',
'_KwargVariablesDict'), ('DefaultOrderedDict', OrderedDict()),
('FunctionNameStr', 'getReprStr')]), 'make': InspectDict([('DefaultIndexInt',
1), ('InputKeyStrsList', ['_InstanceVariable', '_MyFloat']),
('LiargVariablesListKeyStr', '_LiargVariablesList'), ('KwargVariablesSetTagStr',
'_KwargVariablesDict'), ('DefaultOrderedDict', OrderedDict([('_MyFloat',
None)])), ('FunctionNameStr', 'superDo_make')]), 'superDefault_init':
InspectDict([('DefaultIndexInt', 1), ('InputKeyStrsList',
['_InstanceVariable']), ('LiargVariablesListKeyStr', '_LiargVariablesList'),
('KwargVariablesSetTagStr', '_KwargVariablesDict'), ('DefaultOrderedDict',
OrderedDict()), ('FunctionNameStr', 'superDefault_init')]), 'do__print':
InspectDict([('DefaultIndexInt', 1), ('InputKeyStrsList', ['self']),
('LiargVariablesListKeyStr', ''), ('KwargVariablesSetTagStr',
'_KwargVariablesDict'), ('DefaultOrderedDict', OrderedDict()),
('FunctionNameStr', 'do__print')]), 'superDo__print':
InspectDict([('DefaultIndexInt', 1), ('InputKeyStrsList', ['_InstanceVariable',
'_CopyVariable', '_InstanceSkipKeyStrsList', '_InstanceForceKeyStrsList',
'_ClassSkipKeyStrsList', '_ClassForceKeyStrsList', '_BaseBool',
'_NewInstanceBool', '_NewClassBool', '_OutBool', '_SelfBool', '_InfoStr',
'_InstanceForceBaseKeyStrsList']), ('LiargVariablesListKeyStr',
'_LiargVariablesList'), ('KwargVariablesSetTagStr', '_KwargVariablesDict'),
('DefaultOrderedDict', OrderedDict([('_CopyVariable', None),
('_InstanceSkipKeyStrsList', None), ('_InstanceForceKeyStrsList', None),
('_ClassSkipKeyStrsList', None), ('_ClassForceKeyStrsList', None), ('_BaseBool',
None), ('_NewInstanceBool', None), ('_NewClassBool', None), ('_OutBool', None),
('_SelfBool', None), ('_InfoStr', None), ('_InstanceForceBaseKeyStrsList',
None)])), ('FunctionNameStr', 'superDo__print')]), 'superDo_make':
InspectDict([('DefaultIndexInt', 1), ('InputKeyStrsList', ['_InstanceVariable',
'_MyFloat']), ('LiargVariablesListKeyStr', '_LiargVariablesList'),
('KwargVariablesSetTagStr', '_KwargVariablesDict'), ('DefaultOrderedDict',
OrderedDict([('_MyFloat', None)])), ('FunctionNameStr', 'superDo_make')]),
'getDone': InspectDict([('DefaultIndexInt', 1), ('InputKeyStrsList',
['_InstanceVariable', '_DoClassVariable']), ('LiargVariablesListKeyStr', ''),
('KwargVariablesSetTagStr', ''), ('DefaultOrderedDict',
OrderedDict([('_DoClassVariable', None)])), ('FunctionNameStr', 'getDone')]),
'setDefault': InspectDict([('DefaultIndexInt', 2), ('InputKeyStrsList',
['_InstanceVariable', '_ClassVariable', '_AttributeKeyVariable']),
('LiargVariablesListKeyStr', ''), ('KwargVariablesSetTagStr',
'_KwargVariablesDict'), ('DefaultOrderedDict',
OrderedDict([('_AttributeKeyVariable', None)])), ('FunctionNameStr',
'setDefault')]), 'do_interface': InspectDict([('DefaultIndexInt', 1),
('InputKeyStrsList', ['self']), ('LiargVariablesListKeyStr', ''),
('KwargVariablesSetTagStr', '_KwargVariablesDict'), ('DefaultOrderedDict',
OrderedDict()), ('FunctionNameStr', 'do_interface')]), 'interface':
InspectDict([('DefaultIndexInt', 1), ('InputKeyStrsList',
['_InstanceVariable']), ('LiargVariablesListKeyStr', '_LiargVariablesList'),
('KwargVariablesSetTagStr', '_KwargVariablesDict'), ('DefaultOrderedDict',
OrderedDict()), ('FunctionNameStr', 'superDo_interface')]), 'superDo_interface':
InspectDict([('DefaultIndexInt', 1), ('InputKeyStrsList',
['_InstanceVariable']), ('LiargVariablesListKeyStr', '_LiargVariablesList'),
('KwargVariablesSetTagStr', '_KwargVariablesDict'), ('DefaultOrderedDict',
OrderedDict()), ('FunctionNameStr', 'superDo_interface')]), 'setDoing':
InspectDict([('DefaultIndexInt', 1), ('InputKeyStrsList', ['_InstanceVariable',
'_DoClassVariable']), ('LiargVariablesListKeyStr', ''),
('KwargVariablesSetTagStr', '_KwargVariablesDict'), ('DefaultOrderedDict',
OrderedDict([('_DoClassVariable', None)])), ('FunctionNameStr', 'setDoing')]),
'setDefaultMutable': InspectDict([('DefaultIndexInt', 2), ('InputKeyStrsList',
['_InstanceVariable', '_ClassVariable', '_AttributeKeyVariable']),
('LiargVariablesListKeyStr', ''), ('KwargVariablesSetTagStr',
'_KwargVariablesDict'), ('DefaultOrderedDict',
OrderedDict([('_AttributeKeyVariable', None)])), ('FunctionNameStr',
'setDefaultMutable')]), 'default_init': InspectDict([('DefaultIndexInt', 1),
('InputKeyStrsList', ['self', '_MakingMyFloat']), ('LiargVariablesListKeyStr',
''), ('KwargVariablesSetTagStr', ''), ('DefaultOrderedDict',
OrderedDict([('_MakingMyFloat', {'PropertyDocStr': 'I am doing the thing here',
'PropertyInitVariable': 3.0, 'DefaultValueType': <type 'property'>})])),
('FunctionNameStr', 'default_init')]), 'getDo': InspectDict([('DefaultIndexInt',
1), ('InputKeyStrsList', ['_InstanceVariable', '_DoClassVariable']),
('LiargVariablesListKeyStr', ''), ('KwargVariablesSetTagStr', ''),
('DefaultOrderedDict', OrderedDict([('_DoClassVariable', None)])),
('FunctionNameStr', 'getDo')]), '__repr__': InspectDict([('DefaultIndexInt', 1),
('InputKeyStrsList', ['self']), ('LiargVariablesListKeyStr', ''),
('KwargVariablesSetTagStr', '_KwargVariablesDict'), ('DefaultOrderedDict',
OrderedDict()), ('FunctionNameStr', '__repr__')]), 'setDone':
InspectDict([('DefaultIndexInt', 1), ('InputKeyStrsList', ['_InstanceVariable',
'_DoClassVariable']), ('LiargVariablesListKeyStr', ''),
('KwargVariablesSetTagStr', '_KwargVariablesDict'), ('DefaultOrderedDict',
OrderedDict([('_DoClassVariable', None)])), ('FunctionNameStr', 'setDone')])}",
  "superDo_make": "<function superDo_make at 0x10a458410>",
  "DoMethodStr": "make",
  "propertize_delMakingMyFloat": "<function propertize_delMakingMyFloat at
0x10bf9cc80>",
  "DefaultSpecificKeyStrsList": "['MakingMyFloat']",
  "_MakingMyFloat": "3.0",
  "MroDoerClassesList": "[<class
'ShareYourSystem.Standards.Interfacers.Interfacer.InterfacerClass'>, <class
'ShareYourSystem.Standards.Interfacers.Printer.PrinterClass'>, <class
'MakerClass'>]",
  "InspectMethodDict": "MethodDict([('__init__', <unbound method
MakerClass.superDefault_init>), ('__repr__', <unbound method
MakerClass.__repr__>), ('_print', <unbound method MakerClass.superDo__print>),
('callAllMro', <unbound method MakerClass.callAllMro>), ('callDo', <unbound
method MakerClass.callDo>), ('default_init', <unbound method
MakerClass.default_init>), ('do__print', <unbound method MakerClass.do__print>),
('do_interface', <unbound method MakerClass.do_interface>), ('forcePrint',
<unbound method MakerClass.forcePrint>), ('getClass', <unbound method
MakerClass.getClass>), ('getDo', <unbound method MakerClass.getDo>),
('getDoing', <unbound method MakerClass.getDoing>), ('getDone', <unbound method
MakerClass.getDone>), ('getReprStr', <unbound method MakerClass.getReprStr>),
('interface', <unbound method MakerClass.superDo_interface>), ('setDefault',
<unbound method MakerClass.setDefault>), ('setDefaultMutable', <unbound method
MakerClass.setDefaultMutable>), ('setDo', <unbound method MakerClass.setDo>),
('setDoing', <unbound method MakerClass.setDoing>), ('setDone', <unbound method
MakerClass.setDone>), ('superDefault_init', <unbound method
MakerClass.superDefault_init>), ('superDo__print', <unbound method
MakerClass.superDo__print>), ('superDo_interface', <unbound method
MakerClass.superDo_interface>), ('superDo_make', <function superDo_make at
0x10a458410>), ('make', <function superDo_make at 0x10a458410>)])",
  "DoingGetBool": "False",
  "Module": "<module '__builtin__' (built-in)>",
  "DefaultAttributeVariablesOrderedDict": "OrderedDict([('MakingMyFloat',
{'PropertyDocStr': 'I am doing the thing here', 'PropertyInitVariable': 3.0,
'DefaultValueType': <type 'property'>})])",
  "propertize_setMakingMyFloat": "<function propertize_setMakingMyFloat at
0x10bf9ced8>",
  "MroClassesList": "(<class 'MakerClass'>, <class
'ShareYourSystem.Standards.Interfacers.Printer.PrinterClass'>, <class
'ShareYourSystem.Standards.Interfacers.Interfacer.InterfacerClass'>, <type
'object'>)",
  "MroClassesDict": "{'PrinterClass': <class
'ShareYourSystem.Standards.Interfacers.Printer.PrinterClass'>,
'InterfacerClass': <class
'ShareYourSystem.Standards.Interfacers.Interfacer.InterfacerClass'>,
'MakerClass': <class 'MakerClass'>, 'object': <type 'object'>}",
  "NameStr": "Maker"
}
MyMaker.__dict__ before set is

   /{
   /  'DefaultInitBool' : True
   /  'PrintIdInt' : 4495470544
   /  'PrintingInstanceForceKeyStrsList' : []
   /  'PrintingInstanceSkipKeyStrsList' : []
   /}
MyMaker.__dict__ after set is

   /{
   /  'DefaultInitBool' : True
   /  'PrintIdInt' : 4495470544
   /  'PrintingInstanceForceKeyStrsList' : []
   /  'PrintingInstanceSkipKeyStrsList' : []
   /  '_MakingMyFloat' : 7.0
   /}
MyMaker before set is
< (MakerClass), 4495821648 >
   /{
   /  '<Spe><Class>MakingMyFloat' : 3.0
   /}
MyMaker after set is
< (MakerClass), 4495821648 >
   /{
   /  '<Spe><Class>MakingMyFloat' : 7.0
   /}

```



<!---
FrozenIsBool True
-->

##Example

Going back to the Doer cell when we invented a very minimalist Maker.
We now define its MakingMyFloat as a property that can be then defined as
a "binding" attribute thanks to the setMakingMyFloat method definition,
that will be linked to the fset attribute of the property object.

```python
#ImportModules
import ShareYourSystem as SYS

#Define
@SYS.PropertiserClass()
class MakerClass(object):

    def default_init(self,
            _MakingMyFloat={
                            'DefaultValueType':property,
                            'PropertyInitVariable':3.,
                            'PropertyDocStr':'I am doing the thing here'
                            },
            _MakingMyList={
                            'DefaultValueType':property,
                            'PropertyInitVariable':[],
                            'PropertyDocStr':'I am doing the thing here'
                            },
            _MakingMyInt={'DefaultValueType':int},
            _MadeMyInt=0
        ):
        object.__init__(self)

    #Definition a binding function
    def propertize_setMakingMyFloat(self,_SettingValueVariable):

        #Print
        #print('I am going to make the job directly !')

        #set the value of the "hidden" property variable
        self._MakingMyFloat=_SettingValueVariable

        #Bind with MadeInt setting
        self.MadeMyInt=int(self._MakingMyFloat)

    #Definition a binding function
    def propertize_setMakingMyList(self,_SettingValueVariable):

        #set the value of the "hidden" property variable
        self._MakingMyList=_SettingValueVariable+['Hellllllo']


#Definition a default instance
DefaultMaker=MakerClass()

#Definition a special instance
SpecialMaker=MakerClass(_MakingMyFloat=5,_MakingMyList=[4])

#Definition the AttestedStr
print('\n'.join(
    [
        'MakerClass.PropertizedDefaultTuplesList is '+SYS._str(
            MakerClass.PropertizedDefaultTuplesList),
        'What are you saying DefaultMaker ?',
        'DefaultMaker.__dict__ is '+str(DefaultMaker.__dict__),
        'DefaultMaker.MakingMyFloat is '+str(DefaultMaker.MakingMyFloat),
        'DefaultMaker.MakingMyList is '+str(DefaultMaker.MakingMyList),
        'DefaultMaker.MadeMyInt is '+str(DefaultMaker.MadeMyInt),
        'What are you saying SpecialMaker ?',
        'SpecialMaker.__dict__ is '+str(SpecialMaker.__dict__),
        'SpecialMaker.MakingMyFloat is '+str(SpecialMaker.MakingMyFloat),
        'SpecialMaker.MakingMyList is '+str(SpecialMaker.MakingMyList),
        'SpecialMaker.MadeMyInt is '+str(SpecialMaker.MadeMyInt),
    ]
    )
)

#Print


```


```console
>>>
MakerClass.PropertizedDefaultTuplesList is
   /[
   /  0 :
   /   /(
   /   /  0 : MakingMyFloat
   /   /  1 : <property object at 0x10c00a520>
   /   /)
   /  1 :
   /   /(
   /   /  0 : MakingMyList
   /   /  1 : <property object at 0x10c00a470>
   /   /)
   /]
What are you saying DefaultMaker ?
DefaultMaker.__dict__ is {'DefaultInitBool': True}
DefaultMaker.MakingMyFloat is 3.0
DefaultMaker.MakingMyList is []
DefaultMaker.MadeMyInt is 0
What are you saying SpecialMaker ?
SpecialMaker.__dict__ is {'DefaultInitBool': True, 'MadeMyInt': 5,
'_MakingMyFloat': 5, '_MakingMyList': [4, 'Hellllllo']}
SpecialMaker.MakingMyFloat is 5
SpecialMaker.MakingMyList is [4, 'Hellllllo']
SpecialMaker.MadeMyInt is 5

```



<!---
FrozenIsBool True
-->

##Example

Note that setting a propertize method in a derived class works also and
overwrite the previous one. But we need to redefine the property. This will be
automatic in the Classer.

```python
#ImportModules
import ShareYourSystem as SYS

#Define
@SYS.PropertiserClass()
class MakerClass(object):

    def default_init(self,
            _MakingMyFloat={
                            'DefaultValueType':property,
                            'PropertyInitVariable':3.,
                            'PropertyDocStr':'I am doing the thing here'
                            },
            _MakingMyList={
                            'DefaultValueType':property,
                            'PropertyInitVariable':[],
                            'PropertyDocStr':'I am doing the thing here'
                            },
            _MakingMyInt={'DefaultValueType':int},
            _MadeMyInt=0
        ):
        object.__init__(self)

    def propertize_setMakingMyFloat(self,_SettingValueVariable):

        #Print
        #print('I am going to make the job directly !')

        #set the value of the "hidden" property variable
        self._MakingMyFloat=_SettingValueVariable

        #Bind with MadeInt setting
        self.MadeMyInt=int(self._MakingMyFloat)

    def propertize_setMakingMyList(self,_SettingValueVariable):

        #set the value of the "hidden" property variable
        self._MakingMyList=_SettingValueVariable+['Hellllllo']


#Define
@SYS.PropertiserClass()
class BuilderClass(MakerClass):

    def default_init(
                        self
                    ):
        SYS.MakerClass.__init__(self)

    def propertize_setMakingMyList(self,_SettingValueVariable):

        #call the base method
        MakerClass.propertize_setMakingMyList(self,_SettingValueVariable)

        #set the value of the "hidden" property variable
        self._MakingMyList+=['Build en plus !']

    #We need here to redefine
    MakingMyList=property(
            MakerClass.MakingMyList.fget,
            propertize_setMakingMyList,
            MakerClass.MakingMyList.fdel
        )

#Definition a special instance
SpecialBuilder=BuilderClass(_MakingMyFloat=5,_MakingMyList=[4])

#Definition the AttestedStr
print('\n'.join(
    [
        'What are you saying SpecialBuilder ?',
        'SpecialBuilder.__dict__ is '+str(SpecialBuilder.__dict__),
        'SpecialBuilder.MakingMyFloat is '+str(SpecialBuilder.MakingMyFloat),
        'SpecialBuilder.MakingMyList is '+str(SpecialBuilder.MakingMyList),
        'SpecialBuilder.MadeMyInt is '+str(SpecialBuilder.MadeMyInt),
    ]
    )
)

#Print


```


```console
>>>
What are you saying SpecialBuilder ?
SpecialBuilder.__dict__ is {'DefaultInitBool': True}
SpecialBuilder.MakingMyFloat is 3.0
SpecialBuilder.MakingMyList is []
SpecialBuilder.MadeMyInt is 0

```



<!---
FrozenIsBool True
-->

##Example

Note that there is an option in the property to define binding shape attributes
for an array.

```python
#ImportModules
import ShareYourSystem as SYS

#Define
@SYS.PropertiserClass()
class MakerClass(object):

    def default_init(self,
            _MakingMyList={
                            'DefaultValueType':property,
                            'PropertyInitVariable':None,
                            'PropertyDocStr':'I am doing the thing here',
                            'ShapeKeyStrsList':['MakingMyInt']
                            },
            _MakingMyInt=3,
            _MadeMyInt=0
        ):
        object.__init__(self)


#Define
MyMaker=MakerClass()

#Set and this will bind the value of MakingMyInt
MyMaker.MakingMyList=[3,4]

#print
print('MyMaker.__dict__ is ')
print(SYS.indent(MyMaker))
print(MyMaker.__class__.DefaultAttributeVariablesOrderedDict['MakingMyList'])



```


```console
>>>
MyMaker.__dict__ is
{
  "DefaultInitBool": "True",
  "_MakingMyList": "[3, 4]",
  "MakingMyInt": "2"
}
{'ShapeKeyStrsList': ['MakingMyInt'], 'PropertyDocStr': 'I am doing the thing
here', 'PropertyInitVariable': None, 'DefaultValueType': <type 'property'>}

```



<!---
FrozenIsBool True
-->

##Example

In the opposite way

```python
#ImportModules
import ShareYourSystem as SYS

#Define
@SYS.PropertiserClass()
class MakerClass(object):

    def default_init(self,
            _MakingMyList=None,
            _MakingMyInt={
                            'DefaultValueType':property,
                            'PropertyInitVariable':None,
                            'PropertyDocStr':'I am doing the thing here',
                            'ShapeDict':{
                                'MakingMyList':0
                            }
                        },
            _MadeMyInt=0
        ):
        object.__init__(self)


#Define
MyMaker=MakerClass()

#Set and this will bind the value of MakingMyInt
MyMaker.MakingMyInt=2

#print
print('MyMaker.__dict__ is ')
print(SYS.indent(MyMaker))



```


```console
>>>
MyMaker.__dict__ is
{
  "DefaultInitBool": "True",
  "_MakingMyInt": "2"
}

```



<!--
FrozenIsBool False
-->

##Code

----

<ClassDocStr>

<small>
View the Propertiser sources on <a href="https://github.com/Ledoux/ShareYourSyst
em/tree/master/Pythonlogy/ShareYourSystem/Standards/Classors/Propertiser"
target="_blank">Github</a>
</small>

----

```python
# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


The Propertiser is an augmented Defaultor because it will set defaults
attributes
possibly in properties for the new-style decorated classes. This can set objects
with high controlling features thanks to the binding

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Classors.Doer"
DecorationModuleStr=BaseModuleStr
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import inspect
import collections
#</ImportSpecificModules>

#<DefineLocals>
PropertyGetStr="_"
PropertyRepresentationStr="p:"
PropertyPrefixStr="propertize_"
#</DefineLocals>

#<DefineFunctions>
def getPropertizedTupleWithItemTupleAndClass(_ItemTuple,_Class):

        #Debug
        '''
        print('Propertiser l 39')
        print('_ItemTuple is ')
        print(_ItemTuple)
        print('')
        '''

        #Get the KeyStr, and the ValueVariable that should be a dict
        PropertizedKeyStr=_ItemTuple[0]
        PropertizedValueVariable=_ItemTuple[1]
        PropertizedHideKeyStr=PropertyGetStr+PropertizedKeyStr

        #Check that this is a property yet or not
        if type(PropertizedValueVariable)!=property:

                #Init
                PropertizedValueVariable=property()

                #/###################/#
                # Prepare the get property
                #

                #Definition the get function
PropertizedGetFunctionStr=PropertyPrefixStr+'get'+PropertizedKeyStr

                #Check
                if hasattr(_Class,PropertizedGetFunctionStr):

                        #Check for an already defined method
PropertizedGetFunction=getattr(_Class,PropertizedGetFunctionStr)

                else:

                        #Definition a default one
                        def PropertizedGetFunction(_InstanceVariable):

                                """
                                #/#################/#
                                # return the one hidden in the dict
                                # else return the one in the class

                                #Check
                                if
hasattr(_InstanceVariable,PropertizedHideKeyStr):

                                        #return
                                        return
getattr(_InstanceVariable,PropertizedHideKeyStr)
                                else:

                                        #return
                                        return
getattr(_InstanceVariable.__class__,PropertizedKeyStr)
                                """

                                #/#################/#
                                # return the one hidden in the dict
                                # else return None

                                if
hasattr(_InstanceVariable,PropertizedHideKeyStr):

                                        #return
                                        return
getattr(_InstanceVariable,PropertizedHideKeyStr)

                                else:

                                        return None

PropertizedGetFunction.__name__=PropertizedGetFunctionStr

                #/###################/#
                # Prepare the set property
                #

                #Definition the set function
PropertizedSetFunctionStr=PropertyPrefixStr+'set'+PropertizedKeyStr

                #Check
                if hasattr(_Class,PropertizedSetFunctionStr):

                        #/######################/#
                        # Case where there is already something
                        #

                        #Check for an already defined method
PropertizedSetFunction=getattr(_Class,PropertizedSetFunctionStr)

                else:

                        #/######################/#
                        # Default case
                        #

                        #Definition a default one
                        def
PropertizedSetFunction(_InstanceVariable,_SettingValueVariable):
_InstanceVariable.__setattr__(PropertizedHideKeyStr,_SettingValueVariable)
PropertizedSetFunction.__name__=PropertizedSetFunctionStr

                #/######################/#
                # Case where we bind also the setting of the shaping atttributes
                #

                #Check
                if 'ShapeKeyStrsList' in _ItemTuple[1]:

                        #get
PropertizedShapeKeyStrsList=_ItemTuple[1]['ShapeKeyStrsList']

                        #Debug
                        '''
                        print('Propertiser l 111')
                        print('There is a ShapeKeyStrsList')
                        print('PropertizedShapeKeyStrsList is ')
                        print(PropertizedShapeKeyStrsList)
                        print('')
                        '''

                        #import
                        import numpy as np

                        def
PropertizedShapeSetFunction(_InstanceVariable,_SettingValueVariable):

                                #call the first
PropertizedSetFunction(_InstanceVariable,_SettingValueVariable)

                                #get the shape
                                PropertizedShapeIntsList=np.shape(
                                        getattr(
                                                        _InstanceVariable,
                                                        PropertizedHideKeyStr
                                                )
                                )

                                #Debug
                                '''
                                print('Propertiser l 137')
                                print('We shape here')
                                print('PropertizedHideKeyStr is')
                                print(PropertizedHideKeyStr)
                                print('PropertizedShapeKeyStrsList is ')
                                print(PropertizedShapeKeyStrsList)
                                print('PropertizedShapeIntsList is ')
                                print(PropertizedShapeIntsList)
                                print('')
                                '''

                                #map a set
                                map(
                                                lambda
__PropertizedShapeKeyStr,__PropertizedShapeInt:
                                                setattr(
                                                        _InstanceVariable,
__PropertizedShapeKeyStr,
                                                        __PropertizedShapeInt
                                                ),
                                                PropertizedShapeKeyStrsList,
                                                PropertizedShapeIntsList
                                        )

                #/###################/#
                # Prepare the del property
                #

                #Definition the del function
PropertizedDelFunctionStr=PropertyPrefixStr+'del'+PropertizedKeyStr

                #Check
                if hasattr(_Class,PropertizedDelFunctionStr):

                        #Check for an already defined method
PropertizedDelFunction=getattr(_Class,PropertizedDelFunctionStr)

                else:

                        #Definition a default one
                        def PropertizedDelFunction(_InstanceVariable):
_InstanceVariable.__delattr__(PropertizedHideKeyStr)
PropertizedDelFunction.__name__=PropertizedDelFunctionStr

                #Debug
                '''
                print('Propertizer l 109')
                print('PropertizedDetFunction is ')
                print(PropertizedDetFunction)
                print('')
                '''

                #/###################/#
                # Now set in the class
                #

                if 'ShapeKeyStrsList' in _ItemTuple[1]:
                        PropertizedBindSetFunction=PropertizedShapeSetFunction
                else:
                        PropertizedBindSetFunction=PropertizedSetFunction

                #Define in the class...
                map(
                        lambda __PropertizedFunction:
                        setattr(
                                _Class,
                                __PropertizedFunction.__name__,
                                __PropertizedFunction
                        ),
                        [
                                PropertizedGetFunction,
                                PropertizedBindSetFunction,
                                PropertizedDelFunction
                        ]
                )

                #Define in the special dict...
                map(
                        lambda __Function:
                        _Class.PropertyMethodsDict.__setitem__(
                                __Function.__name__,
                                __Function
                        ),
                        [
                                PropertizedGetFunction,
                                PropertizedBindSetFunction,
                                PropertizedDelFunction
                        ]
                )

                #Redefine
                PropertizedValueVariable=property(
                                                        PropertizedGetFunction,
PropertizedBindSetFunction,
                                                        PropertizedDelFunction,
_ItemTuple[1]['PropertyDocStr'
                                                        ]if 'PropertyDocStr' in
_ItemTuple[1]
                                                        else "This is here a
property but with no more details..."
                                                )

        #Definition the property
        return (
                                PropertizedKeyStr,
                                PropertizedValueVariable
                        )

def getPropertizedVariableWithItemTuple(_ItemTuple):

        #Maybe it is already defined
        if 'PropertyInitVariable' in _ItemTuple[1]:
                return _ItemTuple[1]['PropertyInitVariable']
        else:

                #Return the default one associated with the type
                return
SYS.getTypeClassWithTypeStr(SYS.getWordStrsListWithStr(_ItemTuple[0])[-1])

#</DefineFunctions>

#<Define_Class>
@DecorationClass()
class PropertiserClass(BaseClass):

        def default_init(self,
                                                **_KwargVariablesDict
                                        ):

                #Call the parent init method
                BaseClass.__init__(self,**_KwargVariablesDict)

        def __call__(self,_Class):

                #debug
                '''
                print('Propetizer l.179 __call__ method')
                print('_Class is ',_Class)
                print('')
                '''

                #Call the parent init method
                BaseClass.__call__(self,_Class)

                #Debug
                '''
                print('l.146 : We are going to propertize')
                print('')
                '''

                #propertize
                self.propertize()

                #Debug
                '''
                print('l.153 : propertize is done')
                print('')
                '''

                #Return
                return _Class

        def do_propertize(self):

                #Alias
                PropertizedClass=self.DoClass

                #Debug
                '''
                print('PropertizedClass is ',PropertizedClass)
                print('')
                '''

                #init
                PropertizedClass.PropertyMethodsDict={}

                #Add to the KeyStrsList
                PropertizedClass.KeyStrsList+=[
"PropertyMethodsDict"
                                                                        ]

                #debug
                '''
                print('Propertiser l.47 default method')
                print('Class is ',Class)
                print('')
                '''

                #/###################/#
                # Check for new properties in the default dict
                #

                #Check
                if
hasattr(PropertizedClass,"DefaultAttributeVariablesOrderedDict"):

                        #debug
                        '''
print('PropertizedClass.DefaultAttributeVariablesOrderedDict
is',PropertizedClass.DefaultAttributeVariablesOrderedDict)
                        print('')
                        '''

                        #set the PropertizedDefaultTuplesList
PropertizedClass.PropertizedDefaultTuplesList=SYS._filter(
                                lambda __DefaultSetTuple:
                                type(__DefaultSetTuple[1]
                                        )==property or (
                                        hasattr(__DefaultSetTuple[1],'items'
                                                ) and 'DefaultValueType' in
__DefaultSetTuple[1
                                        ] and __DefaultSetTuple[1
                                        ]['DefaultValueType']==property),
PropertizedClass.DefaultAttributeVariablesOrderedDict.items()
                        )

                        #debug
                        '''
                        print('Propertiser l.266')
                        print('Before set
PropertizedClass.PropertizedDefaultTuplesList is
',PropertizedClass.PropertizedDefaultTuplesList)
                        print('')
                        '''

                        #set at the level of the class the PropertyGetStr+KeyStr
                        map(
                                        lambda __PropertizedDefaultTuple:
                                        setattr(
PropertizedClass,
PropertyGetStr+__PropertizedDefaultTuple[0],
getPropertizedVariableWithItemTuple(__PropertizedDefaultTuple)
                                                        ),
PropertizedClass.PropertizedDefaultTuplesList
                                )

                        #set the PropertizedTuple for each at the level of the
class
                        PropertizedClass.PropertizedDefaultTuplesList=map(
                                        lambda __PropertizedDefaultTuple:
getPropertizedTupleWithItemTupleAndClass(
                                                __PropertizedDefaultTuple,
                                                PropertizedClass
                                        ),
PropertizedClass.PropertizedDefaultTuplesList
                                )

                        #debug
                        '''
                        print('Propertiser l 293')
                        print('After set
PropertizedClass.PropertizedDefaultTuplesList is ',
                                PropertizedClass.PropertizedDefaultTuplesList)
                        print('')
                        '''

                        #Reset at the level of the class the properties
                        map(
                                        lambda __PropertizedDefaultTuple:
                                        setattr(
PropertizedClass,
*__PropertizedDefaultTuple
                                                        ),
PropertizedClass.PropertizedDefaultTuplesList
                                )

                        #Check
                        if
hasattr(PropertizedClass,'PrintingClassSkipKeyStrsList'):

                                #map append in  the KeyStrsList
                                map(
                                                lambda
__PropertizedDefaultTuple:
PropertizedClass.PrintingClassSkipKeyStrsList.extend(
                                                        [
#__PropertizedDefaultTuple[0],
PropertyGetStr+__PropertizedDefaultTuple[0]
                                                        ]
                                                ),
PropertizedClass.PropertizedDefaultTuplesList
                                        )

                        #Add to the KeyStrsList
                        PropertizedClass.KeyStrsList+=[
"PropertizedDefaultTuplesList"
                                                                        ]

#</Define_Class>




```


