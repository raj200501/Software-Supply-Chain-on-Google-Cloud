{{- define "payments.name" -}}
payments
{{- end -}}

{{- define "payments.fullname" -}}
{{ printf "%s-payments" .Release.Name }}
{{- end -}}
