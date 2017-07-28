from zmqlocker import LockerClient
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--request", dest="request", action="store_true")
parser.add_argument("--release", dest="release", action="store_true")
parser.add_argument("--jobid", help="the id of the job requesting the GPU")
args = parser.parse_args()

if args.request and args.release:
  raise(ValueError, "both request and release can't be asked at the same time")

# Ada passes something like '5580.ada.cs.ubc.ca' or '5580[1].ada.cs.ubc.ca'
jid = args.jobid.split('.')[0]
locker_cli = LockerClient( jid )

if args.request:
  print "export CUDA_VISIBLE_DEVICES={0}".format( locker_cli.request_gpu() )
elif args.release:
  print "echo {0}".format( locker_cli.release_gpu() )
else:
  raise(ValueError, "must specify request or release")
