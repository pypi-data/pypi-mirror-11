/*
* Based on Lua's all.c -- Lua core & libraries in a single file.
*/

#define luaall_c

#define LUA_USE_POSIX

#include "lua/lapi.c"
#include "lua/lcode.c"
#include "lua/ldebug.c"
#include "lua/ldo.c"
#include "lua/ldump.c"
#include "lua/lfunc.c"
#include "lua/lgc.c"
#include "lua/llex.c"
#include "lua/lmem.c"
#include "lua/lobject.c"
#include "lua/lopcodes.c"
#include "lua/lparser.c"
#include "lua/lstate.c"
#include "lua/lstring.c"
#include "lua/ltable.c"
#include "lua/ltm.c"
#include "lua/lundump.c"
#include "lua/lvm.c"
#include "lua/lzio.c"

#include "lua/lauxlib.c"
#include "lua/lbaselib.c"
#include "lua/ldblib.c"
#include "lua/liolib.c"
#include "lua/lmathlib.c"
#include "lua/loadlib.c"
#include "lua/loslib.c"
#include "lua/lstrlib.c"
#include "lua/ltablib.c"

// Include our custom modules
#include "bitop/bit.c"
#include "libinjection/lualib.c"
#include "luautf8/lutf8lib.c"
#include "lpeg/lptree.c"
#include "lua-cmsgpack/lua_cmsgpack.c"
#include "lua-snapshot/snapshot.c"

// Activate the Lua modules we need and our custom ones.
static const luaL_Reg lualibs[] = {
  {"", luaopen_base},
  {LUA_TABLIBNAME, luaopen_table},
  {LUA_STRLIBNAME, luaopen_string},
  {LUA_MATHLIBNAME, luaopen_math},

  // Include unsafe libs in tests
#if defined(LUA_UNSAFE_MODE)
  {LUA_IOLIBNAME, luaopen_io},
  {LUA_OSLIBNAME, luaopen_os},
#endif

  // SECURITY NOTE:
  // The following modules are unsafe according to http://lua-users.org/wiki/SandBoxes.
  // They are loaded, but never exposed to the sandbox used to run the hook handlers.
  // See lib/boot.lua for more details.
  {LUA_LOADLIBNAME, luaopen_package},
  {LUA_DBLIBNAME, luaopen_debug},  

  // Our custom modules
  {"libinjection", luaopen_libinjection},
  {"utf8", luaopen_utf8},
  {"bit", luaopen_bit},
  {"lpeg", luaopen_lpeg},
  {LUACMSGPACK_NAME, luaopen_cmsgpack},
  {"snapshot", luaopen_snapshot},
  {NULL, NULL}
};
// The previous array replaces the one in linit.c.
// If you update Lua, make sure to comment the lualibs declaration in the following file.
#include "lua/linit.c"
