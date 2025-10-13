{{- define "users.name" -}}
users
{{- end -}}

{{- define "users.fullname" -}}
{{ printf "%s-users" .Release.Name }}
{{- end -}}
