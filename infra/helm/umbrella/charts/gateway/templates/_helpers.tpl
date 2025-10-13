{{- define "gateway.name" -}}
gateway
{{- end -}}

{{- define "gateway.fullname" -}}
{{ printf "%s-gateway" .Release.Name }}
{{- end -}}
