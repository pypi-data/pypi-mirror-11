
import sys
import os
import py
import psutil

std = py.std

def do_xkill(info):
    # return codes:
    # 0   no work to do
    # 1   killed
    # -1  failed to kill
    if not info.pid or not info.isrunning():
        return 0

    try:
        psutil.Process(info.pid).kill()
    except psutil.Error:
        return -1
    else:
        return 1

def do_killxshow(xprocess, tw, xkill):
    ret = 0
    for p in xprocess.rootdir.listdir():
        info = xprocess.getinfo(p.basename)
        if xkill:
            killret = do_xkill(info)
            ret = ret or (killret==1)
            if killret == 1:
                tw.line("%s %s TERMINATED" % (info.pid, info.name))
            elif killret == -1:
                tw.line("%s %s FAILED TO KILL" % (info.pid, info.name))
            elif killret == 0:
                tw.line("%s %s NO PROCESS FOUND" % (info.pid, info.name))
        else:
            running = info.isrunning() and "LIVE" or "DEAD"
            tw.line("%s %s %s %s" %(info.pid, info.name, running,
                                        info.logpath,))
    return ret

class XProcessInfo:
    def __init__(self, path, name):
        self.name = name
        self.controldir = path.ensure(name, dir=1)
        self.logpath = self.controldir.join("xprocess.log")
        self.pidpath = self.controldir.join("xprocess.PID")
        if self.pidpath.check():
            self.pid = int(self.pidpath.read())
        else:
            self.pid = None

    def kill(self):
        return do_xkill(self)

    def isrunning(self):
        if self.pid is None:
            return False
        try:
            proc = psutil.Process(self.pid)
        except psutil.NoSuchProcess:
            return False
        return proc.is_running()


class XProcess:
    def __init__(self, config, rootdir, log=None):
        self.config = config
        self.rootdir = rootdir
        if log is None:
            class Log:
                def debug(self, msg, *args):
                    if args:
                        print (msg % args)
                    else:
                        print (msg)
            log = Log()
        self.log = log

    def getinfo(self, name):
        """ return Process Info for the given external process. """
        return XProcessInfo(self.rootdir, name)

    def ensure(self, name, preparefunc, restart=False):
        """ returns (PID, logfile) from a newly started or already
            running process.

        @param name: name of the external process, used for caching info
                     across test runs.

        @param preparefunc:
                called with a fresh empty CWD for the new process,
                must return (waitpattern, args) tuple where
                ``args`` are used to start the subprocess and the
                the regular expression ``waitpattern`` must be found

        @param restart: force restarting the process if it is running.

        @return: (PID, logfile) logfile will be seeked to the end if the
                 server was running, otherwise seeked to the line after
                 where the waitpattern matched.
        """
        from subprocess import Popen, STDOUT
        info = self.getinfo(name)
        if not restart and not info.isrunning():
            restart = True

        if restart:
            if info.pid is not None:
                info.kill()
            controldir = info.controldir.ensure(dir=1)
            #controldir.remove()
            preparedata = preparefunc(controldir)
            if len(preparedata) == 2:
                wait, args = preparedata
                env = None
            else:
                wait, args, env = preparedata
            args = [str(x) for x in args]
            self.log.debug("%s$ %s", controldir, " ".join(args))
            stdout = open(str(info.logpath), "wb", 0)
            kwargs = {'env': env}
            if sys.platform == "win32":
                kwargs["startupinfo"] = sinfo = std.subprocess.STARTUPINFO()
                if sys.version_info >= (2,7):
                    sinfo.dwFlags |= std.subprocess.STARTF_USESHOWWINDOW
                    sinfo.wShowWindow |= std.subprocess.SW_HIDE
            else:
                kwargs["close_fds"] = True
                kwargs["preexec_fn"] = os.setpgrp  # no CONTROL-C
            popen = Popen(args, cwd=str(controldir),
                          stdout=stdout, stderr=STDOUT,
                          **kwargs)
            info.pid = pid = popen.pid
            info.pidpath.write(str(pid))
            self.log.debug("process %r started pid=%s", name, pid)
            stdout.close()
        f = info.logpath.open()
        if not restart:
            f.seek(0, 2)
        else:
            if not callable(wait):
                check = lambda: self._checkpattern(f, wait)
            else:
                check = wait
            if check():
                self.log.debug("%s process startup detected", name)
            else:
                raise RuntimeError("Could not start process %s" % name)
        logfiles = self.config.__dict__.setdefault("_extlogfiles", {})
        logfiles[name] = f
        newinfo = self.getinfo(name)
        return info.pid, info.logpath

    def _checkpattern(self, f, pattern, count=50):
        while 1:
            line = f.readline()
            if not line:
                std.time.sleep(0.1)
            self.log.debug(line)
            if std.re.search(pattern, line):
                return True
            count -= 1
            if count < 0:
                return False

