import lief

libnative = lief.parse("libimgdecoder.so")
libnative.add_library("libgadget.so") # Injection!
libnative.write("libimgdecoder-9.22-frida.so")