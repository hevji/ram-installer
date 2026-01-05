local Engine = {}

Engine.server = "{server}"
Engine.ip = "{ip}"

function Engine:new()
    local obj = {
        ip = self.ip,
        server = self.server,
        connected = false
    }
    setmetatable(obj, self)
    self.__index = self
    return obj
end

function Engine:connect()
    self.connected = true
    return true
end

function Engine:getAddress()
    return {
        ip = self.ip,
        server = self.server
    }
end

return Engine
