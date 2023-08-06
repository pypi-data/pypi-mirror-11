-- This file is executed when the Lua VM boots.
require 'encode'
require 'bytecode'

-- This is required to make lexers load from test harness.
-- In VM the path is handled for us by vm.rb --ol
lexer_path='lib/lexers/?.lua'
package.path = package.path..';'..lexer_path

-- Define the environment available to code executing in the VM.
-- All available functions must be declared here.
-- Make sure the function is safe before adding it here.
-- See http://lua-users.org/wiki/SandBoxes
SANDBOX_ENV = {
  -- Lua libs
  ipairs = ipairs,
  next = next,
  pairs = pairs,
  pcall = pcall,
  tonumber = tonumber,
  tostring = tostring,
  type = type,
  unpack = unpack,
  assert = assert,
  error = error,
  getmetatable = getmetatable,
  setmetatable = setmetatable,
  rawget = rawget,
  rawset = rawset,
  collectgarbage = collectgarbage,
  math = math,
  string = string,
  bit = {
    band = bit.band,
    extract = bit.extract,
    bor = bit.bor,
    bnot = bit.bnot,
    arshift = bit.arshift,
    rshift = bit.rshift,
    rrotate = bit.rrotate,
    replace = bit.replace,
    lshift = bit.lshift,
    lrotate = bit.lrotate,
    btest = bit.btest,
    bxor = bit.bxor
  },
  coroutine = {
    create = coroutine.create,
    resume = coroutine.resume,
    running = coroutine.running,
    status = coroutine.status,
    wrap = coroutine.wrap,
    yield = coroutine.yield,
  },
  debug = {
    -- Block most debug in sandbox, but allow tracebacks
    traceback = debug.traceback
  },
  select = select,
  utf8 = {
    byte = utf8.byte,
    char = utf8.char,
    find = utf8.find,
    format = utf8.format,
    gmatch = utf8.gmatch,
    gsub = utf8.gsub,
    len = utf8.len,
    lower = utf8.lower,
    match = utf8.match,
    rep = utf8.rep,
    reverse = utf8.reverse,
    sub = utf8.sub,
    upper = utf8.upper,
    split = utf8.split,
    escape = utf8.escape,
    charpos = utf8.charpos,
    insert = utf8.insert,
    remove = utf8.remove,
    next = utf8.next,
    ncasecmp = utf8.ncasecmp,
  },
  table = {
    insert = table.insert,
    maxn = table.maxn,
    remove = table.remove,
    sort = table.sort,
    map = table.map,
    reduce = table.reduce,
    length = table.length,
    concat = table.concat,
  },
  libinjection = {
    sqli = libinjection.sqli,
    fingerprint = libinjection.fingerprint,
    xss = libinjection.xss,
    sqli_tokenize = libinjection.sqli_tokenize
  },
  -- LPeg Library
  lpeg = {
    ptree = lpeg.ptree,
    pcode = lpeg.pcode,
    match = lpeg.match,
    B = lpeg.B,
    V = lpeg.V,
    C = lpeg.C,
    Cc = lpeg.Cc,
    Cmt = lpeg.Cmt,
    Cb = lpeg.Cb,
    Carg = lpeg.Carg,
    Cp = lpeg.Cp,
    Cs = lpeg.Cs,
    Ct = lpeg.Ct,
    Cf = lpeg.Cf,
    Cg = lpeg.Cg,
    P = lpeg.P,
    S = lpeg.S,
    R = lpeg.R,
    locale = lpeg.locale,
    version = lpeg.version,
    setmaxstack = lpeg.setmaxstack,
    type = lpeg.type,
  },
  -- pre built lexer library
  -- the call to load here will both load the code
  -- and compile the LPeg grammar
  lexers = {
    lexer = require('lexers/lexer'),
    bash = require('lexers/lexer').load('bash'), -- bash
    bash_dqstr = require('lexers/lexer').load('bash_dqstr'),  -- bash strings
    markers = require('lexers/lexer').load('markers'),
    html = require('lexers/lexer').load('html'),
    javascript = require('lexers/lexer').load('javascript'),
    css = require('lexers/lexer').load('css'),
  },
  -- Immunio vars
  serverdata = {}, -- Default empty serverdata
  agentdata = {},
  utils = {}, -- Used to store utility functions declared in the sandbox.
  -- pass mode flags into the VM
  DEV_MODE = DEV_MODE,
  DEBUG_MODE = DEBUG_MODE,
  LUA_PLATFORM = LUA_PLATFORM or 'unix',
  IMMUNIO_KEY = IMMUNIO_KEY,
  IMMUNIO_SECRET = IMMUNIO_SECRET
}

