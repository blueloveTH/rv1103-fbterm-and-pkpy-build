//====以下是角色属性
VAR blood= 0 
//血上限
VAR tem_blood=0
//目前血量
VAR energy= 0
//mp上限
VAR tem_energy=0
//目前mp
VAR p_attact= 0
//物攻
VAR m_attact= 0
//魔攻
VAR p_defense= 0
//物防
VAR m_defense= 0
//魔防
VAR intelligence= 0
//智力，用于特殊事件的判定
VAR endurance= 0
//耐力，用于特殊事件的判定
VAR level= 0
//等级
VAR xp= 0
//经验上限
VAR tem_xp=0
//目前经验
VAR sex= "male"
//性别，没任何作用
VAR tn= 1
//体能点数，物理属性都附加值
VAR js= 1
//精神点数，魔法属性的附加值

//====以下是角色种族和角色的伤害类型
//种族决定未来每升一级所增加的各项属性的多少，相当于潜力，伤害类型决定伤害是物理伤害还是魔法伤害
VAR race= "人类"
VAR weapon= "物理"
//以下是怪物的属性
VAR monster_blood= 0
VAR monster_tem_blood= 0
VAR monster_energy= 0
VAR monster_tem_energy=0
VAR monster_p_attact= 0
VAR monster_m_attact= 0
VAR monster_p_defense= 0
VAR monster_m_defense= 0
VAR monster_level= 0
VAR monster_tn= 1
VAR monster_js= 1
//以下是怪物的种族和怪物的伤害类型
VAR monster_race= ""
VAR monster_weapon= "物理"
//以下是世界时间和角色所处的场景，这决定了能够遇到的怪物的类型，强度，以及特殊事件
VAR time= 0
VAR location="???"



-> initial_setting
//以下是一个用来推进时间的函数
== function add_time(x) ==
{
- time+x<24:
~ time= time+x
- time+x>=24:
~ time= time+x-24
}
//以下是一个用来计算怪物属性的函数
== function monster_attribute(x,y,z) ==
// (种族，体能点比例，精神点比例）
//先根据角色等级随机出怪物等级，然后通过输入的点数比例计算怪物de体能点和精神点，最后结合种族，等级，加点来计算怪物的战斗属性
{x:
- "野猪":
~ monster_level= RANDOM(level,level+10)
~ monster_tn= (monster_level+5)/(z+y)*y
~ monster_js= (monster_level+5)/(z+y)*z
~ monster_blood= monster_tn*20*1 + monster_level*20*0.5
~ monster_energy= INT(js*20 *1.5 +monster_level*20*0.5)
~ monster_p_attact= monster_tn*5 *1.5 +monster_level*0.5
~ monster_m_attact= monster_js*5 *1.5+monster_level*0.5
~ monster_p_defense= monster_tn*1 *1.5+monster_level*0.5
~ monster_m_defense= monster_js*1 *1.5+monster_level*0.5
}
~ monster_tem_blood= monster_blood
~ monster_tem_energy= monster_energy

//这是一个用来计算角色属性的函数，计算方法和怪物相同
== function attribute() ==
{race: 
- "人类": 
~ blood= tn*20 *1.5 + level*20*1.5
~ energy= INT(js*20 *1.5 +level*20*1.5)
~ p_attact= tn*5 *1.5 +level*1.5
~ m_attact= js*5 *1.5+level*1.5
~ p_defense= tn*1 *1.5+level*1.5
~ m_defense= js*1 *1.5+level*1.5
~ intelligence= js*1 *1.5+level*1.5
~ endurance= tn*1 *1.5+level*1.5
~ xp= INT(10*POW(10,0.2*level))
- "精灵": 
~ blood= tn*20 *1 +level*20
~ energy= INT(js*20 *2 +level*20*2)
~ p_attact= tn*5 *1 +level
~ m_attact= js*5 *2+level*2
~ p_defense= tn*1 *1+level
~ m_defense= js*1 *2+level*2
~ intelligence= js*1 *2+level*2
~ endurance= tn*1 *1+level
~ xp= INT(10*POW(10,0.2*level))
- "兽人": 
~ blood= tn*20 *2+level*20
~ energy= INT(js*20 *1+level*20)
~ p_attact= tn*5 *2+level*2
~ m_attact= js*5 *1+level
~ p_defense= tn*1 *2+level*2
~ m_defense= js*1 *1+level
~ intelligence= js*1*1+level
~ endurance= tn*1 *2+level*2
~ xp= INT(10*POW(10,0.2*level))
}


