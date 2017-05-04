#!/bin/bash
set -e
LOGFILE=/var/opt/odp/deploy/logs/gunicorn/gunicorn.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3 # idealmente deve ser 2n + 1 (n = qtd de processadores)
USER=www-data
GROUP=www-data
cd /var/opt/odp
test -d $LOGDIR || mkdir -p $LOGDIR
. /etc/default/locale
export LANG
export LC_ALL
exec gunicorn OpenDataCollector.wsgi:application -w $NUM_WORKERS \
  --user=$USER --group=$GROUP --log-level=critical \
  --log-file=$LOGFILE 2>>$LOGFILE \
  --timeout=1800
