
<!---
FrozenIsBool True
-->

##Example

Particular case of the definition of mutable variables in the init method.
If you decide to initialize a mutable variable like a list with a 
default empty value, this is rather to make it shared to all the instances.
On the other hand, if you want to declare a list that has to be unique for each instance,
then set it to the default value None.