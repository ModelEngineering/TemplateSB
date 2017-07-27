"""
   Running the template pre-processor standalone.
   Input: Templated Antimony model (stdin)
   Output: Expanded Antimony model (stdout)
"""
import fileinput
import sys
from TemplateSB.template_processor import TemplateProcessor

template_stg = ''
for line in fileinput.input():
  template_stg += "\n" + line

processor = TemplateProcessor(template_stg)
expanded_stg = processor.do()

sys.stdout.write(expanded_stg)
