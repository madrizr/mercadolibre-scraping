# Scraping Mercadolibre

## how does it work?

This is a process of data extraction from the MercadoLibre website, with the aim of identifying the most popular product based on a given search. The search is performed using a list of specific parameters. In other words, MercadoLibre is being explored to find the most searched or sold product, using search criteria.

As for the api, This Python script sets up an API with FastAPI and Scrapy. When accessing a given endpoint, it triggers a Scrapy spider that extracts data and stores it in a JSON file. The script then reads this file and returns the data as a response from the endpoint.

## Technologies

- Python 3.12.0
- Pip 23.3.1

### Libreries used
- Scrapy 2.11.0
- FastApi  0.108.0
- uvicorn 0.25.0

## Run
- Run the Spider
`scrapy crawl mercadolibre`

- Run the API
`uvicorn main:app --reload`

`--reload` keep the port active and listen for changes

### Note

For this project I used the virtual environment **Virtualenv**


