
//血上限       0   get(player_information,0)
//目前血量      1  get(player_information,1)
//mp上限       2  get(player_information,2)
//目前mp       3  get(player_information,3)
//物攻         4  get(player_information,4)
//魔攻         5  get(player_information,5)
//物防         6  get(player_information,6)
//魔防         7  get(player_information,7)
//智力         8  get(player_information,8)
//耐力         9  get(player_information,9)
//等级        10  get(player_information,10)
//经验上限     11  get(player_information,11)
//目前经验     12  get(player_information,12)
//性别        13  get(player_information,13)
//体能点数     14  get(player_information,14)
//精神点数     15  get(player_information,15)
//种族        16  get(player_information,16)
//地点        17  get(player_information,17)
//时间        18  get(player_information,18)
//名字        19  get(player_information,19)
//金币        20  get(player_information,20)

//血上限       0  get(monster_information,0)
//目前血量      1  get(monster_information,1)
//物攻         2  get(monster_information,2) 
//魔攻         3  get(monster_information,3)
//物防         4  get(monster_information,4) 
//魔防         5  get(monster_information,5)
//等级        6   get(monster_information,6)
//体能点数     7  get(monster_information,7)
//精神点数     8  get(monster_information,8)
//种族        9  get(monster_information,9)

//0a物品栏编号 
//1b物品名称   
//       0:空 
//       1~99:怪物材料 
//       100～200:采集材料
//       200～300:装备
//2c数量
//3d售价（为0不能出售）
//4e购买价（为0不能购买）
//5f装备等级
//6g装备属性 
//       0:非装备
//       1:物理攻击 
//       2:魔法攻击 
//       3:物理防御 
//       4:魔法防御
//7h装备加成值
//8i潜力（100～1000，属性=等级x潜力）

== shop_buy ==
```
༺༺༺༺༺༼ 购༣入༣物༣品 ༽༻༻༻༻༻


== item_pack_examine ==
```
༺༺༺༺༺༼ 物༣品༣背༣包 ༽༻༻༻༻༻
⓪。。『{item_pack_number_to_text(0)}』X {2d_get(item_pack,0,2,10)}
①。。『{item_pack_number_to_text(1)}』X {2d_get(item_pack,1,2,10)}
②。。『{item_pack_number_to_text(2)}』X {2d_get(item_pack,2,2,10)}
③。。『{item_pack_number_to_text(3)}』X {2d_get(item_pack,3,2,10)}
④。。『{item_pack_number_to_text(4)}』X {2d_get(item_pack,4,2,10)}
⑤。。『{item_pack_number_to_text(5)}』X {2d_get(item_pack,5,2,10)}
⑥。。『{item_pack_number_to_text(6)}』X {2d_get(item_pack,6,2,10)}
⑦。。『{item_pack_number_to_text(7)}』X {2d_get(item_pack,7,2,10)}
⑧。。『{item_pack_number_to_text(8)}』X {2d_get(item_pack,8,2,10)}
⑨。。『{item_pack_number_to_text(9)}』X {2d_get(item_pack,9,2,10)}
༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༺装备栏༻༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶
❶  名称：。。『{item_pack_number_to_text(10)}』
    等级：。。{2d_get(item_pack,10,5,10)}
    效果：。。<>
{2d_get(item_pack,10,6,10):
  - 1:物理攻击+
  - 2:魔法攻击+
  - 3:物理防御+
  - 4:魔法防御+
} <>
{2d_get(item_pack,10,7,10)}
    潜力：。。{2d_get(item_pack,10,8,10)}%
.....................................
❷  名称：。。『{item_pack_number_to_text(11)}』
    等级：。。{2d_get(item_pack,11,5,10)}
    效果：。。<>
{2d_get(item_pack,11,6,10):
  - 1:物理攻击+
  - 2:魔法攻击+
  - 3:物理防御+
  - 4:魔法防御+
} <>
{2d_get(item_pack,11,7,10)}
     潜力：。。{2d_get(item_pack,11,8,10)}%
༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༺金币量༻༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶
金币：{get(player_information,20)}
༺༓༻༓༺༓༻༓༺༓༻༓༺༓༻༓༺༓༻༓༺༓༻
```
->-> 
== item_pack_choose ==
+ [⓪。。『{item_pack_number_to_text(0)}』X {2d_get(item_pack,0,2,10)}]
~ item_pack_code=0
+ [①。。『{item_pack_number_to_text(1)}』X {2d_get(item_pack,1,2,10)}]
~ item_pack_code=1
+ [②。。『{item_pack_number_to_text(2)}』X {2d_get(item_pack,2,2,10)}]
~ item_pack_code=2
+ [③。。『{item_pack_number_to_text(3)}』X {2d_get(item_pack,3,2,10)}]
~ item_pack_code=3
+ [④。。『{item_pack_number_to_text(4)}』X {2d_get(item_pack,4,2,10)}]
~ item_pack_code=4
+ [⑤。。『{item_pack_number_to_text(5)}』X {2d_get(item_pack,5,2,10)}]
~ item_pack_code=5
+ [⑥。。『{item_pack_number_to_text(6)}』X {2d_get(item_pack,6,2,10)}]
~ item_pack_code=6
+ [⑦。。『{item_pack_number_to_text(7)}』X {2d_get(item_pack,7,2,10)}]
~ item_pack_code=7
+ [⑧。。『{item_pack_number_to_text(8)}』X {2d_get(item_pack,8,2,10)}]
~ item_pack_code=8
+ [⑨。。『{item_pack_number_to_text(9)}』X {2d_get(item_pack,9,2,10)}]
~ item_pack_code=9
- ->->
== item_pack_choose2 ==
+ [⓪。。『{item_pack_number_to_text(0)}』X {2d_get(item_pack,0,2,10)}]
~ item_pack_code2=0
+ [①。。『{item_pack_number_to_text(1)}』X {2d_get(item_pack,1,2,10)}]
~ item_pack_code2=1
+ [②。。『{item_pack_number_to_text(2)}』X {2d_get(item_pack,2,2,10)}]
~ item_pack_code2=2
+ [③。。『{item_pack_number_to_text(3)}』X {2d_get(item_pack,3,2,10)}]
~ item_pack_code2=3
+ [④。。『{item_pack_number_to_text(4)}』X {2d_get(item_pack,4,2,10)}]
~ item_pack_code2=4
+ [⑤。。『{item_pack_number_to_text(5)}』X {2d_get(item_pack,5,2,10)}]
~ item_pack_code2=5
+ [⑥。。『{item_pack_number_to_text(6)}』X {2d_get(item_pack,6,2,10)}]
~ item_pack_code2=6
+ [⑦。。『{item_pack_number_to_text(7)}』X {2d_get(item_pack,7,2,10)}]
~ item_pack_code2=7
+ [⑧。。『{item_pack_number_to_text(8)}』X {2d_get(item_pack,8,2,10)}]
~ item_pack_code2=8
+ [⑨。。『{item_pack_number_to_text(9)}』X {2d_get(item_pack,9,2,10)}]
~ item_pack_code2=9
+ {2d_get(item_pack,item_pack_code,6,10)>=1 and 2d_get(item_pack,item_pack_code,6,10)<=2} [替换武器❶『{item_pack_number_to_text(10)}。。Lv.{2d_get(item_pack,10,5,10)}』]
~ item_pack_code2=10
+ {2d_get(item_pack,item_pack_code,6,10)>=3} [替换防具❷『{item_pack_number_to_text(10)}。。Lv.{2d_get(item_pack,11,5,10)}』]
~ item_pack_code2=11
- ->->
== item_pack_item_exchange ==
【选择你想要置换的两个物品栏】
-> item_pack_choose -> 
『{item_pack_code}』
⇩
-> item_pack_choose2 ->
『{item_pack_code2}』
~ item_pack_line_exchange(item_pack_code,item_pack_code2,0)
-> item_pack_examine ->
->->

== point_examine ==
~ attribute()
```
༺༺༺༺༺༼ 角༣色༣资༣料 ༽༻༻༻༻༻
  名字: {get(player_information,19)}
  种族: {get(player_information,16)}    
  性别: {get(player_information,13)}
  位置: {get(player_information,17)}    
  时间: {get(player_information,18)}:00
ི༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶
  等级: {get(player_information,10)}
  经验: {get(player_information,12)}/{get(player_information,11)}
  体能点数；       {get(player_information,14)}
  精神点数：       {get(player_information,15)}
༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶
  血量: {get(player_information,1)}/{get(player_information,0)}
  能量: {get(player_information,3)}/{get(player_information,2)}
༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶
  物攻: {get(player_information,4)}    
  魔攻: {get(player_information,5)}
  物防: {get(player_information,6)}    
  魔防: {get(player_information,7)}
༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶
  智力: {get(player_information,8)}    
  耐力: {get(player_information,9)}】