-- Enable a few more things in dev mode. For debugging.
if DEBUG_MODE or DEV_MODE then
  SANDBOX_ENV.print = print
  SANDBOX_ENV.snapshot = snapshot
else
  SANDBOX_ENV.print = function(...) end
end


-- Perform a VM call a method of a lua pseudo-object
function sandboxed_method_call(method, object, vars)
  if DEBUG_MODE then
    SANDBOX_ENV.utils.debug_prefix = "UNKNOWN"
      -- Change the values here to toggle debugging per module.
    SANDBOX_ENV.utils.debug_module_prefixes = {
      UNKNOWN = true,
      IO = true,
      SQLi = true,
      ExceptionHandler = true,
      Redirect = true,
      XSS = true,
      Eval = true,
    }
  end
  -- Merges the vars and the default sandbox env.
  -- The vars can override the sandbox environment.
  -- The table is copied to keep data from leaking
  --   out of the functions.
  local merged_vars = {}
  merged_vars._G = merged_vars
  for k, v in pairs(SANDBOX_ENV) do
    merged_vars[k] = v
  end

  if vars then
    for k, v in pairs(vars) do
      merged_vars[k] = v
    end
  end

  -- XXX Open sandbox in DEBUG_MODE
  if DEBUG_MODE then
    merged_vars['__REAL_G'] = _G
  end
  -- Sets the environment of the function.
  setfenv(method, merged_vars)
  -- Call it!
  local rval = nil
  if object then
    rval = method(object)
  else
    rval = method()
  end
  -- Hint the lua VM GC that the references held to values in merged_vars don't
  -- count anymore. If we omit this line the function environment is held onto
  -- by the GC and we leak the universe... --ol
  setmetatable( merged_vars, {__mode = "v"} )
  -- Remove merged_vars from function environment so it can be collected sooner
  setfenv(method, _G)
  return rval
end

-- Function called by the VM to call and sandbox a function.
function sandboxed_call(func, vars)
  return sandboxed_method_call(func, nil, vars)
end

if DEBUG_MODE then
-- Memory Snapshot Debugger
  local saved_snapshot = {}
  function dump_snapshot( label )
    collectgarbage()
    collectgarbage()
    saved_snapshot = snapshot.snapshot()
    print("------------------------\nSNAPSHOT:\n")
    if label then print(label) end
    for k,v in pairs(saved_snapshot) do
        print( "ALLOCATION:" .. tostring(k):gsub("userdata:", "") .. " " .. v)
    end
  end

  function update_snapshot()
    collectgarbage()
    collectgarbage()
    saved_snapshot = snapshot.snapshot()
  end

  function diff_snapshot( update )
    collectgarbage()
    collectgarbage()
    local S = snapshot.snapshot()
    output = ("------------------------\nDIFF SNAPSHOT:\n")
    for k,v in pairs(S) do
      if saved_snapshot[k] == nil then
        output = output .. "ALLOCATION:" .. tostring(k):gsub("userdata:", "") .. " " .. v .. "\n"

      end
    end
    if update then saved_snapshot = S end
    return output
  end

  -- Uncomment for snapshot tracing
  --snapshot.tron()
  -- Uncomment to generate a snapshot at boot.
  --dump_snapshot('BOOT')
  --snapshot.troff()
end

