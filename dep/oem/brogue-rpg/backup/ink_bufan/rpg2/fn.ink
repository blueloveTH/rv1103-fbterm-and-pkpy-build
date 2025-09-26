
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
//9j
//10k

== function add_money(value) ==
~ set(player_information,20,get(player_information,20)+value)

//设置长度为 10 的数组的第 x 行
////////////////////////////////////////////待办

== function copy_2d_line(origin_array,target_array,step,x,y,z) ==
{
  - z==step:
  ~ return 
  - else:
  ~ set(target_array,y*step+z,get(origin_array,x*step+z))
  ~ return copy_2d_line(origin_array,target_array,step,x,y,z+1)
}

//将背包备份到tem背包
== function copy_item_pack() ==
~ tem_item_pack = concat(item_pack ,array())
//物品栏 x 行与 y 行互换 z 永远是0
== function item_pack_line_exchange(x,y,z) ==
{
  - 2d_get(item_pack,x,1,10) == 2d_get(item_pack,y,1,10) and 2d_get(item_pack,y,6,10) == 0:
    ~ add_item_pack_choose_number(y,get(item_pack,10*x+2))
  ~ item_pack_clear(x)
  - else:
  {
    - (x<=9 and y<=9 and 2d_get(item_pack,x,6,10) == 0 and 2d_get(item_pack,y,6,10) == 0) or (x<=9 and 2d_get(item_pack,x,6,10) >=1) or (y<=9 and 2d_get(item_pack,y,6,10) >=1) :
  ~ copy_item_pack()
  ~ copy_2d_line(tem_item_pack,item_pack,10,x,y,1)
  ~ copy_2d_line(tem_item_pack,item_pack,10,y,x,1)
    - else:
    {
      - (x<=9 and 2d_get(item_pack,x,6,10) == 0) or (y<=9 and 2d_get(item_pack,y,6,10) == 0) :
      ~ return "【无法移动】"
      - else :
      ~ copy_item_pack()
  ~ copy_2d_line(tem_item_pack,item_pack,10,x,y,1)
  ~ copy_2d_line(tem_item_pack,item_pack,10,y,x,1)
}
}
}

//物品栏 x 行数量设置
== function add_item_pack_item_code_number(x,code,value) ==
~ set(item_pack,10*x+1,code)
~ set(item_pack,10*x+2,value)

//物品栏 x 行增加减少数量
== function add_item_pack_choose_number(x,value) ==
{
  - 2d_get(item_pack,x,2,10) + value <= 0 :
  ~ item_pack_clear(x)
  - 2d_get(item_pack,x,2,10) + value > 0 :
  ~ set(item_pack,x*10+2,2d_get(item_pack,x,2,10) + value)
}
  
  //清空物品栏 x 行
== function item_pack_clear(x) ==
~ set(item_pack,x*10+1,0)
~ set(item_pack,x*10+2,0)
~ set(item_pack,x*10+3,0)
~ set(item_pack,x*10+4,0)
~ set(item_pack,x*10+5,0)
~ set(item_pack,x*10+6,0)
~ set(item_pack,x*10+7,0)
~ set(item_pack,x*10+8,0)
~ set(item_pack,x*10+9,0)

//物品栏第 2 列 x 行数字返回对应名称
== function item_pack_number_to_text(x) ==
~ return number_to_text(get(item_pack,x*10+1))
== function number_to_text(x) ==
{x://0:空 0~99:怪物材料 100～200:采集材料 300~400:装备
  -0: ~ return "空"
  -1: ~ return "野猪肉"
  -2: ~ return "野猪獠牙"
  -3: ~ return "野猪皮"
  -4: ~ return "空"
  -5: ~ return "空"
  -6: ~ return "空"
  -7: ~ return "空"
  -8: ~ return "空"
  -9: ~ return "空"
  -10: ~ return "空"
  -100: ~ return "空"
  -101: ~ return "空"
  -102: ~ return "空"
  -103: ~ return "空"
  -104: ~ return "空"
  -105: ~ return "空"
  -106: ~ return "空"
  -200: ~ return "新手短剑"
  -201: ~ return "学徒法杖"
  -202: ~ return "野猪皮甲"
  -203: ~ return "空"
  -204: ~ return "空"
  -205: ~ return "空"
  -206: ~ return "空"
}

