{{- define "inventory.name" -}}
inventory
{{- end -}}

{{- define "inventory.fullname" -}}
{{ printf "%s-inventory" .Release.Name }}
{{- end -}}
