

<!--
FrozenIsBool False
-->

#Watcher

##Doc
----


>
> The Watcher
>
>

----

<small>
View the Watcher notebook on [NbViewer](http://nbviewer.ipython.org/url/shareyou
rsystem.ouvaton.org/Watcher.ipynb)
</small>




<!---
FrozenIsBool True
-->

##Example

Here we watch a MakerClass that sets its WatchBeforeMakeWithMaker and
WatchAfterMakeWithMaker when the make method is called.
Also we can already set reactive method when these properties change.

```python
#ImportModules
import ShareYourSystem as SYS

#Definition a MakerClass with decorated make by a Watcher
@SYS.WatcherClass(**{
    'WatchingIsBool':True,
    #'ObservingWrapMethodStr':'do_make'
    #'ObservingWrapMethodStr':'superDo_make'
    'ObservingWrapMethodStr':'make'
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

    def setWatchAfterMakeWithMakerBool(self,_SettingValueVariable):

        #set
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


#Definition an instance
MyMaker=MakerClass()

#Print
print('Before make, MyMaker.__dict__ is ')
SYS._print(MyMaker.__dict__)

#make once
MyMaker.make(3.)

#print
print('After the first make, MyMaker.__dict__ is ')
SYS._print(MyMaker.__dict__)

#print
print('MakerClass.make is '+str(MakerClass.make))

#Check that the watch_superDo_make has access to the BaseDoClass
print('MakerClass.make.BaseDoClass is ')
print(MakerClass.make.BaseDoClass)


```


```console
>>>
Before make, MyMaker.__dict__ is

   /{
   /  'DefaultInitBool' : True
   /}
After the first make, MyMaker.__dict__ is

   /{
   /  'DefaultInitBool' : True
   /  'MadeMyInt' : 3
   /  'MakingMyFloat' : 3.0
   /  '_WatchAfterMakeWithMakerBool' : True
   /  '_WatchBeforeMakeWithMakerBool' : True
   /}
MakerClass.make is <unbound method MakerClass.watch_superDo_make>
MakerClass.make.BaseDoClass is
<class 'MakerClass'>

```



<!---
FrozenIsBool True
-->

##Example

Check the good way to watch methods that are derived from other base classes

```python
#ImportModules
import ShareYourSystem as SYS

#Definition a MakerClass with decorated make by a Watcher
@SYS.WatcherClass(**{
    'WatchingIsBool':True,
    #'ObservingWrapMethodStr':'do_make'
    #'ObservingWrapMethodStr':'superDo_make'
    'ObservingWrapMethodStr':'make'
    })
class MakerClass(object):

    #Definition
    RepresentingKeyStrsList=[
                                'MakingMyFloat',
                                'MadeMyInt'
                            ]

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

#Definition a MakerClass with decorated make by a Watcher
@SYS.WatcherClass(**{
    'WatchingIsBool':True,
    #'ObservingWrapMethodStr':'do_make'
    #'ObservingWrapMethodStr':'superDo_make'
    'ObservingWrapMethodStr':'make'
    })
class BuilderClass(MakerClass):

    #Definition
    RepresentingKeyStrsList=[
                            ]

    def default_init(self,
                ):
        MakerClass.__init__(self)

    def do_buid(self):
        pass

#Definition an instance
MyBuilder=MakerClass()

#Print
print('Before make, MyBuilder is ')
SYS._print(MyBuilder)

#make once
MyBuilder.make(3.)

#Print
print('After the first make, MyBuilder is ')
SYS._print(MyBuilder)

#Definition the AttestedStr
print('BuilderClass.make is '+str(BuilderClass.make))
print('MyBuilder.__dict__ is ')
print(SYS.indent(MyBuilder.__dict__))



```


