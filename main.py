"""
GeoJSON to Graph Converter
    This script converts a GeoJSON file containing line geometries into a network graph.

GeoJSON File Format:
    Must Contain Point Geometry in the form of LineStrings or MultiLineStrings.
    (Check the Sample GeoJSON file for structure)

Summary:
    1. Load a GeoJSON file into a GeoDataFrame.
    2. Explode any MultiLineStrings into individual LineStrings.
    3. Extract start and end coordinates from each line geometry.
    4. Create unique nodes (and Node IDs) for each coordinate.
    5. Create a GeoDataFrame for nodes with OSMnx attributes.
    6. Create a lookup dictionary to map coordinates to node IDs.
    7. Assign start and end node IDs to each edge.
    8. Set the MultiIndex for edges as required by OSMnx.
    9. Remove duplicate edges.
    10. Create a graph from the nodes and edges GeoDataFrames.
    11. Calculate and add edge lengths to the graph.

Usage:
    Replace '<file_name>' with the actual GeoJSON file path before running.
"""

import osmnx as ox
import geopandas as gpd
from shapely.geometry import Point

# Load the GeoJSON file into a GeoDataFrame
gdf = gpd.read_file("<file_name>.geojson")

# Explode any multi-geometries into individual line segments
gdf_edges = gdf.explode(ignore_index=True).reset_index(drop=True)

# Extract all endpoint coordinates from each line geometry
coords = []
for geom in gdf_edges.geometry:
    coords.extend([geom.coords[0], geom.coords[-1]])  # First and last points of each line

# Create unique nodes from the coordinates
unique_coords = list(set(coords))
nodes = [Point(coord) for coord in unique_coords]

# Create a GeoDataFrame for nodes with required OSMnx attributes
gdf_nodes = gpd.GeoDataFrame(geometry=nodes, crs=gdf.crs)
gdf_nodes["x"] = gdf_nodes.geometry.x
gdf_nodes["y"] = gdf_nodes.geometry.y
gdf_nodes["osmid"] = range(len(gdf_nodes))  # Generate sequential IDs for each node
gdf_nodes = gdf_nodes.set_index("osmid")

# Create a lookup dictionary to map coordinates to node IDs
coord_to_osmid = {
    (row.geometry.x, row.geometry.y): osmid
    for osmid, row in gdf_nodes.iterrows()
}

# Assign start node (u) and end node (v) IDs to each edge
gdf_edges["u"] = [
    coord_to_osmid[(geom.coords[0][0], geom.coords[0][1])]  # Start point node ID
    for geom in gdf_edges.geometry
]
gdf_edges["v"] = [
    coord_to_osmid[(geom.coords[-1][0], geom.coords[-1][1])]  # End point node ID
    for geom in gdf_edges.geometry
]
gdf_edges["key"] = 0  # Default key for parallel edges (required by OSMnx)

# Set the MultiIndex for edges as required by OSMnx
gdf_edges = gdf_edges.set_index(["u", "v", "key"])

# Remove any duplicate edges that might have been created
gdf_edges = gdf_edges[~gdf_edges.index.duplicated()]

# Create a graph from the nodes and edges GeoDataFrames
G = ox.graph_from_gdfs(gdf_nodes, gdf_edges)

# Calculate and add edge lengths in meters to the graph
G = ox.distance.add_edge_lengths(G)