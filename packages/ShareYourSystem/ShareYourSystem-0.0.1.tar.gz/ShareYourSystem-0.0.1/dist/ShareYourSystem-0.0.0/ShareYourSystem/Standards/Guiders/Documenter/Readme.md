

<!--
FrozenIsBool False
-->

#Documenter

##Doc
----


>
> The Documenter
>
>

----

<small>
View the Documenter notebook on [NbViewer](http://nbviewer.ipython.org/url/shareyo
ursystem.ouvaton.org/Documenter.ipynb)
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


The Documenter

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Guiders.Documenter"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import collections
import os
import copy
import sys
from ShareYourSystem.Standards.Classors import Doer
from ShareYourSystem.Guiders import Celler
Readmer=BaseModule
#</ImportSpecificModules>

#<DefineLocals>
DocumentingOntologyLocalFolderPathStr=SYS.ShareYourSystemLocalFolderPathStr+'Ouvat
on/'
DocumentingNbviewerLocalFolderPathStr=SYS.ShareYourSystemLocalFolderPathStr+'Ouvat
on/'
DocumentingDocumentLocalFolderPathStr=SYS.ShareYourSystemLocalFolderPathStr+'docs/
LibraryReference/'
DocumentingOntologyOuvatonFolderPathStr='/httpdocs/slides/'
DocumentingNbviewerOuvatonFolderPathStr='/httpdocs/ipython/'
#</DefineLocals>

#<DefineFunctions>
def getDocumentedReadmeInstanceVariableWithFolderPathStr(
                _InstanceVariable,_FolderPathStr
        ):

        #file first
        return _InstanceVariable.notebook(
                        **{
                                'FolderingPathVariable':_FolderPathStr,
                                'GuidingBookStr':"Doc",
                                'NotebookingFileKeyStr':"Presentation.ipynb"
                        }
        ).nbconvert("Readme.md")
#</DefineFunctions>


#<DefineClass>
@DecorationClass()
class DocumenterClass(BaseClass):

        #Definition
        RepresentingKeyStrsList=[
'DocumentingConceptFolderPathStr',
'DocumentingSubReadmeIsBool',
'DocumentingConceptReadmeIsBool',
'DocumentingConceptDocumentIsBool',
'DocumentingConceptSlideIsBool',
'DocumentingSiteDocumentIsBool',
'DocumentedConceptModule',
'DocumentedConceptModuleStr',
'DocumentedConceptModuleFolderPathStr',
'DocumentedSubNameStrsList',
'DocumentedSubModulesList',
'DocumentedSubModuleStrsList',
'DocumentedSubModuleLocalFolderPathStrsList',
#'DocumentedPresentationsDictsList',
#'DocumentedConceptNotebookDict'
                                                        ]

        def default_init(self,
_DocumentingConceptFolderPathStr="",
                                                _DocumentingSubReadmeIsBool=True,
_DocumentingConceptReadmeIsBool=True,
_DocumentingConceptDocumentIsBool=True,
_DocumentingConceptSlideIsBool=True,
_DocumentingSiteDocumentIsBool=True,
                                                _DocumentedConceptModule=None,
                                                _DocumentedConceptModuleStr="",
_DocumentedConceptModuleFolderPathStr="",
                                                _DocumentedSubNameStrsList=None,
                                                _DocumentedSubModulesList=None,
                                                _DocumentedSubModuleStrsList=None,
_DocumentedSubModuleLocalFolderPathStrsList=None,
_DocumentedPresentationsDictsList=None,
_DocumentedConceptNotebookDict=None,
                                                **_KwargVariablesDict
                                        ):

                #Call the parent __init__ method
                BaseClass.__init__(self,**_KwargVariablesDict)

        def do_inform(self):

                #debug
                '''
                self.debug(('self.',self,['DocumentingSubReadmeIsBool','DocumentingC
onceptDocumentIsBool']))
                '''

                #install first
                self.install()

                #Check
                if self.DocumentingConceptFolderPathStr=="":