```console
>>>
Before make, MyBuilder is
<MakerClass object at 0x10c09a8d0>
self.MakingMyFloat is 3.0
self.MadeMyInt is 0

After the first make, MyBuilder is
<MakerClass object at 0x10c09a8d0>
BuilderClass.make is <unbound method BuilderClass.watch_superDo_make>
MyBuilder.__dict__ is
{
  "MakingMyFloat": "3.0",
  "_WatchBeforeMakeWithMakerBool": "True",
  "DefaultInitBool": "True",
  "_WatchAfterMakeWithMakerBool": "True",
  "MadeMyInt": "3"
}

```



<!--
FrozenIsBool False
-->

##Code

----

<ClassDocStr>

<small>
View the Watcher sources on <a href="https://github.com/Ledoux/ShareYourSystem/t
ree/master/Pythonlogy/ShareYourSystem/Standards/Classors/Watcher"
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


The Watcher

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Classors.Binder"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Tester"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import operator
import copy
from ShareYourSystem.Standards.Classors import Doer,Propertiser,Observer
from ShareYourSystem.Standards.Interfacers import Printer
Binder=BaseModule
#</ImportSpecificModules>

#<DefineLocals>
WatchingPrefixKeyStr="Watch"
#</DefineLocals>

#<SetRepresent>
def getIsBoolWithItemTupleAndPrefixStr(_ItemTuple,_PrefixStr):

        #Debug
        '''
        print('Watcher l 35')
        print('_ItemTuple is ',_ItemTuple)
        print('_PrefixStr is ',_PrefixStr)
        print('')
        '''

        #Return
        return _ItemTuple[0].split('>')[-1].startswith(_PrefixStr)
#</SetRepresent>

#<DefineFunctions>
def watch(_InstanceVariable,*_LiargVariablesList,**_KwargVariablesDict):

        #Debug
        '''
        print('l 67')
        print('In the watch function ')
        print('_KwargVariablesDict is ')
        print(_KwargVariablesDict)
        print('')
        '''

        """
        #alias
        FuncDict=_InstanceVariable.__class__.watch.__dict__

        #Debug
        '''
        print('l 79')
        print('In the watch function ')
        print('FuncDict is ')
        print(FuncDict)
        print('')
        '''
        """

        #Set in the _InstanceVariable
        _InstanceVariable.__setattr__(
                        _KwargVariablesDict['WatchBeforeDoBoolKeyStr'],
                        True
                )

        #get the wrapped method
        WrapUnboundMethod=getattr(
                getattr(
                        SYS,
                        _KwargVariablesDict['BindDoClassStr']
                ),
                _KwargVariablesDict['BindObserveWrapMethodStr']
        )

        #del
        WatchAfterDoBoolKeyStr=_KwargVariablesDict['WatchAfterDoBoolKeyStr']
        map(
                        lambda __KeyStr:
                        _KwargVariablesDict.__delitem__(__KeyStr),
                        [
                                'BindObserveWrapMethodStr',
                                'BindDoClassStr',
                                'WatchBeforeDoBoolKeyStr',
                                'WatchAfterDoBoolKeyStr'
                        ]
                )

        #Call
        OutputVariable=WrapUnboundMethod(
                _InstanceVariable,
                *_LiargVariablesList,
                **_KwargVariablesDict
        )

        #Set in the _InstanceVariable
        _InstanceVariable.__setattr__(
                        WatchAfterDoBoolKeyStr,
                        True
                )

        #return
        return OutputVariable

#</DefineFunctions>