//这是一个用来计算人物血量变化的函数，只要输入一个值，负数表示扣血，正数表示加血，大部分情况下，还要在下一行跳转到用来扣血的节点以便一站式显示血量，以及处理人物或怪物死亡的情况
== function add_tem_blood(x) ==
{ 
- tem_blood + x <= 0 :
~ tem_blood=0

- tem_blood + x >= blood :
~ tem_blood=blood

- tem_blood + x > 0 and tem_blood + x < blood :
~ tem_blood=tem_blood+x
}

//这是用来计算怪物血量变化的
== function add_monster_tem_blood(x) ==
{ 
- monster_tem_blood + x <= 0 :
~ monster_tem_blood=0

- monster_tem_blood + x >= blood :
~ monster_tem_blood=blood

- monster_tem_blood + x > 0 and monster_tem_blood + x < blood :
~ monster_tem_blood=monster_tem_blood+x
}




//这是一个用来计算角色mp变化的函数，大部分情况下，还要在下一行跳转到用来扣mp的小节以便显示剩余mp
== function add_monster_tem_energy(x) ==
{
- monster_tem_energy + x <= 0 :
~ monster_tem_energy=0

- monster_tem_energy + x >= monster_energy :
~ monster_tem_energy=monster_energy

- monster_tem_energy + x > 0 and monster_tem_energy + x < monster_energy :
~ monster_tem_energy=monster_tem_energy+x
}

//这是用来计算怪物mp变化的函数
== function add_tem_energy(x) ==
{
- tem_energy + x <= 0 :
~ tem_energy=0

- tem_energy + x >= energy :
~ tem_energy=energy

- tem_energy + x > 0 and tem_energy + x < energy :
~ tem_energy=tem_energy+x
}



//这是用来计算角色对怪物造成伤害的函数，大部分情况下，是作为计算血量变化的函数的变量使用的，伤害分为物理伤害和魔法伤害，对应物理防御和魔法防御分开计算
== function player_hit_monster_dammage() ==
{weapon:
- "物理":
{
  - p_attact - monster_p_defense >=0:
  ~ return (p_attact - monster_p_defense)
  - p_attact - monster_p_defense <0:
  ~ return 0
}
- "魔法":
{
  - m_attact - monster_m_defense >=0:
  ~ return (m_attact - monster_p_defense)
  - m_attact - monster_m_defense <0:
  ~ return 0
}
}

//这是用来计算怪物对角色造成伤害的函数
== function monster_hit_player_dammage() ==
{monster_weapon:
- "物理":
{
  - monster_p_attact - p_defense >=0:
  ~ return (monster_p_attact - p_defense)
  - monster_p_attact - p_defense <0:
  ~ return 0
}
- "魔法":
{
  - monster_m_attact - m_defense >=0:
  ~ return (monster_m_attact - p_defense)
  - monster_m_attact - m_defense <0:
  ~ return 0
}
}


//这是用来计算角色获取经验的函数，一般下一行会跳转到升级小节，用来一站式处理角色的加点，回状态，以及信息显示
== function add_tem_xp(x) ==
{
- tem_xp + x <= 0 :
~ tem_xp=0

- tem_xp + x >= xp :
~ tem_xp=xp

- tem_xp + x > 0 and tem_xp + x < xp :
~ tem_xp=tem_xp+x
}

//扣能量小节
== word_energy ==
 【你的能量剩余 {tem_energy}/{energy}】
 ->->
 
 //角色扣血小节，当然这里也承包了死亡的功能
== word_blood ==
【你的血量为 {tem_blood}/{blood}】
{ tem_blood == 0 :
 【你死了】
  ~ tem_blood = blood
  ~ add_tem_xp(-xp/5)
 【你在小教堂复活了】
 【你的经验将被清空】
 ~ location= "小教堂"
  -> initial_setting.point_examine -> test2///////
}
->->

//升级小节
== word_xp ==
 【你的经验为 {tem_xp}/{xp}】
{tem_xp == xp :
 【你升级了】
 【level {level} ＞＞ level {level+1}】
 ~ level=level+1
 ~ tem_xp = 0
 【请进行加点】
 -> word_add_point ->
 
} 
->->

