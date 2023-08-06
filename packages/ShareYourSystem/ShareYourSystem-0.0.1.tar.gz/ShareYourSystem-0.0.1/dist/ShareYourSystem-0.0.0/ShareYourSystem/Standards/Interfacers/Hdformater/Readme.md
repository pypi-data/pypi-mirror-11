

<!--
FrozenIsBool False
-->

#Hdformater

##Doc
----


>
> An Hdformater instance maps an apply and so "grinds" a MappingArgDictsList
> to a method.
>
>

----

<small>
View the Hdformater notebook on [NbViewer](http://nbviewer.ipython.org/url/share
yoursystem.ouvaton.org/Hdformater.ipynb)
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


An Hdformater instance maps an apply and so "grinds" a MappingArgDictsList
to a method.

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Interfacers.Writer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import collections
import importlib
import os
import sys
#from ShareYourSystem.Functers import Alerter
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass(**{'SwitchingUnboundMethodStr':'hdformat'})
class HdformaterClass(BaseClass):

        #Definition
        RepresentingKeyStrsList=[
'HdformatingModuleStr',
'HdformatingFileKeyStr',
'HdformatedFileVariable',
'HdformatedConsoleStr'
                                                                ]

        #@Hooker.HookerClass(**{'HookingAfterVariablesList':[{'CallingVariable':
BaseClass.__init__}]})
        def default_init(self,
                        _HdformatingModuleStr="tables",
                        _HdformatingFileKeyStr="",
                        _HdformatedFileVariable=None,
                        _HdformatedFilePathStr="",
                        _HdformatedConsoleStr="",
                        **_KwargVariablesDict
                ):

                #Call the parent __init__ method
                BaseClass.__init__(self,**_KwargVariablesDict)

        #@Alerter.AlerterClass()
        #@Switcher.SwitcherClass()
        def do_hdformat(self):

                #debug
                '''
                self.debug(('self.',self,[
'HdformatingFileKeyStr'
                                                                ]))
                '''

                #Check
                if self.HdformatedFileVariable==None:

                        #folder first
                        self.folder()

                        #set
self.HdformatedFilePathStr=self.FolderingPathVariable+self.HdformatingFileKeyStr

                        #Maybe we have to import
                        if self.HdformatingModuleStr not in sys.modules:

                                #debug
                                '''
                                self.debug('We import first the hdf module')
                                '''

                                #Import
importlib.import_module(self.HdformatingModuleStr)

                        #Check
                        if self.HdformatingFileKeyStr!="":

                                #Check for first write
                                if
os.path.isfile(self.HdformatedFilePathStr)==False:

                                        #debug
                                        '''
                                        self.debug('We create the file first')
                                        '''

                                        #Create the file
self.HdformatedFileVariable=sys.modules[self.HdformatingModuleStr].File(
self.HdformatedFilePathStr,'w')

                                        #Close it
                                        self.HdformatedFileVariable.close()

                                if self.HdformatedFileVariable==None or (
                                        (self.HdformatingModuleStr=='tables' and
self.HdformatedFileVariable.isopen==0
                                                ) or
(self.HdformatingModuleStr=='h5py' and self.HdformatedFileVariable.mode=='c') ):

                                        #debug
                                        '''
                                        self.debug('We open the file')
                                        '''

                                        #Open the HdformatedFileVariable
self.HdformatedFileVariable=sys.modules[self.HdformatingModuleStr].File(
                                                self.HdformatedFilePathStr,'r+')

                #Return self
                #return self

        def hdfview(self):

                #debug
                '''
                self.debug(('self.',self,['HdformatingFilePathStr']))
                '''

                if self.HdformatedFilePathStr!="":

                        #set the HdformatedConsoleStr
                        self.HdformatedConsoleStr=os.popen(
SYS.h5lsPathStr+' -dlr '+self.HdformatedFilePathStr
                                                                ).read()

                #Return self
                return self

        def hdfclose(self):

                #Close the HdformatedFileVariable
                if self.HdformatedFileVariable!=None:
                        self.HdformatedFileVariable.close()

                #Return self
                return self

#</DefineClass>


```

<small>
View the Hdformater sources on <a href="https://github.com/Ledoux/ShareYourSyste
m/tree/master/Pythonlogy/ShareYourSystem/Interfacers/Hdformater"
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
from ShareYourSystem.Standards.Interfacers import Hdformater

#Definition a Hdformater that writes an empty hdf file
MyHdformater=Hdformater.HdformaterClass().hdformat(
    _FileKeyStr='Hdformats.hdf5',
    **{
    'FolderingPathVariable':Hdformater.LocalFolderPathStr
}
).hdfview().hdfclose()

#Definition the AttestedStr
SYS._attest(
    [
        'MyHdformater.HdformatedConsoleStr is '+str(
            MyHdformater.HdformatedConsoleStr)
    ]
)

#Print





```


```console
>>>


*****Start of the Attest *****

MyHdformater.HdformatedConsoleStr is /                        Group


*****End of the Attest *****



```

