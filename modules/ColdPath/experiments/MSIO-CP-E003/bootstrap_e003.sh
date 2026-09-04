#!/usr/bin/env bash
set -euo pipefail

base_dir="/mnt/nvme1/chenhao/modelstateio-runtime"
source_dir="$base_dir/llama.cpp-d230ddd"
build_dir="$base_dir/build-d230ddd-cuda116"
log_dir="$base_dir/logs/MSIO-CP-E003"
commit="d230ddd763ffe27781c7ffd237ea78b639b36b6d"

if [ -e "$source_dir" ] || [ -e "$build_dir" ]; then
  echo "STOP: expected isolated source/build roots already exist" >&2
  exit 20
fi

mkdir -p "$log_dir"
exec > >(tee "$log_dir/bootstrap.log") 2>&1

date -Iseconds
hostname
git clone --depth 1 https://github.com/ggml-org/llama.cpp.git "$source_dir"
actual_commit="$(git -C "$source_dir" rev-parse HEAD)"
test "$actual_commit" = "$commit"
test -z "$(git -C "$source_dir" status --porcelain)"

cmake -S "$source_dir" -B "$build_dir" -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DGGML_CUDA=ON \
  -DCMAKE_CUDA_COMPILER=/usr/local/cuda-11.6/bin/nvcc \
  | tee "$log_dir/configure.log"
cmake --build "$build_dir" --target llama-cli --parallel 4 \
  | tee "$log_dir/build.log"

"$build_dir/bin/llama-cli" --help | tee "$log_dir/llama-cli-help.txt"
ldd "$build_dir/bin/llama-cli" | tee "$log_dir/llama-cli-ldd.txt"
! ldd "$build_dir/bin/llama-cli" | grep -q 'not found'
grep -E -- '--mmap|--no-mmap' "$log_dir/llama-cli-help.txt"
git -C "$source_dir" status --porcelain
sha256sum "$build_dir/bin/llama-cli" "$log_dir/llama-cli-help.txt" "$log_dir/llama-cli-ldd.txt" \
  | tee "$log_dir/SHA256SUMS"

