import os
import json
import logging
import boto3
import psycopg2
import geopandas as gpd
from flask import Flask, jsonify
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
logger = logging.getLogger(__name__)

# ── Config from environment variables (no hardcoding) ─────────
DB_HOST     = os.getenv("DB_HOST", "localhost")
DB_PORT     = os.getenv("DB_PORT", "5432")
DB_NAME     = os.getenv("DB_NAME", "asterra_db")
DB_USER     = os.getenv("DB_USER", "asterra_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "localstack_pass")

S3_ENDPOINT = os.getenv("S3_ENDPOINT", "http://localhost:4566")
AWS_REGION  = os.getenv("AWS_REGION", "us-east-1")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=S3_ENDPOINT,
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name=AWS_REGION
    )

def create_table_if_not_exists(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS geojson_features (
                id SERIAL PRIMARY KEY,
                feature_type VARCHAR(50),
                properties JSONB,
                geometry GEOMETRY,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)
        conn.commit()
    logger.info("Table ready")

def validate_geojson(data):
    if "type" not in data:
        raise ValueError("Missing 'type' field")
    if data["type"] not in ["Feature", "FeatureCollection"]:
        raise ValueError(f"Invalid type: {data['type']}")
    if "features" not in data and data["type"] == "FeatureCollection":
        raise ValueError("FeatureCollection missing 'features'")
    logger.info("GeoJSON validation passed")

def process_geojson(bucket, key):
    logger.info(f"Processing s3://{bucket}/{key}")

    # 1. Download file from S3
    s3 = get_s3_client()
    response = s3.get_object(Bucket=bucket, Key=key)
    content = response["Body"].read()
    data = json.loads(content)

    # 2. Validate
    validate_geojson(data)

    # 3. Load into GeoDataFrame
    gdf = gpd.read_file(BytesIO(content))
    logger.info(f"Loaded {len(gdf)} features")

    # 4. Insert into RDS
    conn = get_db_connection()
    create_table_if_not_exists(conn)

    with conn.cursor() as cur:
        for _, row in gdf.iterrows():
            cur.execute("""
                INSERT INTO geojson_features (feature_type, properties, geometry)
                VALUES (%s, %s, ST_GeomFromText(%s, 4326))
            """, (
                row.geometry.geom_type,
                json.dumps(row.drop("geometry").to_dict()),
                row.geometry.wkt
            ))
        conn.commit()

    logger.info(f"Inserted {len(gdf)} features into database")
    conn.close()
    return len(gdf)

# ── Routes ────────────────────────────────────────────────────
@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/process/<bucket>/<path:key>", methods=["POST"])
def process(bucket, key):
    try:
        count = process_geojson(bucket, key)
        return jsonify({"status": "success", "features_inserted": count})
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        logger.error(f"Processing error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
