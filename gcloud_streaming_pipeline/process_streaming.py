import logging
import argparse
import json

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io.gcp.internal.clients import bigquery


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input-topic",
        dest="input_topic",
        required=True,
        help="Google PubSub topic name to read.",
    )
    parser.add_argument(
        "--output-table",
        dest="output_table",
        required=True,
        help="Google BigQuery table to write results to.",
    )
    parser.add_argument(
        "--bigquery-batch-size",
        dest="bigquery_batch_size",
        default=1,
        help="Google BigQuery batch size to ingest",
    )
    parser.add_argument(
        "--v",
        dest="v",
        type=int,
        choices=[0, 10, 20, 30, 40, 50],
        default=20,
        help="Increase output verbosity",
    )
    return parser


def define_table_schema():
    table_schema = bigquery.TableSchema()

    timestamp_column_schema = bigquery.TableFieldSchema()
    timestamp_column_schema.name = "timestamp"
    timestamp_column_schema.type = "timestamp"
    timestamp_column_schema.mode = "nullable"

    timestampo_column_schema = bigquery.TableFieldSchema()
    timestampo_column_schema.name = "timestampo"
    timestampo_column_schema.type = "timestamp"
    timestampo_column_schema.mode = "nullable"

    action_column_schema = bigquery.TableFieldSchema()
    action_column_schema.name = "action"
    action_column_schema.type = "string"
    action_column_schema.mode = "nullable"

    uid_column_schema = bigquery.TableFieldSchema()
    uid_column_schema.name = "uid"
    uid_column_schema.type = "string"
    uid_column_schema.mode = "nullable"

    source_column_schema = bigquery.TableFieldSchema()
    source_column_schema.name = "source"
    source_column_schema.type = "record"
    source_column_schema.mode = "nullable"
    source_column_schema.fields.append(timestamp_column_schema)
    source_column_schema.fields.append(timestampo_column_schema)
    source_column_schema.fields.append(uid_column_schema)
    source_column_schema.fields.append(action_column_schema)

    table_schema.fields.append(source_column_schema)

    return table_schema


class ProcessRecord(beam.DoFn):
    def process(self, element, *args, **kwargs):
        logging.info("incoming element: {}".format(element))
        data = json.loads(element)
        record = {"source": data}
        return [record]


def run():
    parser = create_parser()
    known_args, pipeline_args = parser.parse_known_args()

    logging.basicConfig(
        level=known_args.v,
        format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
    )

    p = beam.Pipeline(options=PipelineOptions())
    records = p | "ReadFromPubSub" >> beam.io.ReadFromPubSub(
        topic=known_args.input_topic
    ).with_output_types(bytes)
    decoded_records = records | "DecodeRecords" >> beam.Map(lambda x: x.decode("utf-8"))
    processed_records = decoded_records | "ProcessRecords" >> beam.ParDo(
        ProcessRecord()
    )
    processed_records | "WriteToBigQuery" >> beam.io.WriteToBigQuery(
        known_args.output_table,
        schema=define_table_schema(),
        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
        batch_size=known_args.bigquery_batch_size,
    )

    result = p.run()
    result.wait_until_finish()


if __name__ == "__main__":
    run()
