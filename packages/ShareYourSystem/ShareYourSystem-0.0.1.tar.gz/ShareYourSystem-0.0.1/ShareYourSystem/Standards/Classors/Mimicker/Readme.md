

<!--
FrozenIsBool False
-->

#Mimicker

##Doc
----


>
> Mimicker...
>
>

----

<small>
View the Mimicker notebook on [NbViewer](http://nbviewer.ipython.org/url/shareyo
ursystem.ouvaton.org/Mimicker.ipynb)
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

#Definition
@SYS.DoerClass()
class MakerClass(object):

    def default_init(self,
                    _MakingMyFloat=0.,
                    _MakingFirstInt=0,
                    _MakingSecondInt=1,
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
@SYS.MimickerClass(**{
    'MimickingDoMethodStr':'make'
})
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

#Definition an instance
MyBuilder=BuilderClass()

#Print
print('Before make, MyBuilder.__dict__ is ')
print(SYS.indent(MyBuilder.__dict__))

#make once
MyBuilder.make(
    3.,
    _FirstInt=2,
    **{
        'MakingSecondInt':5
    }
)

#Print
print('After the first make, MyBuilder.__dict__ is ')
print(SYS.indent(MyBuilder.__dict__))

#Definition the AttestedStr
print('BuilderClass.make is '+str(BuilderClass.make))

#print
print('MyBuilder.__dict__ is ')
print(SYS.indent(MyBuilder.__dict__))

#Check
print('MakerClass.make.BaseDoClass is ')
print(MakerClass.make.BaseDoClass)
print('BuilderClass.make.BaseDoClass is ')
print(BuilderClass.make.BaseDoClass)






```


```console
>>>
Before make, MyBuilder.__dict__ is
{
  "DefaultInitBool": "True"
}
I am in the mimic_make of the Builder
I am in the do_make of the Maker
After the first make, MyBuilder.__dict__ is
{
  "MakingMyFloat": "3.0",
  "MakingFirstInt": "2",
  "DefaultInitBool": "True",
  "MakingSecondInt": "5",
  "MadeMyInt": "13"
}
BuilderClass.make is <unbound method BuilderClass.superMimic_superDo_make>
MyBuilder.__dict__ is
{
  "MakingMyFloat": "3.0",
  "MakingFirstInt": "2",
  "DefaultInitBool": "True",
  "MakingSecondInt": "5",
  "MadeMyInt": "13"
}
MakerClass.make.BaseDoClass is
<class 'MakerClass'>
BuilderClass.make.BaseDoClass is
<class 'MakerClass'>

```



<!---
FrozenIsBool True
-->

##Example

It is possible to cumulate mimick and switch properties...
Note that only the do_make is a switched method as the
mimic_make continue to work after the first call of make.

```python
#ImportModules
import ShareYourSystem as SYS

#Definition a MakerClass with decorated make by a Switcher
@SYS.SwitcherClass(**{
    'SwitchingIsBool':True,
    'SwitchingWrapMethodStr':'make'
})
class MakerClass(object):

    def default_init(self,
                _MakingMyFloat=1.,
                _MadeMyInt=0
                ):
        object.__init__(self)

    def do_make(self):

        #print
        print('self.MakingMyFloat is '+str(self.MakingMyFloat))
        print('self.MadeMyInt is '+str(self.MadeMyInt))
        print('')

        #Cast
        self.MadeMyInt=int(self.MakingMyFloat)

#Definition
@SYS.MimickerClass(**{
    'MimickingDoMethodStr':"make"
})
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
print(SYS.indent(MyBuilder.__dict__))

#print
print('MyBuilder.getSwitch() is ')
print(SYS.indent(MyBuilder.getSwitch()))

#make once
MyBuilder.make(3.)

#Print
print('After the first make, MyBuilder is ')
print(SYS.indent(MyBuilder.__dict__))

#print
print('MyBuilder.getSwitch() is ')
print(SYS.indent(MyBuilder.getSwitch()))

#make again
MyBuilder.make(5.)

#Print
print('After the second make, MyBuilder is ')
print(SYS.indent(MyBuilder.__dict__))

#make again
print('Now we switch')
MyBuilder.setSwitch(_DoMethodVariable=['make'])

#Print
print('After the switch MyBuilder is ')
print(SYS.indent(MyBuilder.__dict__))



```


```console
>>>
Before make, MyBuilder.__dict__ is
{
  "DefaultInitBool": "True"
}
MyBuilder.getSwitch() is
{
  "WatchBeforeMakeWithMakerBool": "None",
  "WatchAfterMakeWithMakerBool": "None"
}
I am in the mimic_make of the Builder
self.MakingMyFloat is 3.0
self.MadeMyInt is 0

After the first make, MyBuilder is
{
  "MakingMyFloat": "3.0",
  "_WatchBeforeMakeWithMakerBool": "True",
  "DefaultInitBool": "True",
  "_WatchAfterMakeWithMakerBool": "True",
  "MadeMyInt": "13"
}
MyBuilder.getSwitch() is
{
  "WatchBeforeMakeWithMakerBool": "True",
  "WatchAfterMakeWithMakerBool": "True"
}
I am in the mimic_make of the Builder
After the second make, MyBuilder is
{
  "MakingMyFloat": "5.0",
  "_WatchBeforeMakeWithMakerBool": "True",
  "DefaultInitBool": "True",
  "_WatchAfterMakeWithMakerBool": "True",
  "MadeMyInt": "23"
}
Now we switch
After the switch MyBuilder is
{
  "MakingMyFloat": "5.0",
  "_WatchBeforeMakeWithMakerBool": "False",
  "DefaultInitBool": "True",
  "_WatchAfterMakeWithMakerBool": "False",
  "MadeMyInt": "23"
}

```



<!--
FrozenIsBool False
-->

##Code

----

<ClassDocStr>

<small>
View the Mimicker sources on <a href="https://github.com/Ledoux/ShareYourSystem/
tree/master/Pythonlogy/ShareYourSystem/Standards/Classors/Mimicker"
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


Mimicker...

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Classors.Switcher"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Tester"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
from ShareYourSystem.Standards.Classors import Doer
import six
#</ImportSpecificModules>

#<DefineLocals>
MimickingWrapPrefixStr="mimic_"
MimickingDecorationPrefixStr=""
MimickingDecorationTagStr="superMimic"
MimickingDecorationSuffixStr="_"
#</DefineLocals>

#<DefineFunctions>
def mimic(_InstanceVariable,*_LiargVariablesList,**_KwargVariablesDict):

        #Set
        MimicMethodStr=_KwargVariablesDict['MimicMethodStr']
        MimicClassStr=_KwargVariablesDict['MimicClassStr']
        MimicClass=getattr(SYS,MimicClassStr)
        MimicUnBoundMethod=getattr(
                MimicClass,
                MimicMethodStr
        )
        BaseClassStr=_KwargVariablesDict['BaseClassStr']
        BaseClass=getattr(SYS,BaseClassStr)
        del _KwargVariablesDict['MimicMethodStr']
        del _KwargVariablesDict['MimicClassStr']
        del _KwargVariablesDict['BaseClassStr']

        #Debug
        '''
        print('Mimicker l.48 inside of the function mimic')
        #print('_InstanceVariable is ',_InstanceVariable)
        print('_LiargVariablesList is ',_LiargVariablesList)
        print('_KwargVariablesDict is ',_KwargVariablesDict)
        print('')
        '''

        if len(_KwargVariablesDict)>0:

                #group by
                [
                        MimicTempAttributeItemTuplesList,
                        MimicTempNotAttributeItemTuplesList
                ]=SYS.groupby(
                        lambda __KwargItemTuple:
                        hasattr(_InstanceVariable,__KwargItemTuple[0]),
                        _KwargVariablesDict.items()
                )

                #Debug
                '''
                print('MimicTempAttributeItemTuplesList is
',MimicTempAttributeItemTuplesList)
                print('MimicTempNotItemTuplesList is
',MimicTempNotItemTuplesList)
                print('')
                '''

                #set in the instance the corresponding kwarged arguments
                map(
                                lambda __MimicTempAttributeItemTuple:
                                #set direct explicit attributes
_InstanceVariable.__setattr__(*__MimicTempAttributeItemTuple),
                                MimicTempAttributeItemTuplesList
                        )

                #Define
                MimicKwargDict=dict(MimicTempNotAttributeItemTuplesList)

        else:

                #Define
                MimicKwargDict={}

        #Init
        MimicOutputVariable=None

        #Debug
        '''
        print('Mimicker l.96 inside of the function mimic')
        print('MimicClass is ',MimicClass)
        print('MimicMethodStr is ',MimicMethodStr)
        print('MimicUnBoundMethod is ',MimicUnBoundMethod)
        print('')
        '''

        #call the Mimicked function
        if len(MimicKwargDict)>0:
                MimicOutputVariable=MimicUnBoundMethod(
                                                        _InstanceVariable,
                                                        *_LiargVariablesList,
                                                        **MimicKwargDict
                                                )
        else:
                MimicOutputVariable=MimicUnBoundMethod(
                                _InstanceVariable,
                                *_LiargVariablesList
                        )

        #Debug
        '''
        print('Mimicker l.117 inside of the function mimic')
        print('MimicOutputVariable is ',MimicOutputVariable)
        print('')
        '''

        #Check
        if BaseClass.DoingGetBool==False:

                #Return
                return _InstanceVariable

        else:

                #Return the
                return MimicOutputVariable
#</DefineFunctions>

#<DefineClass>
@DecorationClass()
class MimickerClass(BaseClass):

        #Definition
        RepresentingKeyStrsList=[
                'MimickingDoMethodStr',
                'MimickedWrapMethodStr'
        ]

        def default_init(self,
                                        _MimickingDoMethodStr="",
                                        _MimickedWrapMethodStr="",
                                        **_KwargVariablesDict
                                ):

                #Call the init parent method
                BaseClass.__init__(self,**_KwargVariablesDict)

        def __call__(self,_Class):

                #Call the parent init method
                BaseClass.__call__(self,_Class)

                #mimic
                self.mimic()

                #Return
                return _Class

        def do_mimic(self):

                #Debug
                '''
                print('l 174 Mimicker')
                print('self.MimickingDoMethodStr is ',self.MimickingDoMethodStr)
                print('')
                '''

                #Check
                if self.MimickingDoMethodStr!="":

                        #observe
                        self.observe(True,self.MimickingDoMethodStr)

                        #set
self.MimickedWrapMethodStr=MimickingWrapPrefixStr+self.MimickingDoMethodStr

                        #Debug
                        '''
                        print('l 75 Mimicker ')
                        print('self.MimickedWrapMethodStr is
',self.MimickedWrapMethodStr)
                        print('')
                        '''

                        #Define
                        MimickedDoStr=SYS.getUpperWordStr(
                                self.MimickingDoMethodStr
                        )
MimickedDoerStr=Doer.DoStrToDoerStrOrderedDict[MimickedDoStr]

                        #Debug
                        '''
                        print('l 84 Mimicker ')
                        print('MimickedDoStr is ',MimickedDoStr)
                        print('MimickedDoerStr is ',MimickedDoerStr)
                        print('MimickedBaseModule is ',MimickedBaseModule)
                        print('')
                        '''

                        #Definitions
                        MimickedBaseClass=getattr(
                                SYS,
                                SYS.getClassStrWithNameStr(MimickedDoerStr)
                        )

                        #get
                        MimickedDoExecStr=getattr(
                                MimickedBaseClass,
                                'Do'+MimickedBaseClass.NameStr+'ExecStr'
                        )

                        #debug
                        '''
                        print('l 206 Mimicker')
                        print('MimickedDoExecStr is ')
                        print(MimickedDoExecStr)
                        print('')
                        '''

                        #replace
                        MimickedDecorationMethodStr=MimickingDecorationPrefixStr
+MimickingDecorationTagStr+MimickingDecorationSuffixStr
                        MimickedDecorationMethodStr+=self.ObservedWrapMethodStr

                        #Debug
                        '''
                        print('l 232 Mimicker')
                        print('MimickedDecorationMethodStr is
'+MimickedDecorationMethodStr)
                        print('')
                        '''

                        #replace
                        MimickedExecStr='def
'+MimickedDecorationMethodStr+'('+'('.join(
                                MimickedDoExecStr.split('(')[1:]
                        )

                        #Debug
                        '''
                        print('l 208 Mimicker')
                        print('MimickedExecStr is ')
                        print(MimickedExecStr)
                        print('')
                        '''

                        #Add to the ImitatedDoneExecStr
                        MimickedExecStr+='\n\treturn
mimic(_InstanceVariable,*_LiargVariablesList,'
                        MimickedExecStr+='**dict({\'MimicMethodStr\':\''+self.Mi
mickedWrapMethodStr+'\','
MimickedExecStr+='\'MimicClassStr\':\''+self.DoClass.__name__+'\','
MimickedExecStr+='\'BaseClassStr\':\''+MimickedBaseClass.__name__+'\''
                        MimickedExecStr+='},**_KwargVariablesDict))'

                        #Debug
                        '''
                        print('l 223 Mimicker')
                        print('MimickedExecStr is ')
                        print(MimickedExecStr)
                        print('')
                        '''

                        #exec
                        six.exec_(MimickedExecStr)

                        #set
self.MimickedDecorationUnboundMethod=locals()[MimickedDecorationMethodStr]

                        #set in the __class__
                        self.setMethod(
                                                MimickedDecorationMethodStr,
self.MimickedDecorationUnboundMethod
                                        )

                        #make the amalgam
                        self.setMethod(
                                                self.MimickingDoMethodStr,
self.MimickedDecorationUnboundMethod
                                        )

                        #set a pointer to the fundamental class
self.MimickedDecorationUnboundMethod.BaseDoClass=MimickedBaseClass

#</DefineClass>


```


