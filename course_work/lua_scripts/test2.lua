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
  
print("enter a number:")
a = io.read("*number")        -- read a number
print(lvl1(a))