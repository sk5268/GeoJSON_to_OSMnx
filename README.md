# GeoJSON_to_OSMnx

A Python utility for converting GeoJSON files containing line geometries into network graphs using OSMnx.

## Overview

This tool allows you to convert geographic line data (LineString or MultiLineString) stored in GeoJSON format into a fully functional network graph.

## History

I had a GeoJSON file containing road network data as MultiLineString objects, but needed proper node and edge GeoDataFrames to construct an OSMnx-compatible network. I came up with a script to extract vertices, create the required GeoDataFrames, and build a network graph that supports all OSMnx analysis functions.

## Features

- Converts GeoJSON line geometries into OSMnx graph structure
- Handles both LineString and MultiLineString geometries
- Creates unique nodes at all line endpoints
- Generates proper network topology
- Calculates edge lengths
- Compatible with OSMnx's analysis and visualization functions

## Requirements

- Python3
- osmnx

## Installation

```bash
pip install osmnx
```
Note: geopandas and shapely libraries are installed as dependancies for osmnx <br><br>
Clone this repository:
```bash
git clone https://github.com/yourusername/GeoJSON_to_OSMnx.git
cd GeoJSON_to_OSMnx
```

## Usage

1. Place your GeoJSON file in the project directory
2. Modify the script to point to your GeoJSON file:
   ```python
   # Replace with your file path
   gdf = gpd.read_file("your_file.geojson")
   ```
3. Run the script:
   ```bash
   python main.py
   ```

## How It Works

The conversion process follows these steps:

1. Loads a GeoJSON file into a GeoDataFrame
2. Explodes any MultiLineStrings into individual LineStrings
3. Extracts start and end coordinates from each line geometry
4. Creates unique nodes for each coordinate
5. Creates a GeoDataFrame for nodes with OSMnx attributes
6. Maps coordinates to node IDs using a lookup dictionary
7. Assigns start and end node IDs to each edge
8. Sets the MultiIndex for edges as required by OSMnx
9. Removes duplicate edges
10. Creates a graph from the nodes and edges GeoDataFrames
11. Calculates and adds edge lengths to the graph

## GeoJSON File Format

Your GeoJSON file must contain line geometries in the form of LineStrings or MultiLineStrings. Here's a simplified example:

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "id": "1",
        "name": "Main Street"
      },
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [-73.989, 40.733],
          [-73.991, 40.734]
        ]
      }
    }
  ]
}
```
