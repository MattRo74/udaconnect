import grpc
import udaconnect_pb2
import udaconnect_pb2_grpc
from kafka import KafkaConsumer
import json
import logging

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("kafka-consumer")

TOPIC_NAME = 'persons'
KAFKA_SERVER = 'kafka:9092'

consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=[KAFKA_SERVER], value_deserializer=lambda m: json.dumps(m.decode('utf-8')))

#print("Sending sample payload...")

channel = grpc.insecure_channel("udaconnect-grpc_writer:5005")
stub = udaconnect_pb2_grpc.UdaconnectServiceStub(channel)

for queue in consumer:
    json_message = eval(json.loads((queue.value)))

    if "person_id" in json_message:
        location = udaconnect_pb2.LocationMessage(
            person_id = json_message["person_id"],
            creation_time = json_message["creation_time"],
            longitude = json_message["longitude"],
            latitude = json_message["latitude"]
        )
        stub.create_location(location)
    else:
        person = udaconnect_pb2.PersonMessage(
            first_name = json_message["first_name"],
            last_name = json_message["last_name"],
            company_name = json_message["company_name"]
        )
        stub.create_person(person)