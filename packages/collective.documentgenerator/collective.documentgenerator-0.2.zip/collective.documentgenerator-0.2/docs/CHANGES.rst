Changelog
=========

0.2 (2015-09-22)
----------------
- Renamed field 'pod_portal_type' to 'pod_portal_types' as this field
  is a multiselection field.
  [gbastien]
- Renamed 'doc_uid' parameter used by the 'document-generation' view to
  'template_uid', more obvious, and makes it available in the viewlet
  link infos dict.
  [gbastien]
- Added field IConfigurablePODTemplate.pod_formats to be able to select the
  format we want to generate the POD template in.
  [gbastien]
- When evaluating the tal_condition on the template, pass extra_expr_ctx
  to the TAL expression so 'context' and 'here' become the element on which the TAL
  expression is actually evaluated instead of the pod_template and 'template'
  is the pod_template
  [gbastien]


0.1 (2015-07-17)
----------------

- Nothing changed yet.


0.1 (2015-07-17)
----------------
- Initial release.
  [gbastien]

- ...

- Update bootstrap
  use https://raw.githubusercontent.com/buildout/buildout/master/bootstrap/bootstrap.py
  [fngaha]
