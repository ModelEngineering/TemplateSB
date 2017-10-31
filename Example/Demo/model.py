import tellurium as te
import pylab

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
rr.plot (result)
pylab.show()