༺༓༻༓༺༓༻༓༺༓༻༓༺༓༻༓༺༓༻༓༺
  ```
->->

== monster_point_examine ==
```
༺༺༺༺༺༼ 怪༣物༣资༣料 ༽༻༻༻༻༻
  种族: {get(monster_information,9)}
༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶
  等级: {get(monster_information,6)}
༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶
  血量: {get(monster_information,1)}/{get(monster_information,0)}
༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶༶
  物攻: {get(monster_information,2) }    
  魔攻: {get(monster_information,3)}
  物防: {get(monster_information,4) }    
  魔防: {get(monster_information,5)}
༺༓༻༓༺༓༻༓༺༓༻༓༺༓༻༓༺༓༻༓༺
  ```
  ->->
  
  //扣能量小节
== word_energy ==
 【你的能量剩余 {get(player_information,3)}/{get(player_information,2)}】
 ->->
 
 //角色扣血小节，当然这里也承包了死亡的功能
== word_blood ==
【你的血量为 {get(player_information,1)}/{get(player_information,0)}】
{ get(player_information,1) == 0 :
 【你死了】
  ~ set(player_information,3,get(player_information,2))
    ~ set(player_information,1,get(player_information,0))
  ~ add_tem_xp(-get(player_information,11)/5)
 【你在小教堂复活了】
 【你的经验将被清空】
 ~ set(player_information,17, "小教堂")
  -> point_examine -> 
  -> bordertown
}
->->

//升级小节
== word_xp ==
 【你的经验为 {get(player_information,12)}/{get(player_information,11)}】
{get(player_information,12) == get(player_information,11) :
 【你升级了】
 【level {get(player_information,10)} ＞＞ level {get(player_information,10)+1}】
 ~ set(player_information,10,get(player_information,10)+1)
 ~ set(player_information,12, 0)
 【请进行加点】
 -> word_add_point ->
 
} 
->->

//怪物扣血小节，这里也承包了战斗结算的功能
== word_monster_blood ==
【{get(monster_information,9)}的血量为 {get(monster_information,1)}/{get(monster_information,0)}】
{ get(monster_information,1) == 0 :
  {get(monster_information,9):
    - "野猪": -> word_kill_pig ->
  }
  ~ add_tem_xp(gain_monster_xp())
    -> word_xp ->
   【你休息了一会，逐步治疗了创伤，并且恢复了能量】
    ~ set(player_information,3,get(player_information,2))
    ~ set(player_information,1,get(player_information,0))
    + [接下来，继续探索吧]
    {get(player_information,17):
      - "边陲小镇：森林"
      -> explore_bordertown_forest.choice1
    }
    + [算了算了，还是回城吧]
    -> bordertown 
  -else :
    ->->
}

//以下是杀死怪物的一段剧情
== word_kill_pig ==
~ acquire_item_amount= RANDOM(1,INT(POW(get(monster_information,6),0.5)+1))
【"嗷呜......嗷嗷嗷......嗷嗷嗷！"
野猪仰天嘶吼着，它的声音之中充满了浓郁的悲伤和绝望，它的内心中有着深深的悲伤，有着无穷无尽的仇恨，它倒在地上奄奄一息，一动也不动，它的脖子处有一道深深的伤口，已经被切断了....】
【你杀死了野猪，奖励经验{gain_monster_xp()}】
~ temp1 = RANDOM(0,2)
【掉落物品：
{temp1:
  - 0:-> yezhuliaoya -> 
  - 1:-> yezhupi -> 
  - 2:-> yezhurou -> 
}
->->
= yezhuliaoya 

野猪獠牙 X {acquire_item_amount}
+【选择存放位置】
-> item_pack_examine -> item_pack_choose ->
{
  - item_code_judge(item_pack_code,2) == 1:
  ~ add_item_pack_item_code_number(item_pack_code,2,acquire_item_amount+2d_get(item_pack,item_pack_code,2,10))
  - item_code_judge(item_pack_code,2) == 0:
  【无法堆叠】
  -> yezhuliaoya
  }
+ [【丢弃】]
- -> item_pack_examine ->

- ->->

= yezhupi
野猪皮 X {acquire_item_amount}
+【选择存放位置】
-> item_pack_examine -> item_pack_choose ->
{
  - item_code_judge(item_pack_code,3) == 1:
  ~ add_item_pack_item_code_number(item_pack_code,3,acquire_item_amount+2d_get(item_pack,item_pack_code,2,10))
  - item_code_judge(item_pack_code,3) == 0:
  【无法堆叠】
  -> yezhupi
  }
+ [【丢弃】]
- -> item_pack_examine ->

- ->->
= yezhurou

野猪肉 X {acquire_item_amount}
+【选择存放位置】
-> item_pack_examine -> item_pack_choose ->
{
  - item_code_judge(item_pack_code,1) == 1:
  ~ add_item_pack_item_code_number(item_pack_code,1,acquire_item_amount+2d_get(item_pack,item_pack_code,2,10))
  - item_code_judge(item_pack_code,1) == 0:
  【无法堆叠】
  -> yezhurou
  }
+ [【丢弃】]
- -> item_pack_examine ->

- ->->
//加点小节
== word_add_point ==
 + [体能（决定你的物理属性）]
~ set(player_information,14,get(player_information,14)+1)
```
体能：{get(player_information,14)} 
精神: {get(player_information,15)}
```

+ [精神（决定你的神秘侧能力强度）]
~ set(player_information,15,get(player_information,15)+1)
```
体能：{get(player_information,14)} 
精神: {get(player_information,15)}
```
- ~ attribute()
- ~ set(player_information,3,get(player_information,2))
- ~ set(player_information,1,get(player_information,0))
- -> point_examine ->
->->

  //探索小节，会根据location，也就是角色位置的不同而输出不同的剧情
== explore ==
{get(player_information,17) == "边陲小镇：森林":
   ~ add_time(1) 
  【你正在进行搜索】
  【过了一个小时
 现在是： {get(player_information,18)}:00】

  {~ 【你听到远处传来了一声怒吼，接着就是一阵狂风袭过，吹得树木乱颤，地面上的灰尘被吹起，像一根根钢针一样直插天空，看到这个景象，你赶紧跑向声音发出之地。\你看到一个庞大的巨兽从一棵树上掉落下来，直挺挺的砸在地上，溅起一阵烟尘。这个巨兽的身形非常高大，足足有二三十米高，而且还是四肢着地，四只粗壮的手臂撑住了地面，整个脑袋趴在地上，嘴巴张得很大，露出锋利的牙齿，獠牙闪着寒光，看起来狰狞恐怖。\这个巨兽的外表非常怪异，但是这个巨兽长得实在太凶悍了，简直就是一个恐龙。-> search_tree_turtle |                                     【走了没多久，就听到 \"吼~！""吼~！""吼~！"\突然传来了几声低沉的咆哮声，这声音听起来似乎很熟悉，仔细一听却发现并不是人类的声音。】-> search_pig }
}






//npc战斗流程
//这是树龟的战斗流程，当然，我还没做
== search_tree_turtle ==
+ [今天的猎物就决定是你了！(別选这个)]
-> battle

+ [算了算了，还是离远点吧]
-> explore_bordertown_forest.choice1

- + 未完成，点击返回
-> explore_bordertown_forest.choice1

//这是野猪的战斗流程
== search_pig ==
+ [走上去看看]
【这时候，你已经听到了越来越近的脚步声了，这声音显然是狼群发出来的。\
这个地方居然会出现狼群，真是奇怪。\
你迅速的朝着森林深处走去，你想先避避风头，等狼群散去了再回来，不过你并没有发现有什么危险，反而是有些兴奋，因为在这里，你遇到了一只野猪，这只野猪长得肥头大耳的，看上去似乎是一只公的。】
++ [算了算了，还是离远点吧]
-> explore_bordertown_forest.choice1
++ [绕到背后，看看能不能进行偷袭]
-> check_pig
+ [算了算了，还是离远点吧]
-> explore_bordertown_forest.choice1

= check_pig
//生成怪物，利用怪物属性函数来为那些决定怪物属性的变量赋值
~ set(monster_information,9,"野猪")
~ monster_attribute(get(monster_information,9),9,1)

【你成功地来到了{get(monster_information,9)}背后，而目标似乎并没有注意到你】

+ [查看目标信息]
-> monster_point_examine ->
++ [攻击]
-> battle
++ [算了算了，还是离远点吧]
-> explore_bordertown_forest.choice1


== battle ==
//这里是玩家先手
//battle是一个循环的回合制
+ [发动攻击]
~ add_monster_tem_blood(-player_hit_monster_dammage())
【你对{get(monster_information,9)}造成了 {player_hit_monster_dammage()} 点伤害】
-> word_monster_blood ->
【{get(monster_information,9)}对你发动了攻击，你受到了{monster_hit_player_dammage()}点伤害】
~ add_tem_blood(-monster_hit_player_dammage())
-> word_blood ->
-> battle
