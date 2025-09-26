== function 3d_get(array,x,y,z,x_max,y_max,z_max) ==
//返回一个三维数组的某个元素的值，当然当z_max=0时也能用来获取二维数组的值
~ return get(array,y_max*x_max*z+x_max*y+x)

== function 3d_set(array,x,y,z,x_max,y_max,z_max,val) ==
//设置三维数组的某个值
~ return set(array,y_max*x_max*z+x_max*y+x,val)

== function transfer_to_view() ==
~ temp view_x = map( _entity.slice(0,100),->transfer_to_view_x)
~ temp view_y = map( _entity.slice(100,200),->transfer_to_view_y)
~ view = _entity.filter()

== function transfer_to_view_x(x) ==
~ return x-pos_x1
== function transfer_to_view_y(y) ==
~ return y-pos_y1

== function translate_view(x,y) ==
{ view.3d_get(x,y,0,length,width,0):
  -0:
  ~ return "⬛️"
  -1:
  ~ return "👦🏻"
  -2:
  ~ return "👦🏽"
  -3:
  ~ return "🌳"
}