//怪物扣血小节，这里也承包了战斗结算的功能
== word_monster_blood ==
【{monster_race}的血量为 {monster_tem_blood}/{monster_blood}】
{ monster_tem_blood == 0 :
{monster_race:
  - "野猪": -> word_kill_pig ->
}
~ add_tem_xp(INT(10*POW(10,0.2*monster_level)/5))
-> word_xp ->
【你休息了一会，逐步治疗了创伤，并且恢复了能量】
~ tem_energy=energy
~ tem_blood=blood
+ [接下来，继续探索吧]
-> test2.choice1
+ [算了算了，还是回小镇吧]
这个小镇没做好
-> test2.choice1
 
-else :
->->
}

//以下是杀死怪物的一段剧情
== word_kill_pig ==
【"嗷呜......嗷嗷嗷......嗷嗷嗷！"
野猪仰天嘶吼着，它的声音之中充满了浓郁的悲伤和绝望，它的内心中有着深深的悲伤，有着无穷无尽的仇恨，它倒在地上奄奄一息，一动也不动，它的脖子处有一道深深的伤口，已经被切断了....】
【你杀死了野猪，奖励经验{INT(10*POW(10,0.2*monster_level)/5)}】
->->


//加点小节
== word_add_point ==
 + [体能（决定你的物理属性）]
~ tn=tn+1
体能：{tn} \
精神: {js}


+ [精神（决定你的神秘侧能力强度）]
~ js=js+1
体能：{tn} \
精神: {js}

- ~ attribute()
- ~ tem_energy=energy
- ~ tem_blood=blood
- -> initial_setting.point_examine ->
->->

//怪物属性显示器
== monster_point_examine ==
  种族: {monster_race}
  ———————————————————————————\
  等级: {monster_level}\
  ———————————————————————————\
  血量: {monster_tem_blood}/{monster_blood}\
  能量: {monster_tem_energy}/{monster_energy}\
  ———————————————————————————\
  物攻: {monster_p_attact}    <>
  魔攻: {monster_m_attact}\
  物防: {monster_p_defense}    <>
  魔防: {monster_m_defense}\
  ->->
  
  //探索小节，会根据location，也就是角色位置的不同而输出不同的剧情
== explore ==
{location == "未知森林":
   ~ add_time(1) 
  【你正在进行搜索】
  【过了一个小时
 现在是： {time}:00】

  {~ 【你听到远处传来了一声怒吼，接着就是一阵狂风袭过，吹得树木乱颤，地面上的灰尘被吹起，像一根根钢针一样直插天空，看到这个景象，你赶紧跑向声音发出之地。\你看到一个庞大的巨兽从一棵树上掉落下来，直挺挺的砸在地上，溅起一阵烟尘。这个巨兽的身形非常高大，足足有二三十米高，而且还是四肢着地，四只粗壮的手臂撑住了地面，整个脑袋趴在地上，嘴巴张得很大，露出锋利的牙齿，獠牙闪着寒光，看起来狰狞恐怖。\这个巨兽的外表非常怪异，但是这个巨兽长得实在太凶悍了，简直就是一个恐龙。-> tree_turtle |                                     【走了没多久，就听到 \"吼~！""吼~！""吼~！"\突然传来了几声低沉的咆哮声，这声音听起来似乎很熟悉，仔细一听却发现并不是人类的声音。】->pig }
}






//npc战斗流程
//这是树龟的战斗流程，当然，我还没做
== tree_turtle ==
+ [今天的猎物就决定是你了！]
-> battle

+ [算了算了，还是离远点吧]
-> test2.choice1
= battle
+ 未完成，点击返回
-> test2.choice1

//这是野猪的战斗流程
== pig ==
+ [走上去看看]
【这时候，你已经听到了越来越近的脚步声了，这声音显然是狼群发出来的。\
这个地方居然会出现狼群，真是奇怪。\
你迅速的朝着森林深处走去，你想先避避风头，等狼群散去了再回来，不过你并没有发现有什么危险，反而是有些兴奋，因为在这里，你遇到了一只野猪，这只野猪长得肥头大耳的，看上去似乎是一只公的。】
++ [算了算了，还是离远点吧]
-> test2.choice1
++ [绕到背后，看看能不能进行偷袭]
-> battle

