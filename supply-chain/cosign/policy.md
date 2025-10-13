# Cosign Policy Snapshot

Sign images with `cosign sign --key gcpkms://projects/PROJECT/locations/global/keyRings/slsa/cryptoKeys/container` and store provenance in Artifact Registry alongside the image. Verification should run in deployment pipelines using `cosign verify --certificate-identity-regex`. 
