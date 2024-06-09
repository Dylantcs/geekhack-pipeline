# geekhack-pipeline
Scrape geekhack GB pages for GB details and their respective user posts/comments

## Summary

We webscrape the main Group Buy (GB) pages and their sub forums for descriptions of the GB. We then store this data in a `undecided` format for retrieval/usage later on

## Status

- Webscraping (In progress)
    - Collate all GB details and user posts within GB sub-forums (In progress)
    - Update info on a schedules basis
- PostgreSQL DB setup
- Schedule Update code to run using Airflow + Kafka

## Getting started [DEV]

Run the following lines to get started:
- python -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- pip install -e .
- pre-commit install
