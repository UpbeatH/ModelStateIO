#!/usr/bin/env python3
"""Convert the frozen Qwen2 PEFT LoRA artifact without Transformers or torch.

This deliberately supports only the E001 artifact contract: Qwen2.5-0.5B,
24 layers, q_proj/v_proj, F32 rank-8 LoRA.  Any drift is a hard failure.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path


EXPECTED_BASE = "Qwen/Qwen2.5-0.5B-Instruct"
EXPECTED_LAYERS = 24
EXPECTED_RANK = 8
EXPECTED_ALPHA = 16.0
TARGETS = {"q_proj": ("attn_q", 896), "v_proj": ("attn_v", 128)}


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fail(message):
    raise SystemExit("E001 conversion refusal: " + message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--adapter-config", type=Path, required=True)
    parser.add_argument("--adapter-tensors", type=Path, required=True)
    parser.add_argument("--gguf-py", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    sys.path.insert(0, str(args.gguf_py))
    import numpy as np
    from safetensors.numpy import load_file
    import gguf

    config = json.loads(args.adapter_config.read_text(encoding="utf-8"))
    if config.get("base_model_name_or_path") != EXPECTED_BASE:
        fail("unexpected base model")
    if config.get("r") != EXPECTED_RANK or float(config.get("lora_alpha")) != EXPECTED_ALPHA:
        fail("unexpected rank or alpha")
    if set(config.get("target_modules", [])) != set(TARGETS):
        fail("unexpected target modules")

    tensors = load_file(str(args.adapter_tensors))
    expected_names = set()
    mapped = []
    for layer in range(EXPECTED_LAYERS):
        for source, (dest, out_dim) in TARGETS.items():
            prefix = "base_model.model.model.layers.{}.self_attn.{}".format(layer, source)
            a_name = prefix + ".lora_A.weight"
            b_name = prefix + ".lora_B.weight"
            expected_names.update((a_name, b_name))
            if a_name not in tensors or b_name not in tensors:
                fail("missing tensor pair at layer {} {}".format(layer, source))
            a = tensors[a_name]
            b = tensors[b_name]
            if a.dtype != np.float32 or b.dtype != np.float32:
                fail("non-F32 tensor at layer {} {}".format(layer, source))
            if tuple(a.shape) != (EXPECTED_RANK, 896) or tuple(b.shape) != (out_dim, EXPECTED_RANK):
                fail("unexpected shape at layer {} {}".format(layer, source))
            mapped.append(("blk.{}.{}.weight.lora_a".format(layer, dest), a))
            mapped.append(("blk.{}.{}.weight.lora_b".format(layer, dest), b))
    if set(tensors) != expected_names:
        fail("unexpected tensor names")

    if args.output.exists():
        fail("output already exists")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    writer = gguf.GGUFWriter(str(args.output), "qwen2")
    writer.add_string(gguf.Keys.General.TYPE, "adapter")
    writer.add_string(gguf.Keys.Adapter.TYPE, "lora")
    writer.add_float32(gguf.Keys.Adapter.LORA_ALPHA, EXPECTED_ALPHA)
    for name, tensor in mapped:
        writer.add_tensor(name, tensor)
    writer.write_header_to_file()
    writer.write_kv_data_to_file()
    writer.write_tensors_to_file()
    writer.close()
    print(json.dumps({
        "adapter_config_sha256": sha256(args.adapter_config),
        "adapter_tensors_sha256": sha256(args.adapter_tensors),
        "output": str(args.output),
        "output_sha256": sha256(args.output),
        "tensor_pairs": len(mapped) // 2,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
