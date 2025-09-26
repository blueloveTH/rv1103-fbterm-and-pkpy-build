== HomeOption ==//0(此处数字代表菜单的级别)

{
 - house>=2 and deploy==0:
```
[提示：你已经建造了2座房屋，可以进行人员部署了]
```
}
{
 - house>=4 and HuntHouse==0:
```
[提示：你已经建造了4座房屋，可以建造狩猎小屋了]
```
}
{
 - HuntHouse==1 and HuntDeploy==0:
```
[提示：你已经建造狩猎小屋,可以进行狩猎部署了]
```
}
{
 - trap>=1 and information==0:
```
[提示：你已经建造了1个陷阱，可以查看营地信息了]
```
}
｜
<决策中心💡> => 
+ {compass == 1}[冒险⚔️]
-> adventure
+ {TradeHouse == 1}[交易💰]
-> trade -> HomeOption
+ {workshop == 1}[制造🛠]
-> manufacture -> HomeOption
+ { house >= 2 }[部署🚹]
-> deploy -> HomeOption
+ {collect>=1}[建造🪜]
-> build -> HomeOption
+ [收集🪵]
-> collect -> HomeOption
+ {trap>=1}[信息ℹ️]
-> information -> HomeOption


== trade ==//1
｜
<决策中心💡> => <交易>

+ {compass == 0}[罗盘🧭 < 毛皮x300/{fur}] 
{
  - fur - 300 >= 0 :
   ~ fur = fur - 300
   -> UnlockCompass -> trade
  - else :
   毛皮不足
   -> trade
}
+ [布料👕 < 毛皮x10/{fur}]
{
  - fur - 10 >= 0 :
   ~ fur = fur - 10
   ~ cloth = cloth + 1
    -> trade
  - else :
   毛皮不足
   -> trade
}
+ [贝壳 < 毛皮x100/{fur}]
{
  - fur - 100 >= 0 :
   ~ fur = fur - 100
   ~ shell = shell +1 
   -> trade
  - else :
   毛皮不足
   -> trade
}
+ [返回上级]
-> HomeOption

== manufacture ==//1
｜
<决策中心💡> => <制造🛠>

+ {SmallWaterBag==0}[小水袋👝（20容量） < 皮革x30/{leather}]
{
  - leather - 30 >= 0 :
   ~ leather = leather - 30
   ~ SmallWaterBag = 1
   ~ water = 20
   ~ LeftWater = 20
   -> manufacture
  - else :
   材料不足
   -> manufacture
}
+ {SmallLeatherBag==0}[小皮包👜（20容量） < 皮革x30/{leather},布料x20/{cloth}]
{
  - leather - 30 >= 0 and cloth - 20 >= 0:
   ~ leather = leather - 30
   ~ cloth = cloth - 30
   ~ SmallLeatherBag = 1
   ~ space =20
   ~ FreeSpace = 20
   -> manufacture
  - else :
   材料不足
   -> manufacture
}
+ {weapon==0}[骨刃🔪(2伤害)  < 木头x1000/{wood},皮革x100/{leather},牙齿x100/{teeth}]
{
  - leather - 100 >= 0 and wood - 1000 >= 0 and teeth - 100 >=0:
   ~ leather = leather - 100
   ~ wood = wood - 1000
   ~ teeth = teeth - 100
   ~ weapon = 1
[你做出骨刃，如此一来，便能够在荒野上具有一定的自卫能力了]
   -> manufacture
  - else :
   材料不足
   -> manufacture
}
+ [返回上级]
-> HomeOption

== deploy ==//1

｜
<决策中心💡> => <部署🚹> 

目前共有{FreePopulation}人空闲
+ [伐木🪓({CutWood}人)：每次收集 +1木头/人]
++ {FreePopulation>=1}[+1]
~ FreePopulation = FreePopulation -1
~ CutWood = CutWood +1
++ {FreePopulation>=10}[+10]
~ FreePopulation = FreePopulation -10
~ CutWood = CutWood +10
++ {CutWood>=1}[-1]
~ FreePopulation = FreePopulation +1
~ CutWood = CutWood -1
++ {CutWood>=10}[-10]
~ FreePopulation = FreePopulation +10
~ CutWood = CutWood -10
++ { FreePopulation == 0 } {CutWood == 0}[请尝试削减其他工作的人数]
-- -> deploy

