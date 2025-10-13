{{- define "notifications.name" -}}
notifications
{{- end -}}

{{- define "notifications.fullname" -}}
{{ printf "%s-notifications" .Release.Name }}
{{- end -}}
