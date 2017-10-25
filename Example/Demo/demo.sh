#!/bin/bash
# Runs the demo
python3 ../../run.py < sample.tmpl > sample.mdl
python3 model.py
