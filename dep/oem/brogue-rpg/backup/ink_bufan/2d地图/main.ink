INCLUDE gyc.ink
INCLUDE array.ink
INCLUDE function.ink
INCLUDE amount.ink
~ RandomPosition(3,0)
-> ShowWorld -> move 
== ShowWorld ==
~ world = zeros(121)
~ LoadEntity(0)


{
 - (Entity2dget(0,99999)-dx+5)+(Entity2dget(1,99999)-dy+5)*11 <= 120 and (Entity2dget(0,99999)-dx+5)+(Entity2dget(1,99999)-dy+5)*11 >= 0 and (Entity2dget(0,99999)-dx+5) <= 10 and (Entity2dget(0,99999)-dx+5) >= 0:
~ World2dSet(5-dx,5-dy,1)
}
~ World2dSet(5,5,2)
{

```
{ShowMapLine(10)} 坐标：（{dx},{dy})
{ShowMapLine(9)}
{ShowMapLine(8)}
{ShowMapLine(7)}
{ShowMapLine(6)}
{ShowMapLine(5)}
{ShowMapLine(4)}
{ShowMapLine(3)}
{ShowMapLine(2)}
{ShowMapLine(1)}
{ShowMapLine(0)}
```
->->
== move ==
+ [↑]
~ dy = dy + 1
+ [↓]
~ dy = dy - 1
+ [←]
~ dx = dx - 1
+ [→]
~ dx = dx + 1

+ {get(world,59) == 1}[<回家]
+ {get(world,61) == 1}[回家>]
+ {get(world,49) == 1}[v回家]
+ {get(world,71) == 1}[^回家]
+ {get(world,59) == 3}[<搜索]
+ {get(world,61) == 3}[搜索>]
+ {get(world,49) == 3}[v搜索]
+ {get(world,71) == 3}[^搜索]


- -> ShowWorld -> move



