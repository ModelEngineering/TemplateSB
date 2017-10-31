"""
Generates the expanded model from the template and then
runs the model in Antimony. 
Usage:
  python3 model.py
Note: There may be a warning message from Antimony due to an
      issue that is being resolved.
"""

import sys, os
import matplotlib.pylab as plt
import tellurium as te

INPUT = "sample.mdl"

# Reads the model from sample.mdl
with open (INPUT, "r") as myfile:
  lines = myfile.readlines()

antimony_model = "\n".join(lines)

rr = te.loada(antimony_model)

# Carry out a time course simulation results returned in array result.
# Arguments are: time start, time end, number of points
result = rr.simulate (0, 10, 100)

# Plot the results
rr.plot()