//判断 x 行物品的数量是否大于等于 y 
//若大于y 返回1，否则返回0
== function item_judge(x,y) ==
{
  - get(item_pack,item_pack_code*10+1) == x and get(item_pack,item_pack_code*10+2) >= y :
  ~ return 1
  - else :
  ~ return 0
}
//判断 x 行是否有 y 物品
//有 返回1 无 返回0
== function item_code_judge(x,y) ==
{
   - get(item_pack,x*10+1) == y or get(item_pack,x*10+1) == 0 :
   ~ return 1
   - else:
   ~ return 0
 }
   
== function 2d_initial_set_2(in_array,step,modify_position,auto_position) ==
{
  - auto_position == len(in_array):
  ~ return in_array
  - else:
  {
    - auto_position mod step == modify_position :
    ~ set(in_array,auto_position,auto_position/step)
    ~ return 2d_initial_set_2(in_array,step,modify_position,auto_position+1)
    -else:
    ~ return 2d_initial_set_2(in_array,step,modify_position,auto_position+1)
  }
}
== function 2d_initial_set_1(in_array,auto_position) ==
{
  - auto_position == len(in_array):
  ~ return in_array
  - else:
  ~ set(in_array,auto_position,0)
  ~ return 2d_initial_set_1(in_array,auto_position+1)
}


//数组名，行数，列数，步长，值
== function 2d_get(objective,x,y,step) ==
~ return get(objective,step*x+y)
== function 2d_set(objective,x,y,step,value) ==
~ set(objective,step*x+y,value)

//装备属性
== function equipment_attribute(name,type,level,min,max) ==
~ 2d_set(item_pack,item_pack_code,1,10,name)
  ~ 2d_set(item_pack,item_pack_code,2,10,1)
  ~ 2d_set(item_pack,item_pack_code,3,10,0)
  ~ 2d_set(item_pack,item_pack_code,4,10,0)
  ~ 2d_set(item_pack,item_pack_code,5,10,level)
  ~ 2d_set(item_pack,item_pack_code,6,10,type)
  ~ 2d_set(item_pack,item_pack_code,8,10,RANDOM(min,max))
  ~ 2d_set(item_pack,item_pack_code,7,10,2d_get(item_pack,item_pack_code,5,10)*2d_get(item_pack,item_pack_code,8,10)/100+5)
{
  - type <= 2 :
  ~ 2d_set(item_pack,item_pack_code,7,10,INT(2d_get(item_pack,item_pack_code,7,10))/5)
  - else :
  ~ return 
}
  
//以下是一个用来推进时间的函数
== function add_time(x) ==
{
- get(player_information,18)+x<24:
~ set(player_information,18, get(player_information,18)+x)
- get(player_information,18)+x>=24:
~ set(player_information,18, get(player_information,18)+x-24)
~ 1day_renovate =1
}


