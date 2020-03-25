from turf.helpers import (
    Feature,
    Point,
    LineString,
    MultiPoint,
    MultiLineString,
    Polygon,
    MultiPolygon,
    FeatureCollection,
    get_input_dimensions)
from turf.utils.exceptions import InvalidInput
from turf.utils.error_codes import error_code_messages

allowed_types_points = ["Point", "MultiPoint"]
allowed_types_line_string_polygons = [
    "LineString",
    "MultiLineString",
    "Polygon",
    "MultiPolygon",
]


def get_coords_from_geometry(geometry):
    if geometry.get("type", None) in allowed_types_line_string_polygons:
        return geometry.get("coordinates", [])
    else:
        raise InvalidInput(error_code_messages["InvalidLineOrPolygon"])


def get_coords_from_features(features):
    if isinstance(features, (FeatureCollection, dict)):
        if features.get("type") == "FeatureCollection":
            return list(
                map(
                    lambda feature: get_coords_from_geometry(
                        feature.get("geometry", {})
                    ),
                    features.get("features", []),
                )
            )

    if isinstance(features, (Feature, dict)):
        if features.get("type") == "Feature":
            return get_coords_from_geometry(features.get("geometry", {}))

    if isinstance(features, (LineString, Polygon, MultiLineString, MultiPolygon, dict)):
        return get_coords_from_geometry(features)

    if isinstance(features, list) and all(
        isinstance(sub_list, list) for sub_list in features
    ):
        return features

    raise InvalidInput(error_code_messages["InvalidLineOrPolygon"])


def get_coord(coord):
    if get_input_dimensions(coord) == 1 and len(coord) == 2:
        return coord

    elif (
        isinstance(coord, Feature)
        and getattr(coord, "geometry", None)
        and getattr(coord.geometry, "type", None) in allowed_types_points
    ):
        return coord.geometry.coordinates

    elif isinstance(coord, (Point, MultiPoint)):
        return coord.coordinates

    elif isinstance(coord, dict) and coord.get("type", None) == "Feature":
        if (
            "geometry" in coord
            and coord["geometry"].get("type", None) in allowed_types_points
            and "coordinates" in coord["geometry"]
        ):
            return coord["geometry"]["coordinates"]

    elif isinstance(coord, dict) and coord.get("type", None) in allowed_types_points:
        if "coordinates" in coord:
            return coord["coordinates"]

    raise InvalidInput(error_code_messages["InvalidPoint"])