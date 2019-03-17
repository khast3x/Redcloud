FROM traefik:alpine

COPY traefik.toml /etc/traefik/traefik.toml
# admin:Redcloud
COPY .htpasswd /etc/traefik/.htpasswd
CMD ["traefik"]