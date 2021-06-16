-- http://kolenka.su/blog/love/vvedenie-v-lua-chast-5-funkczii.html

local function makeAdder(a)
    return function (b)
        local g = b
        return function (o)
            local da, net = 1, 3
            return o + g - da + net
        end
    end
end

localfunc = 3
localvar = 5
a, b, c = 9,8,7
local g, d, k = 9,8,7