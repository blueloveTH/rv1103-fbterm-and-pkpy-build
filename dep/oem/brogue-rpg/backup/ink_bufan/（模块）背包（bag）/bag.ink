/////////////////////////////////////
//模块名：bag
//作者：布凡
//版本：1.0
//更新内容：
//--创建实体的方法
//--添加背包的方法
//--读写背包数组的方法
//--扩增背包数组的方法
//--添加物品属性的方法
////////////////////////////////////
//
//说明：
//--总体结构
//以下函数，以大写开头的，就是我建议你使用的，如果是小写开头，则是内部函数，这里不建议使用它们
//背包和实体的本质是一个分别存储着背包/实体数组和背包/实体字典的索引的，长度为2的数组
//创建：
//在使用背包之前，你需要定义一个空数组作为拥有该背包的实体,然后将该数组传入Create_entity
//然后再将该实体传入Create_bag
//当然，如果你想同时创建实体和安装背包一步到位，我也提供了Creat_entity_and_bag
//读写：
//下文中所述的实体字典，背包字典，都存储着其实体，背包下的数组内的属性值的索引位置信息
//下文所述的实体数组，背包数组，都存储着其属性的值
//通过访问字典，输入属性名，就可以拿到对应属性值的索引位置，就可以拿着这个索引位置找数组获取该位置的属性值
////////////////////////////////////
//下面是一个模型:
//方括号是该元素相对于entity的索引,当然，这是参考，实际使用时我会将其封装为一个简单的函数以供调用
//花括号就是数组或者字典
//entity
//--{
//
//  entity_dict
//[entity.get(0)]
//  --{
//
//    "bag":?,  
//    attribute01:1,
//    attribute02:2,
//    ...
//    },
//
//  entity_array
//[entity.get(1)]
//  --{
//
//    bag
//[entity.get(1).get(entity.get(0).get("bag"))]
//    --{ 
//
//      bag_dict_01  //存储背包属性
//[entity.get(1).get(entity.get(0).get("bag")).get(0)]
//      --{ 
//
//        attribute00:abc,
//        attribute01:efg,
//        attribute02:hij,
//        ...
//        },
//
//      bag_array
//[entity.get(1).get(entity.get(0).get("bag")).get(1)]
//      --{
//
//        att00,att01,att02...,
//        att00,att01,att02...,
//        ...
//[entity.get(1).get(entity.get(0).get("bag")).get(1).2d_get(y,entity.get(1).get(entity.get(0).get("bag")).get(2).get(attributeXX))]
//        },
//
//      bag_dict_02  //存储物品属性
//[entity.get(1).get(entity.get(0).get("bag")).get(2)]
//      --{ 
//
//        attribute00:0,
//        attribute01:1,
//        attribute02:2,
//        ...
//        }
//      }
//    }
//  }
/////////////////////////////////////
//----背包部分：
//一个背包有两部分组成：背包数组和背包字典
//
//- 背包数组是一个一维数组，它以表格的形式折叠起来存储物品的自定义属性值
//
//- 背包字典存储着背包属性和自定义的物品属性
//-- 背包属性：它的键是一个固定的字符串，它的值就是对应的属性值，它的键是固定的，你无法自定义一个背包具备哪些属性，但是你可以通过一个函数设置一个背包的各属性的值
//-- 自定义物品属性：它的键是一个可以自定义的字符串，对应的值是一个自动分配的整数，存放着物品属性在背包数组内的对应列数，你可以通过一个函数设置任意一行的物品的具体属性的值
///////////////////////////////////////
//下面是一个例子：
//
//bag_dict01
//--{
//(背包属性)
//  "owner_type":"player" 
//  "storage_mode":"type-limited" 
//  "space":10 
//  }
//bag_array
//--{
//(背包数组)
//  "新手剑",1,flase,false 
//  "新手布衣",1,false,false
//  }
//bag_dict02
//--{
//(自定义的物品属性)
//  "name":0 
//  "quantity":1 
//  "dropable":2 
//  "changeable":3
//  }
/////////////////////////////////////
== function Create_entity(entity) ==
//以下构建entity内的实体字典和实体数组
//entity:你自己创建的，一个将要作为容纳背包的实体的空数组
~ entity.push(dict())
~ entity.push(array())
~ return entity
== function Create_bag(entity,bag_name,owner_type,storage_mode,space) ==
//bag：你自己创建的，一个将要作为背包的空数组

//owner_type：字符串，确定拥有该背包的对象
//- "player"：玩家类
//- "changeable"：可交易类（不可掉落）
//- "dropable"：可产出掉落类（不可交易）

//storage_mode：字符串，确定该背包的存储模式
//- "type-limited"：限制物品种类的数量(你必须定义一个叫"number"的属性来存放每种物品的数量)
//- "number-limited"：限制物品总数(必须定义"number")
//- "weight-limited"：限制物品总重(你必须定义"number"和"weight"其中"weight"用于存放该种物品的单位重量)

