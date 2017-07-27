"""
   Running the template pre-processor standalone.
   Input: Templated Antimony model (stdin)
   Output: Expanded Antimony model (stdout)
"""
import fileinput
import sys
from TemplateSB.templatesb import TemplateSB

template_stg = ''
for line in fileinput.input():
  template_stg += "\n" + line

templatesb = TemplateSB(template_stg)
expanded_stg = templatesb.do()

sys.stdout.write(expanded_stg)
