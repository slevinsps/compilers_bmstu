function fact (n)
  if n == 0 then
    return 1
  else
    return n * fact(n-1)
  end
end

function func4 (n)
  for i = 1, n do
    print("func4")
  end
end

function func3 (n)
  print("func3")
  b, c = 5, 8
  func4(b + c + n)
end


function func2 (n)
  for i = 1, n % 3 do
    print("func2")
    func3(i*n/3)
  end
end

function func1 (n)
  print("func1")
  n = n + 2
  func2(n)
end

function square(num)
  local function square_inner_function(n)
    return n + 1
  end
  num = square_inner_function(num)
  res = num * num
  return res
end

local function sub(num1, num2)
  local res = num1 - num2
  return res
end

function add(num1, num2)
  b5 = square(num1)
  b6 = fact(num2)
  res = b5 + b6
  return res
end


a, b, c = 9, 8
res_func = func1(a)
res_add = add(b, c)
local a1, a2, a3 = 5, 2, 1
-- a = 5
-- b = 'a("bbbbb")'

my_table = {a = 5}
-- my_table.n1, my_table.n2 = 1, 2
-- my_table.str1, my_table['str2'] = {1,2,3}, {4,5,6}
-- my_table['str1'][3] = 100
-- my_table['str1'][30] = 200
-- my_table['str2'][3] = {'nn', 10, 20, {x = 5, y = 7}}

-- function my_table.table_method(arg1, arg2) 
--   local some = 3 
--   res = arg1 + arg2 + some
--   return res
-- end

-- res_example = my_table.table_method(51, 10)
-- print(res_example)

-- my_table['square_'] = square
-- res_square = my_table['square_'](5)
-- print(res_square)
