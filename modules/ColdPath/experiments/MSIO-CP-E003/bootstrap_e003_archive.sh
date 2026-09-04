#!/usr/bin/env bash
set -euo pipefail

base_dir="/mnt/nvme1/chenhao/modelstateio-runtime"
archive="$base_dir/incoming/llama.cpp-d230ddd.tar.gz"
source_dir="$base_dir/llama.cpp-d230ddd"
build_dir="$base_dir/build-d230ddd-cuda116"
log_dir="$base_dir/logs/MSIO-CP-E003"
archive_sha="2625B2172F06AB97E0B4331AC6D2FF93D76278922699212B1BE61758D27E816F"

test -f "$archive"
test ! -e "$source_dir"
test ! -e "$build_dir"
test "$(sha256sum "$archive" | awk '{print toupper($1)}')" = "$archive_sha"

mkdir -p "$source_dir" "$log_dir"
exec > >(tee "$log_dir/bootstrap-archive.log") 2>&1

date -Iseconds
hostname
tar -xzf "$archive" --strip-components=1 -C "$source_dir"
test -f "$source_dir/CMakeLists.txt"

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
sha256sum "$archive" "$build_dir/bin/llama-cli" "$log_dir/llama-cli-help.txt" "$log_dir/llama-cli-ldd.txt" \
  | tee "$log_dir/SHA256SUMS"

