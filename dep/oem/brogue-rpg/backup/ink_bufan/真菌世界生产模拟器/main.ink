INCLUDE gyc.ink
INCLUDE array.ink
VAR speed = 60
VAR tree = 2
VAR k = 0
VAR seed = 4

VAR time = 0
~ time = POW(2,(4-speed/25)-1)

-> init

== init ==
~ k= k+1
{k % time == 0:
~ seed = seed + tree
}
```
{k}游戏刻
{time}间隔
种子：{seed}
```
-> init