== function attribute() ==
{get(player_information,16): 
- "人类": 
~ set(player_information ,0 , get(player_information,14)*20 *1.5 + get(player_information,10)*20*1.5)
~ set(player_information,2, INT(get(player_information,15)*20 *1.5 +get(player_information,10)*20*1.5))
~ set(player_information,4, get(player_information,14)*5 *1.5 +get(player_information,10)*1.5)
~ set(player_information,5, get(player_information,15)*5 *1.5+ get(player_information,10)*1.5)
~ set(player_information,6, get(player_information,14)*1 *1.5+get(player_information,10)*1.5)
~ set(player_information,7,get(player_information,15)*1 *1.5+get(player_information,10)*1.5)
~ set(player_information,8,get(player_information,15)*1 *1.5+get(player_information,10)*1.5)
~ set(player_information,9,get(player_information,14)*1 *1.5+get(player_information,10)*1.5)
~ set(player_information,11,10*get(player_information,10)*get(player_information,10)+10)
- "精灵": 
~ set(player_information ,0 , get(player_information,14)*20 *1 + get(player_information,10)*20*1)
~ set(player_information,2, INT(get(player_information,15)*20 *2 +get(player_information,10)*20*2))
~ set(player_information,4, get(player_information,14)*5 *1 +get(player_information,10)*1)
~ set(player_information,5, get(player_information,15)*5 *2+ get(player_information,10)*2)
~ set(player_information,6, get(player_information,14)*1 *1+get(player_information,10)*1)
~ set(player_information,7,get(player_information,15)*1 *2+get(player_information,10)*2)
~ set(player_information,8,get(player_information,15)*1 *2+get(player_information,10)*2)
~ set(player_information,9,get(player_information,14)*1 +get(player_information,10)*1)
~ set(player_information,11,10*get(player_information,10)*get(player_information,10)+10)
- "兽人": 
~ set(player_information ,0 , get(player_information,14)*20 *2 + get(player_information,10)*20*1)
~ set(player_information,2, INT(get(player_information,15)*20 *1 +get(player_information,10)*20*1))
~ set(player_information,4, get(player_information,14)*5 *2 +get(player_information,10)*2)
~ set(player_information,5, get(player_information,15)*5 *1+ get(player_information,10)*1)
~ set(player_information,6, get(player_information,14)*1 *1.5+get(player_information,10)*1.5)
~ set(player_information,7,get(player_information,15)*1 *1+get(player_information,10)*1)
~ set(player_information,8,get(player_information,15)*1 *1+get(player_information,10)*1)
~ set(player_information,9,get(player_information,14)*1 *2+get(player_information,10)*2)
//经验上限= 10* 等级*等级+10
~ set(player_information,11,10*get(player_information,10)*get(player_information,10)+10)
}

{2d_get(item_pack,10,6,10):
  - 0:
  ~ weapon = "物理"
  - 1:
  ~ set(player_information,4,get(player_information,4)+2d_get(item_pack,10,7,10))
  ~ weapon="物理"
  - 2:
  ~ set(player_information,5,get(player_information,5)+2d_get(item_pack,10,7,10))
  ~ weapon="魔法"
}
{2d_get(item_pack,11,6,10):
  - 3:
  ~ set(player_information,6,get(player_information,6)+2d_get(item_pack,11,7,10))
  ~ weapon="物理"
  - 4:
  ~ set(player_information,7,get(player_information,7)+2d_get(item_pack,11,7,10))
  ~ weapon="魔法"
}

== function monster_attribute(x,y,z) ==
// (种族，体能点比例，精神点比例）
//先根据角色等级随机出怪物等级，然后通过输入的点数比例计算怪物de体能点和精神点，最后结合种族，等级，加点来计算怪物的战斗属性
{x:
- "野猪":
~ set(monster_information,6,RANDOM(INT(0.8*get(player_information,10)),INT(1+(0.5*POW(get(player_information,10),0.5)+get(player_information,10)))))
~ set(monster_information,7,INT((get(monster_information,6)+5)/((z+y)+0.001)*y))
~ set(monster_information,8,INT((get(monster_information,6)+5)/((z+y)+0.001)*z))
~ set(monster_information,0,get(monster_information,7)*20*1 + get(monster_information,6)*20*0.5)
~ set(monster_information,2,get(monster_information,7)*5 *1.5 +get(monster_information,6)*0.5)
~ set(monster_information,3,get(monster_information,8)*5 *1.5+get(monster_information,6)*0.5)
~ set(monster_information,4,get(monster_information,7)*1 *1.5+get(monster_information,6)*0.5)
~ set(monster_information,5,get(monster_information,8)*1 *1.5+get(monster_information,6)*0.5)
}
~ set(monster_information,1,get(monster_information,0))

