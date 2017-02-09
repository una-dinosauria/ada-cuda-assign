
"""Sends jobs with all combinations of certain parameters"""

import os
import itertools

fname   = "job3dpred.pbs"

def submit_jobs( fields, values ):
  """
  Function that submits jobs with certain parameters

  Args.
    fields. List of strings with parameters to pass.
    values. Tuple of lists. Each list has values for each field.

  Returns
    Nothing. The jobs will be sent to sched.

  """

  # === Argument examples ===
  # fields = ["learning_rate", "seq_length_out", "loss_velocities"]
  #
  # learning_rate   = [0.2, 0.1, .05, 0.01]
  # seq_length_out  = [10, 25]
  # loss_velocities = [1.0, 0.5]
  # values = ( learning_rate, seq_length_out, loss_velocities )

  configs = []
  for element in itertools.product( *values ):
    configs.append( element )

  for config in configs:

    # print config
    line = "python predict_3dpose.py "

    for i in range( len(config) ):
      if isinstance( config[i], bool ):
        if config[i]:
          line = line + "--{0} ".format( fields[i] )
        else:
          pass # do not add the flag

      else:
        line = line + "--{0} {1} ".format( fields[i], config[i] )


    line = line + "\n"
    print( line )

    # Open the submission file
    with open(fname, "r") as f:
      data = f.readlines()

    # Change the arguments line
    data[-5] = line

    # Write back
    with open(fname, "w") as f:
      f.writelines( data )

    # Send to the cluster
    bashCommand = "qsub {0}".format( fname )
    print( bashCommand )
    os.system( bashCommand )

def linear_experiment():


  actions = ["Directions","Discussion","Eating","Greeting",
        "Phoning","Photo","Posing","Purchases",
        "Sitting","SittingDown","Smoking","Waiting",
        "WalkDog","Walking","WalkTogether"]
  # actions = ["Directions"]
  # actions = ["Directions","Discussion","Eating","Greeting",
  #            "Phoning","Photo","Posing","Purchases"]
  actions.reverse()

  # (1) action-specific, lsmt-3lr, no noise, supervised
  fields = []
  values = ()

  fields.append("action")
  values = values + (actions,)

  fields.append("epochs")
  values = values + ([200],)

  fields.append("kinematic_box")
  #values = values + ([False, True],)
  values = values + ([False],)

  fields.append("linear_size")
  values = values + ([1024],)

  fields.append("residual")
  #values = values + ([False, True],)
  values = values + ([False],)

  fields.append("num_layers")
  #values = values + ([1, 2, 4],)
  values = values + ([1],)

  fields.append("dropout")
  #values = values + ([1, 2, 4],)
  values = values + ([1],)

  fields.append("learning_rate")
  # values = values + ([1e-3, 1e-4, 1e-5],)
  values = values + ([1e-4],)

  submit_jobs(fields, values)


def main():
  # First experiment
  linear_experiment()

  # Second experiment
  # lstm3lr_residual_self_fed_experiment()

if __name__ == "__main__":
  main()
