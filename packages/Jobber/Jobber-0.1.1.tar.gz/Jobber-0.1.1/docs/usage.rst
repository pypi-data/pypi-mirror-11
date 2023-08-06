========
Usage
========

Preparation
^^^^^^^^^^^

After installation start the Jobber daemon:

.. code-block:: bash

    $ nohup jobber_server > jobber.log 2>&1 &

.. note::

    If you installed Jobber as user you might not have an access to the jobber_server. By
    default the binary location is $HOME/.local/bin and you have to export it in bash:

    .. code-block:: python

        $ export PATH="$HOME/.local/bin:$PATH"


    or add this statement to .bashrc file.

    jobber_server produces ~/.jobber/jobber.pid file that indicates whether the Jobber is already
    running. If the file exists one cannot start new instance of the jobber_server. This file is
    not clean when jobber_server is killed - only when it was stopped with stop command. Thus,
    after some crash one have to remove this file in order to start jobber_server again.


This will automatically create a ~/.jobber and ~/jobber/log directories and
it will put there config.py and executers.py files. Look at them and adjust
according to your needs.

This should create a jobber.sqlite file next to config.py where jobs will be stored (all in ~/.jobber).
Now you can create pipelines that will be managed with a python script.


To stop the jobber daemon, run following command:

.. code-block:: bash

    $ jobber_server -stop

You can watch and control your jobs and pipelines present in the database using simple we interface.
To launch it type:

.. code-block:: bash

    $ jobber_web

or

.. code-block:: bash

    $ jobber_web --ip Your.IP.addres --port YourPort

Basic usage
^^^^^^^^^^^

Here is the minimal working code for the pipeline composed of only one command that does echo:

.. code-block:: python

    from Jobber.JobClient import Jobber

    jobber = Jobber()
    jobId = jobber.job("echo 23", {
       'name': "Echo",
           'description': "echoes 23"

    })
    jobber.launch(jobId)

Creating pipelines
^^^^^^^^^^^^^^^^^^

There are 2 different concepts that we use, groups and jobs. A job is basically a command that we
want to execute, and a group is a special job that contains multiple jobs. To start a group, we do following:

.. code-block:: python

    jobber = Jobber()

    jobberId = jobber.startGroup({

        'name': 'Group',

        'description': 'my group'

    })

    ...
    jobber.endGroup()

The "startGroup" function starts a group and accepts a dictionary containing the settings for the group.
You can set following settings for a job (all settings are optional):

+----------------+---------------------------------------------------------------------------------------------------------------------------------------------+
| Name           | Description                                                                                                                                 |
+================+=============================================================================================================================================+
| name           | Name of job (default "anonymous")                                                                                                           |
+----------------+---------------------------------------------------------------------------------------------------------------------------------------------+
| dependencies   |    Description of job                                                                                                                       |
+----------------+---------------------------------------------------------------------------------------------------------------------------------------------+
| options        |    Options we can set for this Job. If this job is a group, the members of this job will inherit this options. An option is an array,       |
|                |    where the first argument is the type of the option, the second argument the option value. The option is always interpreted as an         |
|                |    "drmaa" option, with the exception of following options:                                                                                 |
|                |     * module: Those are interpreted as to which module to load for this job using the bc2 module system.                                    |
|                |     * cores: The nr of cores to use (e.g. 2)                                                                                                |
|                |     * runtime: The max runtime of the job (e.g. 24:00:00)                                                                                   |
|                |     * memory: Max memory the job will user (e.g. 16000M)                                                                                    |
+----------------+---------------------------------------------------------------------------------------------------------------------------------------------+
| executer       |                                   "drmaa" for jobs executed in the cluster (the default), or, "local" for jobs executed locally.            |
+----------------+---------------------------------------------------------------------------------------------------------------------------------------------+
| uniqueId       |  A unique identifier for this job. Setting this will prevent other jobs with the same unique identifier to be created.                      |
|                |  The unique identifier will only prevent duplicate jobs that are in the same group (or top level jobs). A job with the same unique id that  |
|                |  A job with the same unique id that is in a different group than another job is not considered a duplication and will still be created.     |
|                |  You can also pass the value True instead of a string. Then, the command of the job will be taken to compare jobs if they are unique.       |
+----------------+---------------------------------------------------------------------------------------------------------------------------------------------+
| maxNrOfJobs    |  The maximal nr of jobs that can be run in parallel and have the same name. You can only set this for top level job (jobs that are not      |
|                |  a child of another job).                                                                                                                   |
+----------------+---------------------------------------------------------------------------------------------------------------------------------------------+

