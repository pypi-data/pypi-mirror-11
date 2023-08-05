# This program uses status message notifications to submit jobs to
# discoro processes.

# StatusMessage must be imported in global scope as below; otherwise,
# unserializing status messages fails (if external scheduler is used)
from asyncoro.discoro import StatusMessage
import asyncoro.discoro as discoro
import asyncoro.disasyncoro as asyncoro

# this generator function is sent to remote server to run
# coroutines there
def rcoro_proc(n, coro=None):
    yield coro.sleep(n)
    raise StopIteration(n)

def client_proc(computation, njobs, coro=None):
    status = {'submitted': 0, 'done': 0}

    def submit_job(where, coro=None):
        arg = random.uniform(5, 20)
        rcoro = yield computation.run_at(where, rcoro_proc, arg)
        if isinstance(rcoro, asyncoro.Coro):
            print('%s processing %s' % (rcoro.location, arg))
        else:
            print('Job %s failed: %s' % (status['submitted'], str(rcoro)))
        status['submitted'] += 1

    computation.status_coro = coro
    # if scheduler is shared (i.e., running as program), nothing needs
    # to be done (its location can optionally be given to 'schedule');
    # othrwise, start scheduler:
    # discoro.Scheduler()
    if (yield computation.schedule()):
        raise Exception('Failed to schedule computation')
    # job submitter assumes that one process can run one coroutine at a time
    while True:
        msg = yield coro.receive()
        if isinstance(msg, asyncoro.MonitorException):
            # a process finished job
            rcoro = msg.args[0]
            if msg.args[1][0] == StopIteration:
                print('Remote coroutine %s finished with %s' % (rcoro.location, msg.args[1][1]))
            else:
                asyncoro.logger.warning('Remote coroutine %s terminated with "%s"' %
                                        (rcoro.location, str(msg.args[1])))
            status['done'] += 1
            if status['done'] == njobs:
                break
            if status['submitted'] < njobs:
                # schedule another job at this process
                asyncoro.Coro(submit_job, rcoro.location)
        elif isinstance(msg, StatusMessage):
            asyncoro.logger.debug('Node/Process status: %s, %s' % (msg.status, msg.location))
            if msg.status == discoro.Scheduler.ProcInitialized:
                # a new process is ready (if special initialization is
                # required for preparing process, schedule it)
                asyncoro.Coro(submit_job, msg.location)
        else:
            asyncoro.logger.debug('Ignoring status message %s' % str(msg))
    yield computation.close()

if __name__ == '__main__':
    import logging, random
    asyncoro.logger.setLevel(logging.DEBUG)
    computation = discoro.Computation([rcoro_proc])
    # run 10 jobs
    asyncoro.Coro(client_proc, computation, 10)
