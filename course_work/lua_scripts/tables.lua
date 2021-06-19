local luaValue = {"1","2","3","4","5","6"}
local luaValue = {"Yellow","Blue","Red"} 
-- table.insert(luaValue,"Green")
-- table.remove(luaValue)
-- outputChatBox("Last color added "..luaValue[4])

-- table.sort(luaValue)

-- for k,v in ipairs(luaValue) do 
--   outputChatBox("Index: "..k..", Value:"..v)
-- end 

mytable = {}
mytable["key"] = "value" -- is the same as
mytable.key = "value"

local tbl = {1, "Some Value", 10}
 
-- for key, value in pairs(tbl) do d(key .. " => " .. value) end

-- local tbl = {	[1] = "one", 	[2] = "two", 	[3] = "three" }
-- for key, value in pairs(tbl) do d(key .. " => " .. value) end
-- d(#tbl) 	-- 3
 

local map = {["key"] = "value"}

-- deep[0][1][2][3] = 4

usual_s = 1
strange = 2
not_so_much, strange, naMES = 6,4,3


MyAddOn = {["inside"] ={}, ["second"] = {}}
MyAddOn.myString = "wasd"
MyAddOn.defaults = {
 
}

local coords = {123, 321, 231}

function MyAddOn.FirstFunction(arg1, arg2) 
    local some = 3 
    some = 1 
    return 
end

MyAddOn.FirstFunction(a, b)

function MyAddOn.inside.SecondFunction(arg1, arg2) return end

aaa = MyAddOn

local widgets = {
  { id = 246, num1 = 90885, val2 = "NA" },
  { id = 250, num1 = 95689, val2 = "NA" },
  { id = 257, num1 = 95694, val2 = "NA" } 
}

t,k = {}, {}
a, b, c = {1,2}, {3,4}, {5,6}


local deep = {
  { { { { { { { { 1 }}}}}}} },
}