The function also returns and identifier for this job. You can use this identifier to define dependencies.
For each "startGroup", you also need to call "endGroup". Each job created between "startGroup" and "endGroup" will be a member of this group.

To create a normal job, you can do following:

.. code-block:: python

    job1 = jobber.job("echo 23", {

        'name': "Echo",

        'description': "echoes 23",

        'options': [

             ['module', 'SAMtools'],
             ['l', "runtime=24:00:00"]
    ]

    })

A job is defined using the "job" function. The first argument is the command of the job.
This can be any command that you can also define using the "os.system" call. The second argument are the job settings.
A job has the same settings like a group. Here, we defined 2 options. The "module" options will load the "SAMtools"
module for this job. The "l" option is a drmaa option (because all options except "module" are drmaa options),
which sets the maximal runtime of this job.

After creating all your jobs in your pipeline, you'll need to launch your pipeline using the "launch" command.
The launch command requires the job id to be launched. Here's a complete example using all discussed concepts
(Assuming the PYTHONPATH is pointing to the jobber folder correctly):


.. code-block:: python

    from jobber.JobClient import Jobber
     
      
     
    jobber = Jobber()
     
      
     
    #First we declare the whole pipeline in a group
     
    #Unique id makes sure that only 1 group with this id can exist. Trying to create a group with the same unique id will not create the group but reuse the existing one all job creation will be ignored
     
    pipelineId = jobber.startGroup({
     
        'name': "Pipeline",
     
        'description': "Description of pipeline",
     
        "uniqueId": 'pipeline x',
     
        'options': [
     
             ['module', 'Python'],
     
             ['module', 'Perl']
     
        ]
     
    })
     
      
     
      
     
    #Jobs inside a group inherit all options of all parent groups, so no need to define module Python and Perl
     
    job1 = jobber.job("echo 23", {
     
        'name': "Echo",
     
        'description': "echoes 23",
     
        'options': [
     
             ['module', 'SAMtools']
     
        ]
     
    })
     
      
     
    #Groups can ve nested indefinetely
     
    group2 = jobber.startGroup({
     
        'name': 'Group2',
     
        'description': 'Bla'
     
    })
     
      
     
    jobber.job("echo 25", {
     
        "name": "Echo25",
     
        "description": "Job inside Group2"
     
    })
     
      
     
    jobber.endGroup()
     
      
     
    #Jobs can depend on jobs or groups
     
    job3 = jobber.job("echo 3", {
     
         'name': "Job 2",
     
         "description": "depends on job1 and group 2",
     
         'dependencies': [job1, group2]
     
    })
     
      
     
    jobber.endGroup()
     
      
     
    #We launch the pipeline. As long as we don't call the function, the pipeline remains inactive.
     
    jobber.launch(pipelineId)


Watching the jobs in database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can see the jobs by using the web interface or by command line as described here.

To see how your jobs are progressing, you can login into the database and query the "t_jobs" table
(if you use SQLite):

.. code-block:: bash

    $ sqlite3 ~/.jobber/jobber.sqlite
    >>> select * from t_jobs;

The table contains following columns:

+--------------------+---------------------------------------------------------------------------------------------------------+
| Column             |                     Description                                                                         |
+====================+=========================================================================================================+
| id                 | The id of this job                                                                                      |
+--------------------+---------------------------------------------------------------------------------------------------------+
| parent_id          | The group this job is member of, or null if none                                                        |
+--------------------+---------------------------------------------------------------------------------------------------------+
| name               | The name of this job                                                                                    |
+--------------------+---------------------------------------------------------------------------------------------------------+
| description        | The description of this job                                                                             |
+--------------------+---------------------------------------------------------------------------------------------------------+
| drmaa_id           | The id this job has from drmaa. U can use this id to identify the job with qstat.                       |
+--------------------+---------------------------------------------------------------------------------------------------------+
| status             | RUNNING, FAILED, FINISHED or CANCELLED                                                                  |
+--------------------+---------------------------------------------------------------------------------------------------------+
| job_command        | The command of the job                                                                                  |
+--------------------+---------------------------------------------------------------------------------------------------------+
| error              | The error message in case an error happened                                                             |
+--------------------+---------------------------------------------------------------------------------------------------------+
| is_unique          | If the job is unique                                                                                    |
+--------------------+---------------------------------------------------------------------------------------------------------+
| unique_key         | The unique id of the job                                                                                |
+--------------------+---------------------------------------------------------------------------------------------------------+
| is_group_job       | If this is a group job                                                                                  |
+--------------------+---------------------------------------------------------------------------------------------------------+
| max_nr_of_restarts | Max nr of restarts before giving up and setting job to FAILED status                                    |
+--------------------+---------------------------------------------------------------------------------------------------------+
| current_run        | The current run number. Starts at 1. Every time the job is restarted, this number is incremented by 1.  |
+--------------------+---------------------------------------------------------------------------------------------------------+
| max_parallel_nr    | Maximal nr of jobs that can be run in parallel. Only applies to top level jobs.                         |
+--------------------+---------------------------------------------------------------------------------------------------------+

