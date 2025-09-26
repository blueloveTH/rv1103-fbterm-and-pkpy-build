VAR wood = 0//木头
VAR fur = 0//毛皮
VAR meat = 0//肉
VAR shell = 0//贝壳
VAR bone = 0//骨头
VAR teeth = 0//牙齿
//————————————————————————————
VAR bacon = 10//熏肉
VAR leather = 0//皮革
//————————————————————————————
VAR cloth = 0//布料
//————————————————————————————
VAR FreeSpace = 0//剩余背包空间
VAR space = 0//背包空间
VAR water = 0//水
VAR LeftWater = 0//剩余水
VAR BringBacon = 0//携带熏肉
VAR weapon = 0//武器等级（0空手1骨刃2铁剑）
//————————————————————————————
VAR house = 0//房屋
VAR MaxPopulation = 0 //最大人口（不建议修改
VAR FreePopulation = 0//空闲人口（不建议修改
VAR trap = 0//陷阱
//————————————————————————————
VAR CutWood = 0//伐木人数（不建议修改
VAR hunt = 0//狩猎人数（不建议修改
VAR SmokeMeat = 0//熏肉人数（不建议修改
VAR TanLeather = 0//制革人数（不建议修改
//————————————————————————————
VAR HuntHouse = 0//是否解锁狩猎小屋（0否1是
VAR BaconHouse = 0//是否解锁熏肉工坊（0否1是
VAR LeatherHouse = 0//是否解锁制革工坊（0否1是
VAR workshop = 0 //是否解锁加工车间（0否1是
VAR TradeHouse = 0//是否解锁交易站（0否1是
VAR compass = 0//是否解锁罗盘（0否1是
VAR SmallWaterBag = 0 //是否解锁小水袋（0否1是
VAR SmallLeatherBag = 0 //是否解锁小皮包（0否1是
VAR HuntDeploy = 0//是否经历狩猎部署选项(0否1是，不建议修改）
//——————————————————————————————————
VAR entity = 0
VAR world = 0
VAR dx = 0
VAR dy = 0
VAR m = 5
VAR MinPosition = -99
VAR MaxPosition = 99
VAR EntityLenth =0
~ world = zeros(121)
~ entity = zeros(300000)