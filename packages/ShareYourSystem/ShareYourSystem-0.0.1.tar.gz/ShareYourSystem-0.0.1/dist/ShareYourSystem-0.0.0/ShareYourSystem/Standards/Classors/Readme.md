

<!--
FrozenIsBool False
-->

#Classors

##Doc
----


> The Classors help for decorating a Class.
> Here are defined the important derived Objects that
> facilitates the manners to set a new defined Class in the
> SYS scope and set automatically into it new 'boilerplates'
> methods like the 'default_init' (cf. Defaultor),'do_<DoMethodStr>'
>  (cf. Doer), 'mimic_<DoMethodStr>' (cf. Mimicker), also
>  decorates methods for making it switch or resetting.
>
>

----

<small>
View the Classors notebook on [NbViewer](http://nbviewer.ipython.org/url/shareyo
ursystem.ouvaton.org/Classors.ipynb)
</small>




<!--
FrozenIsBool False
-->

##Concept and SubModules family

<script type="text/javascript">

        var HrefStr=window.location.href;
        //alert(window.location.href)

        if(HrefStr ==
"http://shareyoursystem.ouvaton.org/site/LibraryReference/Classors/"){

            //alert('Ouvaton')
            document.write("from ")
            document.write("http://shareyoursystem.ouvaton.org/slides/ ")
            document.write("<iframe width=\"725\" height=\"300\" src=\"")
            document.write("http://shareyoursystem.ouvaton.org")
            document.write("/slides/Classors.php\"></iframe>")
        }
        else if(HrefStr == "http://127.0.0.1:8000/LibraryReference/Classors/"){

        //alert('Localhost')
        document.write("from ")
        document.write("localhost mkdocs but direct to ouvaton")
        document.write("<iframe width=\"725\" height=\"300\" src=\"")
        document.write("http://shareyoursystem.ouvaton.org")
        document.write("/slides/Classors.php\"></iframe>")
    }
    else
    {

        //alert('Local')
            document.write("from ")
            document.write("/Users/ledoux/Documents/ShareYourSystem/Ouvaton/ ")
            document.write("<iframe width=\"725\" height=\"300\" src=\"")
            document.write("/Users/ledoux/Documents/ShareYourSystem/Ouvaton/")
            document.write("Classors.html\"></iframe>")

    }

</script>

<small>
View the Classors concept on <a
href="http://shareyoursystem.ouvaton.org/slides/Classors.php"
target="_blank">Ouvaton</a>
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

The Classors help for decorating a Class.
Here are defined the important derived Objects that
facilitates the manners to set a new defined Class in the
SYS scope and set automatically into it new 'boilerplates'
methods like the 'default_init' (cf. Defaultor),'do_<DoMethodStr>'
 (cf. Doer), 'mimic_<DoMethodStr>' (cf. Mimicker), also
 decorates methods for making it switch or resetting.

"""

#<DefineConcept>
import ShareYourSystem as SYS
SYS.setConceptModule(globals())
#</DefineConcept>

```

<small>
View the Classors sources on <a href="https://github.com/Ledoux/ShareYourSystem/
tree/master/Pythonlogy/ShareYourSystem/Classors" target="_blank">Github</a>
</small>


