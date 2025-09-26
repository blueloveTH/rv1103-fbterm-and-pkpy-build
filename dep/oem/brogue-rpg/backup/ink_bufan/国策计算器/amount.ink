VAR population = 100
VAR pop_rate = 0
VAR pop_rate_dec = 0
VAR GDP = 0
VAR tax_rate = 10%
VAR money = 100000000
VAR m_rate = 0
VAR m_rate_dec = 0
VAR time = 0
VAR land = 1000
VAR max_land = 100000000
VAR land_rate = 10
//人口(受到资源1限制)
//增长率(百分比) (受到掌控力，政策影响)
//年度GDP (GDP增长速度，来源于资源和加I品的生产速度) 
//税率(百分比) (来源于GDP， 受到政策影响)
// 国库资金(来源于税率和交易(对自家和别家) )
// 资金增长率(生产资源和开发科技都需要持续投入资金）
//年份
//现有开发土地面积（决定人口上限）
//最大土地面积
//土地开发速度
VAR resources1 = 1000
VAR r1_speed = 100
VAR r1_dec = 0
VAR resources2 = 1000
VAR r2_speed = 100
VAR r2_dec = 0
VAR resources3 = 1000
VAR r3_speed = 100
VAR r3_dec = 0
VAR resources4 = 100
VAR r4_speed = 0
VAR r4_dec = 0
// 四类初级资源国家库存(来源于生产和交易(对自家和别家)*资源1内定为粮食 ) 1粮食作物2工业作物3矿物4环境（百分比）

//对应生产速度(受到科技，人口，资金投入，掌控力的影响) 
VAR production1 = 0
VAR pro1_speed = 0
VAR pro1_dec = 0
VAR production2 = 0
VAR pro2_speed = 0
VAR pro2_dec = 0
VAR production3 = 0
VAR pro3_speed = 0
VAR pro3_dec = 0
VAR production4 = 0
VAR pro4_speed = 0
VAR pro4_dec = 0
VAR production5 = 0
VAR pro5_speed = 0
VAR pro5_dec = 0
VAR production6 = 0
VAR pro6_speed = 0
VAR pro6_dec = 0
VAR production7 = 0
VAR pro7_speed = 0
VAR pro7_dec = 0
VAR production8 = 0
VAR pro8_speed = 0
VAR pro8_dec = 0
//八类加工成品国家库存  1食品(1粮食=1人口->1食品=（1+tec1*0.1）人口，消耗1能源)2钢铁（）3机械零件4能源5水泥6电子零件7军械8民生相关产品
//对应生产速度
VAR education = 0
VAR edu_speed = 0
VAR edu_speed_dec = 0
VAR science_point = 100
VAR sp_speed = 0
VAR tec1_add_rate = 20
VAR tec2_add_rate = 40
VAR tec3_add_rate = 0
VAR tec4_add_rate = 10
VAR tec5_add_rate = 10
VAR tec6_add_rate = 5
VAR tec7_add_rate = 10
VAR tec8_add_rate = 5
// 知识水平(对科技点生产速度有直接加成)
// 知识水平增长速度(受 资金投入，政策，掌控力影响)
//科技点(用于分配八项科技) 
//科技点生产速度(取决于人口基数，资金投入和掌控力)
//八类科技(加起来为100) (科技 点的分配比例直接作用在对应元素上的增 长率，受到政策影响) 1制造2农业3军事4土地开发5教育6资源开发7民生8贸易

VAR control_power = 0
VAR satisfaction = 0
VAR policy_point = 0
//掌控力(百分比) (受到支持率和武力值的影响， 直接决定政策有效执行多寡，也影响生产力)
//民众支持率(百分比) (增加/减少受到税率和政策影响，直接影响掌控力)
//年度政策点(有效执行政策需要消耗不定数量的政策点，掌控力的多寡直接决定每年获得的政策点的数量)
VAR army_power = 0
VAR army = 0
//武力值（受士兵数量，科技，政策影响，直接影响掌控力）
//士兵数量 (受政策影响，直接影响武力值）()