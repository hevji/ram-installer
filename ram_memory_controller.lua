local MemoryController = {}
MemoryController.__index = MemoryController

local function createModule(name, size)
    return {
        name = name,
        size = size,
        installed = false
    }
end

function MemoryController:new()
    local obj = {
        modules = {},
        initialized = false
    }
    setmetatable(obj, self)
    return obj
end

function MemoryController:initialize()
    self.initialized = true
    print("[Lua] Initializing memory controller...")
    self:delay(0.2)
    print("[Lua] Controller online.")
end

function MemoryController:addModule(module)
    table.insert(self.modules, module)
end

function MemoryController:scan()
    print("[Lua] Scanning memory slots...")
    for i = 1, #self.modules do
        self:delay(0.05)
        print(string.format("[Lua] Slot %d detected (%dGB)", i, self.modules[i].size))
    end
end

function MemoryController:install()
    print("[Lua] Installing RAM modules...")
    for _, module in ipairs(self.modules) do
        self:delay(0.1)
        module.installed = true
        print(string.format("[Lua] Installed %s (%dGB)", module.name, module.size))
    end
end

function MemoryController:uninstall()
    print("[Lua] Uninstalling RAM modules...")
    for _, module in ipairs(self.modules) do
        self:delay(0.1)
        module.installed = false
        print(string.format("[Lua] Removed %s", module.name))
    end
end

function MemoryController:diagnostics()
    print("[Lua] Running diagnostics...")
    self:delay(0.2)
    for _, module in ipairs(self.modules) do
        print(string.format(
            "[Lua] Module %s | Size: %dGB | Installed: %s",
            module.name,
            module.size,
            tostring(module.installed)
        ))
    end
end

function MemoryController:delay(seconds)
    local start = os.clock()
    while os.clock() - start < seconds do end
end

local Utils = {}

function Utils.generateModules(count)
    local modules = {}
    local sizes = {4, 8, 16, 32, 64}
    for i = 1, count do
        local size = sizes[(i % #sizes) + 1]
        table.insert(modules, createModule("RAM_SLOT_" .. i, size))
    end
    return modules
end

local controller = MemoryController:new()
controller:initialize()

local generatedModules = Utils.generateModules(6)
for _, module in ipairs(generatedModules) do
    controller:addModule(module)
end

controller:scan()
controller:diagnostics()
controller:install()
controller:diagnostics()
controller:uninstall()
controller:diagnostics()

print("[Lua] Memory operation completed successfully.")
print("[Lua] No actual RAM was modified.")
