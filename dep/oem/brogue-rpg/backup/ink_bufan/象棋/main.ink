INCLUDE gyc.ink
INCLUDE array.ink
INCLUDE as.ink
INCLUDE tabletop.ink

== _init ==
VAR a = 0
== function _draw() ==
{a}
~ a = a+1
{a<20:
~ _draw()
}

== function _on_tap(x) ==
~ a = 0
~ refresh()