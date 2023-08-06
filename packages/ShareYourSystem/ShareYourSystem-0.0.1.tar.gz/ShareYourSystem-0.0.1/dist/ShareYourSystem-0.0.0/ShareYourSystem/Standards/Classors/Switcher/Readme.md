

<!--
FrozenIsBool False
-->

#Switcher

##Doc
----


>
> The Switcher
>
>

----

<small>
View the Switcher notebook on [NbViewer](http://nbviewer.ipython.org/url/shareyo
ursystem.ouvaton.org/Switcher.ipynb)
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

#Definition a MakerClass with decorated make by a Switcher
@SYS.SwitcherClass(**{
    'SwitchingIsBool':True,
    #'ObservingWrapMethodStr':'do_make'
    #'ObservingWrapMethodStr':'superDo_make'
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

#print
print('MakerClass.SwitchMethodDict is ')
print(SYS.indent(MakerClass.SwitchMethodDict))

#Definition an instance
MyMaker=MakerClass()

#print
print('MyMaker.getSwitch() is ')
print(SYS.indent(MyMaker.getSwitch()))

#Print
print('Before make, MyMaker.__dict__ is ')
SYS._print(MyMaker.__dict__)

#make once
print('We make for the first time')
MyMaker.make(3.)

#Print
print('After the first make, MyMaker.__dict__ is ')
SYS._print(MyMaker.__dict__)

#print
print('MyMaker.getSwitch() is ')
print(SYS.indent(MyMaker.getSwitch()))

#make again
MyMaker.make(5.)

#Print
print('After the second make, MyMaker.__dict__ is ')
SYS._print(MyMaker.__dict__)

#make again
print('Now we switch')
MyMaker.setSwitch()

#Print
print('After the switch MyMaker.__dict__ is ')
SYS._print(MyMaker.__dict__)

#print
print('MyMaker.getSwitch() is ')
print(SYS.indent(MyMaker.getSwitch()))

#make again
MyMaker.make(7.)

#Print
print('After the third make, MyMaker.__dict__ is ')
SYS._print(MyMaker.__dict__)

#print
print('MakerClass.make is '+str(MakerClass.make))

#print
print('MyMaker.__dict__ is '+SYS._str(MyMaker.__dict__))




```


```console
>>>
MakerClass.SwitchMethodDict is
{
  "make": "[<class 'MakerClass'>]"
}
MyMaker.getSwitch() is
{
  "WatchBeforeMakeWithMakerBool": "None",
  "WatchAfterMakeWithMakerBool": "None"
}
Before make, MyMaker.__dict__ is

   /{
   /  'DefaultInitBool' : True
   /}
We make for the first time
self.MakingMyFloat is 3.0
self.MadeMyInt is 0

After the first make, MyMaker.__dict__ is

   /{
   /  'DefaultInitBool' : True
   /  'MadeMyInt' : 3
   /  'MakingMyFloat' : 3.0
   /  '_WatchAfterMakeWithMakerBool' : True
   /  '_WatchBeforeMakeWithMakerBool' : True
   /}
MyMaker.getSwitch() is
{
  "WatchBeforeMakeWithMakerBool": "True",
  "WatchAfterMakeWithMakerBool": "True"
}
After the second make, MyMaker.__dict__ is

   /{
   /  'DefaultInitBool' : True
   /  'MadeMyInt' : 3
   /  'MakingMyFloat' : 3.0
   /  '_WatchAfterMakeWithMakerBool' : True
   /  '_WatchBeforeMakeWithMakerBool' : True
   /}
Now we switch
After the switch MyMaker.__dict__ is

   /{
   /  'DefaultInitBool' : True
   /  'MadeMyInt' : 3
   /  'MakingMyFloat' : 3.0
   /  '_WatchAfterMakeWithMakerBool' : False
   /  '_WatchBeforeMakeWithMakerBool' : False
   /}
MyMaker.getSwitch() is
{
  "WatchBeforeMakeWithMakerBool": "False",
  "WatchAfterMakeWithMakerBool": "False"
}
self.MakingMyFloat is 7.0
self.MadeMyInt is 3

After the third make, MyMaker.__dict__ is

   /{
   /  'DefaultInitBool' : True
   /  'MadeMyInt' : 7
   /  'MakingMyFloat' : 7.0
   /  '_WatchAfterMakeWithMakerBool' : True
   /  '_WatchBeforeMakeWithMakerBool' : True
   /}
MakerClass.make is <unbound method MakerClass.switch_watch_superDo_make>
MyMaker.__dict__ is
   /{
   /  'DefaultInitBool' : True
   /  'MadeMyInt' : 7
   /  'MakingMyFloat' : 7.0
   /  '_WatchAfterMakeWithMakerBool' : True
   /  '_WatchBeforeMakeWithMakerBool' : True
   /}

```



<!---
FrozenIsBool True
-->

##Example

We can augment a Watch<DoStr>With<NameStr>Bool with a property to make it
reactive

```python
#ImportModules
import ShareYourSystem as SYS

#Definition a MakerClass with decorated make by a Switcher
@SYS.SwitcherClass(**{
    'SwitchingIsBool':True,
    #'ObservingWrapMethodStr':'do_make'
    #'ObservingWrapMethodStr':'superDo_make'
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
        #print('self.MakingMyFloat is '+str(self.MakingMyFloat))
        #print('self.MadeMyInt is '+str(self.MadeMyInt))
        #print('')

        #Cast
        self.MadeMyInt=int(self.MakingMyFloat)

    def getWatchAfterMakeWithMakerBool(self):

        #try
        try:
            return getattr(self,'_WatchAfterMakeWithMakerBool')
        except:
            return False

    def setWatchAfterMakeWithMakerBool(self,_SettingValueVariable):

        #set the value of the "hidden" property variable
        self._WatchAfterMakeWithMakerBool=_SettingValueVariable

        #Check
        if _SettingValueVariable:

            #debug
            print('\n**We have Made here !**')
            print('self.MakingMyFloat is '+str(self.MakingMyFloat))
            print('self.MadeMyInt is '+str(self.MadeMyInt))
            print('')

        else:

            #debug
            print(
                '\n**We have switch the Make here !**\n'
            )

    def delWatchAfterMakeWithMakerBool(self):
        self.__delattr__('_WatchAfterMakeWithMakerBool')

    WatchAfterMakeWithMakerBool=property(
            getWatchAfterMakeWithMakerBool,
            setWatchAfterMakeWithMakerBool,
            delWatchAfterMakeWithMakerBool,
            'WatchAfterMakeWithMakerBool is now reactive !'
        )

#Definition an instance
MyMaker=MakerClass()

#Print
print('Before make, MyMaker.__dict__ is ')
SYS._print(MyMaker.__dict__)

#make once
MyMaker.make(3.)

#Print
print('After the first make, MyMaker.__dict__ is ')
SYS._print(MyMaker.__dict__)

#make again
MyMaker.make(5.)

#Print
print('After the second make, MyMaker.__dict__ is ')
SYS._print(MyMaker.__dict__)

#make again
print('Now we switch')
MyMaker.setSwitch()

#Print
print('After the switch MyMaker.__dict__ is ')
SYS._print(MyMaker.__dict__)

#make again
MyMaker.make(7.)

#Print
print('After the third make, MyMaker.__dict__ is ')
SYS._print(MyMaker.__dict__)

#print
print('MakerClass.make is '+str(MakerClass.make))

#print
print('MyMaker.__dict__ is '+SYS._str(MyMaker.__dict__))





```


```console
>>>
Before make, MyMaker.__dict__ is

   /{
   /  'DefaultInitBool' : True
   /}

**We have Made here !**
self.MakingMyFloat is 3.0
self.MadeMyInt is 3

After the first make, MyMaker.__dict__ is

   /{
   /  'DefaultInitBool' : True
   /  'MadeMyInt' : 3
   /  'MakingMyFloat' : 3.0
   /  '_WatchAfterMakeWithMakerBool' : True
   /  '_WatchBeforeMakeWithMakerBool' : True
   /}
After the second make, MyMaker.__dict__ is

   /{
   /  'DefaultInitBool' : True
   /  'MadeMyInt' : 3
   /  'MakingMyFloat' : 3.0
   /  '_WatchAfterMakeWithMakerBool' : True
   /  '_WatchBeforeMakeWithMakerBool' : True
   /}
Now we switch

**We have switch the Make here !**

After the switch MyMaker.__dict__ is

   /{
   /  'DefaultInitBool' : True
   /  'MadeMyInt' : 3
   /  'MakingMyFloat' : 3.0
   /  '_WatchAfterMakeWithMakerBool' : False
   /  '_WatchBeforeMakeWithMakerBool' : False
   /}

**We have Made here !**
self.MakingMyFloat is 7.0
self.MadeMyInt is 7

After the third make, MyMaker.__dict__ is

   /{
   /  'DefaultInitBool' : True
   /  'MadeMyInt' : 7
   /  'MakingMyFloat' : 7.0
   /  '_WatchAfterMakeWithMakerBool' : True
   /  '_WatchBeforeMakeWithMakerBool' : True
   /}
MakerClass.make is <unbound method MakerClass.switch_watch_superDo_make>
MyMaker.__dict__ is
   /{
   /  'DefaultInitBool' : True
   /  'MadeMyInt' : 7
   /  'MakingMyFloat' : 7.0
   /  '_WatchAfterMakeWithMakerBool' : True
   /  '_WatchBeforeMakeWithMakerBool' : True
   /}

```



<!---
FrozenIsBool True
-->

##Example

Note that the swith can be specific to a Name and an Do

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

        #Cast
        self.MadeMyInt=int(self.MakingMyFloat)

#Definition a MakerClass with decorated make by a Switcher
@SYS.SwitcherClass(**{
    'SwitchingIsBool':True,
    'SwitchingWrapMethodStr':'build'
})
class BuilderClass(MakerClass):

    def default_init(self,
                _BuiltMyStr=""
                ):
        object.__init__(self)

    def do_build(self):

        #print
        print('We build here')

        #first make
        self.make()

        #Cast
        self.BuiltMyStr='My MadeMyInt is '+str(self.MadeMyInt)

#print
print('BuilderClass.SwitchMethodDict is ')
print(SYS.indent(BuilderClass.SwitchMethodDict))

#Definition an instance
MyBuilder=BuilderClass()

#Print
print('Before make, MyBuilder.__dict__ is ')
SYS._print(MyBuilder.__dict__)

#make once
print('NOW we build')
MyBuilder.build(**{'MakingMyFloat':3.})

#Print
print('After the build, MyBuilder.__dict__ is ')
SYS._print(MyBuilder.__dict__)

#Switch by default it is just the last Name and the the last do in the mro
print('Now we switch')
MyBuilder.setSwitch()

#Print
print('After the switch MyBuilder.__dict__ is ')
SYS._print(MyBuilder.__dict__)

#Definition an instance
MyBuilder=BuilderClass()

#Print
print('\nNow an other trial, \nBefore make, MyBuilder.__dict__ is ')
SYS._print(MyBuilder.__dict__)

#make once
MyBuilder.build(**{'MakingMyFloat':3.})

#Print
print('After the build, MyBuilder.__dict__ is ')
SYS._print(MyBuilder.__dict__)

#Switch by default it is just the last Name and the the last do in the mro
print('Now we switch')
MyBuilder.setSwitch('make',MakerClass,'Before')

#Print
print('After the switch MyBuilder.__dict__ is ')
SYS._print(MyBuilder.__dict__)

#make once
MyBuilder.build(**{'MakingMyFloat':6.})

#Print
print('After the final build, MyBuilder.__dict__ is ')
SYS._print(MyBuilder.__dict__)





```


```console
>>>
BuilderClass.SwitchMethodDict is
{
  "make": "[<class 'MakerClass'>]",
  "build": "[<class 'BuilderClass'>]"
}
Before make, MyBuilder.__dict__ is

   /{
   /  'DefaultInitBool' : True
   /}
NOW we build
We build here
After the build, MyBuilder.__dict__ is

   /{
   /  'BuiltMyStr' : My MadeMyInt is 3
   /  'DefaultInitBool' : True
   /  'MadeMyInt' : 3
   /  'MakingMyFloat' : 3.0
   /  '_WatchAfterBuildWithBuilderBool' : True
   /  '_WatchAfterMakeWithMakerBool' : True
   /  '_WatchBeforeBuildWithBuilderBool' : True
   /  '_WatchBeforeMakeWithMakerBool' : True
   /}
Now we switch
After the switch MyBuilder.__dict__ is

   /{
   /  'BuiltMyStr' : My MadeMyInt is 3
   /  'DefaultInitBool' : True
   /  'MadeMyInt' : 3
   /  'MakingMyFloat' : 3.0
   /  '_WatchAfterBuildWithBuilderBool' : False
   /  '_WatchAfterMakeWithMakerBool' : True
   /  '_WatchBeforeBuildWithBuilderBool' : False
   /  '_WatchBeforeMakeWithMakerBool' : True
   /}

Now an other trial,
Before make, MyBuilder.__dict__ is

   /{
   /  'DefaultInitBool' : True
   /}
We build here
After the build, MyBuilder.__dict__ is

   /{
   /  'BuiltMyStr' : My MadeMyInt is 3
   /  'DefaultInitBool' : True
   /  'MadeMyInt' : 3
   /  'MakingMyFloat' : 3.0
   /  '_WatchAfterBuildWithBuilderBool' : True
   /  '_WatchAfterMakeWithMakerBool' : True
   /  '_WatchBeforeBuildWithBuilderBool' : True
   /  '_WatchBeforeMakeWithMakerBool' : True
   /}
Now we switch
After the switch MyBuilder.__dict__ is

   /{
   /  'BuiltMyStr' : My MadeMyInt is 3
   /  'DefaultInitBool' : True
   /  'MadeMyInt' : 3
   /  'MakingMyFloat' : 3.0
   /  '_WatchAfterBuildWithBuilderBool' : True
   /  '_WatchAfterMakeWithMakerBool' : True
   /  '_WatchBeforeBuildWithBuilderBool' : True
   /  '_WatchBeforeMakeWithMakerBool' : False
   /}
After the final build, MyBuilder.__dict__ is

   /{
   /  'BuiltMyStr' : My MadeMyInt is 3
   /  'DefaultInitBool' : True
   /  'MadeMyInt' : 3
   /  'MakingMyFloat' : 3.0
   /  '_WatchAfterBuildWithBuilderBool' : True
   /  '_WatchAfterMakeWithMakerBool' : True
   /  '_WatchBeforeBuildWithBuilderBool' : True
   /  '_WatchBeforeMakeWithMakerBool' : False
   /}

```


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

        #Cast
        self.MadeMyInt=int(self.MakingMyFloat)

        #print
        print('self.MadeMyInt is ')
        print(self.MadeMyInt)

#Definition a MakerClass with decorated make by a Switcher
@SYS.SwitcherClass()
class BuilderClass(MakerClass):

    def default_init(self,
                ):
        MakerClass.__init__(self)


#print
print('BuilderClass.SwitchMethodDict is ')
print(SYS.indent(BuilderClass.SwitchMethodDict))

#Definition an instance
MyBuilder=BuilderClass()

#Print
print('Before make, MyBuilder.__dict__ is ')
SYS._print(MyBuilder.__dict__)

#print
print('MyBuilder.getSwitch()')
print(SYS.indent(MyBuilder.getSwitch()))

#make once
print('We make')
print(MyBuilder.make)
MyBuilder.make(3.)

#print
print('MyBuilder.getSwitch()')
print(SYS.indent(MyBuilder.getSwitch()))

#Print
print('After the make, MyBuilder.__dict__ is ')
SYS._print(MyBuilder.__dict__)

#make again
print('Now we switch')
MyBuilder.setSwitch()

#Switch by default it is just the last Name and the the last do in the mro
print('Now we switch')
MyBuilder.setSwitch('make')

#Print
print('After the switch MyBuilder.__dict__ is ')
SYS._print(MyBuilder.__dict__)




```


```console
>>>
BuilderClass.SwitchMethodDict is
{
  "make": "[<class 'MakerClass'>]"
}
Before make, MyBuilder.__dict__ is

   /{
   /  'DefaultInitBool' : True
   /}
MyBuilder.getSwitch()
{
  "WatchBeforeMakeWithMakerBool": "None",
  "WatchAfterMakeWithMakerBool": "None"
}
We make
<bound method BuilderClass.switch_watch_superDo_make of <BuilderClass object at
0x10c0c9210>>
self.MadeMyInt is
3
MyBuilder.getSwitch()
{
  "WatchBeforeMakeWithMakerBool": "True",
  "WatchAfterMakeWithMakerBool": "True"
}
After the make, MyBuilder.__dict__ is

   /{
   /  'DefaultInitBool' : True
   /  'MadeMyInt' : 3
   /  'MakingMyFloat' : 3.0
   /  '_WatchAfterMakeWithMakerBool' : True
   /  '_WatchBeforeMakeWithMakerBool' : True
   /}
Now we switch
Now we switch
After the switch MyBuilder.__dict__ is

   /{
   /  'DefaultInitBool' : True
   /  'MadeMyInt' : 3
   /  'MakingMyFloat' : 3.0
   /  '_WatchAfterMakeWithMakerBool' : False
   /  '_WatchBeforeMakeWithMakerBool' : False
   /}

```



<!--
FrozenIsBool False
-->

##Code

----

<ClassDocStr>

<small>
View the Switcher sources on <a href="https://github.com/Ledoux/ShareYourSystem/
tree/master/Pythonlogy/ShareYourSystem/Standards/Classors/Switcher"
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


The Switcher

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Classors.Watcher"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Tester"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import operator
import copy
from ShareYourSystem.Standards.Classors import Doer,Observer
#</ImportSpecificModules>

#<DefineFunctions>
def setSwitch(
                        _InstanceVariable,
                        _DoMethodVariable=None,
                        _DoerClassVariable=None,
                        _HookVariable=None
                ):

        #Debug
        '''
        print('l 31 setSwitch')
        print('_DoerVariable is ',_DoerVariable)
        print('_DoVariable is ',_DoVariable)
        print('_HookVariable is ',_HookVariable)
        #print('_InstanceVariable.__class__.NameStr is
',_InstanceVariable.__class__.NameStr)
        print('')
        '''

        #/#################/#
        # Adapt the shape of the do method str to switch
        #

        #Check
        if type(_DoMethodVariable)!=list:

                #Check
                if _DoMethodVariable==None:

                        #/#################/#
                        # Give all the do method str
                        #

                        #alias
                        #DoMethodStrsList=_InstanceVariable.DoMethodStrsList

                        #/#################/#
                        # Give just the last DoMethodStr
                        #

                        #Check
                        if _InstanceVariable.__class__.DoMethodStr in
_InstanceVariable.__class__.SwitchMethodDict:

                                #listify
DoMethodStrsList=[_InstanceVariable.__class__.DoMethodStr]

                        else:

                                #listify
                                DoMethodStrsList=[]

                else:

                        #listify
                        DoMethodStrsList=[_DoMethodVariable]


        else:

                #just alias
                DoMethodStrsList=_DoMethodVariable

        #/#################/#
        # Adapt the shape of the mro doer to switch
        #

        #get
        DoerClassesList=SYS.GetList(_DoerClassVariable)

        #Debug
        '''
        print('l 94 Switcher')
        print('_DoerClassVariable is')
        print(_DoerClassVariable)
        print('DoerClassesList is')
        print(DoerClassesList)
        print('')
        '''

        #Check
        if _DoerClassVariable==None:

                #/#################/#
                # by default this is all the mro doer that have all the switch
do method
                # so do the intersection

                #Check
                if len(DoMethodStrsList)>0:

                        #intersection
                        DoerClassesList=list(
                                set.intersection(*
                                        map(
                                                lambda __DoMethodStr:
set(_InstanceVariable.__class__.SwitchMethodDict[__DoMethodStr]),
                                                DoMethodStrsList
                                        )
                                )
                        )

                else:

                        #init
                        DoerClassesList=[]

        #/#################/#
        # Adapt the shape of the hook strs
        #

        #Check
        if type(_HookVariable)!=list:
                if _HookVariable==None:
                        HookStrsList=['Before','After']
                else:
                        HookStrsList=[_HookVariable]
        else:
                HookStrsList=_HookVariable


        #/#################/#
        # Now map the switch
        #

        #Debug
        '''
        print('l 139 Switcher')
        #print('_InstanceVariable is ')
        #print(_InstanceVariable)
        print('DoMethodStrsList is')
        print(DoMethodStrsList)
        print('DoerClassesList is ')
        print(DoerClassesList)
        print('HookStrsList is ')
        print(HookStrsList)
        print('')
        '''

        #map
        map(
                lambda __HookStr:
                map(
                        lambda __DoerClass:
                        map(
                                        lambda __DoMethodStr:
                                        _InstanceVariable.__setattr__(
'Watch'+__HookStr+__DoMethodStr[0].upper(
)+__DoMethodStr[1:]+'With'+__DoerClass.NameStr+'Bool',
                                                False
                                        ),
                                        DoMethodStrsList,
                                ),
                        DoerClassesList
                        ),
                HookStrsList
                )

        #Debug
        '''
        print('l 170 Switcher')
        print('End of setSwitch')
        print('')
        '''

        #return
        return _InstanceVariable

def switch(_InstanceVariable,*_LiargVariablesList,**_KwargVariablesDict):

        #Debug
        '''
        print('l 196 Switcher')
        print('In the switch function ')
        print('_KwargVariablesDict is ')
        print(_KwargVariablesDict)
        print('')
        '''

        """
        #alias
        FuncDict=switch.__dict__

        #Debug
        '''
        print('l 52')
        print('In the switch function ')
        print('FuncDict is ')
        print(FuncDict)
        print('')
        '''
        """

        #Check
        if
hasattr(_InstanceVariable,_KwargVariablesDict['WatchBeforeDoBoolKeyStr']):

                #Debug
                '''
                print('Switcher l 201')
                print('Check for a WatchBeforeDoBoolKeyStr')
                print("_KwargVariablesDict['WatchBeforeDoBoolKeyStr'] is ")
                print(_KwargVariablesDict['WatchBeforeDoBoolKeyStr'])
                print('')
                '''

                #get
                WatchDoBool=getattr(
                                _InstanceVariable,
                                _KwargVariablesDict['WatchBeforeDoBoolKeyStr']
                        )

                #Debug
                '''
                print('Switcher l 236')
                print('WatchDoBool is')
                print(WatchDoBool)
                '''

                #Switch
                if WatchDoBool:
                        return _InstanceVariable

        #get the wrapped method
        WrapUnboundMethod=getattr(
                getattr(
                        SYS,
                        _KwargVariablesDict['BindDoClassStr']
                ),
                _KwargVariablesDict['BindObserveWrapMethodStr']
        )

        #del
        map(
                        lambda __KeyStr:
                        _KwargVariablesDict.__delitem__(__KeyStr),
                        [
                                'BindObserveWrapMethodStr',
                                'BindDoClassStr',
                                'WatchBeforeDoBoolKeyStr'
                        ]
                )

        #Call
        return WrapUnboundMethod(
                _InstanceVariable,
                *_LiargVariablesList,
                **_KwargVariablesDict
        )

def getSwitch(_InstanceVariable,_MethodVariable=None):

        #Check
        if _MethodVariable==None:
                SwitchItemTuplesList=_InstanceVariable.SwitchMethodDict.items()
        elif type(_MethodVariable) in [list,tuple]:
                SwitchItemTuplesList=map(
                        lambda __MethodStr:
                        (
                                __MethodStr,
                                _InstanceVariable.SwitchMethodDict[__MethodStr]
                        ),
                        _MethodVariable
                )
        else:
                SwitchItemTuplesList=[
                        (
                                _MethodVariable,
_InstanceVariable.SwitchMethodDict[_MethodVariable]
                        )
                ]


        #Debug
        '''
        print('getSwitch l 266')
        print('_MethodVariable is ')
        print(_MethodVariable)
        print('SwitchItemTuplesList is ')
        print(SwitchItemTuplesList)
        print('')
        '''

        #return
        WatchKeyStrsList=SYS.flat(
                SYS.flat(
                        map(
                                lambda __SwitchItemTuple:
                                map(
                                        lambda __ClassStr:
                                        map(
                                                lambda __HookStr:
'Watch'+__HookStr+SYS.getUpperWordStr(
                                                        __SwitchItemTuple[0]
)+'With'+SYS.getNameStrWithClassStr(
                                                        __ClassStr
                                                )+'Bool',
                                                ['Before','After']
                                        ),
                                        map(lambda
__Class:__Class.__name__,__SwitchItemTuple[1])
                                ),
                                SwitchItemTuplesList
                        )
                )
        )

        #Debug
        '''
        print('getSwitch l 300')
        print('WatchKeyStrsList is ')
        print(WatchKeyStrsList)
        print('WatchKeyStrsList is ')
        print(WatchKeyStrsList)
        print('')
        '''

        #return
        return dict(
                                zip(
                                        WatchKeyStrsList,
                                        map(
                                                lambda __WatchKeyStr:
getattr(_InstanceVariable,__WatchKeyStr),
                                                WatchKeyStrsList
                                        )
                                )
                        )


#</DefineFunctions>

#<DefineClass>
@DecorationClass()
class SwitcherClass(BaseClass):

        #Definition
        RepresentingKeyStrsList=[
                'SwitchingIsBool',
                'SwitchingWrapMethodStr'
        ]

        def default_init(self,
                                                _SwitchingIsBool=False,
                                                _SwitchingWrapMethodStr="",
                                                **_KwargVariablesDict
                                ):

                #Call the parent init method
                BaseClass.__init__(self,**_KwargVariablesDict)

        def __call__(self,_Class):

                #Call the parent method
                Observer.ObserverClass.__bases__[0].__call__(self,_Class)

                #reset
                self.switch()

                #Return
                return _Class

        def do_switch(self):

                #Check
                if self.SwitchingIsBool:

                        #alias
                        SwitchedClass=self.DoClass

                        #Debug
                        '''
                        print('l 195 Switcher')
                        print('self.SwitchingWrapMethodStr is
'+self.SwitchingWrapMethodStr)
                        print('')
                        '''

                        #watch first
                        self.watch(
                                                True,
**{'ObservingWrapMethodStr':self.SwitchingWrapMethodStr}
                                        )

                        #Debug
                        '''
                        print('l 204 Switcher')
                        print('self.WatchedDecorationMethodStr is
',self.WatchedDecorationMethodStr)
                        print('')
                        '''

                        #first bind
                        self.bind(
                                                True,
                                                switch,
                                                "",
                                                switch.__name__,
[('WatchBeforeDoBoolKeyStr',self.WatchedBeforeDoBoolKeyStr)],
**{'ObservingWrapMethodStr':self.WatchedDecorationMethodStr}
                                        )

                        #Define
                        SwitchedDecorationUnboundMethod=getattr(
                                                SwitchedClass,
                                                self.BindedDecorationMethodStr
                                        )

                        #Now make the amalgam
                        setattr(
                                        SwitchedClass,
                                        self.SwitchingWrapMethodStr,
                                        SwitchedDecorationUnboundMethod
                                )

                        #/##################/#
                        # Set maybe for the first time
                        # the setSwitch and the getSwitch

                        #Check
                        if hasattr(SwitchedClass,'setSwitch')==False:

                                #set
                                setattr(
                                                SwitchedClass,
                                                setSwitch.__name__,
                                                setSwitch
                                        )

                                #get the unbound
                                setSwitchUnboundMethod=getattr(
                                        SwitchedClass,
                                        setSwitch.__name__
                                )

                                #add in the inspect
SwitchedClass.InspectMethodDict[setSwitch.__name__]=setSwitchUnboundMethod
SwitchedClass.InspectInspectDict[setSwitch.__name__]=SYS.InspectDict(
                                        setSwitchUnboundMethod
                                )

                                #set
                                self.setMethod(
                                        getSwitch.__name__,
                                        getSwitch
                                )

                        #/##################/#
                        # Init the SwitchMethodDict
                        #

                        #Check
                        if hasattr(SwitchedClass,'SwitchMethodDict')==False:

                                #Debug
                                '''
                                print('Switcher l 345')
                                print('SwitchedClass is ')
                                print(SwitchedClass)
                                print('we init a SwitchMethodDict')
                                print('')
                                '''

                                #Check
                                if
hasattr(SwitchedClass.__bases__[0],'SwitchMethodDict'):

                                        #Debug
                                        print('Switcher l 488')
                                        print('SwitchedClass is ')
                                        print(SwitchedClass)
                                        print('SwitchedClass.__bases__[0] is ')
                                        print(SwitchedClass.__bases__[0])
                                        print('')

                                        #copy
SwitchedClass.SwitchMethodDict=copy.copy(
SwitchedClass.__bases__[0].SwitchMethodDict
                                        )

                                else:

                                        #init
                                        SwitchedClass.SwitchMethodDict={
self.SwitchingWrapMethodStr:[SwitchedClass]
                                        }

                        else:

                                #/##################/#
                                # add
                                #

                                #Debug
                                '''
                                print('Switcher l 514')
                                print('SwitchedClass is ')
                                print(SwitchedClass)
                                print('there is already a SwitchMethodDict')
                                print('self.SwitchingWrapMethodStr  is ')
                                print(self.SwitchingWrapMethodStr)
                                print('SwitchedClass.SwitchMethodDict is ')
                                print(SwitchedClass.SwitchMethodDict)
                                print('')
                                '''

                                #copy
                                SwitchedClass.SwitchMethodDict=copy.copy(
                                        SwitchedClass.SwitchMethodDict
                                )

                                #update
                                if self.SwitchingWrapMethodStr in
self.DoClass.SwitchMethodDict:
                                        SwitchedClass.SwitchMethodDict[
                                                self.SwitchingWrapMethodStr
                                        ].append(SwitchedClass)
                                else:
                                        SwitchedClass.SwitchMethodDict[
                                                self.SwitchingWrapMethodStr
                                        ]=[SwitchedClass]

                        #Add to the KeyStrsList
                        SwitchedClass.KeyStrsList+=[
'SwitchMethodDict'
                                                                ]



#</DefineClass>


```


