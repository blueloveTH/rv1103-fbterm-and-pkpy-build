
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


== bordertown ==
【边境小镇】
~ set(player_information,17,"边境小镇")
+ 镇长家
-> bordertown_mayor
+ 铁匠铺
-> bordertown_blacksmith
+ 裁缝铺
-> item_pack_examine -> item_pack_choose ->
{
  - item_code_judge(item_pack_code,1) == 1:
  [王裁缝] 谢谢惠顾！
  【你获得了 野猪皮甲*1】
  【金币 -50】
  ~ add_money(-50)
  ~ equipment_attribute(202,3,3,100,400)
  - item_code_judge(item_pack_code,1) == 0:
  【无法存放】
  -> bordertown_tailor.yezhupijia
  }
-> bordertown_tailor
+ 餐馆
【未开放】
-> bordertown
+ 教堂
【未开放】
-> bordertown
+ 驿站
【未开放】
-> bordertown
+ 森林
-> explore_bordertown_forest
+ [个人信息]
-> point_examine ->
-> bordertown
+ [打开背包]
-> item_pack_examine ->
++ [移动物品]
-> item_pack_item_exchange ->
-> bordertown
++ [返回]
-> bordertown


== bordertown_mayor ==
[马镇长] 你好，冒险者，请问你有什么事吗？
+ {1day_renovate==1} [提交任务(该任务每日会刷新一次)]
[{get(player_information,19)}] 呃，我想找一份有报酬的任务
[马镇长] 呃...我想想....对了，也许你可以去森林猎杀一些野猪，裁缝铺的王大娘最近好像缺皮料了，如果你可以给我10份野猪皮，那么我可以用30个金币作为报酬

++ 提交任务：提交10份野猪皮
【请选择你的物品栏进行提交】
-> item_pack_examine -> item_pack_choose ->

{
 - item_judge(3,10) == 1 :
  【任务完成】
  【野猪皮 -10】
  【金币 +30】
  
  ~ add_money(30)
  ~ add_item_pack_choose_number(item_pack_code,-10)
  ~ 1day_renovate =0
 - item_judge(3,10) == 0 :
[马镇长] 我虽然人老了，可是眼睛却没有花，年轻人，好自为之！
【你被村长赶走了】
-> bordertown
}
[马镇长] 你做的很好，希望你再接再厉！
-> bordertown
++ [没什么事，来看看您老]
[{get(player_information,19)}] 没什么事，来看看您老
[马镇长] 那你走吧，我还有别的事
【你被村长打发走了】
-> bordertown
+ [返回]
-> bordertown


== bordertown_blacksmith ==
【章铁匠正在打造着一件像是长剑一样的装备】
+ [交易(未完成)]
-> bordertown
* [领取新手装备]
-> receive_equipment1
+ [没事，就进来随便看看]
-> bordertown

= receive_equipment1 
* [领取新手装备]
[章铁匠] 哟，这位冒险者，看你面生的很，是小镇新来的？
** [是]
[{get(player_information,19)}] 是
既然这样，那我就免费赞助你一件初始装备吧，反正放我这儿没人买，都快积灰了
*** [啊那真是太感谢了]
[{get(player_information,19)}] 啊那真是太感谢了！
【选择一件装备】
**** [新手短剑]
-> jian ->
**** [学徒法杖]
-> zhang ->
---- -> bordertown

= jian
+【选择存放位置】
-> item_pack_examine -> item_pack_choose ->
{
  - item_code_judge(item_pack_code,1) == 1:
  ~ equipment_attribute(200,1,1,100,200)
  - item_code_judge(item_pack_code,1) == 0:
  【无法存放】
  -> jian
  }
+ [【丢弃】]
- -> item_pack_examine ->
- ->->

= zhang
+【选择存放位置】
-> item_pack_examine -> item_pack_choose ->
{
  - item_code_judge(item_pack_code,1) == 1:
  ~ equipment_attribute(201,1,2,100,200)
  - item_code_judge(item_pack_code,1) == 0:
  【无法存放】
  -> jian
  }
+ [【丢弃】]
- -> item_pack_examine ->
- ->->

== bordertown_tailor ==
【王裁缝正在使用着野猪皮制作一件皮甲】
[王裁缝] 这位客人，自己请问需要些什么
+ [定制野猪皮甲(50金)]
[{get(player_information,19)}] 是这样的，我想要一套野猪皮甲。
[王裁缝] 好的，一共收你50金
++ {get(player_information,20)>=50}[买！]
-> yezhupijia ->
-> bordertown
++ [太贵了诶，买不起啊]
[王裁缝] 那么欢迎这位客人下次再来哟～
【你最终还是没能买下这件装备】
-> bordertown
+ [没事，就进来随便看看]
[{get(player_information,19)}] 没事，就进来随便逛逛，马上走
-> bordertown

= yezhupijia
+【选择存放位置】
-> item_pack_examine -> item_pack_choose ->
{
  - item_code_judge(item_pack_code,1) == 1:
  [王裁缝] 谢谢惠顾！
  【你获得了 野猪皮甲*1】
  【金币 -50】
  ~ add_money(-50)
  ~ equipment_attribute(202,3,3,100,400)
  - item_code_judge(item_pack_code,1) == 0:
  【无法存放】
  -> yezhupijia
  }
+ [【不买】]
【你最终还是没能买下这件装备】
- -> item_pack_examine
- ->->
