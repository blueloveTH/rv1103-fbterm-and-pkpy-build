[]VAR weapon="物理"
VAR monster_weapon="物理"
VAR temp1=0
VAR temp2=0
VAR temp3=0
////////////
VAR player_information= 0
~ player_information= array()

~ push(player_information,0)
~ push(player_information,0)
~ push(player_information,0)
~ push(player_information,0)
~ push(player_information,0)
~ push(player_information,0)
~ push(player_information,0)
~ push(player_information,0)
~ push(player_information,0)
~ push(player_information,0)
~ push(player_information,1)
~ push(player_information,0)
~ push(player_information,0)
~ push(player_information,"")
~ push(player_information,1)
~ push(player_information,1)
~ push(player_information,"人类")
~ push(player_information,"系统空间")
~ push(player_information,0)
~ push(player_information," ")
~ push(player_information,0)
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

VAR monster_information= 0
~ monster_information= array()

~ push(monster_information,0)
~ push(monster_information,0)
~ push(monster_information,0)
~ push(monster_information,0)
~ push(monster_information,0)
~ push(monster_information,0)
~ push(monster_information,0)
~ push(monster_information,0)
~ push(monster_information,0)
~ push(monster_information,"野猪")

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


VAR item_pack = 0
~ item_pack = array()
~ item_pack = range(0,120)

VAR npc_item_pack = 0
~ npc_item_pack = array()
~ npc_item_pack = range(0,100)

VAR tem_item_pack = 0
~ tem_item_pack = array()
~ tem_item_pack = range(0,120)

VAR item_pack_code = 0 
VAR item_pack_code2= 0
//选择一个物品栏后返回的对应行数


VAR  acquire_item_amount=0
//掉落物品数量


VAR 1day_renovate = 0
//每过0点分数会变为一