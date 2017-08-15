#!/bin/bash
# Compare the original file with the model file

function filter {
  this_file=$1
  grep -v  "^ *\/" ${this_file}   \
    | grep -v "^ *#"              \
    | grep -v "^ *$"              \
    | sed 's/^ *//'               \
    | sort                        \
    > /tmp/${this_file}
}  

original=`ls BIOM*.mdl`
processed_name="bray_model"
processed=`ls ${processed_name}.mdl`
python ../../run.py < ${processed_name}.tmpl > ${processed}
filter $original
filter $processed
diff /tmp/${original} /tmp/${processed} > /tmp/assess.out
cat /tmp/assess.out
