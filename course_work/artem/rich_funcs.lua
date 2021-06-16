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
  --b7 = max(num, 5)
  res = num * num
  return res
end



function max(num1, num2)
  return num1
end

function fact (n)
  if n == 0 then
    return 1
  else
    return n * fact(n-1)
  end
end

function func_call_arg (arg) 
  return arg("aaa")
end

a1 = 5        -- read a 
b1 = 6

a2 = 5.        -- read a 
b2 = 6.
  
b = 'if_you_see_it_is_bug("it is not function call")'
print('enter a number:')
local a = io.read('*number')        -- read a number
print(lvl1(a))
-- fact 122


local res = max(a, b)
function max(num1, num2)
  return num1 + num2
end

print(res)

func_call_arg(print)


-- require( 'microscope' )( 'res.dot', res )
-- require( "microscope" )( "res.dot", res )

