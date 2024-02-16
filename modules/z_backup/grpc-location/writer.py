import grpc
import location_pb2
import location_pb2_grpc

"""
Sample implementation of a writer that can be used to write message to gRPC
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:5005")
stub    = location_pb2_grpc.LocationServiceStub(channel)

## Update this with descired payload

location = location_pb2.LocationMessage(
    person_id=9,
    longitude="7.014793",
    latitude="51.451355",
    creation_time="2024-02-16T14:56:23"
)

response = stub.Create(location)
