== function 3d_get(array,x,y,z,x_max,y_max,z_max) ==
//返回一个三维数组的某个元素的值，当然当z_max=0时也能用来获取二维数组的值
~ return get(array,y_max*x_max*z+x_max*y+x)

== function 3d_set(array,x,y,z,x_max,y_max,z_max,val) ==
~ return set(array,y_max*x_max*z+x_max*y+x,val)

== function coordinate_get_chessboard(x,y,z) ==
~ return 3d_get(_chessboard,x,y,z,length,width,height)

== function coordinate_set_chessboard(x,y,z,val) ==
~ return 3d_set(_chessboard,x,y,z,length,width,height,val)

== function sequence_get_chessboard(sequence,z) ==
~ return get(_chessboard,z*length*width+sequence)

== function sequence_set_chessboard(sequence,z,val) ==
~ return set(_chessboard,(z-1)*length*width+sequence,val)


== function translate_chessboard(x,y) ==
{ coordinate_get_chessboard(x,y,1):
  -0:
  ~ return "⬛️"
  -1:
  ~ return "🟣"
  -2:
  ~ return "⚪"
}

== function draw_line(y) ==
{ u:
  - width: 
   ~ u = 0
   ~ return temp3
  -else: 
   ~ temp3 = "{temp3}{translate_chessboard(u,y)}"
   ~ u = u+1
   ~ return draw_line(y)
}

== function draw_chessboard() ==
{ i:
  -length: 
   ~ i = 0
   ~ return join(temp1,__newline__)
  -else: 
   ~ temp1 = push(temp1,draw_line(i))
   ~ temp3 = ""
   ~ i = i+1
   ~ return draw_chessboard()
}


///////////////
== function _get_canvas_size() ==
~ return array(width,length+10)
== function _get_max_players() ==
~ return 2