The table "t_job_options" contains the options for each job.

The table "t_job_dependencies" contains the dependencies defined for each job.

For every job, a folder is created where the log files of this job are stored.
The folders per default are created in the "log/jobs" folder that is created relative
to the jobber root folder. For example, for a job with id 1 and current_run 1, following
folder will be created:

    $ ~/.jobber/log/jobs/1/1

In the folder, you'll find an "out" file with the stdout and "err" file with the stderr.
When the job is restarted, the current_run will become 2, and a new folder will be created
for the second run of job 1:

    $ ~/.jobber/log/jobs/1/2



Controlling jobs in command line
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can control the execution by using the web interface or by command line.
You can send commands to jobber by using the "-command" argument. Following commands are available:

Delete
------

To delete a job, use following arguments:

.. code-block:: bash

    $ jobber_server -command delete -jobId 1

The "-jobId" tells what job you want to delete. Deleting a job will remove all entries of this job in
the database and also remove all log files in the log folder, and kill the job if it is currently running.
If the job is a group, all its members will be also deleted.

Status
------

You can change the status of a job using the "status" command. You can use following options:


+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Option    |      Description                                                                                                                                               |
+===========+================================================================================================================================================================+
| jobId     |      The job id to change the status                                                                                                                           |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| status    |    The status to change to. You can use following status:                                                                                                      |
|           |     * FINISHED: Sets the job to finished state.                                                                                                                |
|           |     * CANCELLED: Set's the job to cancelled state. If the job is currently running, it will be killed. The job will not be executed having this status.        |
|           |     * IDLE: Sets the job to IDLE state. If the job is currently running, it will be killed. The job will be executed when all its dependencies are fulfilled.  |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| recursive |    Set this option if you want to set the status to all jobs that depend directly or indirectly to this job.                                                   |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+

For example, to restart a job, you would do following:

.. code-block:: bash

    $ jobber_server -command status -status IDLE -jobId 6

If you want to restart a  job and all job's that depend on this job, you can add the recursive argument:

.. code-block:: bash

    $ jobber_server -command status -status IDLE -jobId 6 -recursive

Configuration
^^^^^^^^^^^^^

The ~/.jobber/config.py contains the configuration for jobber.
It is already configured to use sqlite and write log files into a ~/.jobber/log directory.
The file that must contain following properties:


+-----------------+-----------------------------------------------------------------------+
| Property        |  Description                                                          |
+=================+=======================================================================+
| sqlite_path     | If you're using a sqlite database, this is the path to the database   |
+-----------------+-----------------------------------------------------------------------+
| db_host         | The host of the mysql database                                        |
+-----------------+-----------------------------------------------------------------------+
| db_name         | The name of the mysql database                                        |
+-----------------+-----------------------------------------------------------------------+
| db_password     | The password of the mysql database                                    |
+-----------------+-----------------------------------------------------------------------+
| db_user         | The username of the mysql database                                    |
+-----------------+-----------------------------------------------------------------------+
| defaultExecuter | The default executer to use if none is specified for a job            |
+-----------------+-----------------------------------------------------------------------+


Executers
---------

The file "~/.jobber/executers.py" contains additional user-defined executers that can be used by jobber.
Each Executer is a class that will be instantiated by the system and the jobs will be sent to.
The standard configuration contains the 2 executers "local" and "drmaa". If you want to run jobber
locally on your computer, remove the "drmaa" executer from the dictionary and from the import and change the
defaultExecuter in the config.py file to "local".
