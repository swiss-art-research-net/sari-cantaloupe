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

The script takes two optional parameters to specify an offset (the number of the line in the csv where the download should start) and a limit (the number of images to download) . E.g. download 10 images, starting from the 20th:

`docker exec bso_iiif_jobs python downloadImages.py 20 10`