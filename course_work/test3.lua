-- defines a factorial function

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
  a3 = add(num1, num2)
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
  
b = 'a("bbbbb")'
print("enter a number:")
a = io.read("*number")        -- read a number
print(lvl1(a))
print "aaa"

a = 5        -- read a 
b = 6
local c, d, e = 7, 8, 9
local res = max(a, b)
print(res)