== function gain_monster_xp ==
~ return INT(0.02*get(player_information,11)+get(player_information,11)*(POW(3,(get(monster_information,6)-get(player_information,10)-3))))



//这是一个用来计算人物血量变化的函数，只要输入一个值，负数表示扣血，正数表示加血，大部分情况下，还要在下一行跳转到用来扣血的节点以便一站式显示血量，以及处理人物或怪物死亡的情况
== function add_tem_blood(x) ==
{ 
- get(player_information,1) + x <= 0 :
~ set(player_information,1,0)

- get(player_information,1) + x >= get(player_information,0) :
~ set(player_information,1,get(player_information,0))

- get(player_information,1) + x > 0 and get(player_information,1) + x < get(player_information,0) :
~ set(player_information,1,get(player_information,1)+x)
}



//这是用来计算怪物血量变化的
== function add_monster_tem_blood(x) ==
{ 
- get(monster_information,1) + x <= 0 :
~ set(monster_information,1,0)
- get(monster_information,1) + x >= get(monster_information,0) :
~ set(monster_information,1,get(monster_information,0))
- get(monster_information,1) + x > 0 and get(monster_information,1) + x < get(monster_information,0) :
~ set(monster_information,1,get(monster_information,1)+x)
}




//这是一个用来计算角色mp变化的函数，大部分情况下，还要在下一行跳转到用来扣mp的小节以便显示剩余mp
== function add_tem_energy(x) ==
{
- get(player_information,3) + x <= 0 :
~ set(player_information,3,0)

- get(player_information,3) + x >= get(player_information,2) :
~ set(player_information,3,get(player_information,2))

- get(player_information,3) + x > 0 and get(player_information,3) + x < get(player_information,2) :
~ set(player_information,3,get(player_information,3)+x)
}



//这是用来计算角色对怪物造成伤害的函数，大部分情况下，是作为计算血量变化的函数的变量使用的，伤害分为物理伤害和魔法伤害，对应物理防御和魔法防御分开计算
== function player_hit_monster_dammage() ==
{weapon:
- "物理":
{
  - get(player_information,4) - get(monster_information,4)  >=0:
  ~ return (get(player_information,4) - get(monster_information,4) )
  - get(player_information,4) - get(monster_information,4)  <0:
  ~ return 0
}
- "魔法":
{
  - get(player_information,5) - get(monster_information,5) >=0:
  ~ return (get(player_information,5) - get(monster_information,5))
  - get(player_information,5) - get(monster_information,5) <0:
  ~ return 0
}
}

//这是用来计算怪物对角色造成伤害的函数
== function monster_hit_player_dammage() ==
{monster_weapon:
- "物理":
{
  - get(monster_information,2)  - get(player_information,6) >=0:
  ~ return (get(monster_information,2)  - get(player_information,6))
  - get(monster_information,2)  - get(player_information,6) <0:
  ~ return 0
}
- "魔法":
{
  - get(monster_information,3) - get(player_information,7) >=0:
  ~ return (get(monster_information,3) - get(player_information,6))
  - get(monster_information,3) - get(player_information,7) <0:
  ~ return 0
}
}


//这是用来计算角色获取经验的函数，一般下一行会跳转到升级小节，用来一站式处理角色的加点，回状态，以及信息显示
== function add_tem_xp(x) ==
{
- get(player_information,12) + x <= 0 :
~ set(player_information,12,0)

- get(player_information,12) + x >= get(player_information,11) :
~ set(player_information,12,get(player_information,11))

- get(player_information,12) + x > 0 and get(player_information,12) + x < get(player_information,11) :
~ set(player_information,12,get(player_information,12)+x)
}