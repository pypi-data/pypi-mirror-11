-- Encode a Lua object to be sent to the server.
function encode(object)
  return cmsgpack.pack(object)
end