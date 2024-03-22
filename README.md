# SARI Cantaloupe

A Docker configuration of the [Cantaloupe](https://cantaloupe-project.github.io/) IIIF Image Server

## How to use

Copy and edit .env.example file:
`cp .env.example .env`

(optional) Edit configuration stored in `config/cantaloupe.properties`

Start with `docker-compose up -d`.

Place images in `images` directory.

## Download images

Execute the image download script via the docker container:

`docker exec bso_iiif_jobs python downloadImages.py`

The script expects a csv file `images.csv` in the `/data` folder. It is expected to contain the following columns:
- `id`: the URI of the artwork starting with `https://resource.swissartresearch.net/artwork/`
- `image`: the URL of the image that should be downloaded.

The script takes two optional parameters to specify an offset (the number of the line in the csv where the download should start) and a limit (the number of images to download) . E.g. download 10 images, starting from the 20th:

`docker exec bso_iiif_jobs python downloadImages.py 20 10`
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
