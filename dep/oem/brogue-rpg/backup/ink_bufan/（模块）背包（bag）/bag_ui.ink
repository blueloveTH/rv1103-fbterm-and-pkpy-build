== show_bag(entity,bag_name) ==
```
"--------༺背包༻--------"
 {entity.get_item_attribute_dict(bag_name).keys().join(" ··· ")} 
!
```
-> show_bag_line(entity,bag_name,0) ->
```

"------------------------"
```

->->
== show_bag_line(entity,bag_name,i) ==
{i < entity.get_bag_array(bag_name).len()/entity.get_item_attribute_dict(bag_name).len():
```
{entity.Get_item_line(bag_name,i).join("···")}
!
{entity.Get_item_line(bag_name,i+1).join("···")}
!
{entity.Get_item_line(bag_name,i+2).join("···")}
!
{entity.Get_item_line(bag_name,i+3).join("···")}
!
```
    -> show_bag_line(entity,bag_name,i+4) ->
}
->->