INCLUDE gyc.ink
INCLUDE array.ink
INCLUDE fn.ink
INCLUDE amount.ink
INCLUDE sentence.ink
INCLUDE townsentence.ink
~ 2d_initial_set_1(item_pack,0)
~ 2d_initial_set_2(item_pack,10,0,0)

这是一个rpg战斗游戏，由于数组的出现，我准备重新制作一个 
-> initial_setting

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

== initial_setting ==
= greeting
【你好！冒险者！欢迎来到这个不知名的世界】
【但是在这之前，你得先编辑自己的个人信息】
1、设置名字（只能支持英文）
-> set_name

= set_name

+[q   w   e   r   t   y   u   i   o   p]
++[q]
~ set(player_information,19,get(player_information,19)+"q")
名字:{get(player_information,19)}
-> set_name
++[w]
~ set(player_information,19,get(player_information,19)+"w")
名字:{get(player_information,19)}
-> set_name
++[e]
~ set(player_information,19,get(player_information,19)+"e")
名字:{get(player_information,19)}
-> set_name
++[r]
~ set(player_information,19,get(player_information,19)+"r")
名字:{get(player_information,19)}
-> set_name
++[t]
~ set(player_information,19,get(player_information,19)+"t")
名字:{get(player_information,19)}
-> set_name
++[y]
~ set(player_information,19,get(player_information,19)+"y")
名字:{get(player_information,19)}
-> set_name
++[u]
~ set(player_information,19,get(player_information,19)+"u")
名字:{get(player_information,19)}
-> set_name
++[i]
~ set(player_information,19,get(player_information,19)+"i")
名字:{get(player_information,19)}
-> set_name
++[o]
~ set(player_information,19,get(player_information,19)+"o")
名字:{get(player_information,19)}
-> set_name
++[p]
~ set(player_information,19,get(player_information,19)+"p")
名字:{get(player_information,19)}
-> set_name

+  [a   s   d   f   g   h   j   k   l]
++[a]
~ set(player_information,19,get(player_information,19)+"a")
名字:{get(player_information,19)}
-> set_name
++[s]
~ set(player_information,19,get(player_information,19)+"s")
名字:{get(player_information,19)}
-> set_name
++[d]
~ set(player_information,19,get(player_information,19)+"d")
名字:{get(player_information,19)}
-> set_name
++[f]
~ set(player_information,19,get(player_information,19)+"f")
名字:{get(player_information,19)}
-> set_name
++[g]
~ set(player_information,19,get(player_information,19)+"g")
名字:{get(player_information,19)}
-> set_name
++[h]
~ set(player_information,19,get(player_information,19)+"h")
名字:{get(player_information,19)}
-> set_name
++[j]
~ set(player_information,19,get(player_information,19)+"j")
名字:{get(player_information,19)}
-> set_name
++[k]
~ set(player_information,19,get(player_information,19)+"k")
名字:{get(player_information,19)}
-> set_name
++[l]
~ set(player_information,19,get(player_information,19)+"l")
名字:{get(player_information,19)}
-> set_name

+    [z   x   c   v   b   n   m]
++[z]
~ set(player_information,19,get(player_information,19)+"z")
名字:{get(player_information,19)}
-> set_name
++[x]
~ set(player_information,19,get(player_information,19)+"x")
名字:{get(player_information,19)}
-> set_name
++[c]
~ set(player_information,19,get(player_information,19)+"c")
名字:{get(player_information,19)}
-> set_name
++[v]
~ set(player_information,19,get(player_information,19)+"v")
名字:{get(player_information,19)}
-> set_name
++[b]
~ set(player_information,19,get(player_information,19)+"b")
名字:{get(player_information,19)}
-> set_name
++[n]
~ set(player_information,19,get(player_information,19)+"n")
名字:{get(player_information,19)}
-> set_name
++[m]
~ set(player_information,19,get(player_information,19)+"m")
名字:{get(player_information,19)}
-> set_name
+ [确认]
-> name_confirm

+ [清空]
~ set(player_information,19,"")
名字:{get(player_information,19)}
-> set_name


= name_confirm
【好了！你叫"{get(player_information,19)}"对吧？】

+ “我再想想...”
~  set(player_information, 19,"")
-> set_name

+ “是！”
【那么接下来，设置你的属性吧！注意你只有3点】

-> set_point


= set_point

+ {get(player_information,15)+get(player_information,14) <= 4}[体能（决定你的物理属性）]
~ set(player_information,14,get(player_information,14)+1)
```
体能：{get(player_information,14)} 
精神: {get(player_information,15)}
```
-> set_point

+ {get(player_information,15)+get(player_information,14) <= 4}[精神（决定你的神秘侧能力强度）]
~ set(player_information,15,get(player_information,15)+1)
```
体能：{get(player_information,14)} 
精神: {get(player_information,15)}
```
-> set_point

+ {get(player_information,15)+get(player_information,14) == 5}[确认]
【好的！那么接下来，你想变成什么种族呢？】
-> set_race
+ {get(player_information,15)+get(player_information,14) == 5}[重置]
~ set(player_information,15,1)
~ set(player_information,14,1)
-> set_point


= set_race

+ [人类（发展均衡的生物）]
~ set(player_information,16, "人类")
-> set_race ->
+ [精灵（魔法强大的生物）]
~ set(player_information,16, "精灵")
-> set_race
+ [兽人（武力高强的生物）]
~ set(player_information,16, "兽人")
-> set_race
+ 确认为 {get(player_information,16)} !
-> set_sex

= set_sex
【确认你的性别】
+ 男
~ set(player_information,13,"男")
+ 女
~ set(player_information,13,"女")
+ 无
~ set(player_information,13,"无")
- ~ attribute()
- ~ set(player_information,3,get(player_information,2))
- ~ set(player_information,1,get(player_information,0))
- -> point_examine -> point_confirm

= point_confirm
【你确定吗？】
+ [确定]
【好！人物已生成】

-> bordertown
+ [否定]
-> set_point

== explore_bordertown_forest ==
【你来到了一处森林】
~ set(player_information,17, "边陲小镇：森林")

【时间：  {get(player_information,18)}：00】
-> choice1
= choice1
+ [搜寻猎物]
-> explore
+ [回城]
-> bordertown
+ [个人信息]
-> point_examine ->
-> choice1
+ [打开背包]
-> item_pack_examine ->
++ [移动物品]
-> item_pack_item_exchange ->
-> choice1
++ [返回]
-> choice1

