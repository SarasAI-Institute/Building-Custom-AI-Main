# Integration inputs

Copy these JSON files into the notebook working directory before Module 5. Null/empty values are deliberate: fill them from your actual saved components rather than pretending example identities are real.

- `risklens_config.json`: inspector revision/prompt/processor settings, frozen corpus, embedding revision, selected Analyst arm/dtype and actual Module 4 review record.
- `source_products.json`: map each existing source ID to a list of externally verified applicable product IDs. An unrelated appliance review must not be mapped to a bottle.
- `risklens_batch_manifest.json`: ≥10 distinct real cases, each with `case_id`, `image_path`, `product_id`, `reference_verdict` (GOOD or DEFECTIVE). Keep acquisition provenance. Labels are for evaluation only.

The one-argument `analyze_product(image)` reads `image.info["product_id"]`. The optional second argument supplies the same external identity explicitly. It never guesses product identity from a dataset label. `analyze_product_trace` provides the full per-stage batch trace. Public results always contain `note`, `evidence` (string) and `report` (string); GOOD returns empty evidence/report.
