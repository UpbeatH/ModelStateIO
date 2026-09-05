# MSIO-SP-E007R1 private prerequisite acquisition correction

## Objective

Repeat the unstarted prerequisite build after E007's g130 GitHub download
stall. The only changed acquisition mechanism is a locally downloaded,
SHA-256-verified official libffi 3.4.6 release archive transferred into g130's
permitted private incoming directory.

## Frozen scope

- Verify the incoming archive byte count `1391684` and SHA-256
  `b0dea9df23c863a7a50e825440f3ebffabd65df1497108e5d437747843895a4e`
  before copying it under a new E007R1 build root.
- Download only the already verified official SQLite 3.45.3 and Python 3.10.14
  archives from their HTTPS sources; record all identities.
- Build libffi, SQLite, and Python only below
  `/mnt/nvme1/chenhao/modelstateio-runtime/python-runtime/statepatch-e007r1`.
  Use the same private library flags and E007's individual import pass rule.

## Boundary

E007 remains closed. This has no model conversion or GPU action and does not
alter system packages, interpreter, CUDA, cache, Lustre/PFS, g129, or any
other-user path.
