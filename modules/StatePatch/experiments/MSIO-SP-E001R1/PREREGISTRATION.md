# MSIO-SP-E001R1: adapter container correction

E001 closed before lifecycle measurement: the converted artifact omitted the
required `general.type=adapter` GGUF field, and the runtime rejected it during
model construction.  E001R1 changes only that container metadata field.  It
retains the same base, source adapter, 48-tensor mapping, hashes, endpoint,
prompt, decoding settings, bounded server lifetime, and decision rule from
E001.  A new adapter output path and a new raw-log directory are mandatory;
E001 receipts cannot be reused as lifecycle evidence.
