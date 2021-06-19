MyAddOn = {b = 40, c = 70}
function MyAddOn.FirstFunction(arg1, arg2) 
    local some = 3 
    some = 1 
    return 
end

function func(aa)
    aa.FirstFunction(5, 6)
end

MyAddOn.FirstFunction(a, b)
func(4)


function func3(aa)
    return aa
end

bb = {a = 6, c = func3}
 
r = bb['c'](5)

rr = func
vv = rr
bbb = rr(6)
vv(7)
-- function a1(x1, x2)
--     c = 51
--     local function b2(r, rr)
--         v = 5
--         function b3(r, rr)
--             v = 5
--             return v
--         end
--         tt = a2(5, 8)
--         return v
--     end
--     -- t = a2(5, 8)
-- end

-- function a2(x1, x2)
--     c = 51
--     local function b2(v)
--         yyyyyyyy = 5
--         return yyyyyyyy
--     end
--     t = b2(5, 8)
-- end


-- local function b2(b, bb)
--     yyTy = 5
--     return yyTy
-- end


-- b2(a2(45))