#<DefineClass>
@DecorationClass()
class WatcherClass(BaseClass):

        def default_init(self,
                                                _WatchingIsBool=False,
                                                _WatchedBeforeDoBoolKeyStr="",
                                                _WatchedAfterDoBoolKeyStr="",
                                                _WatchedDecorationMethodStr="",
                                                **_KwargVariablesDict
                                ):

                #Call the parent init method
                BaseClass.__init__(self,**_KwargVariablesDict)

        def __call__(self,_Class):

                #debug
                '''
                print('Watcher l.139 __call__ method')
                print('_Class is ',_Class)
                print('')
                '''

                #Call the parent method
                Observer.ObserverClass.__bases__[0].__call__(self,_Class)

                #Watch
                self.watch()

                #Return
                return _Class

        def do_watch(self):

                #Check
                if self.WatchingIsBool:

                        #Debug
                        '''
                        print('l 133 Watcher')
                        print('self.ObservingWrapMethodStr is
'+self.ObservingWrapMethodStr)
                        print('')
                        '''

                        #Keep the old value
                        self.WatchedWrapMethodStr=self.ObservingWrapMethodStr

                        #observe first
                        self.observe(
                                                        True
                                                )

                        #Debug
                        '''
                        print('l 171 Watcher')
                        print('self.ObservedWrapMethodStr is
',self.ObservedWrapMethodStr)
                        '''

                        #Check
                        if self.ObservedWrapMethodStr.startswith(
                                watch.__name__+Binder.BindingDecorationSuffixStr
                        )==False:

                                #Debug
                                '''
                                print('l 173 this is a new watch method')
                                print('')
                                '''

                                #Define
                                WatchedDoMethodStr=self.WatchedWrapMethodStr
WatchedDoStr=WatchedDoMethodStr[0].upper()+WatchedDoMethodStr[1:]
self.WatchedBeforeDoBoolKeyStr=WatchingPrefixKeyStr+'Before'+WatchedDoStr
self.WatchedBeforeDoBoolKeyStr+='With'+self.DoClass.NameStr
                                self.WatchedBeforeDoBoolKeyStr+='Bool'
self.WatchedAfterDoBoolKeyStr=WatchingPrefixKeyStr+'After'+WatchedDoStr
self.WatchedAfterDoBoolKeyStr+='With'+self.DoClass.NameStr
                                self.WatchedAfterDoBoolKeyStr+='Bool'

                                #set
                                WatchedIsInitBool=True

                                #Check
                                if hasattr(self.DoClass,'ResetDoBoolKeyStr'):
                                        if
self.WatchedBeforeDoBoolKeyStr!=self.DoClass.ResetDoBoolKeyStr:
                                                WatchedIsInitBool=False

                                #Check
                                if WatchedIsInitBool:

                                        #WARNING this cancels the reset property
binding before
                                        #Set already in the class but also check
if a property was not already setted
                                        if
hasattr(self.DoClass,self.WatchedBeforeDoBoolKeyStr)==False:

                                                #Debug
                                                '''
                                                print('Watcher')
                                                print('self.DoClass is
'+str(self.DoClass))
print('self.WatchedBeforeDoBoolKeyStr is '+self.WatchedBeforeDoBoolKeyStr)
                                                print('Set it to False')
                                                print('')
                                                '''

                                                '''
                                                #If we want just to init it as a
Bool....
                                                #set
                                                setattr(
                                                                self.DoClass,
self.WatchedBeforeDoBoolKeyStr,
                                                                False
                                                        )
                                                '''

                                                #...Better to init it as a
property to facilite the reactivity setting after
[PropertizedKeyStr,PropertizedValueVariable
]=Propertiser.getPropertizedTupleWithItemTupleAndClass(
                                                        (
self.WatchedBeforeDoBoolKeyStr,
                                                                {
'DefaultValueType':property,
'PropertyInitVariable':False,
'PropertyDocStr':'I am watching before'
                                                                }
                                                        ),
                                                        self.DoClass
                                                )

                                                #Debug
                                                '''
                                                print('Watcher l 235')
                                                print('PropertizedKeyStr is ')
                                                print(PropertizedKeyStr)
                                                print('PropertizedValueVariable
is ')
                                                print(PropertizedValueVariable)
                                                print('')
                                                '''

                                                #set
                                                setattr(
                                                                self.DoClass,
PropertizedKeyStr,
PropertizedValueVariable
                                                        )

                                        else:

                                                #Debug
                                                '''
                                                print('There is already a
property here for ')
                                                print('self.DoClass is
'+str(self.DoClass))
print('self.WatchedBeforeDoBoolKeyStr is '+self.WatchedBeforeDoBoolKeyStr)
                                                print('')
                                                '''

                                        #WARNING this cancels the reset property
