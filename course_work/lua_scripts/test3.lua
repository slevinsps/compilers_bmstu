function lvl5 (n)
  for i = 1, n % 5 do
    print("lvl5")
  end
  if n % 100 then 
    lvl5(n/100)
  end 
end

function lvl4 (n)
  for i = 1, n % 4 do
    print("lvl4")
    lvl5(i*n/4)
  end
end

function lvl3 (n)
  for i = 1, n % 3 do
    print("lvl3")
    lvl4(i*n/3)
  end
end

function lvl2 (n)
  for i = 1, n % 3 do
    print("lvl2")
    lvl3(i*n/3)
  end
end

function lvl1 (n)
  lvl2(n)
end

function square(num)
  b7 = max(num, 5)
  res = num * num
  return res
end



local function sub(num1, num2)
  local res = num1 - num2
  res_square = square(res)
  return res_square
end

function add(num1, num2)
  b5 = square(num1)
  b6 = fact(num2)
  res = num1 + num2
  return res
end

local function max(num1, num2)
  a1 = sub(num1, num2)
  a2 = add(num1, num2)
  ff = {d = 4, g = 1}
  ff['d'] = 12
  ff.d = 'hello'
  ff['g'] = {v = {c = 'world'}, t = 45}

  local a3 = add(num1, num2)
  if (a1 > a2) then
     result = a1
  else
     result = a2
  end

  return result; 
end


function fact (n)
  if n == 0 then
    return 1
  else
    return n * fact(n-1)
  end
end


function makeAdder(a)
  a, n = 5
  vv = a
  bb = sub(a, n)
  local nn = 18
  return function (b)
      local g = b
      return function (o)
          local da, net = 1, 3
          return o + g - da + net
      end
  end
end

a, b, c = 9, 8

localfunc = 3
local localvar,         a2,     a3 = 5, 2, 1
makeAdder(a)
  
b = 'a("bbbbb")'
print("enter a number:")
a = io.read("*number")        -- read a number
print(lvl1(a))
print "aaa"

a = 5        -- read a 
b = 6
local c, d, e = 7, 8
local res = max(a, b)
print(res)

o = {}
o.n1, o.n2 = 1, 2

o.str1, o.str2  = {1,2,3}, {4,5,6}
o['str1'][3] = 100
o['str1'][30] = 200

o['str2'][3] = {'nn', 10, 20, {x = 5, y = 7}}