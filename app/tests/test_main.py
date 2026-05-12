import json
import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from main import validate_geojson

def test_valid_feature_collection():
    data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [34.78, 32.08]},
                "properties": {"pipe_id": "P-001"}
            }
        ]
    }
    validate_geojson(data)

def test_missing_type_raises():
    with pytest.raises(ValueError):
        validate_geojson({"features": []})

def test_invalid_type_raises():
    with pytest.raises(ValueError):
        validate_geojson({"type": "InvalidType"})

def test_feature_collection_missing_features():
    with pytest.raises(ValueError):
        validate_geojson({"type": "FeatureCollection"})