binding before
                                        #Set already in the class but also check
if a property was not already setted
                                        if
hasattr(self.DoClass,self.WatchedAfterDoBoolKeyStr)==False:

                                                #Debug
                                                '''
                                                print('Watcher')
                                                print('self.DoClass is
'+str(self.DoClass))
print('self.WatchedAfterDoBoolKeyStr is '+self.WatchedAfterDoBoolKeyStr)
                                                print('Set it to False')
                                                print('')
                                                '''

                                                #set
                                                #If we want just to init it as a
Bool....
                                                '''
                                                setattr(
                                                                self.DoClass,
self.WatchedAfterDoBoolKeyStr,
                                                                False
                                                        )
                                                '''

                                                #...Better to init it as a
property to facilite the reactivity setting after
                                                [
PropertizedKeyStr,PropertizedValueVariable
]=Propertiser.getPropertizedTupleWithItemTupleAndClass(
                                                        (
self.WatchedAfterDoBoolKeyStr,
                                                                {
'DefaultValueType':property,
'PropertyInitVariable':False,
'PropertyDocStr':'I am watching after'
                                                                }
                                                        ),
                                                        self.DoClass
                                                )

                                                #Debug
                                                '''
                                                print('Watcher l304')
                                                print('PropertizedKeyStr is ')
                                                print(PropertizedKeyStr)
                                                print('PropertizedValueVariable
is ')
                                                print(PropertizedValueVariable)
                                                print('')
                                                '''

                                                #set
                                                setattr(
                                                                self.DoClass,
PropertizedKeyStr,
PropertizedValueVariable
                                                        )

                                        else:

                                                #Debug
                                                '''
                                                print('There is already a
property here for ')
                                                print('self.DoClass is
'+str(self.DoClass))
print('self.WatchedAfterDoBoolKeyStr is '+self.WatchedAfterDoBoolKeyStr)
                                                print('')
                                                '''

                                        #append in the skip repr
                                        if
hasattr(self.DoClass,'PrintingClassSkipKeyStrsList'):

                                                #extend
self.DoClass.PrintingClassSkipKeyStrsList.extend(
                                                        [
self.WatchedBeforeDoBoolKeyStr,
self.WatchedAfterDoBoolKeyStr,
Propertiser.PropertyGetStr+self.WatchedBeforeDoBoolKeyStr,
Propertiser.PropertyGetStr+self.WatchedAfterDoBoolKeyStr
                                                        ]
                                                )

                                                #Debug
                                                '''
                                                print('Defaultor l 233')
                                                print('self.DoClass is ')
                                                print(self.DoClass)
print('self.DoClass.PrintingClassSkipKeyStrsList is ')
print(self.DoClass.PrintingClassSkipKeyStrsList)
                                                print('')
                                                '''


                                #Debug
                                '''
                                print('l 145 Watcher')
                                print('WatchedDoMethodStr is
',WatchedDoMethodStr)
                                print('WatchedDoStr is ',WatchedDoStr)
                                print('self.WatchedBeforeDoBoolKeyStr is
',self.WatchedBeforeDoBoolKeyStr)
                                print('')
                                '''

                                #first bind
                                self.bind(
                                                        True,
                                                        watch,
                                                        "",
                                                        watch.__name__,
                                                        [
('WatchBeforeDoBoolKeyStr',self.WatchedBeforeDoBoolKeyStr),
('WatchAfterDoBoolKeyStr',self.WatchedAfterDoBoolKeyStr)
                                                        ],
**{'ObservingWrapMethodStr':self.ObservedWrapMethodStr}
                                                )

                                #set
self.WatchedDecorationMethodStr=self.BindedDecorationMethodStr

                                #Now make the amalgam
                                self.setMethod(
                                                WatchedDoMethodStr,
self.BindedDecorationUnboundMethod
                                        )

                        else:

                                #set
self.WatchedDecorationMethodStr=self.ObservedWrapMethodStr

#</DefineClass>

```


