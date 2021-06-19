local function imap(t, f, ...)
    local result = {}

    for i, v in ipairs(t) do
        aa = 5
        result[i] = f(v, ...)
        result[ii] = aa()
        result['dd'] = 5
        result['vv'] = 'rrr'
        result['gg'] = {a = 12, b = 5, 'aa', 2, c = {1, 2, 3, d = f(), c = a}}

    end

    return result
end