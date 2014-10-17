export PROJ_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}/"/)" && cd .. && pwd )"

echo -e "\n** starting service from $PROJ_HOME **\n"

# configuration
export PYTHONPATH=${PROJ_HOME}/pin:${PYTHONPATH}

# run
python ${PROJ_HOME}/pin/run.py ${PROJ_HOME} ${PROJ_HOME}/conf/pin.conf
