# SARI Cantaloupe

A Docker configuration of the [Cantaloupe](https://cantaloupe-project.github.io/) IIIF Image Server

## How to use

Copy and edit .env.example file:
`cp .env.example .env`

(optional) Edit configuration stored in `config/cantaloupe.properties`

Start with `docker-compose up -d`.

Place images in `images` directory.

## Configure Proxy

If Cantaloupe is behind a reverse proxy, CORS settings need to be set in order for it to function correctly with IIIF image viewers. For [our Nginx](https://github.com/swiss-art-research-net/sari-nginx) configuration, create a _location_ overwrite by creating a file in the `vhost.d` directory with the name of the virtual host followed by `_location`. e.g. for https://iiif.swissartresearch.net the file should be called `iiif.swissartresearch.net_location`. Specify the CORS settings in this file, for example as follows:

```
add_header      "Access-Control-Allow-Methods" "GET, OPTIONS" always;
add_header      "Access-Control-Allow-Headers" "Accept,DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range" always;
add_header      "Access-Control-Max-Age" 1728000;
```

The `rs-iiif-mirador` component in Metaphacts/ResearchSpace tends to introduce additional slashes in the URL to an image. To redirect URLs with double slashes, insert the following in the _location_ overwrite:

```
if ($request_uri ~ "^[^?]*?//") {
   add_header   "Access-Control-Allow-Origin" "*" always;
   add_header      "Access-Control-Allow-Methods" "GET, OPTIONS" always;
   add_header      "Access-Control-Allow-Headers" "Accept,DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range" always;
   add_header      "Access-Control-Max-Age" 1728000;
   rewrite "^" $scheme://$host$uri permanent;
}
```

This will rewrite the URL to single slashes and insert a CORS header so that the 301 redirect is followed.