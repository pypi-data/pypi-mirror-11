

<!--
FrozenIsBool False
-->

#Databasers

##Doc
----


>
> The Databasers defines the Noders that take the role of
> the client-side "Model" in the MVC architecture of SYS.
> Here the databasing process relies on a hdf5
> pytable wrapping, going from simple encapsulations
> of the create_table,insert methods to 'sophisticated'
> routines that facilitate the joins between tables and
> the automatic shaping of the rowed datas.
>
>
>

----

<small>
View the Databasers notebook on [NbViewer](http://nbviewer.ipython.org/url/share
yoursystem.ouvaton.org/Databasers.ipynb)
</small>




<!--
FrozenIsBool False
-->

##Concept and SubModules family

<script type="text/javascript">

        var HrefStr=window.location.href;
        //alert(window.location.href)

        if(HrefStr ==
"http://shareyoursystem.ouvaton.org/site/LibraryReference/Databasers/"){

            //alert('Ouvaton')
            document.write("from ")
            document.write("http://shareyoursystem.ouvaton.org/slides/ ")
            document.write("<iframe width=\"725\" height=\"300\" src=\"")
            document.write("http://shareyoursystem.ouvaton.org")
            document.write("/slides/Databasers.php\"></iframe>")
        }
        else if(HrefStr ==
"http://127.0.0.1:8000/LibraryReference/Databasers/"){

        //alert('Localhost')
        document.write("from ")
        document.write("localhost mkdocs but direct to ouvaton")
        document.write("<iframe width=\"725\" height=\"300\" src=\"")
        document.write("http://shareyoursystem.ouvaton.org")
        document.write("/slides/Databasers.php\"></iframe>")
    }
    else
    {

        //alert('Local')
            document.write("from ")
            document.write("/Users/ledoux/Documents/ShareYourSystem/Ouvaton/ ")
            document.write("<iframe width=\"725\" height=\"300\" src=\"")
            document.write("/Users/ledoux/Documents/ShareYourSystem/Ouvaton/")
            document.write("Databasers.html\"></iframe>")

    }

</script>

<small>
View the Databasers concept on <a
href="http://shareyoursystem.ouvaton.org/slides/Databasers.php"
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


The Databasers defines the Noders that take the role of
the client-side "Model" in the MVC architecture of SYS.
Here the databasing process relies on a hdf5
pytable wrapping, going from simple encapsulations
of the create_table,insert methods to 'sophisticated'
routines that facilitate the joins between tables and
the automatic shaping of the rowed datas.


"""

#<DefineConcept>
import ShareYourSystem as SYS
SYS.setConceptModule(globals())
#</DefineConcept>

```

<small>
View the Databasers sources on <a href="https://github.com/Ledoux/ShareYourSyste
m/tree/master/Pythonlogy/ShareYourSystem/Databasers" target="_blank">Github</a>
</small>


