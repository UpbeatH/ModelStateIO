#!/usr/bin/env python3
"""Strict converter for the frozen E002 rank-16 Qwen2 LoRA artifact."""
import argparse
import hashlib
import json
import sys
from pathlib import Path

BASE = "Qwen/Qwen2.5-0.5B-Instruct"
LAYERS, RANK, ALPHA = 24, 16, 32.0
TARGETS = {
    "q_proj": ("self_attn", "attn_q", 896, 896),
    "k_proj": ("self_attn", "attn_k", 128, 896),
    "v_proj": ("self_attn", "attn_v", 128, 896),
    "o_proj": ("self_attn", "attn_output", 896, 896),
    "gate_proj": ("mlp", "ffn_gate", 4864, 896),
    "up_proj": ("mlp", "ffn_up", 4864, 896),
    "down_proj": ("mlp", "ffn_down", 896, 4864),
}


def refuse(message):
    raise SystemExit("E002 conversion refusal: " + message)


def digest(path):
    out = hashlib.sha256()
    with open(path, "rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            out.update(block)
    return out.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--tensors", type=Path, required=True)
    parser.add_argument("--gguf-py", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(args.gguf_py))
    import numpy as np
    from safetensors.numpy import load_file
    import gguf

    config = json.loads(args.config.read_text(encoding="utf-8"))
    if config.get("base_model_name_or_path") != BASE:
        refuse("unexpected base")
    if config.get("r") != RANK or float(config.get("lora_alpha")) != ALPHA:
        refuse("unexpected rank or alpha")
    if set(config.get("target_modules", [])) != set(TARGETS):
        refuse("unexpected targets")
    tensors, expected, mapped = load_file(str(args.tensors)), set(), []
    for layer in range(LAYERS):
        for source, (scope, destination, out_dim, in_dim) in TARGETS.items():
            prefix = "base_model.model.model.layers.{}.{}.{}".format(layer, scope, source)
            a_name, b_name = prefix + ".lora_A.weight", prefix + ".lora_B.weight"
            expected.update((a_name, b_name))
            if a_name not in tensors or b_name not in tensors:
                refuse("missing pair {}".format(prefix))
            a, b = tensors[a_name], tensors[b_name]
            if a.dtype != np.float32 or b.dtype != np.float32:
                refuse("non-F32 {}".format(prefix))
            if tuple(a.shape) != (RANK, in_dim) or tuple(b.shape) != (out_dim, RANK):
                refuse("shape mismatch {}".format(prefix))
            stem = "blk.{}.{}.weight".format(layer, destination)
            mapped.extend(((stem + ".lora_a", a), (stem + ".lora_b", b)))
    if set(tensors) != expected:
        refuse("unexpected tensor names")
    if args.output.exists():
        refuse("output exists")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    writer = gguf.GGUFWriter(str(args.output), "qwen2")
    writer.add_string(gguf.Keys.General.TYPE, "adapter")
    writer.add_string(gguf.Keys.Adapter.TYPE, "lora")
    writer.add_float32(gguf.Keys.Adapter.LORA_ALPHA, ALPHA)
    for name, tensor in mapped:
        writer.add_tensor(name, tensor)
    writer.write_header_to_file(); writer.write_kv_data_to_file(); writer.write_tensors_to_file(); writer.close()
    print(json.dumps({"config_sha256": digest(args.config), "tensors_sha256": digest(args.tensors),
                      "output_sha256": digest(args.output), "pairs": len(mapped) // 2}, sort_keys=True))


if __name__ == "__main__":
    main()
