import time
import zmq
import socket

class LockerServer():

  def __init__(self, url="tcp://*:7777"):

    NODES_WITH_GPUS = [17,18,19,20,21]
    N_GPUS_PER_NODE = 4
    GPU_NODES       = ["ada{0}".format(x) for x in NODES_WITH_GPUS]

    # This dictionary keeps track of GPU usage
    gpus = {}
    for i in GPU_NODES:
      gpus[i] = {}
      gpus[i]["free"] = range( N_GPUS_PER_NODE )
      gpus[i]["free"].reverse()

    cnt    = zmq.Context()
    sck    = cnt.socket(zmq.REP)
    sck.bind( url )

    # Always listening
    while True:
      msg = sck.recv()

      cmd, client_id, job_id = msg.split(' ')

      if not client_id in GPU_NODES:
        sck.send("-1")
        continue

      if cmd == "REQUEST":
        print("GPU requested on {0}".format(client_id))
        free_gpus = gpus[ client_id ]["free"]
        if not free_gpus:
          print("{1}:{0} requested a GPU but there are none available".format(job_id, client_id))
          sck.send("-1")
        else:
          gpu_id = free_gpus.pop()
          print("Giving GPU {0} to {2}:{1}".format(gpu_id, job_id, client_id))
          gpus[ client_id ][job_id] = gpu_id
          sck.send("{0}".format(gpu_id))

      elif cmd == "RELEASE":
        print("{1}:{0} is returning its GPU".format(job_id, client_id))
        print( client_id, gpus[client_id] )

        if not job_id in gpus[client_id].keys():
          print("No GPU assigned to {1}:{0} was found".format(job_id, client_id))
          sck.send("-1")
          continue

        gpu_id = gpus[client_id][ job_id ]
        del gpus[ client_id ][ job_id ]
        gpus[ client_id ]["free"].append(gpu_id)
        print("GPU returned successfully")

        sck.send("-1") # Just to acknowledge

      else:
        print("There was an unrecognized request: %s" % cmd)

class LockerClient():

  SERVER_URL = "tcp://ada:7777"

  def __init__(self, job_id, url=SERVER_URL):
    cnt = zmq.Context()
    self.sck = cnt.socket(zmq.REQ)
    self.sck.connect(url)
    self.job_id = job_id

  def request_gpu(self):
    self.sck.send( "REQUEST {0} {1}".format(socket.gethostname(), self.job_id))
    gpu_id = int(self.sck.recv())
    return gpu_id

  def release_gpu(self):
    self.sck.send( "RELEASE {0} {1}".format(socket.gethostname(), self.job_id) )
    gpu_id = int(self.sck.recv())
    return gpu_id
