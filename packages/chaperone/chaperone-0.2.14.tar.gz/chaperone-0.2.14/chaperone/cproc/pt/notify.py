import asyncio
import socket
import re
from functools import partial

from chaperone.cutil.errors import ChProcessError
from chaperone.cutil.protocol import Server, ServerProtocol
from chaperone.cutil.proc import ProcStatus
from chaperone.cproc.subproc import SubProcess

_RE_NOTIFY = re.compile(r'^([A-Za-z]+)=(.+)$')

class NotifyProtocol(ServerProtocol):

    process = None              # filled in by _get_notifier_socket_name()

    def datagram_received(self, data, addr):
        lines = data.decode().split("\n")
        for line in lines:
            m = _RE_NOTIFY.match(line)
            if m and self.process:
                self.process.have_notify(m.group(1), m.group(2))

    
class NotifyListener(Server):

    def _create_server(self):
        loop = asyncio.get_event_loop()
        return loop.create_datagram_endpoint(NotifyProtocol.buildProtocol(self), family=socket.AF_UNIX)


class NotifyProcess(SubProcess):

    process_timeout = 300

    _fut_monitor = None
    _notifier = None
    _ready_event = None

    @asyncio.coroutine
    def _get_notifier_socket_name(self):
        if self._notifier:
            return self._notifier[0]

        abstract_name = '/chaperone/' + self.service.name

        notify = self._notify_listener = NotifyListener()
        future = notify.run()

        (transport, protocol) = yield from future
        protocol.process = self

        transport._sock.bind("\0" + abstract_name)
        self._notifier = ("@" + abstract_name, notify)

        return self._notifier[0]

    def _close_notifier(self):
        if self._notifier:
            self._notifier[1].close()
            self._notifier = None

    @asyncio.coroutine
    def process_prepare_co(self, environ):
        environ['NOTIFY_SOCKET'] = yield from self._get_notifier_socket_name()

        # Now, set up an event which is triggered upon ready
        self._ready_event = asyncio.Event()

    def _notify_timeout(self):
        service = self.service
        message = "notify service '{1}' did not receieve ready notification after {2} second(s), {3}".format(
            service.type,
            service.name, self.process_timeout, 
            "proceeding due to 'ignore_failures=True'" if service.ignore_failures else
            "terminating due to 'ignore_failures=False'")
        if not service.ignore_failures:
            self.terminate()
        raise ChProcessError(message)

    @asyncio.coroutine
    def reset(self, restart = False, dependents = False, enable = False):
        yield from super().reset(restart, dependents, enable)
        self._close_notifier()

    @asyncio.coroutine
    def final_stop(self):
        yield from super().final_stop()
        self._close_notifier()

    @asyncio.coroutine
    def process_started_co(self):
        if self._fut_monitor:
            self._fut_monitor.cancel()
            self._fut_monitor = None
        self._fut_monitor = asyncio.async(self._monitor_service())
        self.add_pending(self._fut_monitor)

        if self._ready_event:
            try:
                if not self.process_timeout:
                    raise asyncio.TimeoutError()
                yield from asyncio.wait_for(self._ready_event.wait(), self.process_timeout)
            except asyncio.TimeoutError:
                self._ready_event = None
                self._notify_timeout()
            else:
                self._ready_event = None
                rc = self.returncode
                if rc is not None and not rc.normal_exit:
                    raise ChProcessError("{0} failed with reported error {1}".format(self.name, rc))

    @asyncio.coroutine
    def _monitor_service(self):
        """
        We only care about errors here.  The rest is dealt with by having notifications
        occur.
        """
        result = yield from self.wait()
        if isinstance(result, int) and result > 0:
            self._close_notifier()
            yield from self._abnormal_exit(result)
            
    def have_notify(self, var, value):
        callfunc = getattr(self, "notify_" + var.upper(), None)
        #print("HAVE NOTIFY", var, value)
        if callfunc:
            callfunc(value)

    def _setready(self):
        if self._ready_event:
            self._ready_event.set()
            return True
        return False

    def notify_MAINPID(self, value):
        try:
            pid = int(value)
        except ValueError:
            self.logdebug("{0} got MAINPID={1}, but not a valid pid#", self.name, value)
            return
        self.pid = pid

    def notify_BUSERROR(self, value):
        code = ProcStatus(value)
        if not self._setready():
            self.process_exit(code)
        else:
            self.returncode = code

    def notify_ERRNO(self, value):
        try:
            intval = int(value)
        except ValueError:
            self.logdebug("{0} got ERROR={1}, not a valid error code", self.name, value)
            return
        code = ProcStatus(intval << 8)
        if not self._setready():
            self.process_exit(code)
        else:
            self.returncode = code

    def notify_READY(self, value):
        if value == "1":
            self._setready()

    def notify_STATUS(self, value):
        self.note = value

    @property
    def status(self):
        if self._ready_event:
            return "activating"
        return super().status
