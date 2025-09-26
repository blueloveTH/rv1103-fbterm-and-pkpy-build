
VAR blood= 0
VAR tem_blood=0
VAR energy= 0
VAR tem_energy=0
VAR p_attact= 0
VAR m_attact= 0
VAR p_defense= 0
VAR m_defense= 0
VAR intelligence= 0
VAR endurance= 0
VAR level= 0
VAR xp= 0
VAR tem_xp=0
VAR sex= "male"
VAR tn= 1
VAR js= 1
VAR race= "人类"


== function attribute() ==
{race: 
- "人类": 
~ blood= tn*20 *1.5 + level*20*1.5
~ energy= js*20 *1.5 +level*1.5
~ p_attact= tn*5 *1.5 +level*1.5
~ m_attact= js*5 *1.5+level*1.5
~ p_defense= tn*1 *1.5+level*1.5
~ m_defense= js*1 *1.5+level*1.5
~ intelligence= js*1 *1.5+level*1.5
~ endurance= tn*1 *1.5+level*1.5
~ xp= 10*POW(10,0.2*level)
- "精灵": 
~ blood= tn*20 *1 +level*20
~ energy= js*20 *2 +level*2
~ p_attact= tn*5 *1 +level
~ m_attact= js*5 *2+level*2
~ p_defense= tn*1 *1+level
~ m_defense= js*1 *2+level*2
~ intelligence= js*1 *2+level*2
~ endurance= tn*1 *1+level
~ xp= 10*POW(10,0.2*level)
- "兽人": 
~ blood= tn*20 *2+level*20
~ energy= js*20 *1+level
~ p_attact= tn*5 *2+level*2
~ m_attact= js*5 *1+level
~ p_defense= tn*1 *2+level*2
~ m_defense= js*1 *1+level
~ intelligence= js*1*1+level
~ endurance= tn*1 *2+level*2
~ xp= 10*POW(10,0.2*level)
}

== function add_tem_blood(x) ==
{ 
- tem_blood + x <= 0 :
~ tem_blood=0

- tem_blood + x >= blood :
~ tem_blood=blood

- tem_blood + x > 0 and tem_blood + x < blood :
~ tem_blood=tem_blood+x
}

== function add_xp(x) ==
- tem_xp + x <= 0 :
~ tem_xp=0

- tem_xp + x >= xp :
~ tem_xp=xp

- tem_xp + x > 0 and tem_xp + x < xp :
~ tem_xp=tem_xp+x
}

== a ==
-> initial_setting

== word_blood ==
【你的血量为 {tem_blood}/{blood}】
{tem_blood == 0 :
 【你死了】
  ~ tem_blood = blood
  ~ {add_xp(-xp/5)}
}
->->

== word_xp ==
 【你的经验为 {tem_xp}/{xp}】
{tem_xp == xp :
 【你升级了】
 【level {level} ＞＞ level {level+1}】
 ~ level=level+1
 ~ tem_xp = 0
}
->->



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

= set_sex
【确认你的性别】
+ 男
~ sex="男"
+ 女
~ sex="女"
+ 无
~ sex="无"
-~ tem_energy = energy
-~ tem_blood = blood
- -> point_confirm

= point_confirm
【你的资料是：

  名字:{name}
  种族:{race}
  性别:{sex}
  
  血量:{tem_blood}/{blood}
  能量:{energy}
  物攻:{p_attact}
  魔攻:{m_attact}
  物防:{p_defense}
  魔防:{m_defense}
  
  智力:{intelligence}
  耐力:{endurance}】
->->
【你确定吗？】
+ [确定]
-> DONE
【好！人物已生成】
+ [否定]
-> set_point

