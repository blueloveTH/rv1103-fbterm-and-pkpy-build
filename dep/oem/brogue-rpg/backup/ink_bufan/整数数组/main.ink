INCLUDE gyc.ink
INCLUDE array.ink
INCLUDE Integer_array.ink

-> init

== init ==
VAR a = 0
~ a = int_arr(1)
{str(a)}
{str_arr(a)}
VAR b = 0
~ b = int_arr(9999)
{str(b)}
{str_arr(b)}
{str(a.add_arr(b))}
{str_arr(a.add_arr(b))}
-> END

== test ==

->END
