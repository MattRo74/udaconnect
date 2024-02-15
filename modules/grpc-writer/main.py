import time
from concurrent import futures
from __future__ import annotations
from models import Location, Person

import os
import grpc
import udaconnect_pb2
import udaconnect_pb2_grpc

from concurrent import futures
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from geoalchemy2.functions import ST_Point

DB_USER = os.environ["DB_USERNAME"]
DB_PW= os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]


class UdaconnectServicer(udaconnect_pb2_grpc.UdaconnectServiceServicer):
    def Create_Location(self, request, context):

        new_person = Location()
        new_person.person_id = request.person_id
        new_person.coordinate = ST_Point(request.latitude, request.longitude)
        new_person.creation_time = request.creation_time
        db_con_string = f"postgresql://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        db = create_engine(db_con_string)
        Session = sessionmaker(bind=db)
        session = Session()
        session.add(new_person)
        session.commit()
        location_value = {
            "person_id": request.person_id,
            "creation_time": request.creation_time,
            "longitute": request.longitute,
            "latitude": request.latitude
        }
        print(location_value)
        return udaconnect_pb2.UdaconnectMessage(**location_value)

    def Create_Person(self, request, context):

        new_person = Person()
        new_person.first_name = request.first_name
        new_person.last_name = request.last_name,
        new_person.company_name = request.company_name
        db_con_string = f"postgresql://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        db = create_engine(db_con_string)
        Session = sessionmaker(bind=db)
        session = Session()
        session.add(new_person)
        session.commit()
        person_value = {
            "first_name": request.first_name,
            "last_name": request.last_name,
            "company_name": request.company_name
        }
        print(person_value)
        return udaconnect_pb2.UdaconnectMessage(**person_value)
    

# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
udaconnect_pb2_grpc.add_UdaconnectServiceServicer_to_server(UdaconnectServicer(), server)


print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)