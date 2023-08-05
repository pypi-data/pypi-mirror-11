Relay Web UI:
![](/screenshot_relay.png?raw=true)
Mesos Web UI:
![](/screenshot_mesos.png?raw=true)


Relay.Mesos:  Run Relay and Mesos
==========

In short, Relay.Mesos runs Relay as a Mesos framework.  By combining
both of these tools, we can solve control loop problems that arise in
distributed systems.  An example problem Relay.Mesos might solve is to
spin up queue consumers to maintain or minimize a queue size.  You could also
use Relay.Mesos to set a target CPU usage over time for all instances of
a particular task running on your mesos cluster.

What is Relay?
----------
Relay is "a thermostat for distributed systems."  It is a tool that
attempts to make a metric timeseries as similar to a target
as possible, and it works like thermostat does for temperature.

[Details on Relay's Github page.](
https://github.com/sailthru/relay/blob/master/README.md)

What is Mesos?
----------
Apache Mesos is "a distributed systems kernel."  It pools resources from
networked machines and then provides a platform that executes code over
those resources.  It's basically a bin-packing scheduler and resource
manager that identifies which resources are available and then provides
ways to use those resources.

[Details on Mesos's landing page.](http://mesos.apache.org/)

[White paper about Mesos (this is good
reading)](http://mesos.berkeley.edu/mesos_tech_report.pdf)


What is Relay.Mesos?
----------
Relay.Mesos will iteratively ask Mesos to run tasks on the cluster.
These tasks will either eventually increase or eventually decrease some
measured metric.  Relay.Mesos will quickly learn how the metric changes
over time and tune its requests to Mesos so it can minimize the difference
between the metric and a desired target value for that metric.


Quickstart
==========

1. Install Docker
    - https://docs.docker.com/installation
    - (if on a mac, you may need boot2docker and don't forget to add env vars to your .profile)
    - (if on ubuntu, you may need 3.16 kernel or later)

1. Identify docker in /etc/hosts

        # I added this to my /etc/hosts file:
        #    192.168.59.103 localdocker
        # If you use boot2docker, this should work:
        # $ echo "$(boot2docker ip) localdocker" | sudo tee -a /etc/hosts

1. Run the demo script.
    - When you run this for the first time, docker may need to download a
      lot of the required images to get mesos running on your computer

            # ./bin/demo.sh     # run the demo


Background
==========

Relay.Mesos is made up of two primary components: a Mesos framework and
a Relay event loop.  Relay continuously requests that the mesos
framework run a number of tasks.  The framework receives resource
offers from mesos and, if the most recent Relay request can be fulfilled,
it will attempt to fulfill it by spinning up "warmer" or "cooler" tasks.
If Relay requests can't be fulfilled because
Mesos cluster is at capacity, then Relay will continue to ask to spin up
tasks, but nothing will happen.

If no mesos resource offers are available for a long time, Relay.Mesos
will become starved for resources.  This can result in Relay.Mesos
building up a history of error between the target and the metric.  If
Relay.Mesos has been starved for Mesos resources for a while, when
resources become available again, Relay might initially ask for too many
resources because it's learned that asking for a lot of tasks to spin up
results in very little or no difference in the metric.  In any case, it
will quickly re-learn the right thing to do.

In Relay.Mesos, as with Relay generally, there are 4 main components:
metric, target, warmer and cooler.

The ```metric``` and ```target``` are both python generator functions
(ie timeseries), that, when called, each yield a number.  The
```metric``` is a signal that we're monitoring and manipulating.  The
```target``` represents a desired value that Relay attempts to make the
```metric``` mirror as closely as possible.

The ```warmer``` and ```cooler``` are expected to (eventually) modify
the metric.  Executing a ```warmer``` will increase the metric.
Executing a ```cooler``` will decrease the metric.  In Relay.Mesos, the
```warmer``` and ```cooler``` are bash commands.  These may be executed in
your docker containers, if you wish.


Examples:
----------

(See QuickStart for a demo using Docker containers)

#### Autoscaling processes that run, complete, and then exit:

Relay.Mesos can ensure that the number of jobs running at any given
time is enough to consume a queue.

    Metric = queue size
    Target = 0
    Warmer = "./start-worker.sh"
    (Cooler would not be defined)

Relay.Mesos can schedule the number of consumers or servers running at a
particular time of day

    Metric = number of consumers
    Target = max_consumers * is_night  # this could work too: sin(time_of_day) * max_consumers
    Warmer = "./start-consumer.sh"
    (Cooler would not be defined)

Relay.Mesos can attempt to maintain a desired amount of cpu usage

    Metric = cpu_used - expected_cpu_used
    Target = 0
    Cooler = "run a bash command that uses the cpu"
    (Warmer not defined)

#### Autoscaling long-running processes that never die.

Relay.Mesos can auto-scale the number of web-servers running:

    Metric = desired number of web servers (as function of current load)
    Target = number of webserver instances currently running
    Warmer = Marathon API call to increase # webserver instances by 1
    Cooler = Marathon API call to decrease # webserver instances by 1

Relay.Mesos can guarantee a minimum number of running redis instances

    Metric = max(min_instances, desired num of redis instances)
    Target = current number of redis instances
    Warmer = API call to increase # redis instances by 1
    Cooler = API call to decrease # redis instances by 1

##### Math side-note if you need help calculating a Metric function

A Metric function that might ensure that the number of instances is
between some bounds could use the following equation:

```
(Qsize - Qminsize) / (Qmaxsize - Qminsize) * (Imax - Imin) + Imin
```
where
```
Qsize = current queue size
Qmax = maximum expected queue size
Qmin = minimum expected queue size (ie 0)
Imax = Max desired num of instances
Imin = Min desired num of instances
```

To get you thinking in the right direction, consider this scenario:
Perhaps you have a real-valued metric that is much larger than the
number of tasks/instances you may be auto scaling.  Perhaps you also don't know
the max and min values of the metric, but you have a mean and standard
deviation.  You can experiment with a metric function that bounces
between -1 and 1, with occasional numbers beyond the range.  For
instance, you could try the below function, and also perhaps have the
mean and standard deviation iteratively update over time:

    Metric = `(Qsize - Qmean) // Qstdev`  # the // means integer division
                                          # rather than floating point division
                                          # 1 / 2 == .5  VS 1 // 2 = 0`
    Target = 0
    Warmer = "cmd to add more servers"
    Cooler = "cmd to remove some servers"

More complex metrics might use other scaling functions, a logistic
function, probabilistic expressions or regression functions.

When auto-scaling long-running processes, you may need to set the
```--relay_delay```  (ie. min num seconds between warmer / cooler calls)
to a number larger than the default value of 1 second.  Also, if you
find that the long-running process is already mesos-aware (ie running
via Marathon), it might make it more sense for you to use
[Relay](http://www.github.com/sailthru/relay) rather than Relay.Mesos.


Configuration Options:
----------

All configuration options specific to Relay.Mesos are visible when you
run one of the following commands:
```
$ docker-compose run relay relay.mesos -h

# or, if you have relay.mesos installed locally

$ relay.mesos -h
```

Configuration options can also be passed in via environment variables

Relay.Mesos options are prefixed with `RELAY_MESOS`.  For instance:

    RELAY_MESOS_MASTER=zk://zookeeper:2181/mesos

Relay-only options (ie those that start with "RELAY_"):

    RELAY_DELAY=60
