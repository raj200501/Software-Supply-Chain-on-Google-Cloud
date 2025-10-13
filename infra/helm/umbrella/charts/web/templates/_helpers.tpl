{{- define "web.name" -}}
web
{{- end -}}

{{- define "web.fullname" -}}
{{ printf "%s-web" .Release.Name }}
{{- end -}}