self.DocumentingConceptFolderPathStr='ShareYourSystem'.join(
                                os.getcwd().split('ShareYourSystem')[:-1]
                        )+'ShareYourSystem/'

                #debug
                '''
                self.debug(('self.',self,['DocumentingConceptFolderPathStr']))
                '''

                #debug
                self.folder(self.DocumentingConceptFolderPathStr)
                self.DocumentedConceptModuleStr=self.FolderedModuleStr

                #debug
                '''
                self.debug(('self.',self,[
'FolderedModuleStr',
'FolderedDirKeyStrsList'
                                                                ]))
                '''

                #filter
                self.DocumentedSubNameStrsList=SYS._filter(
                        lambda __FolderedDirKeyStr:
                        os.path.isdir(
                                self.FolderingPathVariable+__FolderedDirKeyStr
                        ) and __FolderedDirKeyStr in
Doer.DoerStrToDoStrOrderedDict.keys(),
                        self.FolderedDirKeyStrsList
                )

                #debug
                '''
self.debug(('self.',self,['DocumentedSubNameStrsList','InstalledNameStrsList']))
                '''

                #sort
                self.DocumentedSubNameStrsList=SYS._filter(
                                lambda __InstalledNameStr:
                                __InstalledNameStr in
self.DocumentedSubNameStrsList,
                                self.InstalledNameStrsList
                        )
                #map
                self.DocumentedSubModuleStrsList=map(
                        lambda __DocumentedSubNameStr:
                        self.DocumentedConceptModuleStr+'.'+__DocumentedSubNameStr,
                        self.DocumentedSubNameStrsList
                )

                #Check
                self.DocumentedConceptNameStr=self.FolderingPathVariable.split(
                                        '/'
                        )[-1] if self.FolderingPathVariable[-1]!='/' else
self.FolderingPathVariable.split('/'
                        )[-2]

                #debug
                '''
                self.debug(('self.',self,[
'DocumentedSubNameStrsList',
'DocumentedSubModuleStrsList',
'DocumentedConceptNameStr'
                                                                ]))
                '''

                #check
                if self.DocumentedConceptNameStr in
SYS.PluralStrToSingularStrOrderedDict.keys():

                        #package
                        self.DocumentedConceptModule=self.package(
                                self.FolderedModuleStr
                        ).PackagedModuleVariable

                #join
                self.DocumentedConceptModuleFolderPathStr='/'.join(
                        self.DocumentedConceptModule.__file__.split(
                        '/'
                        )[:-1]
                )+'/'

                #debug
                '''
                self.debug(('self.',self,['DocumentedConceptModule']))
                '''

                #filter
                self.DocumentedSubModulesList=SYS._filter(
                                lambda __AttributeValueVariable:
type(__AttributeValueVariable).__name__=='module',
                                self.DocumentedConceptModule.__dict__.values()
                        )

                #debug
                '''
                self.debug((
                                        'self.',self,[
                                                        'DocumentedSubModulesList'
                                                ]
                                        ))
                '''

                #Check
                if self.DocumentingSubReadmeIsBool:

                        #debug
                        '''
                        self.debug(
                                                [
                                                        'we build sub modules
readmes here',
('self.',self,['DocumentedSubModuleStrsList'])
                                                ]
                                        )
                        '''

                        #map
                        map(
                                        lambda __DocumentedSubModuleStr:
                                        self.package(
                                                        __DocumentedSubModuleStr
                                                ).scriptbook(
                                                _GuideTuplesList=[
('001','Document','Markdown'),
                                                        ],
                                                        **{
'GuidingBookStr':"Doc",
                                                        }
                                                ).notebook(
                                                        "PreReadme.ipynb"
                                                ).nbconvert(
                                                        "Readme.md"
                                                ),
                                        self.DocumentedSubModuleStrsList
                                )

                #Check
                if self.DocumentingConceptSlideIsBool:

                        #debug
                        '''
                        self.debug(
                                                [
                                                        'we slide here',
('self.',self,['DocumentedSubModuleStrsList'])
                                                ]
                                                )
                        '''

                        #map
                        map(
                                        lambda __DocumentedSubModuleStr:
                                        self.package(
                                                        __DocumentedSubModuleStr
                                                ).scriptbook(
                                                _GuideTuplesList=[
('001','Document','Markdown'),
('002','Github','Markdown'),
                                                        ],
                                                        **{
'GuidingBookStr':"Doc",
                                                        }
                                                ).notebook(
                                                        "Presentation.ipynb",
**{'WritingLoadBool':False}
                                                ).nbconvert(
                                                        "Presentation.html",
                                                        'Slide'
                                                ),
                                        self.DocumentedSubModuleStrsList
                                )

                        #mv for Nbviewer ipython notebooks
                        map(
                                        lambda __DocumentedSubModuleStr:
                                        os.popen(
                                                'cp '+sys.modules[
                                                        __DocumentedSubModuleStr
].LocalFolderPathStr+'Presentation.ipynb
'+DocumentingNbviewerLocalFolderPathStr+__DocumentedSubModuleStr.split(
                                                                '.'
                                                        )[-1]+'.ipynb'
                                        ),
                                        self.DocumentedSubModuleStrsList
                                )

                        #mv for Ouvaton slide in html
                        map(
                                        lambda __DocumentedSubModuleStr:
                                        os.popen(
                                                'cp '+sys.modules[
                                                        __DocumentedSubModuleStr
].LocalFolderPathStr+'Presentation.html
'+DocumentingOntologyLocalFolderPathStr+__DocumentedSubModuleStr.split(
                                                                '.'
                                                        )[-1]+'.html'
                                        ),
                                        self.DocumentedSubModuleStrsList
                                )

                        #mv for Ouvaton slide in php
                        map(
                                        lambda __DocumentedSubModuleStr:
                                        os.popen(
                                                'cp '+sys.modules[
                                                        __DocumentedSubModuleStr
].LocalFolderPathStr+'Presentation.html
'+DocumentingOntologyLocalFolderPathStr+__DocumentedSubModuleStr.split(
                                                                '.'
                                                        )[-1]+'.php'
                                        ),
                                        self.DocumentedSubModuleStrsList
                                )

                        #map
                        self.DocumentedSubModuleLocalFolderPathStrsList=map(
                                        lambda __DocumentedSubModuleStr:
SYS.PythonlogyLocalFolderPathStr+__DocumentedSubModuleStr.replace(
                                                '.','/'
                                        ),
                                        self.DocumentedSubModuleStrsList
                                )

                        #map
                        self.DocumentedPresentationsDictsList=map(
                                        lambda __DocumentedSubModuleFolderPathStr:
                                        self.load(
                                                **{
'FolderingPathVariable':__DocumentedSubModuleFolderPathStr,
'FilingKeyStr':'Presentation.ipynb',
'LoadingFormatStr':'json'
                                                }
                                        ).close(
                                        ).LoadedReadVariable,
self.DocumentedSubModuleLocalFolderPathStrsList
                                )

                        #debug
                        '''
                        self.debug(
'self.DocumentedPresentationsDictsList is
'+SYS._str(self.DocumentedPresentationsDictsList)
                                        )
                        '''

                        #copy
