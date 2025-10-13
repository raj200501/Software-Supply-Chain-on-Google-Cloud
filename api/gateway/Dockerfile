# syntax=docker/dockerfile:1.4
FROM golang:1.21 AS build
WORKDIR /src
COPY go.mod ./
RUN go mod download
COPY . .
RUN go build -o /out/gateway ./api/gateway

FROM gcr.io/distroless/base-debian12
COPY --from=build /out/gateway /gateway
ENTRYPOINT ["/gateway"]
