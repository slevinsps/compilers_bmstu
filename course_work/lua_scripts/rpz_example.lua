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
  local function func3_inner_function(n)
    return n + 1
  end
  print("func3")
  b, c = 5, 8
  b = func3_inner_function(b)
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
a = 5
res_func = func1(a)
res_add = add(b, c)
local a1, a2, a3 = 5, 2, 1
b = 'a("bbbbb")'

o = {}
o.n1, o.n2 = 1, 2
o.str1, o['str2']  = {1,2,3}, {4,5,6}
o['str1'][3] = 100
o['str1'][30] = 200
o['str2'][3] = {'nn', 10, 20, {x = 5, y = 7}}