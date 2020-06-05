# route-poi

![python (scoped)](https://img.shields.io/badge/python-%3E%3D3.7.6-brightgreen.svg)

## Description
`route-poi` gets points of interest along a route given start and destination addresses and a list of requested POI types.

`route-poi` finds towns at approximately 30 minute increments along the driven route from your start to destination. `route-poi` then finds the request POI types for all found towns.

## Usage

### Installation

Install the dependencies with the following command.

`pip install -r requirements.txt`

### Execution

To run `route-poi`, use the following command.

`python app.py -s="start_address" -d="dest_address" -p="poi_1,...,poi_n"`

where

`-s="start_address"` specifies the starting address of the route (required)

`-d="dest_address"` specifies the destination address of the route (required)

`-p="poi_1,...,poi_n"` specifies the list (comma-separated) of requested POI types (optional, finds all available POI in each town by default)

## Authors

* Rishi Masand

* Ishaan Masand

