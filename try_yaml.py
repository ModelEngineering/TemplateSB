import yaml

fd = open("config.yaml", "r")
lines = ''.join(fd.readlines())
fd.close()

my_dict = yaml.load(lines)
import pdb; pdb.set_trace()
