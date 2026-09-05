# MSIO-KVG-E001R1 server-build correction

E001 closed before execution because its existing build configuration enabled
prebuilt UI provisioning. E001R1 changes only the build configuration to
`LLAMA_USE_PREBUILT_UI=OFF`, retaining the same isolated source, CUDA build,
server target, model, loopback binding, slot-state protocol and stop rules.
This prevents an unrelated network/UI dependency; it does not install software
or change any system path. If the server target builds, E001R1 performs the
same single exact slot save/restore capability gate from E001.
