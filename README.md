# SbStar
SbStar is a template pre-processor for Antimony, a system for expression kinetics models in Tellurium. The name SbStar is a combination of the chemical symbol for the element antimony and the use of the the star ("*") operator in templates such as regular expressions.

The motivation for SbStar is as follows. Often, realistic kinetics models require representing a large number of reactions. The resulting model is difficult to write, and difficult to understand.

Fortunately, the set of reactions can often be simplified due to independence assumptions used in the model. To illustrate this, consider a part of the chemotaxis model in Spiro (PNAS, 1997). We focus on receptor methylation. The state of a receptor is determined by three factors: whether or not it is bound to a ligand; whether or not it is phosphorylated; and its methylation level. Methylation may occur once a receptor (in any state) is bound to CheR (herein denoted by R). The reactions for a methylation level of 2 are:

  J1: T2R -> T3 + R; k2\*T2R
  
  J2: LT2R -> LT3 + R; k2\*LT2R
  
  J3: T2pR -> T3p + R; k2\*T2pR
  
  J4: LT2pR -> LT3p + R; k2\*LT2pR
  
Note that the reactions are independent of phosphorylation and ligand binding in that the kinetics constants do not change with these receptor states. To represent the complete set of methylation reactions in the Spiro model, we’d consider methylation levels of 3 and 4 as well, resulting in 12 reactions.

SbStar is a template preprocessor to antimony whereby the complete set of 12 reactions can be expressed in a more compact way. The idea of a template is drawn from the Jinja template system for rendering web pages that provides variable substitutions. For the Antimony template processor, variables will be declared with a set of possible values. A reaction is written with template variables enclosed in braces ({, }). For example, suppose l is template variable for a ligand (as in LT2) that takes on either the values of 'L' or '', and p is a template variable for phosphorylation (as in T2p) that takes on the values of either 'p' or ''. Then the above four reactions can be expressed in a single line as:

{l}T2{p}R -> {l}T3{p} + R; k2*{l}T2{p}R

For example, reaction J1 is realized by assigning '' (the null string) to both l and p. The other four reactions are constructed by using the other three combinations of the values of template variables. Note that both kinetics expressions and reaction labels can use template variables.

Template variables are explicitly at the top of the model using the escape string “#!”. The declaration has the syntax of a python dictionary. A line is continued if it ends with a backslash (“\”).

Below is a representation in templates of the 64 methylation 
reactions (24 reactions for each of
J1\* and J2\* and 8 reactions for each of 
J3\*2\* and J3\*3\*) as required by the Spiro model. 

  <p>#! SbStar Version 1.0 {‘p’:[‘p’,‘’], ‘l’:[‘L’,‘’], ‘r’:[‘R’,‘’], \ </p>

  ‘m’:[‘2’, ‘3’, ‘4’]}
 
  J1{l}{m}{p}: {l}T{m}{p} + R -> {l}T{m}{p}R; k1{m} \* {l}T{m}{p} \* R
  
  J2{l}{m}{p}: {l}T{m}{p}R -> {l}T{m}{p} + R; k2{m} \* {l}T{m}{p}R
  
  J3{l}2{p}: {l}T2{p}R -> {l}T3{p} + R; k32 \* {l}T2{p}R
  
  J3{l}3{p}: {l}T3{p}R -> {l}T4{p} + R; k33 \* {l}T3{p}R

One possible extension is to permit having a python expression inside a template instance (within “{“ and “}”). This feature would eliminate one of the templated model lines in the above model by using {m+1} as a template instance.

The repository is organized as follows:

*  The Code directory contains the python code and tests for the template preprocessor.
*  The Examples directory contains an example of a template input and the output produced by SbStar.
*  setup.py installs prerequisites for running SbStar.
*  run.py is runs SbStar using stdin and stdout.
