"""
   Running the template pre-processor standalone.
   Input: Templated Antimony model (stdin)
   Output: Expanded Antimony model (stdout)
"""
import fileinput
import sys
from SbStar.sbstar import SbStar

template_stg = ''
for line in fileinput.input():
  template_stg += "\n" + line

sbstar = SbStar(template_stg)
expanded_stg = sbstar.expand()

sys.stdout.write(expanded_stg)