self.DocumentedConceptNotebookDict=copy.copy(Celler.CellingInitDict)

                        #flat
                        DocumentedFlatPresentationsDictsList=SYS.flat(
                                        map(
                                                        lambda
__DocumentedPresentationsDict:
                                                        copy.deepcopy(
__DocumentedPresentationsDict['worksheets'][0]['cells']
                                                                ),
self.DocumentedPresentationsDictsList
                                                )
                                        )

                        #Flat all the presentations
                        self.DocumentedConceptNotebookDict['worksheets']=[
                                {
                                        'cells':map(
                                                lambda
__DocumentedFlatPresentationsDict,__IndexInt:
dict(__DocumentedFlatPresentationsDict,**{
'prompt_number':__IndexInt}),
DocumentedFlatPresentationsDictsList,
xrange(len(DocumentedFlatPresentationsDictsList))
                                        )
                                }
                        ]

                        #debug
                        '''
self.debug(('self.',self,['DocumentedConceptNotebookDict']))
                        '''

                        #Write
                        self.write(
                                self.DocumentedConceptNotebookDict,
                                **{
'FolderingPathVariable':self.DocumentingConceptFolderPathStr,
'FilingKeyStr':'Concept'+self.GuidingBookStr+'.ipynb',
                                        'LoadingFormatStr':'json'
                                }
                        ).close()


                        #nbconvert
                        self.NotebookedCodeDict=self.DocumentedConceptNotebookDict
                        self.nbconvert(
                                _FormatStr='Slide',
                                **{
'FolderingPathVariable':self.DocumentingConceptFolderPathStr,
'NotebookingFileKeyStr':'Concept'+self.GuidingBookStr+'.ipynb'
                                }
                        )

                        #set
                        self.DocumentedSlideLocalFilePathStr=DocumentingOntologyLoca
