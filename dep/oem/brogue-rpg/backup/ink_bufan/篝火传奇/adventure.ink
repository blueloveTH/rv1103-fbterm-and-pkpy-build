== adventure ==//1
｜
<决策中心> => <冒险>
+ [携带物资]
-> prepare
+ [返回上级]
-> HomeOption

== prepare ==//2

背包剩余空间：{space-FreeSpace}/{space}
武器：{weapon == 1:骨刃}
+ [储备熏肉{bacon} ＜——＞ 携带熏肉{BringBacon}]
++ {FreeSpace>=1}[携带+1]
~ FreeSpace = FreeSpace -1
~ BringBacon = BringBacon +1
~ bacon = bacon -1
++ {FreeSpace>=10}[携带+10]
~ FreeSpace = FreeSpace -10
~ BringBacon = BringBacon +10
~ bacon = bacon -10
++ {BringBacon>=1}[携带-1]
~ FreeSpace = FreeSpace +1
~ BringBacon = BringBacon -1
~ bacon = bacon +1
++ {BringBacon>=10}[携带-10]
~ FreeSpace = FreeSpace +10
~ BringBacon = BringBacon -10
~ bacon = bacon +10
++ { FreeSpace == 0 } {BringBacon == 0}[请尝试削减其他物资以携带更多]
-- -> prepare

+ {weapon==0}[你没有携带武器！荒野上非常危险，还是不要出去为妙]
-> prepare
+ {BringBacon<=2}[你没有携带足够食物！你走不了多远的]
-> prepare
+ {weapon>=1 and BringBacon>=0}[准备就绪！]
-> explore
+ [返回上级]
-> adventure

== explore ==

-> ShowWorld -> move 
== ShowWorld ==
~ world = zeros(121)
~ LoadEntity(0)
{
 - (Entity2dget(0,99999)-dx+5)+(Entity2dget(1,99999)-dy+5)*11 <= 120 and (Entity2dget(0,99999)-dx+5)+(Entity2dget(1,99999)-dy+5)*11 >= 0 and (Entity2dget(0,99999)-dx+5) <= 10 and (Entity2dget(0,99999)-dx+5) >= 0:
~ World2dSet(5-dx,5-dy,1)
}
~ World2dSet(5,5,2)
```
{ShowMapLine(10)} 坐标：  （{dx},{dy})
{ShowMapLine(9)} 食物：   {BringBacon}
{ShowMapLine(8)} 水:     {LeftWater}
{ShowMapLine(7)} 背包空间:{FreeSpace}
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
+ {get(world,59) == 1}[<回家]
~ dx = 0
~ dy = 0
-> HomeOption
+ {get(world,61) == 1}[回家>]
~ dx = 0
~ dy = 0
-> HomeOption
+ {get(world,49) == 1}[v回家]
~ dx = 0
~ dy = 0
-> HomeOption
+ {get(world,71) == 1}[^回家]
~ dx = 0
~ dy = 0
-> HomeOption
+ {get(world,59) == 3}[<搜索]
-> SearchHouse
+ {get(world,61) == 3}[搜索>]
-> SearchHouse
+ {get(world,49) == 3}[v搜索]
-> SearchHouse
+ {get(world,71) == 3}[^搜索]
-> SearchHouse
+ [↑]
~ dy = dy + 1
+ [↓]
~ dy = dy - 1
+ [←]
~ dx = dx - 1
+ [→]
~ dx = dx + 1
- 
{
 -BringBacon == 0 or LeftWater ==0:
你眼前一黑昏了过去。
你被人救回了村庄，不过你背包中的物资全部没有了。
~ BringBacon = 0
~ LeftWater = 20
~ FreeSpace = space
-> HomeOption
}
~ BringBacon = BringBacon -1
~ LeftWater = LeftWater -1
~ FreeSpace = FreeSpace+1
-> ShowWorld -> move
== SearchHouse ==
你对这间房子进行了搜索，里面存有非常多的食物。
背包剩余空间：{space-FreeSpace}/{space}
+ [储备熏肉 ♾️ ＜——＞ 携带熏肉{BringBacon}]
++ {FreeSpace>=1}[携带+1]
~ FreeSpace = FreeSpace -1
~ BringBacon = BringBacon +1
++ {FreeSpace>=10}[携带+10]
~ FreeSpace = FreeSpace -10
~ BringBacon = BringBacon +10
++ {BringBacon>=1}[携带-1]
~ FreeSpace = FreeSpace +1
~ BringBacon = BringBacon -1
++ {BringBacon>=10}[携带-10]
~ FreeSpace = FreeSpace +10
~ BringBacon = BringBacon -10
-- -> SearchHouse
+ [退出]
-> move