+ {HuntHouse == 1}[狩猎🏹({hunt }人)：每次收集 +1肉+1毛皮/人]
~ HuntDeploy=1
++ {FreePopulation>=1}[+1]
~ FreePopulation = FreePopulation -1
~ hunt = hunt +1
++ {FreePopulation>=10}[+10]
~ FreePopulation = FreePopulation -10
~ hunt = hunt +10
++ {hunt >=1}[-1]
~ FreePopulation = FreePopulation +1
~ hunt = hunt -1
++ {hunt >=10}[-10]
~ FreePopulation = FreePopulation +10
~ hunt = hunt -10
++ { FreePopulation == 0 }{hunt == 0}[请尝试削减其他工作的人数]
-- -> deploy

+ {BaconHouse == 1}[熏肉🍗({SmokeMeat }人)：每次收集 -5肉-5木头+1熏肉/人]
++ {FreePopulation>=1}[+1]
~ FreePopulation = FreePopulation -1
~ SmokeMeat = SmokeMeat +1
++ {FreePopulation>=10}[+10]
~ FreePopulation = FreePopulation -10
~ SmokeMeat = SmokeMeat +10
++ {SmokeMeat >=1}[-1]
~ FreePopulation = FreePopulation +1
~ SmokeMeat = SmokeMeat -1
++ {SmokeMeat >=10}[-10]
~ FreePopulation = FreePopulation +10
~ SmokeMeat = SmokeMeat -10
++ { FreePopulation == 0 }{SmokeMeat == 0}[请尝试削减其他工作的人数]
-- -> deploy

+ {LeatherHouse == 1}[制革💼({TanLeather }人)：每次收集 -5毛皮+1皮革/人]
++ {FreePopulation>=1}[+1]
~ FreePopulation = FreePopulation -1
~ TanLeather = TanLeather +1
++ {FreePopulation>=10}[+10]
~ FreePopulation = FreePopulation -10
~ TanLeather = TanLeather +10
++ {TanLeather >=1}[-1]
~ FreePopulation = FreePopulation +1
~ TanLeather = TanLeather -1
++ {TanLeather >=10}[-10]
~ FreePopulation = FreePopulation +10
~ TanLeather = TanLeather -10
++ { FreePopulation == 0 }{TanLeather == 0}[请尝试削减其他工作的人数]
-- -> deploy

+ [返回上级]
-> HomeOption



== build ==//1

｜
<决策中心💡> => <建造🪜>

+ [建造房屋 需求木头🪵：{wood}/{200 + 50 * house}]
{
  - wood - ( 200 + 50 * house ) >= 0 :
   -> AddHouse -> build
  - else :
   木头不足
   -> build
}
//
+ [建造陷阱🪤 需求木头🪵：{wood}/{10 + 10 * trap}]
{ 
  - wood - ( 10 + 10 * trap ) >= 0 :
   -> AddTrap -> build
  - else :
   木头不足
   -> build
}
//
+ { house >= 4 and HuntHouse == 0}[解锁狩猎小屋⛺️ 需求—木头🪵：{wood}/300—毛皮{fur}/10—肉{meat}/20]
{ 
  - wood >= 300 and fur >= 10 and meat >= 20 :
   -> UnlockHuntHouse -> build
  - else :
   材料不足
   -> build
}
-> HomeOption
//
+ { house < 4 }[(建造4座房屋🏠以解锁更多建筑)]
-> build
//
+ { HuntHouse == 1 and BaconHouse == 0}[解锁熏肉工坊🏭 需求—木头：{wood}/400—毛皮{fur}/60—肉{meat}/100]
{ 
  - wood >= 400 and fur >= 60 and meat >= 100 :
   -> UnlockBaconHouse -> build
  - else :
   材料不足
   -> build
}
-> HomeOption
//
+ { HuntHouse == 1 and LeatherHouse == 0}[解锁制革工坊🏭 需求—木头🪵：{wood}/600—毛皮{fur}/100]
{ 
  - wood >= 600 and fur >= 100 :
   -> UnlockLeatherHouse -> build
  - else :
   材料不足
   -> build
}
-> HomeOption
//
+ { BaconHouse == 1 and LeatherHouse == 1 and workshop == 0 }[解锁加工车间🏭 需求—木头🪵：{wood}/400—皮革💼{leather}/10—熏肉🍗{bacon}/20]
{ 
  - wood >= 400 and leather >= 10 and bacon >= 20 :
   -> UnlockWorkshop -> build
  - else :
   材料不足 
   -> build
}
-> HomeOption
//
+ { BaconHouse == 1 and LeatherHouse == 1 and TradeHouse == 0 }[解锁交易站 需求—木头🪵：{wood}/600—皮革💼{leather}/20—熏肉🍗{bacon}/40]
{ 
  - wood >= 600 and leather >= 20 and bacon >= 40 :
   -> UnlockTradeHouse -> build
  - else :
   材料不足 
   -> build
}
-> HomeOption
//
+ [返回上级]
-> HomeOption


