== function clear_arr(a_array) ==
//一个通用的清空函数，可以将传入数组变成一个空数组
{
  - len(a_array)!=0:
  ~ a_array.pop()
  ~ clear_arr(a_array)
}



== function reverse_arr(a_array) ==
//返回一个前后完全颠倒的数组
~ temp out=a_array.copy_arr()
~ reverse_arr_while_1(a_array,out,0)
~ return out.copy_arr()

== function reverse_arr_while_1(a_array,out,i) ==
{
  - i<len(a_array):
  ~ out.set(i,a_array.get(len(a_array)-i-1))
  ~ reverse_arr_while_1(a_array,out,i+1)
}



== function del_arr(a_array, pos) ==
//删除pos位置元素的函数
~ temp a_piece = a_array.slice(0,pos)
~ temp b_piece = a_array.slice(pos+1,len(a_array))
~ a_array.clear_arr()
~ a_piece.concat_to_arr(a_array)
~ b_piece.concat_to_arr(a_array)



== function copy_arr(template_array) ==
//返回一个数组的浅拷贝的函数
~ return template_array.slice(0,len(template_array))



== function concat_to_arr(template_array, aim_array) ==
//将一个数组拼接到到另一个数组的函数
~ concat_to_arr_while_1(template_array, aim_array, 0)

== function concat_to_arr_while_1(template_array, aim_array, i)==
{
  - i!=len(template_array):
  ~ aim_array.push(0)
  ~ aim_array.set(len(aim_array)-1, template_array.get(i))
  ~ concat_to_arr_while_1(template_array, aim_array, i+1)
}



== function insert_arr(a_array, pos, a_obj) ==
//一个通用的插入方法，可以在数组的pos位置插入元素a_obj
~ a_array.push(0)
~ insert_arr_while_1(a_array, pos, a_obj, 0)

== function insert_arr_while_1(a_array, pos, a_obj, i)==
{
  - i<len(a_array)-1:
  {
    - pos==i:
    ~ insert_arr_while_2(a_array, pos, len(a_array)-1)
    ~ a_array.set(i, a_obj)
  }
  ~ insert_arr_while_1(a_array, pos, a_obj, i+1)

}

== function insert_arr_while_2(a_array, pos, j)==
{
  - j>pos:
  ~ a_array.set(j, a_array.get(j-1))
  ~ insert_arr_while_2(a_array, pos, j-1)
}



== function int_arr(a_int) ==
//输出整数的一种特殊数组表示，这是最重要的部分！！
//最后的元素表示整数的正负，用1和-1表示
//例如：-54321就是{5,4,3,2,1,-1}
~ temp out = array()
{
  - a_int>=0:
  ~ out.push(1)
  ~ int_arr_while_1(a_int, out)
  - else:
  ~ out.push(-1)
  ~ int_arr_while_1(-a_int, out)
}
~ return out.copy_arr()

== function int_arr_while_1(a_int, out) ==
~ temp now_a_int = a_int
{
  - now_a_int==0 or now_a_int==-1: //传入0,-1时终止,最后一位表示正负
  {
    - len(out)==1:
    ~ out.insert_arr(0,0)
  }
  - else: //否则继续递归
  ~ out.insert_arr(0, now_a_int%10)
  ~ now_a_int = now_a_int/10
  ~ int_arr_while_1(now_a_int, out)
}



== function str_arr(a_array) ==
//返回整数数组的可读字符串
~ temp clone_a_array = a_array.copy_arr()
{
  - clone_a_array.pop()==1:
  ~ return join(clone_a_array,"")
  - else:
  ~ clone_a_array.insert_arr(0,"-")
  ~ return join(clone_a_array,"")
}



== function add_arr(arr1, arr2) ==
//整数数组的加法和减法，返回一个结果数组
~ temp arr1_copy = arr1.slice(0,len(arr1)).reverse_arr()
~ temp arr2_copy = arr2.slice(0,len(arr2)).reverse_arr()
~ temp result_sign = 1

//决定结果的符号
{
  - arr1_copy.get(0)==arr2_copy.get(0):
  ~ result_sign = arr1_copy.get(0)
  - else:
  ~ result_sign = arr2_copy.get(0)
  }
}

//决定结果的位数
~ temp len_result = 0
{
  - len(arr1)>len(arr2):
  ~ len_result = len(arr1)
  - else:
  ~ len_result = len(arr2)
}

//carry：进位数，这里用数组方便传递
~ temp result = zeros(len_result-1)
~ temp carry = array(0)

//将输入的两个加数的符号位去除
~ arr1_copy = arr1_copy.slice(1,len(arr1_copy))
~ arr2_copy = arr2_copy.slice(1,len(arr2_copy))

//该循环依次对所有的位相加，每次相加都生成carry，并留到下一次循环作为第三加数。它最终将产生位权由低到高排列的结果数组
~ add_arr_while_1(result,arr1_copy,arr2_copy,0,carry,len_result)

//如果最高位没有产生carry，则去除结果数组中给进位预留的位置
{
  - carry.get(0)!=0:
  ~ result.push(carry.get(0))
}

//将结果加上它的符号，前后颠倒后输出
~ result.insert_arr(0,result_sign)
~ return result.reverse_arr()

== function add_arr_while_1(result,arr1_copy,arr2_copy,i,carry,len_result) ==
/*
result:{str(result)}
carry:{str(carry)}
1:{str(arr1_copy)}
2:{str(arr2_copy)}
i:{i}
aaaaaaa
*/
a
{
  - i < len_result-1:
  ~ temp a_digit = 0
  ~ temp b_digit = 0
  {
    - i<len(arr1_copy):
    ~ a_digit = arr1_copy.get(i)
  }
  {
    - i<len(arr2_copy):
    ~ b_digit = arr2_copy.get(i)
  }
  ~ result.set(i, (a_digit+b_digit+carry.get(0))%10)
  ~ carry.set(0,(a_digit+b_digit+carry.get(0))/10)
  ~ add_arr_while_1(result,arr1_copy,arr2_copy,i+1,carry,len_result)
}

