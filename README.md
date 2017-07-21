# TemplateSB
TemplateSB is a template processor 
for use in kinetics models for systems biology.
The work was motivated by modeling in [Antimony](http://antimony.sourceforge.net/), a system for expression kinetics models in Tellurium.

The motivation for TemplateSB is as follows. Often, realistic kinetics models require representing a large number of reactions. The resulting model is difficult to write, and difficult to understand.

Fortunately, the set of reactions can often be simplified due to independence assumptions used in the model. 
To illustrate this, consider a part of the chemotaxis model for E. coli in Spiro (PNAS, 1997). 
We focus on receptor methylation. The state of a receptor is determined by three factors: whether or not it is bound to a ligand; whether or not it is phosphorylated; and its methylation level. Methylation may occur once a receptor (in any state) is bound to CheR (herein denoted by R). The reactions for a methylation level of 2 are:

  T2R -> T3 + R; k2\*T2R
  
  LT2R -> LT3 + R; k2\*LT2R
  
  T2pR -> T3p + R; k2\*T2pR
  
  LT2pR -> LT3p + R; k2\*LT2pR
  
Note that the reactions are independent of phosphorylation and ligand binding in that the kinetics constants do not change with these receptor states. To represent the complete set of methylation reactions in the Spiro model, we’d consider methylation levels of 3 and 4 as well, resulting in 12 reactions.

With TemplateSB, the complete set of 12 reactions can be expressed in a more compact way. 
Templates provide a way to describe model elements using expressions.
A template variable or expression is surrounded by curly braces ("{", "}").
Consider the template variable {L}.
Further, by default this variable has two expansions: "L" and "".
The template variable {p} is handled in the same way.
Thus, the above four reactions can be expressed as a single templated reaction:

{L}T2{p}R -> {L}T3{p} + R; k2\*{L}T2{p}R

The template processor expands this expression into the above four reactions.
That is, the first reaction above is realized by assigning '' (the null string) both {L} and {p}. 
The other four reactions are constructed by using the other three combinations of the values of template variables. Note that both kinetics expressions and reaction labels can use template variables.

In the foregoing, we considered template variables that have two possible values, either the non-white space value
enclosed within the braces or the null string.
Template variables can also have a list a values. 
This is specified by a comma separated list. White space is ignored.
For example "T{1,2,3} -> ;k" expands to:

  T1 -> ;k
  
  T2 -> ;k
  
  T3 -> ;k
  
Note that with list values there is no substituion for the null string.

Yet another possibility is to explicitly declare
the values assigned to template variables at the top of the Antimony model.
This is done using the escape string “#!”. The declaration has the syntax of a python dictionary. 
A line is continued if it ends with a backslash (“\”).

Below is a representation in templates of the 64 methylation 
reactions (24 reactions for each of
J1\* and J2\* and 8 reactions for each of 
J3\*2\* and J3\*3\*) as required by the Spiro model.
TemplateSB uses a Python code to specify how processing should proceed
based on opertions on the object api.
In particular, api.addDefinitions takes a dictionary as its arguement.
The keys are template variables; the associated values are the possible
values that can be assigned to the template variable.

  <p>{{

   api.addDefinitions({‘p’:[‘p’,‘’], ‘L’:[‘L’,‘’], ‘r’:[‘R’,‘’], ‘m’:[‘2’, ‘3’, ‘4’]})

   }}
 
  J1{L}{m}{p}: {L}T{m}{p} + R -> {L}T{m}{p}R; k1{m} \* {L}T{m}{p} \* R
  
  J2{L}{m}{p}: {L}T{m}{p}R -> {L}T{m}{p} + R; k2{m} \* {L}T{m}{p}R
  
  J3{L}2{p}: {L}T2{p}R -> {L}T3{p} + R; k32 \* {L}T2{p}R
  
  J3{L}3{p}: {L}T3{p}R -> {L}T4{p} + R; k33 \* {L}T3{p}R

One possible extension is to permit having a python expression inside a template instance (within “{“ and “}”). This feature would eliminate one of the templated model lines in the above model by using {m+1} as a template instance.

The repository is organized as follows:

*  The Code directory contains the python code and tests for the template preprocessor.
*  The Examples directory contains an example of a template input and the output produced by TemplateSB.
*  setup.py installs prerequisites for running TemplateSB.
*  run.py is runs TemplateSB using stdin and stdout.
