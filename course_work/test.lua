function square(num)
  b7 = max(num, 5)
  b8 = 15
  res = num * num
  b7 = b7 + res
  b8 = b7 + 3
  return res
end



function sub(num1, num2)
  res = num1 - num2
  res_square = square(res)
  return res_square
end

function add(num1, num2)
  b5 = square(num1)
  b6 = fact(num2)
  res = num1 + num2
  return res
end

function max(num1, num2)
  local a1 = sub(num1, num2)
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


a = 5        -- read a 
b = 6
local res = max(a, b)
print(res)