lFolderPathStr+self.DocumentedConceptModule.__name__.split('.')[-1]+'.html'

                        #cp
                        os.popen('cp '+self.FiledPathStr+' '+self.DocumentedSlideL
ocalFilePathStr+self.DocumentedConceptModule.__name__.split('.')[-1]+'.ipynb')

                        #mv with .html extension
                        os.popen(
                                        'cp '+self.FiledPathStr.replace(
                                        '.ipynb',
                                        '.html'
                                        )+' '+self.DocumentedSlideLocalFilePathStr
                                )

                        #mv with .php extension
                        os.popen(
                                        'mv '+self.FiledPathStr.replace(
                                        '.ipynb',
                                        '.html'
                                        )+'
'+self.DocumentedSlideLocalFilePathStr.replace('.html','.php')
                                )

                        #deploy
                        try:
                                self.deploy(
_ClientFilePathStrToServerFilePathStrOrderedDict=collections.OrderedDict(
                                                [
                                                        (
self.DocumentedSlideLocalFilePathStr,
                                                                DocumentingOntolog
yOuvatonFolderPathStr+self.DocumentedConceptModule.__name__.split('.'
)[-1]+'.php'
                                                        )
                                                ]
                                        )
                                )
                        except:
                                print('There is NO Internet !')

                #Check
                if self.DocumentingConceptReadmeIsBool:

                        #debug
                        '''
                        self.debug('we build the concept readme here')
                        '''

                        #import submodules
                        '''
                        map(
                                        lambda __DocumentedSubModuleStr:
importlib.import_modules(__DocumentedSubModuleStr),
                                        self.DocumentedSubModuleStrsList
                                )
                        '''

                        #readme
                        self.package(
                                        self.DocumentedConceptModuleStr
                                ).scriptbook(
                                        _GuideTuplesList=[
                                                ('001','Document','Markdown'),
                                                ('002','Ouvaton','Markdown'),
                                                ('1','Github','Markdown'),
                                        ],
                                        **{'GuidingBookStr':"Doc"}
                                )

                        #notebook
                        self.scriptbook(
                                        _GuideTuplesList=[]
                                ).notebook(
                                        "PreReadme.ipynb"
                                ).nbconvert(
                                        "Readme.md",
                                        'Markdown',
                        )

                #Check
                if self.DocumentingConceptDocumentIsBool:

                        #debug
                        '''
                        self.debug(
                                                [
                                                        'we document here',
('self.',self,['DocumentedConceptModuleFolderPathStr'])
                                                ]
                                        )
                        '''

                        '''
                        #document
                        self.document(
**{'PackagingModuleVariable':self.DocumentedConceptModuleStr}
                        )
                        '''

                        #package
                        self.package(self.DocumentedConceptModuleStr)

                        #mv with .php extension
                        os.popen(
                                        'cp
'+self.PackagedLocalFolderPathStr+'Readme.md  '+DocumentingDocumentLocalFolderPath
Str+self.DocumentedConceptModuleStr.split('.')[-1]+'.md'
                                )

                        #Return self
                        #return self

                if self.DocumentingSiteDocumentIsBool:

                        #open
                        os.popen(
                                                'mkdocs build --clean'
                                )

                        #deploy
                        try:
                                self.deploy(
_ClientFilePathStrToServerFilePathStrOrderedDict=collections.OrderedDict(
                                                [
                                                        (
self.DocumentedSlideLocalFilePathStr,
                                                                DocumentingOntolog
yOuvatonFolderPathStr+self.DocumentedConceptModule.__name__.split('.'
)[-1]+'.php'
                                                        )
                                                ]
                                        )
                                )
                        except:
                                print('There is NO Internet !')

#</DefineClass>

```

<small>
View the Documenter sources on <a href="https://github.com/Ledoux/ShareYourSystem/
tree/master/Pythonlogy/ShareYourSystem/Guiders/Documenter"
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
from ShareYourSystem.Guiders import Documenter

#Definition an Documenter instance
MyDocumenter=Documenter.DocumenterClass()

#Definition the AttestedStr
SYS._attest(
    [
        'MyDocumenter is '+SYS._str(
        MyDocumenter,
        **{
            'RepresentingBaseKeyStrsListBool':False,
            'RepresentingAlineaIsBool':False
        }
        )
    ]
)



```


```console
>>>


*****Start of the Attest *****

MyDocumenter is < (DocumenterClass), 4540656336>
   /{
   /  '<New><Instance>IdInt' : 4540656336
   /  '<Spe><Class>DocumentedConceptModule' : None
   /  '<Spe><Class>DocumentedConceptModuleFolderPathStr' :
   /  '<Spe><Class>DocumentedConceptModuleStr' :
   /  '<Spe><Class>DocumentedSubModuleLocalFolderPathStrsList' : None
   /  '<Spe><Class>DocumentedSubModuleStrsList' : None
   /  '<Spe><Class>DocumentedSubModulesList' : None
   /  '<Spe><Class>DocumentedSubNameStrsList' : None
   /  '<Spe><Class>DocumentingConceptDocumentIsBool' : True
   /  '<Spe><Class>DocumentingConceptFolderPathStr' :
   /  '<Spe><Class>DocumentingConceptReadmeIsBool' : True
   /  '<Spe><Class>DocumentingConceptSlideIsBool' : True
   /  '<Spe><Class>DocumentingSiteDocumentIsBool' : True
   /  '<Spe><Class>DocumentingSubReadmeIsBool' : True
   /}

*****End of the Attest *****



```

