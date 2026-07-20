# H0 Immutability Protocol — Revision 2

Effective from this revision, every H0 cell directory is frozen at the byte
level. No process may write into an H0 cell directory after the H0 run is
recorded. This prohibition includes, without limitation, adding or updating
`healer` fields, Healer pass provenance, repaired-source hashes, or
`repaired_candidate.py` files.

All H1 outputs must be stored in a separate experiment-level results directory.
The canonical layout is the structure used by
`docs/experiments/results/math16_healer_vnext_qualification_v1/`:

```text
predictions/
reports/
cells/<cell_id>/
  repaired_candidate.py
  artifact_h1.json
```

H1 artifacts must reference their H0 inputs by path and hash; they must never
mutate those inputs in place.

## Revision history and non-retroactivity

During the revision 1 period, through commit
`9d8381f36c313b18f197ba67182b3c6391e384c8`, writing approved H1 fields and
repaired candidates into H0 cell directories was permitted by the protocol in
force at that time. Those results remain valid and are not retroactively
invalidated by revision 2.

Revision 2 changes storage policy to reduce audit cost and strengthen the
immutability guarantee. It changes evidence placement only; it does not revise
or rerun previously accepted model outputs or formal evaluations.
