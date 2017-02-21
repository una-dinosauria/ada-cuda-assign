# cuda-assigner

A simple, [pyzmq](https://github.com/zeromq/pyzmq)-based server and client that perform GPU assignments on the ada cluster at UBC.

### Before everything

Make sure you are in the `nvusers` group (you can email the helpdesk to be added), otherwise you will not even be able to see the GPUs.

### Server set up

Someone (usually me) should be running `./run_server.py` on the head node, `ada.cs`.

### Client

If you are running a job on ada that wants to use GPUs, you should configure your `.pbs` script so that it asks for a GPU from the server, and releases it when the job is done.

Here is an example of what your `.pbs` file might look like:

```bash
#!/bin/sh

#PBS -l walltime=10:00:00
#PBS -l mem=8000mb
#PBS -l gpus=1
#PBS -W x=GRES:gpu at 1
#PBS -q nvidia
#PBS -e jobfiles/
#PBS -o jobfiles/

cd $PBS_O_WORKDIR
echo "Current working directory is `pwd`"

echo "Starting run at: `date`"

# Ask the server for a GPU and set the CUDA_VISIBLE_DEVICES variable
eval $(python run_client.py --request --jobid $PBS_JOBID)

# Run your code that uses a GPU
python my_fancy_gpu_code.py --param1 donald --param2 trump

# Once the job is done, release the GPU that we took
eval $(python run_client.py --release --jobid $PBS_JOBID)

echo "Program finished with exit code $? at: `date`"
```

### TODOs

* Query GPU status on demand
* Add ability to assign multiple GPUs
* Manually release GPUs (in case a job crashes and does not release it)
* Better output visualization