== AddTrap ==//2
~ wood = wood - ( 10 + 10 * trap )
~ trap = trap + 1
部署了一个陷阱🪤，现有{trap}个
->->
== AddHouse ==//2
~ wood = wood - ( 200 + 50 * house )
~ house = house + 1
~ MaxPopulation = house*4
~ FreePopulation = FreePopulation+4

营地新增了一栋房子🏠，现有{house}座
营地现在可以接纳{MaxPopulation}人

->->

== UnlockHuntHouse ==//2
~ HuntHouse = 1
~ wood = wood - 300
~ fur = fur - 10
~ meat = meat - 20

经过一番努力，终于是将狩猎小屋建好了，现在，猎人们在此集结，可以前去外出狩猎。
[现在，你可以部署村民们前去狩猎了]
->->
== UnlockBaconHouse ==//2
~ BaconHouse = 1
~ wood = wood - 400
~ fur = fur - 60
~ meat = meat - 100

熏肉房建好了，现在能够将肉制作成熏肉，以便保存更长时间
[现在，你可以部署村民们前去熏肉了]
->->
== UnlockLeatherHouse ==//2
~ LeatherHouse = 1
~ wood = wood - 600
~ fur = fur - 100

制革房建好了，现在能够将毛皮制作成皮革，以便进行进一步加工
[现在，你可以部署村民们前去制革了]
->->

== UnlockWorkshop ==
~ workshop = 1
~ wood = wood - 400
~ leather = leather - 10
~ bacon = bacon - 20

加工车间建好了，众所周知，科技改变生活
[现在，你可以利用物资制作更加复杂的物品]
->->

== UnlockTradeHouse ==
~ TradeHouse = 1
~ wood = wood - 600
~ leather = leather - 20
~ bacon = bacon - 40

交易站建好了，在这里可以买到好东西
[现在，你可以利用资源进行各种交换]
->->

== UnlockCompass ==
~ compass = 1

你买到了一个罗盘，它可以指引营地的方向
[现在，你可以进行野外冒险了]
->->

== collect ==//1

｜
<决策中心> => <收集>
~ wood = wood + 10 + CutWood
男人外出收集了{10+CutWood}个木头
现在营地里的木头有{wood}个
{
  - trap>0:
  男人检查了陷阱,发现了一些东西
  ~ meat = meat+RANDOM(trap/2,trap)+hunt *1
  ~ fur = fur+RANDOM(trap/2,trap)+hunt *1
  ~ bone = bone+RANDOM(trap/70,trap/50)+  INT(RANDOM(0,200)/100)
  ~ teeth = teeth+RANDOM(trap/50,trap/30)+  INT(RANDOM(0,120)/100)
  ~ shell = shell+RANDOM(trap/50,trap/30)+  INT(RANDOM(0,120)/100)
}
{
  - LeatherHouse == 1 and fur >= 5 :
  ~ fur = fur - TanLeather*5
  ~ leather = leather + TanLeather
}
{
  - BaconHouse == 1 and meat >= 5 and wood >= 5 :
  ~ meat = meat - SmokeMeat*5
  ~ wood = wood - SmokeMeat*5
  ~ bacon = bacon + SmokeMeat
}
->->

 
== information ==//1
```
【基本物资】
木头  ：{wood} 
肉    ：{meat}
毛皮  ：{fur}
贝壳  ：{shell} 
骨头  ：{bone}
牙齿  ：{teeth}
熏肉  : {bacon}
皮革  : {leather}
.
.
【生产力相关】
总人口：{MaxPopulation}
空闲  ：{FreePopulation}
.
房屋  ：{house}
陷阱  ：{trap}
.
.
【进度】
{collect>=1:进行一次收集(解锁建造)}
{trap>=1:建造1个陷阱（解锁信息面板）}
{house>=2:建造两座房子（解锁部署）}
{HuntHouse==1:建造猎人小屋（解锁狩猎部署）}
{BaconHouse==1:建造熏肉工坊（解锁熏肉部署）}
{LeatherHouse==1:建造制革工坊（解锁制革部署）}
{workshop==1:建造加工车间（解锁制造）}
{TradeHouse==1:建造交易站（解锁交易）}
{compass==1:购买罗盘(解锁冒险)}
{SmallWaterBag==1 and SmallLeatherBag==1:初级探险装备}
.
.
.
```

->->