+ [算了算了，还是离远点吧]
-> test2.choice1

= battle
//生成怪物，利用怪物属性函数来为那些决定怪物属性的变量赋值
~ monster_race= "野猪"
~ monster_attribute(monster_race,3,1)

【你成功地来到了野猪背后，而野猪似乎并没有注意到你】

+ [查看目标信息]
-> monster_point_examine ->
++ [暴起！举刀！挥砍！]
-> battle2
++ [算了算了，还是离远点吧]
-> test2.choice1
+ [算了算了，还是离远点吧]
-> test2.choice1


//从这行往上，都是战前剧情，以下是真正的战斗部分
== battle2
//这里是玩家先手
~ add_monster_tem_blood(-player_hit_monster_dammage())
【你一刀结结实实地砍在了野猪的背上，对其造成了 {player_hit_monster_dammage()} 点伤害】
-> word_monster_blood ->
“嗷！～～～”
【野猪发出了杀猪般的叫声（实际上就是在杀猪）】
【肉眼可见地，刀锋破开了野猪的皮肤，
鲜血狂涌而出，瞬间染红了整张皮毛，而这只野猪则是痛苦万分地嘶吼着，疯狂的挣扎着，却无济于事。
"吼！"
野猪猛地抬起头颅，猩红色的眸子中带着愤怒与仇恨，转头狠狠瞪向了站在背后持刀准备再一次挥砍的你】
-> battle3
//battle3是一个循环的回合制
= battle3
+ [疾步后撤～～]
【你于是拔出砍刀，疾步后撤，避免被这只野猪追上，可是这只野猪却依旧紧随其后，并且不停的咆哮，那种恐怖声音震撼心弦，让人不由自主地打了个寒颤。】
【野猪的速度很快，几乎就是眨眼间的功夫就已经冲到了你的面前，锋利而尖锐的獠牙毫不犹豫的朝着你的喉咙刺去，你赶忙用手护住自己的脖子，但还是晚了一步，这只野猪的獠牙正好刺穿了你的手掌，顿时鲜血顺着手掌流淌，那种冰冷刺骨的痛楚让你不禁发出了惨叫声。】
【你受到了{monster_hit_player_dammage()}点伤害】
~ add_tem_blood(-monster_hit_player_dammage())
-> word_blood ->

++ [进行反击]
~ add_monster_tem_blood(-player_hit_monster_dammage())
【"噗呲"锋利的牙齿撕裂衣服的声音响起，你身形一晃，堪堪躲过了野猪那锋利的一击，随即右脚抬起狠狠踹向野猪的肚皮, 对其造成了 {player_hit_monster_dammage()} 点伤害】
-> word_monster_blood ->
"吼吼吼吼！"
【野猪发狂般地叫喊着，猩红的眸子闪烁着嗜血的光芒，疯狂地咆哮着，似乎要把你吞噬殆尽】
【野猪冲向了你！你的身体被一股巨大的推力撞飞。】
【你受到了{monster_hit_player_dammage()}点伤害】
~ add_tem_blood(-monster_hit_player_dammage())
-> word_blood ->

-> battle3

+ [再一次攻过去]
~ add_monster_tem_blood(-player_hit_monster_dammage())
【"噗呲！"
又一块皮肉被切割了下来，鲜血喷洒，对其造成了 {player_hit_monster_dammage()} 点伤害】
-> word_monster_blood ->
"吼吼吼吼！"
【野猪发狂般地叫喊着，猩红的眸子闪烁着嗜血的光芒，疯狂地咆哮着，似乎要把你吞噬殆尽】
【野猪冲向了你！你的身体被一股巨大的推力撞飞。】
【你受到了{monster_hit_player_dammage()}点伤害】
~ add_tem_blood(-monster_hit_player_dammage())
-> word_blood ->

-> battle3







//正式流程

== initial_setting ==
= greeting
【你好！冒险者！欢迎来到这个不知名的世界】
【但是在这之前，你得先编辑自己的个人信息】
1、设置名字（只能支持英文）
-> set_name

= set_name
VAR name= ""

