-- Compile and load base 64 encoded Lua bytecode.

require 'base64'

bytecode = {}

local function dump(func)
  return base64.encode(string.dump(func))
end

-- Compile Lua code to base 64 encoded bytecode.
function bytecode.compile(code, name)
  return dump(loadstring(code, name))
end

-- Compile Lua file to base 64 encoded bytecode.
function bytecode.compile_file(file)
  return dump(loadfile(file))
end

-- Lua bytecode signature (Base64 encoded "\eLua")
local LUA_BYTECODE_SIG = "G0x1Y"

-- Load the Lua base 64 encoded bytecode (or plain text code) into a function and returns it.
-- This function will detect if the code is bytecode and decode it.
function bytecode.load(code, name)
  if code:sub(1, 5) == LUA_BYTECODE_SIG then
    -- `code` contains Base64 encoded bytecode. Decode it.
    code = base64.decode(code)
  end

  return assert(loadstring(code, name))
end