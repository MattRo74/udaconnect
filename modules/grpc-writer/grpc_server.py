import time
from concurrent import futures

import grpc
import udaconnect_pb2
import udaconnect_pb2_grpc


class LocationService(udaconnect_pb2_grpc.UdaconnectServiceServicer):
    def create_location(self, request, context):
        print("Received a message!")
        request_value = {
            "person_id": request.person_id,
            "latitude": request.latitude,
            "longitude": request.longitude,
            "creation_time": request.creation_time
        }
        print(request_value)
        return udaconnect_pb2.LocationMessage(**request_value)

# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
udaconnect_pb2_grpc.add_UdaconnectServiceServicer_to_server(LocationService(), server)


print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)