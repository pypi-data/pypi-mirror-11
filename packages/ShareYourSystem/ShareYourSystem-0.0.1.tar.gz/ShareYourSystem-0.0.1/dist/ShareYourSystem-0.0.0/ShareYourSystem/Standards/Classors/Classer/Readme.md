

<!--
FrozenIsBool False
-->

#Classer

##Doc
----


>
> The Classer
>
>

----

<small>
View the Classer notebook on [NbViewer](http://nbviewer.ipython.org/url/shareyou
rsystem.ouvaton.org/Classer.ipynb)
</small>




<!---
FrozenIsBool True
-->

##Example

For this non directly very useful Module we just define a decorated FooClass
for which the Functer decoration by default call the decorated method...

```python
#ImportModules
import ShareYourSystem as SYS
import operator

#Definition
@SYS.ClasserClass(**{
    'ClassingSwitchMethodStrsList':[
        'make'
    ]
})
class MakerClass(object):

    def default_init(self,
                    _MakingMyFloat=0.,
                    _MadeMyInt=0,
                    **_KwarVariablesDict
                ):
        object.__init__(self,**_KwarVariablesDict)

    def do_make(self):

        #print
        print('I am in the do_make of the Maker')

        #cast
        self.MadeMyInt=int(self.MakingMyFloat)

#Definition
@SYS.ClasserClass(**{
    'ClassingSwitchMethodStrsList':[
        'make',
        'build'
    ]
}
)
class BuilderClass(MakerClass):

    def default_init(self,
                    **_KwarVariablesDict
                ):
        MakerClass.__init__(self,**_KwarVariablesDict)

    def mimic_make(self):

        #print
        print('I am in the mimic_make of the Builder')

        #call the parent method
        MakerClass.make(self)

        #cast
        self.MadeMyInt+=10

    def do_build(self):
        pass

#Definition an instance
MyBuilder=BuilderClass()

#Print
print('Before make, MyBuilder.__dict__ is ')
SYS._print(MyBuilder.__dict__)

#make once
MyBuilder.make(3.)

#Print
print('After the first make, MyBuilder.__dict__ is ')
SYS._print(MyBuilder.__dict__)

#make again
MyBuilder.make(5.)

#Print
print('After the second make, MyBuilder.__dict__ is ')
SYS._print(MyBuilder.__dict__)

#make again
print('Now we switch all')
MyBuilder.setSwitch('make',BuilderClass)

#Print
print('After the switch MyBuilder.__dict__ is ')
SYS._print(MyBuilder.__dict__)

#make again
MyBuilder.make(7.)

#Print
print('After the third make, MyBuilder.__dict__ is ')
SYS._print(MyBuilder.__dict__)

#Definition the AttestedStr
SYS._attest(
    [
        'BuilderClass.WatchBeforeMakeWithMakerBool is
'+str(BuilderClass.WatchBeforeMakeWithMakerBool),
        'BuilderClass.make is '+str(BuilderClass.make),
        'BuilderClass.build is '+str(BuilderClass.build),
        'MyBuilder.__dict__ is '+SYS._str(
            MyBuilder.__dict__
        )
    ]
)

#Print





```


```console
>>>
Before make, MyBuilder.__dict__ is

   /{
   /  'DefaultInitBool' : True
   /}
I am in the mimic_make of the Builder
I am in the do_make of the Maker
After the first make, MyBuilder.__dict__ is

   /{
   /  'DefaultInitBool' : True
   /  'MadeMyInt' : 13
   /  'MakingMyFloat' : 3.0
   /  '_WatchAfterMakeWithBuilderBool' : True
   /  '_WatchAfterMakeWithMakerBool' : True
   /  '_WatchBeforeMakeWithBuilderBool' : True
   /  '_WatchBeforeMakeWithMakerBool' : True
   /}
After the second make, MyBuilder.__dict__ is

   /{
   /  'DefaultInitBool' : True
   /  'MadeMyInt' : 13
   /  'MakingMyFloat' : 3.0
   /  '_WatchAfterMakeWithBuilderBool' : True
   /  '_WatchAfterMakeWithMakerBool' : True
   /  '_WatchBeforeMakeWithBuilderBool' : True
   /  '_WatchBeforeMakeWithMakerBool' : True
   /}
Now we switch all
After the switch MyBuilder.__dict__ is

   /{
   /  'DefaultInitBool' : True
   /  'MadeMyInt' : 13
   /  'MakingMyFloat' : 3.0
   /  '_WatchAfterMakeWithBuilderBool' : False
   /  '_WatchAfterMakeWithMakerBool' : True
   /  '_WatchBeforeMakeWithBuilderBool' : False
   /  '_WatchBeforeMakeWithMakerBool' : True
   /}
I am in the mimic_make of the Builder
After the third make, MyBuilder.__dict__ is

   /{
   /  'DefaultInitBool' : True
   /  'MadeMyInt' : 23
   /  'MakingMyFloat' : 7.0
   /  '_WatchAfterMakeWithBuilderBool' : True
   /  '_WatchAfterMakeWithMakerBool' : True
   /  '_WatchBeforeMakeWithBuilderBool' : True
   /  '_WatchBeforeMakeWithMakerBool' : True
   /}


*****Start of the Attest *****

            BuilderClass.WatchBeforeMakeWithMakerBool is <property object at
0x10c0f20a8>

------

            BuilderClass.make is <unbound method
BuilderClass.switch_watch_superMimic_switch_watch_superDo_make>

------

            BuilderClass.build is <unbound method
BuilderClass.switch_watch_superDo_build>

------

            MyBuilder.__dict__ is
               /{
               /  'DefaultInitBool' : True
               /  'MadeMyInt' : 23
               /  'MakingMyFloat' : 7.0
               /  '_WatchAfterMakeWithBuilderBool' : True
               /  '_WatchAfterMakeWithMakerBool' : True
               /  '_WatchBeforeMakeWithBuilderBool' : True
               /  '_WatchBeforeMakeWithMakerBool' : True
               /}

*****End of the Attest *****



```



<!---
FrozenIsBool True
-->

Note that now setting a propertize method in a derived class works also and
overwrite the previous one. (without redefine the property)

```python
#ImportModules
import ShareYourSystem as SYS

#Define
@SYS.ClasserClass()
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
@SYS.ClasserClass()
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

