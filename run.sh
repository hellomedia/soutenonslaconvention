#!/bin/sh
APP=slc.appbootstrap:app
LISTEN=${1-"0:8090"}
GUNICORN_ARGS="-t 1200 -k gevent -w1 -b $LISTEN --log-level=INFO --log-config=logging.ini --forwarded-allow-ips \* $APP --reload"
GUNICORN=${GUNICORN:-./venv/bin/gunicorn}
DEPS='ls -1 .env* settings.py; find slc \! -path "*/.gup" -name "*.py" -o -name "*.mo"; find venv/bin -type f'
PIDFILE=".gunicorn.pid"

trap "trap - TERM && kill -- -$$" INT TERM EXIT

./venv/bin/huey_consumer -w1 -k process slc.queuing.huey &
entr gup requirements.txt << "EOF" &
requirements.in
EOF

while true; do
    $GUNICORN -p $PIDFILE $GUNICORN_ARGS
    sleep 1;
done
