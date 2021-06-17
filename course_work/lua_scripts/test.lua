local up1, up2, up3, up4 = false, 11 < 12, true and false, io.stdout

local t1 = { val = "aa", aaa = true and false, ["2"] = "2" }
local t2 = { val = 2 }
t3 = {val = 10}
t1['val'] = 5
t3.bbb  = 50
t3['2'] = 500
t1[2] = 500
-- setmetatable( t1, { __index = function( t, k )
--   if t2[ k ] ~= nil then
--     return t2[ k ]
--   else
--     return up1 or up2
--   end
-- end } )
-- setmetatable( t2, { __index = t1 } )

-- require( "microscope" )( "example1.dot", t1 )