//space：整数，确定在特定存储模式下的存储空间
//当限制物品种类的数量时，space值就是能够容纳物品的种类数
//当限制物品总数时，space值就是能够容纳所有物品的总数
//当限制物品总重时，space值就是能够承载所有物品的总重量
/////////////////////////////////////
//以下将这个背包插入entity字典,创建entity内的实体数组内的背包内的背包字典和背包数组
~ entity.get(0).set(bag_name,entity.get(0).len())
~ entity.get(1).push(array())
~ entity.get(1).get(entity.get(0).get(bag_name)).push(dict())
~ entity.get(1).get(entity.get(0).get(bag_name)).push(array())
~ entity.get(1).get(entity.get(0).get(bag_name)).push(dict())

//以下设置bag背包的背包字典的键和值，也就是设置背包的一系列初始的属性
~ entity.get(1).get(entity.get(0).get(bag_name)).get(0).set("owner_type",owner_type)
~ entity.get(1).get(entity.get(0).get(bag_name)).get(0).set("storage_mode",storage_mode)
~ entity.get(1).get(entity.get(0).get(bag_name)).get(0).set("space",space)
== function Create_entity_and_bag(entity,bag_name,owner_type,storage_mode,space) ==
//创建一个实体，同时顺便给它背上一个背包
~ entity.Create_entity()
~ entity.Create_bag(bag_name,owner_type,storage_mode,space)

== function get_2d(array,y,x,line_len) ==
//返回折叠成二维的数组的y行x列元素
~ return array.get(y*line_len+x)
== function set_2d(array,y,x,line_len,value) ==
~ array.set(y*line_len+x,value)

== function get_bag_pos(entity,bag_name) ==
//内部函数，若非理解，切勿使用!
//返回entity的背包在实体数组内的索引位置
~ return entity.get(0).get(bag_name)

== function get_bag(entity,bag_name) ==
//内部函数，若非理解，切勿使用!
//返回entity的背包索引
~ return entity.get(1).get(entity.get_bag_pos(bag_name))
== function get_bag_attribute_dict(entity,bag_name) ==
~ return entity.get_bag(bag_name).get(0)
== function get_item_attribute_dict(entity,bag_name) ==
~ return entity.get_bag(bag_name).get(2)
== function get_bag_array(entity,bag_name) ==
//内部函数，若非理解，切勿使用!
//返回entity的背包数组的索引
~ return entity.get_bag(bag_name).get(1)

== function Get_item_line(entity,bag_name,y) ==
//返回entity的bag的背包数组的y行新切片
//bag: 利用get_bag获取的背包的索引
{y<entity.get_bag_array(bag_name).len()/entity.get_item_attribute_dict(bag_name).len():
~ return entity.get_bag_array(bag_name).slice(y*entity.get_item_attribute_dict(bag_name).len(),y*entity.get_item_attribute_dict(bag_name).len()+entity.get_item_attribute_dict(bag_name).len())
-else:
~ return array()
}
== function Set_item_line(entity,bag_name,y,array,i) ==
//一次性替换entity的bag背包数组的y行
//array: 拿这个数组替换目标行
//i：循环变量，你必须传入0，否则会出错
{ i<=array.len()-1:
~ entity.get_bag_array(bag_name).set_2d(y,i,entity.get_bag(bag_name).get(0).len(),array.get(i))
~ return Set_item_line(entity,bag_name,y,array,i+1)
- else:
~ return 0
}
== function Get_bag_attribute_value(entity,bag_name,attribute) ==
//返回某实体的背包的某属性
~ return entity.get_bag_attribute_dict(bag_name).get(attribute)
== function Get_item_attribute_value(entity,bag_name,y,attribute) ==
//返回某实体的背包数组的y行物品的某个属性值
//attribute: 字符串，物品的属性名
~ return entity.Get_item_line(bag_name,y).get(entity.get_item_attribute_dict(bag_name).get(attribute))

== function Set_item_attribute_value(entity,bag_name,y,attribute,value) ==
//设置某实体的背包数组的y行物品的某个属性值
//attribute: 字符串，物品的属性名
//value:将要设定的值
~ entity.get_bag_array(bag_name).set(y*entity.get_item_attribute_dict(bag_name).len()+entity.get_item_attribute_dict(bag_name).get(attribute),value)

== function add_item_attribute(entity,bag_name,attribute) ==
//新增一项物品属性，此方法没有为背包数组扩容，请谨慎使用
~ entity.get_item_attribute_dict(bag_name).set(attribute,entity.get_item_attribute_dict(bag_name).len())

== function Add_item_attributes(entity,bag_name,array,i) ==
//为entity的背包的背包字典新增一堆物品属性
//array:属性名组成的数组
//i:循环变量，必须传入0
{array.len()-i-1>=0:
~ entity.add_item_attribute(bag_name,array.get(i))
~ Add_item_attributes(entity,bag_name,array,i+1)
-else:
~ return 0
}

== function Add_item_void_line(entity,bag_name,num) ==
//为背包数组的最后增添num行全部值为0的元素
~ entity.get_bag_array(bag_name).push_array(zeros(entity.get_item_attribute_dict(bag_name).len()*num))

//== function Pick_item(entity,item) ==
//{entity.get_bag_attribute_value("storage_mode") == "type-limited":

== function push_array(obj,array) ==
//将array添加到obj数组的末尾
//该方法将使array清空！
{array.len() > 0:
    ~ obj.push(array.pop())
    ~ push_array(obj,array)
 - else:
    ~ return 0
}








