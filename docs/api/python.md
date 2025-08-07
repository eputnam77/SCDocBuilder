# Python API

Use these helpers when you embed SCDocBuilder in your own tools.

## fill_template

```python
fill_template(template_path, worksheet_path, output_path=None, schema=None)
```

Fill a template with answers from a worksheet.

* **template_path** – path to the template DOCX.
* **worksheet_path** – path to the worksheet DOCX.
* **output_path** – optional output location; default creates a
  timestamped file.
* **schema** – optional placeholder mapping.

Returns the path to the generated DOCX.

## extract_fields

```python
extract_fields(doc, field_mappings=None)
```

Pull placeholder values from a worksheet document.

## replace_placeholders

```python
replace_placeholders(doc, values)
```

Swap placeholders in a document for supplied values.

## apply_conditionals

```python
apply_conditionals(doc, answers)
```

Remove blocks that do not match the chosen option.

## load_placeholder_schema

```python
load_placeholder_schema(path)
```

Load placeholder mappings from JSON or YAML.

## validate_input_files

```python
validate_input_files(template, worksheet)
```

Check that template and worksheet exist, are DOCX and under 10MB.

## load_document

```python
load_document(path)
```

Open a Word document using `python-docx`.

## save_document

```python
save_document(doc, path)
```

Write a document to disk.

## validate_mandatory_fields

```python
validate_mandatory_fields(doc)
```

Raise `ValueError` if required fields or questions are missing.

## export_html

```python
export_html(doc)
```

Convert a document to sanitized HTML.

## reject_macros

```python
reject_macros(path)
```

Raise `ValueError` when macros are detected.

## cleanup_uploads

```python
cleanup_uploads(*paths)
```

Delete uploaded files after processing.

## benchmark_processing

```python
benchmark_processing(template, worksheet)
```

Return the time in seconds needed to load both files.