+[q   w   e   r   t   y   u   i   o   p]
++[q]
~ name=name+"q"
名字:{name}
-> set_name
++[w]
~ name=name+"w"
名字:{name}
-> set_name
++[e]
~ name=name+"e"
名字:{name}
-> set_name
++[r]
~ name=name+"r"
名字:{name}
-> set_name
++[t]
~ name=name+"t"
名字:{name}
-> set_name
++[y]
~ name=name+"y"
名字:{name}
-> set_name
++[u]
~ name=name+"u"
名字:{name}
-> set_name
++[i]
~ name=name+"i"
名字:{name}
-> set_name
++[o]
~ name=name+"o"
名字:{name}
-> set_name
++[p]
~ name=name+"p"
名字:{name}
-> set_name

+  [a   s   d   f   g   h   j   k   l]
++[a]
~ name=name+"a"
名字:{name}
-> set_name
++[s]
~ name=name+"s"
名字:{name}
-> set_name
++[d]
~ name=name+"d"
名字:{name}
-> set_name
++[f]
~ name=name+"f"
名字:{name}
-> set_name
++[g]
~ name=name+"g"
名字:{name}
-> set_name
++[h]
~ name=name+"h"
名字:{name}
-> set_name
++[j]
~ name=name+"j"
名字:{name}
-> set_name
++[k]
~ name=name+"k"
名字:{name}
-> set_name
++[l]
~ name=name+"l"
名字:{name}
-> set_name

+    [z   x   c   v   b   n   m]
++[z]
~ name=name+"z"
名字:{name}
-> set_name
++[x]
~ name=name+"x"
名字:{name}
-> set_name
++[c]
~ name=name+"c"
名字:{name}
-> set_name
++[v]
~ name=name+"v"
名字:{name}
-> set_name
++[b]
~ name=name+"b"
名字:{name}
-> set_name
++[n]
~ name=name+"n"
名字:{name}
-> set_name
++[m]
~ name=name+"m"
名字:{name}
-> set_name

+ [确认]
-> name_confirm

+ [清空]
~ name= ""
名字:{name}
-> set_name


= name_confirm
【好了！你叫"{name}"对吧？】

+ “我再想想...”
~ name= ""
-> set_name

+ “是！”
【那么接下来，设置你的属性吧！注意你只有3点】

-> set_point


= set_point

+ {js+tn <= 4}[体能（决定你的物理属性）]
~ tn=tn+1
体能：{tn} \
精神: {js}
-> set_point

+ {js+tn <= 4}[精神（决定你的神秘侧能力强度）]
~ js=js+1
体能：{tn} \
精神: {js}
-> set_point

+ {js+tn == 5}[确认]
【好的！那么接下来，你想变成什么种族呢？】
-> set_race
+ {js+tn == 5}[重置]
~ js=1
~ tn=1
-> set_point


= set_race

+ [人类（发展均衡的生物）]
~ race= "人类"
-> set_race
+ [精灵（魔法强大的生物）]
~ race= "精灵"
-> set_race
+ [兽人（武力高强的生物）]
~ race= "兽人"
-> set_race
+ 确认为 {race} !
-> set_sex

= set_sex
【确认你的性别】
+ 男
~ sex="男"
+ 女
~ sex="女"
+ 无
~ sex="无"
- ~ attribute()
- ~ tem_energy = energy
- ~ tem_blood = blood
- -> point_examine -> point_confirm

= point_examine
~ attribute()
【你的资料是：
\
  名字: {name}\
  种族: {race}    <>
  性别: {sex}\
  位置: {location}    <>
  时间: {time}:00\
  ———————————————————————————\
  等级: {level}\
  经验: {tem_xp}/{xp}\
  ———————————————————————————\
  血量: {tem_blood}/{blood}\
  能量: {tem_energy}/{energy}\
  ———————————————————————————\
  物攻: {p_attact}    <>
  魔攻: {m_attact}\
  物防: {p_defense}    <>
  魔防: {m_defense}\
  ———————————————————————————\
  智力: {intelligence}    <>
  耐力: {endurance}】
  
->->

= point_confirm
【你确定吗？】
+ [确定]
【好！人物已生成】
-> test2
+ [否定]
-> set_point

== test2 ==
【探索及对抗】
【你来到了一处森林】
~ location = "未知森林"
【时间：  {time}：00】
-> choice1
= choice1
+ [搜寻猎物]
-> explore
+ [个人信息]
-> initial_setting.point_examine ->
-> choice1

