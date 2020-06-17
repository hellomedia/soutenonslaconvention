#!/bin/sh
APP=slc.appbootstrap:app
LISTEN=${1-"0:8080"}
GUNICORN_ARGS="-t 1200 -k gevent -w1 -b $LISTEN --log-level=INFO --log-config=logging.ini --forwarded-allow-ips \* $APP --reload"
GUNICORN=${GUNICORN:-./venv/bin/gunicorn}
DEPS='ls -1 .env* settings.py; find slc \! -path "*/.gup" -name "*.py" -o -name "*.mo"; find venv/bin -type f'
PIDFILE=".gunicorn.pid"
SLC_SETTINGS=${SKC_SETTINGS:-"$(dirname $(realpath $0))/settings.py"}
trap "trap - SIGTERM && kill -- -$$" INT TERM EXIT

entr gup << "EOF" &
requirements.in
EOF

while true; do
    $GUNICORN -p $PIDFILE $GUNICORN_ARGS
    sleep 1;
done
