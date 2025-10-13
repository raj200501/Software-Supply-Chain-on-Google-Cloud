{{- define "orders.name" -}}
orders
{{- end -}}

{{- define "orders.fullname" -}}
{{ printf "%s-orders" .Release.Name }}
{{- end -}}
