# Used by Ruby to compile the extension.
require 'mkmf'


# libinjection doesn't support `#include`ing all the .c files directly
# in the source, since it has symbols which conflict. Instead the `$objs`
# list below compiles each file separately then links them in the final
# step.
$objs = [
  "all.o",
  "libinjection/libinjection_html5.o",
  "libinjection/libinjection_xss.o",
  "libinjection/libinjection_sqli.o",
#Compile in LPEG
  "lpeg/lpcap.o",
  "lpeg/lpcode.o",
  "lpeg/lpprint.o",
  "lpeg/lpvm.o",
#  "lpeg/lptree.o",
]

# The created Makefile puts the compiled .o files into the `libinjection`
# subdirectory, but it doesn't create it. Make sure it exists.
xsystem "mkdir -p libinjection"
xsystem "mkdir -p lpeg"

# Build init hook, only used when running agent in dev mode
STDERR.puts `make -C ../../../../lua-hooks hooks/__init__.lua`

#!!! PLEASE ALWAYS make sure the flags here match the Lua Makefile so our tests are valid
# Enable safety assertions
$CFLAGS << " -DLUA_USE_APICHECK -Dlua_assert=assert "
# Enable omptimisation
$CFLAGS << " -O3 "
# Without this flag, I get this error when trying to compile in agent-java:
# relocation R_X86_64_32S against `.rodata' can not be used when making a shared object; recompile with -fPIC
$CFLAGS << " -fPIC "
create_makefile 'immunio/lua-hooks'
