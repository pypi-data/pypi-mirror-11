import time

import pytest

from pytestqt.qt_compat import QtCore, Signal


class Signaller(QtCore.QObject):
    signal = Signal()
    signal_2 = Signal()


def test_signal_blocker_exception(qtbot):
    """
    Make sure waitSignal without signals and timeout doesn't hang, but raises
    ValueError instead.
    """
    with pytest.raises(ValueError):
        qtbot.waitSignal(None, None).wait()
    with pytest.raises(ValueError):
        qtbot.waitSignals([], None).wait()


def explicit_wait(qtbot, signal, timeout, multiple, raising, should_raise):
    """
    Explicit wait for the signal using blocker API.
    """
    func = qtbot.waitSignals if multiple else qtbot.waitSignal
    blocker = func(signal, timeout, raising=raising)
    assert not blocker.signal_triggered
    if should_raise:
        with pytest.raises(qtbot.SignalTimeoutError):
            blocker.wait()
    else:
        blocker.wait()
    return blocker


def context_manager_wait(qtbot, signal, timeout, multiple, raising,
                         should_raise):
    """
    Waiting for signal using context manager API.
    """
    func = qtbot.waitSignals if multiple else qtbot.waitSignal
    if should_raise:
        with pytest.raises(qtbot.SignalTimeoutError):
            with func(signal, timeout, raising=raising) as blocker:
                pass
    else:
        with func(signal, timeout, raising=raising) as blocker:
            pass
    return blocker


def build_signal_tests_variants(params):
    """
    Helper function to use with pytest's parametrize, to generate additional
    combinations of parameters in a parametrize call:
    - explicit wait and context-manager wait
    - raising True and False (since we check for the correct behavior inside
      each test).
    """
    result = []
    for param in params:
        for wait_function in (explicit_wait, context_manager_wait):
            for raising in (True, False):
                result.append(param + (wait_function, raising))
    return result


@pytest.mark.parametrize(
    ('delay', 'timeout', 'expected_signal_triggered',
     'wait_function', 'raising'),
    build_signal_tests_variants([
        # delay, timeout, expected_signal_triggered
        (100, None, True),
        (100, 200, True),
        (200, 100, False),
    ])
)
def test_signal_triggered(qtbot, single_shot, stop_watch, wait_function, delay,
                          timeout, expected_signal_triggered, raising):
    """
    Testing for a signal in different conditions, ensuring we are obtaining
    the expected results.
    """
    signaller = Signaller()
    single_shot(signaller.signal, delay)

    should_raise = raising and not expected_signal_triggered

    stop_watch.start()
    blocker = wait_function(qtbot, signaller.signal, timeout, raising=raising,
                            should_raise=should_raise, multiple=False)

    # Check that event loop exited.
    assert not blocker._loop.isRunning()

    # ensure that either signal was triggered or timeout occurred
    assert blocker.signal_triggered == expected_signal_triggered

    stop_watch.check(timeout, delay)


@pytest.mark.parametrize(
    ('delay_1', 'delay_2', 'timeout', 'expected_signal_triggered',
     'wait_function', 'raising'),
    build_signal_tests_variants([
        # delay1, delay2, timeout, expected_signal_triggered
        (100, 150, 200, True),
        (150, 100, 200, True),
        (100, 150, None, True),
        (200, 200, 100, False),
        (100, 200, 150, False),
        (200, 100, 100, False),
        (100, 500, 200, False),
    ])
)
def test_signal_triggered_multiple(qtbot, single_shot, stop_watch, wait_function,
                                   delay_1, delay_2, timeout,
                                   expected_signal_triggered, raising):
    """
    Testing for a signal in different conditions, ensuring we are obtaining
    the expected results.
    """
    signaller = Signaller()
    single_shot(signaller.signal, delay_1)
    single_shot(signaller.signal_2, delay_2)

    should_raise = raising and not expected_signal_triggered

    stop_watch.start()
    blocker = wait_function(qtbot, [signaller.signal, signaller.signal_2],
                            timeout, multiple=True, raising=raising,
                            should_raise=should_raise)

    # Check that event loop exited.
    assert not blocker._loop.isRunning()

    # ensure that either signal was triggered or timeout occurred
    assert blocker.signal_triggered == expected_signal_triggered

    stop_watch.check(timeout, delay_1, delay_2)


def test_explicit_emit(qtbot):
    """
    Make sure an explicit emit() inside a waitSignal block works.
    """
    signaller = Signaller()
    with qtbot.waitSignal(signaller.signal, timeout=5000) as waiting:
        signaller.signal.emit()

    assert waiting.signal_triggered


def test_explicit_emit_multiple(qtbot):
    """
    Make sure an explicit emit() inside a waitSignal block works.
    """
    signaller = Signaller()
    with qtbot.waitSignals([signaller.signal, signaller.signal_2],
                           timeout=5000) as waiting:
        signaller.signal.emit()
        signaller.signal_2.emit()

    assert waiting.signal_triggered


@pytest.yield_fixture
def single_shot():
    """
    Fixture that provides a callback with signature: (signal, delay) that
    triggers that signal once after the given delay in ms.

    The fixture is responsible for cleaning up after the timers.
    """

    def shoot(signal, delay):
        timer = QtCore.QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(signal.emit)
        timer.start(delay)
        timers.append(timer)

    timers = []
    yield shoot
    for t in timers:
        t.stop()


@pytest.fixture
def stop_watch():
    """
    Fixture that makes it easier for tests to ensure signals emitted and
    timeouts are being respected in waitSignal and waitSignals tests.
    """

    class StopWatch:

        def __init__(self):
            self._start_time = None

        def start(self):
            self._start_time = time.time()

        def check(self, timeout, *delays):
            """
            Make sure either timeout (if given) or at most of the given
            delays used to trigger a signal has passed.
            """
            if timeout is None:
                timeout = max(delays) * 1.25  # 25% tolerance
            max_wait_ms = max(delays + (timeout,))
            assert time.time() - self._start_time < (max_wait_ms / 1000.0)

    return StopWatch()


@pytest.mark.parametrize('multiple, raising',
                         [(True, True), (True, False), (False, True),
                          (False, False)])
def test_wait_signals_handles_exceptions(qtbot, multiple, raising):
    """
    Make sure waitSignal handles exceptions correctly.
    """
    class TestException(Exception):
        pass

    signaller = Signaller()

    if multiple:
        func = qtbot.waitSignals
        arg = [signaller.signal, signaller.signal_2]
    else:
        func = qtbot.waitSignal
        arg = signaller.signal

    with pytest.raises(TestException):
        with func(arg, timeout=10, raising=raising):
            raise TestException
