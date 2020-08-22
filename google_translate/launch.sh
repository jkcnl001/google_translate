WORK_PATH=$(cd `dirname $0`; pwd)
export PYTHONPATH=$WORK_PATH"/site-packages:"
python google_translate.py "$@"