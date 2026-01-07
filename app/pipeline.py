from pyspark.sql import SparkSession
from pyspark.sql.functions import col, window, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, TimestampType
from delta import *

# Configuração do Spark com Delta Lake
builder = SparkSession.builder.appName("StreamingToDelta") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

# 1. Definir o Schema dos logs
schema = StructType([
    StructField("user_id", StringType(), True),
    StructField("event_type", StringType(), True),
    StructField("page_id", StringType(), True),
    StructField("timestamp", TimestampType(), True),
    StructField("ip_address", StringType(), True)
])

# 2. Ler o Stream (Monitorando a pasta data/input)
df_stream = spark.readStream \
    .schema(schema) \
    .json("data/input")

# 3. Transformação: Agregação por Janela (Cliques por minuto)
df_aggregated = df_stream \
    .withWatermark("timestamp", "2 minutes") \
    .groupBy(
        window(col("timestamp"), "1 minute"),
        col("event_type")
    ).count()

# 4. Escrita em Delta Lake (Append para logs e Overwrite/Complete para agregados)
query = df_stream.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "spark-checkpoints/raw_events") \
    .start("data/delta/raw_events")

query_agg = df_aggregated.writeStream \
    .format("delta") \
    .outputMode("complete") \
    .option("checkpointLocation", "spark-checkpoints/agg_events") \
    .start("data/delta/agg_events")

print("⚡ Pipeline em execução e gravando em Delta Lake...")
spark.streams.awaitAnyTermination()
