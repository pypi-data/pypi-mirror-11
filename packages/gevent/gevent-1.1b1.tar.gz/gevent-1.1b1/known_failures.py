# This is a list of known failures (=bugs).
# The tests listed there must fail (or testrunner.py will report error) unless they are prefixed with FLAKY
# in which cases the result of them is simply ignored
import os
import sys


LEAKTEST = os.getenv('GEVENTTEST_LEAKCHECK')
PYPY = hasattr(sys, 'pypy_version_info')
PY3 = sys.version_info[0] >= 3
PYGTE279 = (
    sys.version_info[0] == 2
    and sys.version_info[1] >= 7
    and sys.version_info[2] >= 9
)


FAILING_TESTS = [

    # Sometimes fails with AssertionError: ...\nIOError: close() called during concurrent operation on the same file object.\n'
    # Sometimes it contains "\nUnhandled exception in thread started by \nsys.excepthook is missing\nlost sys.stderr\n"
    "FLAKY test__subprocess_interrupted.py",
]


if os.environ.get('GEVENT_RESOLVER') == 'ares' or LEAKTEST:
    # XXX fix this
    FAILING_TESTS += [
        'FLAKY test__socket_dns.py',
        'FLAKY test__socket_dns6.py',
    ]
else:
    FAILING_TESTS += [
        # A number of the host names hardcoded have multiple, load
        # balanced DNS entries. Therefore, multiple sequential calls
        # of the resolution function, whether gevent or stdlib, can
        # return non-equal results, possibly dependent on the host
        # dns configuration
        'FLAKY test__socket_dns6.py',
    ]

if sys.platform == 'win32':
    # currently gevent.core.stat watcher does not implement 'prev' and 'attr' attributes on Windows
    FAILING_TESTS += ['test__core_stat.py']

    # other Windows-related issues (need investigating)
    FAILING_TESTS += [
        'monkey_test test_threading.py',
        'monkey_test --Event test_threading.py',
        'monkey_test test_subprocess.py',
        'monkey_test --Event test_subprocess.py'
    ]


if LEAKTEST:
    FAILING_TESTS += [
        'FLAKY test__backdoor.py',
        'FLAKY test__socket_errors.py'
    ]


if PYPY:
    FAILING_TESTS += [
        ## Different in PyPy:

        ## Not implemented:

        ## ---

        ## BUGS:

    ]

    import cffi
    if cffi.__version_info__ < (1, 2, 0):
        FAILING_TESTS += [

            # check_sendall_interrupted and testInterruptedTimeout fail due to
            # https://bitbucket.org/cffi/cffi/issue/152/handling-errors-from-signal-handlers-in
            # See also patched_tests_setup and 'test_signal.InterProcessSignalTests.test_main'
            'test_socket.py',
        ]


if PY3:
    # No idea / TODO
    FAILING_TESTS += '''
FLAKY test__socket_dns.py
'''.strip().split('\n')

    if LEAKTEST:
        FAILING_TESTS += ['FLAKY test__threadpool.py']
        # refcount problems:
        FAILING_TESTS += '''
            test__timeout.py
            test__greenletset.py
            test__core.py
            test__systemerror.py
            test__exc_info.py
            test__api_timeout.py
            test__event.py
            test__api.py
            test__hub.py
            test__queue.py
            test__socket_close.py
            test__select.py
            test__greenlet.py
            FLAKY test__socket.py
'''.strip().split()


if __name__ == '__main__':
    import pprint
    pprint.pprint(FAILING_TESTS)
