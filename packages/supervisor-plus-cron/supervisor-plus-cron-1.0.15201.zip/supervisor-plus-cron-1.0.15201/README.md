Supervisor + Cron
=================

This is a fork of [Supervisor](https://github.com/Supervisor/supervisor)
with the addition of cron!  The only difference is the addition of one
extra parameter that controls when a program is started again.

``[program:x]`` Section Values
------------------------------

``startintervalsecs``

  After a program has exited, Supervisor will delay restarting the program
  for the given number of seconds since the *last started* time.  This
  can be used to regularly schedule jobs.

  *Default*: 0 - Restarting according to normal Supervisor convention

  *Required*:  No.

  *Introduced*: in this fork!


Contributing
------------

If you would like to make this CRON feature better, work is being done at 
[https://github.com/klahnakoski/supervisor-plus-cron](https://github.com/klahnakoski/supervisor-plus-cron).
