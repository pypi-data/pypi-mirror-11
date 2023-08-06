
  # the monitor should never finish when the parent shell dies.  This is
  # equivalent to starting monitor.sh via 'nohup'
  trap "" HUP

  # create the monitor wrapper script once -- this is used by all job startup
  # scripts to actually run job.sh.  The script gets a PID as argument,
  # denoting the job to monitor.   The monitor will write 3 pids to a named pipe
  # (listened to by the wrapper):
  #
  #   rpid: pid of the actual job              (not exposed to user)
  #   mpid: pid of this monitor.sh instance    (== pid of process group for cancel)
  #   upid: mpid + unique postfix on pid reuse (== SAGA id)

  MPID=$$
  NOTIFICATIONS="/home/merzky/saga/radical.pilot.devel/notifications"

  # on reuse of process IDs, we need to generate new, unique derivations of the
  # job directory name.  That name is, by default, the job's rpid.  Id the job
  # dies and that rpid is reused, we don't want to remove the old dir (job state
  # may still be queried), so we append an (increasing) integer to that dirname,
  # i.e. that job id
  POST=0
  UPID="$MPID.$POST"
  DIR="/home/merzky/saga/radical.pilot.devel/$UPID"
  
  while test -d "$DIR"
  do
    POST=$(($POST+1))
    UPID="$MPID.$POST"
    DIR="/home/merzky/saga/radical.pilot.devel/$UPID"
  done

  \mkdir -p "$DIR"

# exec 2>"$DIR/monitor.trace"
# set -x 


  # FIXME: timestamp
  START=`\awk 'BEGIN{srand(); print srand()}'`
  \printf "START : $START\n"  > "$DIR/stats"
  \printf "NEW \n"            >> "$DIR/state"

  # create represents the job.  The 'exec' call will replace
  # the subshell instance with the job executable, leaving the I/O redirections
  # intact.
  \touch  "$DIR/in"
  \printf "#!/bin/sh\n\n" > $DIR/cmd
  \printf "$@\n"        >> $DIR/cmd
  \chmod 0700               $DIR/cmd

  (
    \printf  "RUNNING \n"          >> "$DIR/state"
    \printf  "$UPID:RUNNING: \n"  >> "$NOTIFICATIONS"
    \exec "$DIR/cmd"   < "$DIR/in" > "$DIR/out" 2> "$DIR/err"
  ) 1>/dev/null 2>/dev/null 3</dev/null &

  # the real job ID (not exposed to user)
  RPID=$!

  \printf "$RPID\n"    > "$DIR/rpid"  # real process  pid
  \printf "$MPID\n"    > "$DIR/mpid"  # monitor shell pid
  \printf "$UPID\n"    > "$DIR/upid"  # unique job    pid

  # signal the wrapper that job startup is done, and report job id
  \printf "$UPID\n" >> "/home/merzky/saga/radical.pilot.devel/fifo"

  # start monitoring the job
  while true
  do
    \wait $RPID
    retv=$?

    # if wait failed for other reason than job finishing, i.e. due to
    # suspend/resume, then we need to wait again, otherwise we are done
    # waiting...
    if test -e "$DIR/suspended"
    then
      \rm -f "$DIR/suspended"
      TIME=`\awk 'BEGIN{srand(); print srand()}'`
      \printf "SUSPEND: $TIME\n"    >> "$DIR/stats"
      \printf "$UPID:SUSPENDED: \n" >> "/home/merzky/saga/radical.pilot.devel/notifications"

      # need to wait again
      continue
    fi

    if test -e "$DIR/resumed"
    then
      \rm -f "$DIR/resumed"
      TIME=`\awk 'BEGIN{srand(); print srand()}'`
      \printf "RESUME : $TIME\n"  >> "$DIR/stats"
      \printf "$UPID:RUNNING: \n" >> "/home/merzky/saga/radical.pilot.devel/notifications"

      # need to wait again
      continue
    fi

    TIME=`\awk 'BEGIN{srand(); print srand()}'`
    \printf "STOP   : $TIME\n"  >> "$DIR/stats"

    # evaluate exit val
    \printf "$retv\n" > "$DIR/exit"

    test   "$retv" -eq 0  && \printf "DONE   \n" >> "$DIR/state"
    test   "$retv" -eq 0  || \printf "FAILED \n" >> "$DIR/state"

    test   "$retv" -eq 0  && \printf "$UPID:DONE:$retv   \n" >> "$NOTIFICATIONS"
    test   "$retv" -eq 0  || \printf "$UPID:FAILED:$retv \n" >> "$NOTIFICATIONS"


    # done waiting
    break
  done

  exit

