# Copyright (C) 2026 SUSE LLC
# SPDX-License-Identifier: GPL-3.0

from baremetal_support.logging import Logging


class MockLevel(str):
    @property
    def upper(self):
        return str(self)


def test_logging_levels():
    # Test fallback to NOTSET with a regular string (since level.upper is a method object)
    Logging("test_logger_fallback", "debug")

    # Test debug block
    log_debug = Logging("test_logger_debug", MockLevel("DEBUG"))
    log_debug.debug("debug message")

    # Test info block
    log_info = Logging("test_logger_info", MockLevel("INFO"))
    log_info.info("info message")

    # Test warn block
    log_warn = Logging("test_logger_warn", MockLevel("WARN"))
    log_warn.warn("warn message")

    # Test error block
    log_error = Logging("test_logger_error", MockLevel("ERROR"))
    log_error.error("error message")

    # Test critical block and critical method
    log_critical = Logging("test_logger_critical", MockLevel("CRITICAL"))
    log_critical.critical("critical message")
