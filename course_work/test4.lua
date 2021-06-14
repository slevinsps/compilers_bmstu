function makeAdder(a)
  a, n = 5
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