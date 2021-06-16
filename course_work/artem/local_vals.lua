-- -- http://kolenka.su/blog/love/vvedenie-v-lua-chast-5-funkczii.html

local function makeCounter()
    local i = 0
    return function ()
        i = i + 1
        return i
    end
end

local count = makeCounter()

local function make(initial)
    local value = initial
    local function get()
        return value end
    local function set(newValue)
        value = newValue
    end
    return get, set
end

local getX, setX = make()


local function factorial(n)
    if n < 0 then
        error("n must be non-negative")
    end

    if n == 0 then
        return 1
    end

    return factorial(n - 1) * n
end

local function makeGreeter(name)
    local text = "Hello, " .. name
    local function greet()
        print(text)
    end
    greet()
end

makeGreeter("Bob") --> "Hello, Bob"

-- imap вызывает указанную функцию для всех элементов массива и возвращает массив с результатами
local function imap(t, f, ...)
    local result = {}

    for i, v in ipairs(t) do
        result[i] = f(v, ...)
    end

    return result
end

local squares = imap({5, 6, 7, 8, 9, 10}, function (v) return v ^ 2 end)

for i, v in ipairs(squares) do
    print(i, v)
end

-- local function wtf(...)
--     local args = {...}
--     local first, second = ...
--     local x = ... * 5

--     print(..., "a")
--     print(first, second, x)
--     print((...))
-- end

local function sign(x)
    if x > 0 then
        return 1
    elseif x < 0 then
        return -1
    else
        return 0
    end
end

print(sign(-16)) --> -1

local function lerp(a, b, amount)
    return a + (b - a) * amount
end

print(lerp(3, 7, 0.375)) --> 4.5

local function foo()
    return 3, 4, 5
end

local a, b, c = foo()

d, f, g = foo()

localfunc = 8