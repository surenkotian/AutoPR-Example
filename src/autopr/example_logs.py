"""Example CI logs and coverage reports to demonstrate enhanced parsing capabilities.

This module provides realistic example outputs for testing and demonstration purposes.
"""
from __future__ import annotations

from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class ExampleLog:
    """Represents an example CI log with metadata."""
    name: str
    description: str
    framework: str
    log_content: str
    expected_analysis: Dict[str, Any]


class ExampleLogsGenerator:
    """Generates example CI logs and coverage reports for testing and demonstration."""
    
    def __init__(self):
        self.examples = self._generate_examples()
    
    def _generate_examples(self) -> List[ExampleLog]:
        """Generate comprehensive example logs."""
        return [
            # Pytest Examples
            self._generate_pytest_success_example(),
            self._generate_pytest_failures_example(),
            self._generate_pytest_flaky_example(),
            self._generate_pytest_mixed_results_example(),
            
            # Unittest Examples
            self._generate_unittest_success_example(),
            self._generate_unittest_failures_example(),
            self._generate_unittest_errors_example(),
            
            # GitHub Actions Examples
            self._generate_github_actions_success_example(),
            self._generate_github_actions_failure_example(),
            self._generate_github_actions_mixed_example(),
            
            # Coverage Examples
            self._generate_coverage_improvement_example(),
            self._generate_coverage_decline_example(),
            self._generate_coverage_trivial_change_example(),
            self._generate_coverage_html_format_example(),
        ]
    
    def _generate_pytest_success_example(self) -> ExampleLog:
        """Generate a successful pytest run example."""
        log_content = '''============================= test session starts ==============================
platform win32 -- Python 3.9.7, pytest-6.2.5, py-1.10.0, pluggy-0.13.1
rootdir: C:\\Users\\TestUser\\project
collected 25 items

tests\\test_auth.py::test_login_success PASSED                                    [  4%]
tests\\test_auth.py::test_logout PASSED                                          [  8%]
tests\\test_auth.py::test_invalid_credentials PASSED                             [ 12%]
tests\\test_database.py::test_connection PASSED                                  [ 16%]
tests\\test_database.py::test_query_execution PASSED                             [ 20%]
tests\\test_database.py::test_transaction_rollback PASSED                        [ 24%]
tests\\test_api.py::test_user_creation PASSED                                    [ 28%]
tests\\test_api.py::test_user_deletion PASSED                                    [ 32%]
tests\\test_api.py::test_data_validation PASSED                                  [ 36%]
tests\\test_models.py::test_user_model_creation PASSED                           [ 40%]
tests\\test_models.py::test_model_validation_rules PASSED                        [ 44%]
tests\\test_models.py::test_model_relationships PASSED                           [ 48%]
tests\\test_utils.py::test_string_helpers PASSED                                 [ 52%]
tests\\test_utils.py::test_date_helpers PASSED                                   [ 56%]
tests\\test_utils.py::test_file_operations PASSED                                [ 60%]
tests\\test_integration.py::test_full_user_workflow PASSED                       [ 64%]
tests\\test_integration.py::test_api_database_integration PASSED                 [ 68%]
tests\\test_integration.py::test_error_handling_integration PASSED               [ 72%]
tests\\test_performance.py::test_load_testing PASSED                             [ 76%]
tests\\test_performance.py::test_memory_usage PASSED                             [ 80%]
tests\\test_security.py::test_sql_injection_prevention PASSED                    [ 84%]
tests\\test_security.py::test_xss_protection PASSED                              [ 88%]
tests\\test_security.py::test_csrf_protection PASSED                             [ 92%]
tests\\test_security.py::test_authentication_bypass PASSED                       [ 96%]
tests\\test_security.py::test_authorization_levels PASSED                        [100%]

========================== 25 passed in 2.34s =========================='''

        return ExampleLog(
            name="pytest_success",
            description="Successful pytest run with 25 passing tests",
            framework="pytest",
            log_content=log_content,
            expected_analysis={
                "total": 25,
                "passed": 25,
                "failed": 0,
                "errors": 0,
                "skipped": 0,
                "duration": 2.34,
                "failures": []
            }
        )
    
    def _generate_pytest_failures_example(self) -> ExampleLog:
        """Generate pytest run with failures example."""
        log_content = '''============================= test session starts ==============================
platform win32 -- Python 3.9.7, pytest-6.2.5, py-1.10.0, pluggy-0.13.1
rootdir: C:\\Users\\TestUser\\project
collected 30 items

tests\\test_auth.py::test_login_success PASSED                                    [  3%]
tests\\test_auth.py::test_logout PASSED                                          [  6%]
tests\\test_auth.py::test_invalid_credentials PASSED                             [ 10%]
tests\\test_database.py::test_connection PASSED                                  [ 13%]
tests\\test_database.py::test_query_execution FAILED                             [ 16%]
tests\\test_database.py::test_transaction_rollback PASSED                        [ 20%]
tests\\test_api.py::test_user_creation FAILED                                    [ 23%]
tests\\test_api.py::test_user_deletion PASSED                                    [ 26%]
tests\\test_api.py::test_data_validation PASSED                                  [ 30%]
tests\\test_models.py::test_user_model_creation PASSED                           [ 33%]
tests\\test_models.py::test_model_validation_rules FAILED                        [ 36%]
tests\\test_models.py::test_model_relationships PASSED                           [ 40%]
tests\\test_utils.py::test_string_helpers PASSED                                 [ 43%]
tests\\test_utils.py::test_date_helpers PASSED                                   [ 46%]
tests\\test_utils.py::test_file_operations PASSED                                [ 50%]
tests\\test_integration.py::test_full_user_workflow PASSED                       [ 53%]
tests\\test_integration.py::test_api_database_integration PASSED                 [ 56%]
tests\\test_integration.py::test_error_handling_integration PASSED               [ 60%]
tests\\test_performance.py::test_load_testing PASSED                             [ 63%]
tests\\test_performance.py::test_memory_usage PASSED                             [ 66%]
tests\\test_security.py::test_sql_injection_prevention PASSED                    [ 70%]
tests\\test_security.py::test_xss_protection PASSED                              [ 73%]
tests\\test_security.py::test_csrf_protection PASSED                             [ 76%]
tests\\test_security.py::test_authentication_bypass PASSED                       [ 80%]
tests\\test_security.py::test_authorization_levels PASSED                        [ 83%]
tests\\test_api.py::test_edge_case_user_creation ERROR                           [ 86%]
tests\\test_database.py::test_connection_pool_exhaustion ERROR                   [ 90%]
tests\\test_utils.py::test_concurrent_file_access PASSED                         [ 93%]
tests\\test_performance.py::test_concurrent_requests PASSED                       [ 96%]
tests\\test_security.py::test_rate_limiting PASSED                               [100%]

=================================== FAILURES ===================================
________________________ test_query_execution ________________________

    def test_query_execution():
        db = get_test_database()
        result = db.execute_query("SELECT * FROM users WHERE id = ?", (1,))
>       assert len(result) == 1
E       AssertionError: assert 0 == 1
E       
E       _test_query_execution:12: in <module>
E       ???: ???

________________________ test_user_creation ________________________

    def test_user_creation():
        user_data = {"username": "testuser", "email": "test@example.com"}
        user = create_user(user_data)
>       assert user.id is not None
E       AttributeError: 'NoneType' object has no attribute 'id'
E       
E       _test_user_creation:8: in <module>
E       ???: ???

________________________ test_model_validation_rules ________________________

    def test_model_validation_rules():
        with pytest.raises(ValueError, match="Invalid email format"):
>           User(email="invalid-email")
E       Failed: DID NOT RAISE <class 'ValueError'> containing "Invalid email format"
E       
E       _test_model_validation_rules:15: in <module>
E       ???: ???

=================================== ERRORS ===================================
________________________ test_edge_case_user_creation ________________________

    def test_edge_case_user_creation():
        # This test sometimes fails due to race conditions
        user_data = {"username": "", "email": "test@example.com"}
>       user = create_user(user_data)
E       ConnectionError: Failed to establish connection to database: Connection refused
E       
E       _test_edge_case_user_creation:5: in <module>
E       ???: ???

________________________ test_connection_pool_exhaustion ________________________

    def test_connection_pool_exhaustion():
        # Simulate connection pool exhaustion
        connections = []
        for i in range(100):
>           conn = get_database_connection()
E       TimeoutError: Database connection timeout after 30 seconds
E       
E       _test_connection_pool_exhaustion:8: in <module>
E       ???: ???

========================== 22 passed, 3 failed, 2 errors in 15.67s =========================='''

        return ExampleLog(
            name="pytest_failures",
            description="Pytest run with 3 failures and 2 errors",
            framework="pytest",
            log_content=log_content,
            expected_analysis={
                "total": 30,
                "passed": 22,
                "failed": 3,
                "errors": 2,
                "skipped": 0,
                "duration": 15.67,
                "failures": [
                    {
                        "name": "test_query_execution",
                        "status": "failed",
                        "error_type": "assertion_error",
                        "message": "assert 0 == 1"
                    },
                    {
                        "name": "test_user_creation",
                        "status": "failed",
                        "error_type": "attribute_error",
                        "message": "'NoneType' object has no attribute 'id'"
                    },
                    {
                        "name": "test_model_validation_rules",
                        "status": "failed",
                        "error_type": "runtime_error",
                        "message": "DID NOT RAISE <class 'ValueError'> containing 'Invalid email format'"
                    }
                ],
                "errors": [
                    {
                        "name": "test_edge_case_user_creation",
                        "status": "error",
                        "error_type": "connection_error",
                        "message": "Failed to establish connection to database: Connection refused"
                    },
                    {
                        "name": "test_connection_pool_exhaustion",
                        "status": "error",
                        "error_type": "timeout_error",
                        "message": "Database connection timeout after 30 seconds"
                    }
                ]
            }
        )
    
    def _generate_pytest_flaky_example(self) -> ExampleLog:
        """Generate pytest run with flaky test indicators."""
        log_content = '''============================= test session starts ==============================
platform win32 -- Python 3.9.7, pytest-6.2.5, py-1.10.0, pluggy-0.13.1
rootdir: C:\\Users\\TestUser\\project
collected 15 items

tests\\test_network.py::test_api_endpoint_consistency PASSED                     [  6%]
tests\\test_network.py::test_api_endpoint_consistency PASSED                     [ 13%]
tests\\test_network.py::test_api_endpoint_consistency FAILED                     [ 20%]
tests\\test_network.py::test_api_endpoint_consistency PASSED                     [ 26%]
tests\\test_network.py::test_api_endpoint_consistency PASSED                     [ 33%]
tests\\test_concurrent.py::test_race_condition_detection PASSED                  [ 40%]
tests\\test_concurrent.py::test_race_condition_detection FAILED                  [ 46%]
tests\\test_concurrent.py::test_race_condition_detection PASSED                  [ 53%]
tests\\test_timing.py::test_timeout_handling PASSED                              [ 60%]
tests\\test_timing.py::test_timeout_handling FAILED                              [ 66%]
tests\\test_timing.py::test_timeout_handling PASSED                              [ 73%]
tests\\test_database.py::test_transaction_isolation PASSED                       [ 80%]
tests\\test_database.py::test_transaction_isolation PASSED                       [ 86%]
tests\\test_database.py::test_transaction_isolation FAILED                       [ 93%]
tests\\test_database.py::test_transaction_isolation PASSED                       [100%]

=================================== FAILURES ===================================
________________________ test_api_endpoint_consistency ________________________

    def test_api_endpoint_consistency():
        # This test sometimes fails due to network instability
        response = requests.get("https://api.example.com/health")
        assert response.status_code == 200
        # Sometimes the API is slow to respond, causing timeouts
E       TimeoutError: Request timed out after 30 seconds
E       
E       _test_api_endpoint_consistency:8: in <module>
E       ???: ???

________________________ test_race_condition_detection ________________________

    def test_race_condition_detection():
        # Flaky test due to race condition in concurrent operations
        counter = SharedCounter()
        threads = []
        for i in range(10):
            t = threading.Thread(target=counter.increment)
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
>       assert counter.value == 10
E       AssertionError: assert 7 == 10
E       
E       _test_race_condition_detection:18: in <module>
E       ???: ???

________________________ test_timeout_handling ________________________

    def test_timeout_handling():
        # This test occasionally fails due to timing issues
        import time
        time.sleep(0.1)  # Sometimes this takes longer
        result = slow_operation()
        assert result.status == "completed"
E       TimeoutError: Operation timed out after expected delay
E       
E       _test_timeout_handling:12: in <module>
E       ???: ???

________________________ test_transaction_isolation ________________________

    def test_transaction_isolation():
        # Transaction isolation test - sometimes fails under load
        with database.transaction() as tx1:
            with database.transaction() as tx2:
                # Race condition between transactions
                balance = tx1.get_balance("user123")
                tx1.update_balance("user123", balance + 100)
                
                # This sometimes shows inconsistent state
                assert tx2.get_balance("user123") == balance  # Sometimes fails
E       AssertionError: assert 150 == 100
E       
E       _test_transaction_isolation:15: in <module>
E       ???: ???

========================== 11 passed, 4 failed in 8.45s =========================='''

        return ExampleLog(
            name="pytest_flaky",
            description="Pytest run with flaky tests showing intermittent failures",
            framework="pytest",
            log_content=log_content,
            expected_analysis={
                "total": 15,
                "passed": 11,
                "failed": 4,
                "errors": 0,
                "skipped": 0,
                "duration": 8.45,
                "flaky_tests": [
                    "test_api_endpoint_consistency",
                    "test_race_condition_detection", 
                    "test_timeout_handling",
                    "test_transaction_isolation"
                ],
                "flaky_indicators": [
                    "network_dependency",
                    "timing_dependency",
                    "race condition"
                ]
            }
        )
    
    def _generate_pytest_mixed_results_example(self) -> ExampleLog:
        """Generate pytest run with mixed results including xfailed/xpassed."""
        log_content = '''============================= test session starts ==============================
platform win32 -- Python 3.9.7, pytest-6.2.5, py-1.10.0, pluggy-0.13.1
rootdir: C:\\Users\\TestUser\\project
plugins: asyncio-0.15.1,cov-2.12.1
collected 20 items

tests\\test_features.py::test_new_feature_basic PASSED                           [  5%]
tests\\test_features.py::test_new_feature_advanced PASSED                       [ 10%]
tests\\test_features.py::test_experimental_feature XFAIL (Experimental feature not ready) [ 15%]
tests\\test_features.py::test_deprecated_feature XPASS (Deprecated feature still works) [ 20%]
tests\\test_auth.py::test_login_basic PASSED                                    [ 25%]
tests\\test_auth.py::test_login_advanced PASSED                                 [ 30%]
tests\\test_auth.py::test_login_invalid_credentials PASSED                      [ 35%]
tests\\test_auth.py::test_password_reset PASSED                                 [ 40%]
tests\\test_api.py::test_create_user PASSED                                     [ 45%]
tests\\test_api.py::test_update_user PASSED                                     [ 50%]
tests\\test_api.py::test_delete_user PASSED                                     [ 55%]
tests\\test_api.py::test_user_not_found FAILED                                  [ 60%]
tests\\test_api.py::test_concurrent_user_creation ERROR                         [ 65%]
tests\\test_database.py::test_basic_crud PASSED                                 [ 70%]
tests\\test_database.py::test_complex_query PASSED                              [ 75%]
tests\\test_database.py::test_backup_restore PASSED                             [ 80%]
tests\\test_utils.py::test_string_operations PASSED                             [ 85%]
tests\\test_utils.py::test_date_operations PASSED                               [ 90%]
tests\\test_utils.py::test_file_operations PASSED                               [ 95%]
tests\\test_utils.py::test_concurrent_file_access PASSED                        [100%]

========================== 17 passed, 1 failed, 1 error, 1 xfailed, 1 xpassed in 5.23s =========================='''

        return ExampleLog(
            name="pytest_mixed",
            description="Pytest run with mixed results including xfailed and xpassed",
            framework="pytest",
            log_content=log_content,
            expected_analysis={
                "total": 20,
                "passed": 17,
                "failed": 1,
                "errors": 1,
                "skipped": 0,
                "xfailed": 1,
                "xpassed": 1,
                "duration": 5.23
            }
        )
    
    def _generate_unittest_success_example(self) -> ExampleLog:
        """Generate successful unittest run example."""
        log_content = '''----------------------------------------------------------------------
Ran 18 tests in 1.456s

OK'''

        return ExampleLog(
            name="unittest_success",
            description="Successful unittest run with 18 tests",
            framework="unittest",
            log_content=log_content,
            expected_analysis={
                "total": 18,
                "passed": 18,
                "failed": 0,
                "errors": 0,
                "skipped": 0,
                "duration": 1.456
            }
        )
    
    def _generate_unittest_failures_example(self) -> ExampleLog:
        """Generate unittest run with failures example."""
        log_content = '''F..
======================================================================
FAIL: test_user_creation (tests.test_models.TestUserModel)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\\Users\\TestUser\\project\\tests\\test_models.py", line 23, in test_user_creation
    self.assertIsNotNone(user.id)
AssertionError: unexpectedly None

----------------------------------------------------------------------
FAIL: test_email_validation (tests.test_validators.TestEmailValidator)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\\Users\\TestUser\\project\\tests\\test_validators.py", line 15, in test_email_validation
    self.assertTrue(validator.is_valid("invalid-email"))
AssertionError: True is not false

----------------------------------------------------------------------
FAIL: test_database_connection (tests.test_database.TestDatabase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\\Users\\TestUser\\project\\tests\\test_database.py", line 8, in test_database_connection
    self.assertEqual(connection.status, "connected")
AssertionError: 'disconnected' != 'connected'

----------------------------------------------------------------------
Ran 15 tests in 2.345s

FAILED (failures=3)'''

        return ExampleLog(
            name="unittest_failures",
            description="Unittest run with 3 failures",
            framework="unittest",
            log_content=log_content,
            expected_analysis={
                "total": 15,
                "passed": 12,
                "failed": 3,
                "errors": 0,
                "skipped": 0,
                "duration": 2.345,
                "failures": [
                    {
                        "name": "test_user_creation",
                        "status": "failed",
                        "error_type": "assertion_error",
                        "message": "unexpectedly None"
                    },
                    {
                        "name": "test_email_validation", 
                        "status": "failed",
                        "error_type": "assertion_error",
                        "message": "True is not false"
                    },
                    {
                        "name": "test_database_connection",
                        "status": "failed", 
                        "error_type": "assertion_error",
                        "message": "'disconnected' != 'connected'"
                    }
                ]
            }
        )
    
    def _generate_unittest_errors_example(self) -> ExampleLog:
        """Generate unittest run with errors example."""
        log_content = '''E..
======================================================================
ERROR: test_network_operation (tests.test_network.TestNetworkOps)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\\Users\\TestUser\\project\\tests\\test_network.py", line 12, in test_network_operation
    response = requests.get("https://api.example.com/data")
ConnectionError: HTTPSConnectionPool(host='api.example.com', port=443): Max retries exceeded with url: /data (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x7f8b3c0b1d30>: Failed to establish a new connection: [Errno 110] Connection timed out'))

======================================================================
ERROR: test_file_processing (tests.test_files.TestFileProcessor)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\\Users\\TestUser\\project\\tests\\test_files.py", line 8, in test_file_processing
    data = processor.read_file("nonexistent.txt")
FileNotFoundError: [Errno 2] No such file or directory: 'nonexistent.txt'

----------------------------------------------------------------------
Ran 12 tests in 3.210s

OK (errors=2)'''

        return ExampleLog(
            name="unittest_errors",
            description="Unittest run with 2 errors",
            framework="unittest",
            log_content=log_content,
            expected_analysis={
                "total": 12,
                "passed": 10,
                "failed": 0,
                "errors": 2,
                "skipped": 0,
                "duration": 3.210,
                "errors": [
                    {
                        "name": "test_network_operation",
                        "status": "error",
                        "error_type": "connection_error",
                        "message": "Connection timed out"
                    },
                    {
                        "name": "test_file_processing",
                        "status": "error",
                        "error_type": "environment_error",
                        "message": "No such file or directory"
                    }
                ]
            }
        )
    
    def _generate_github_actions_success_example(self) -> ExampleLog:
        """Generate successful GitHub Actions workflow example."""
        log_content = '''Run python -m pytest tests/ --cov=src --cov-report=xml
============================= test session starts ==============================
platform linux -- Python 3.9.7, pytest-6.2.5, py-1.10.0, pluggy-0.13.1
rootdir: /home/runner/work/myproject/myproject
plugins: asyncio-0.15.1, cov-2.12.1
collected 25 items

tests/test_main.py::test_basic_functionality PASSED                      [  4%]
tests/test_main.py::test_advanced_features PASSED                        [  8%]
tests/test_api.py::test_endpoint_creation PASSED                         [ 12%]
tests/test_api.py::test_endpoint_validation PASSED                       [ 16%]
tests/test_models.py::test_model_creation PASSED                         [ 20%]
tests/test_models.py::test_model_validation PASSED                       [ 24%]
tests/test_database.py::test_connection PASSED                           [ 28%]
tests/test_database.py::test_queries PASSED                              [ 32%]
tests/test_integration.py::test_full_workflow PASSED                     [ 36%]
tests/test_integration.py::test_error_handling PASSED                    [ 40%]
tests/test_security.py::test_authentication PASSED                       [ 44%]
tests/test_security.py::test_authorization PASSED                        [ 48%]
tests/test_performance.py::test_load_testing PASSED                      [ 52%]
tests/test_performance.py::test_memory_usage PASSED                      [ 56%]
tests/test_utils.py::test_helpers PASSED                                 [ 60%]
tests/test_utils.py::test_validators PASSED                              [ 64%]
tests/test_webhooks.py::test_webhook_handling PASSED                     [ 68%]
tests/test_webhooks.py::test_webhook_validation PASSED                   [ 72%]
tests/test_email.py::test_email_sending PASSED                           [ 76%]
tests/test_email.py::test_email_templates PASSED                         [ 80%]
tests/test_notifications.py::test_notification_creation PASSED            [ 84%]
tests/test_notifications.py::test_notification_delivery PASSED            [ 88%]
tests/test_monitoring.py::test_metrics_collection PASSED                 [ 92%]
tests/test_monitoring.py::test_alerting PASSED                           [ 96%]
tests/test_monitoring.py::test_dashboard_updates PASSED                  [100%]

========================== 25 passed in 12.34s ==========================
Coverage.py warning: No data for collected files ('src/utils.py' not found)
Coverage.py warning: No data for collected files ('src/validators.py' not found)

----------- coverage: platform linux, python 3.9.7 ----------
Name                             Stmts   Miss  Cover
----------------------------------------------------
src/main.py                        145      0   100%
src/api.py                         203     12    94%
src/models.py                      178      8    95%
src/database.py                    156      4    97%
src/integration.py                  89     15    83%
src/security.py                    234     18    92%
src/performance.py                 167     23    86%
src/webhooks.py                    123      7    94%
src/email.py                       145     11    92%
src/notifications.py               189     14    93%
src/monitoring.py                  201     19    91%
----------------------------------------------------
TOTAL                            1830    131    93%

##[group]Run actions/upload-artifact
##[command]upload-artifact artifact=coverage.xml
Upload artifact successful

##[success]CI pipeline completed successfully'''

        return ExampleLog(
            name="github_actions_success",
            description="Successful GitHub Actions workflow with full test suite",
            framework="github_actions",
            log_content=log_content,
            expected_analysis={
                "total": 25,
                "passed": 25,
                "failed": 0,
                "errors": 0,
                "skipped": 0,
                "coverage": 93.0,
                "duration": 12.34,
                "environment": {
                    "platform": "linux",
                    "python_version": "3.9.7"
                }
            }
        )
    
    def _generate_github_actions_failure_example(self) -> ExampleLog:
        """Generate GitHub Actions workflow failure example."""
        log_content = '''Run python -m pytest tests/ --cov=src
============================= test session starts ==============================
platform linux -- Python 3.9.7, pytest-6.2.5, py-1.10.0, pluggy-0.13.1
rootdir: /home/runner/work/myproject/myproject
plugins: asyncio-0.15.1, cov-2.12.1
collected 30 items

tests/test_main.py::test_basic_functionality PASSED                      [  3%]
tests/test_main.py::test_advanced_features PASSED                        [  6%]
tests/test_api.py::test_endpoint_creation PASSED                         [ 10%]
tests/test_api.py::test_endpoint_validation PASSED                       [ 13%]
tests/test_models.py::test_model_creation FAILED                         [ 16%]
tests/test_models.py::test_model_validation PASSED                       [ 20%]
tests/test_database.py::test_connection FAILED                           [ 23%]
tests/test_database.py::test_queries PASSED                              [ 26%]
tests/test_integration.py::test_full_workflow FAILED                     [ 30%]
tests/test_integration.py::test_error_handling PASSED                    [ 33%]

=================================== FAILURES ===================================
________________________ test_model_creation ________________________

    def test_model_creation():
        data = {"name": "Test", "email": "test@example.com"}
>       model = Model.create(data)
E       AttributeError: 'Model' object has no attribute 'create'
E       
E       _test_model_creation:8: in <module>
E       ???: ???

________________________ test_connection ________________________

    def test_connection():
>       db = Database.get_connection()
E       ConnectionError: Unable to connect to database
E       
E       _test_connection:5: in <module>
E       ???: ???

________________________ test_full_workflow ________________________

    def test_full_workflow():
        # Test the complete user workflow
        user = create_user({"name": "John", "email": "john@example.com"})
        result = process_user_data(user)
        assert result.status == "success"
E       AssertionError: assert 'failed' == 'success'
E       
E       _test_full_workflow:15: in <module>
E       ???: ???

========================== 22 passed, 3 failed in 8.45s ==========================
##[error]Test execution failed
##[error]Process completed with exit code 1.
##[error]GitHub Actions workflow failed: Tests failed (3 failures)

##[group]Run actions/upload-artifact
Uploading artifacts is only available on actions/upload-artifact@v2 and up.
##[error]Artifact upload failed - workflow must complete successfully first
##[error]Workflow run failed with 3 test failures'''

        return ExampleLog(
            name="github_actions_failure",
            description="GitHub Actions workflow with test failures",
            framework="github_actions",
            log_content=log_content,
            expected_analysis={
                "total": 30,
                "passed": 22,
                "failed": 3,
                "errors": 0,
                "skipped": 0,
                "duration": 8.45,
                "workflow_status": "failed"
            }
        )
    
    def _generate_github_actions_mixed_example(self) -> ExampleLog:
        """Generate GitHub Actions workflow with mixed results."""
        log_content = '''Run python -m pytest tests/ -v
============================= test session starts ==============================
platform linux -- Python 3.9.7, pytest-6.2.5, py-1.10.0, pluggy-0.13.1
rootdir: /home/runner/work/myproject/myproject
plugins: asyncio-0.15.1, timeout-1.4.2
collected 20 items

##[group]Running tests for authentication module
tests/test_auth.py::test_login_valid PASSED                              [  5%]
tests/test_auth.py::test_login_invalid PASSED                            [ 10%]
tests/test_auth.py::test_token_refresh PASSED                            [ 15%]
tests/test_auth.py::test_logout_cleanup PASSED                           [ 20%]
##[error]tests/test_auth.py::test_concurrent_login ERROR                [ 25%]
##[error]ConnectionError: Database connection pool exhausted
##[group]Running tests for API endpoints
tests/test_api.py::test_get_user PASSED                                  [ 30%]
tests/test_api.py::test_create_user PASSED                               [ 35%]
tests/test_api.py::test_update_user FAILED                               [ 40%]
##[error]TimeoutError: API request timed out after 30 seconds
tests/test_api.py::test_delete_user PASSED                               [ 45%]
##[group]Running tests for data processing
tests/test_data.py::test_data_validation PASSED                          [ 50%]
tests/test_data.py::test_data_transformation PASSED                      [ 55%]
tests/test_data.py::test_data_export FAILED                              [ 60%]
##[error]PermissionError: Insufficient permissions to write export file
tests/test_data.py::test_data_import PASSED                              [ 65%]
##[group]Running tests for reporting
tests/test_reporting.py::test_report_generation PASSED                   [ 70%]
tests/test_reporting.py::test_report_formatting PASSED                   [ 75%]
tests/test_reporting.py::test_report_delivery PASSED                     [ 80%]
##[group]Running tests for monitoring
tests/test_monitoring.py::test_metrics_collection PASSED                 [ 85%]
tests/test_monitoring.py::test_alert_system PASSED                       [ 90%]
tests/test_monitoring.py::test_health_checks PASSED                      [ 95%]

========================== 16 passed, 2 failed, 3 error in 25.67s ==========================
##[warning]Some tests had timeout issues - may need investigation
##[warning]Database connection issues detected
##[success]Partial workflow completion - review failed tests'''

        return ExampleLog(
            name="github_actions_mixed",
            description="GitHub Actions workflow with mixed results and warnings",
            framework="github_actions",
            log_content=log_content,
            expected_analysis={
                "total": 20,
                "passed": 16,
                "failed": 2,
                "errors": 3,
                "skipped": 0,
                "duration": 25.67,
                "warnings": [
                    "Some tests had timeout issues - may need investigation",
                    "Database connection issues detected"
                ],
                "workflow_status": "partial"
            }
        )
    
    def _generate_coverage_improvement_example(self) -> ExampleLog:
        """Generate coverage report showing improvement."""
        before_content = '''Name                             Stmts   Miss  Cover
----------------------------------------------------
src/main.py                        145     23    84%
src/api.py                         203     45    78%
src/models.py                      178     34    81%
src/database.py                    156     28    82%
src/utils.py                       123     31    75%
src/auth.py                        167     29    83%
src/validation.py                  145     38    74%
----------------------------------------------------
TOTAL                            1117    228    80%'''

        after_content = '''Name                             Stmts   Miss  Cover
----------------------------------------------------
src/main.py                        145     12    92%
src/api.py                         203     28    86%
src/models.py                      178     19    89%
src/database.py                    156     15    90%
src/utils.py                       123     18    85%
src/auth.py                        167     21    87%
src/validation.py                  145     25    83%
----------------------------------------------------
TOTAL                            1117    138    88%'''

        return ExampleLog(
            name="coverage_improvement",
            description="Coverage report showing 8% improvement (80% -> 88%)",
            framework="coverage",
            log_content=f"BEFORE:\n{before_content}\n\nAFTER:\n{after_content}",
            expected_analysis={
                "before_coverage": 80.0,
                "after_coverage": 88.0,
                "improvement": 8.0,
                "meaningful_change": True,
                "files_improved": 7,
                "severity": "significant"
            }
        )
    
    def _generate_coverage_decline_example(self) -> ExampleLog:
        """Generate coverage report showing decline."""
        before_content = '''Name                             Stmts   Miss  Cover
----------------------------------------------------
src/main.py                        145      8    95%
src/api.py                         203     15    93%
src/models.py                      178     12    93%
src/database.py                    156      9    94%
src/utils.py                       123     18    85%
src/auth.py                        167     23    86%
src/validation.py                  145     21    86%
----------------------------------------------------
TOTAL                            1117    106    91%'''

        after_content = '''Name                             Stmts   Miss  Cover
----------------------------------------------------
src/main.py                        145      8    95%
src/api.py                         203     45    78%
src/models.py                      178     12    93%
src/database.py                    156      9    94%
src/utils.py                       123     65    47%
src/auth.py                        167     23    86%
src/validation.py                  145     21    86%
----------------------------------------------------
TOTAL                            1117    183    84%'''

        return ExampleLog(
            name="coverage_decline",
            description="Coverage report showing 7% decline (91% -> 84%)",
            framework="coverage",
            log_content=f"BEFORE:\n{before_content}\n\nAFTER:\n{after_content}",
            expected_analysis={
                "before_coverage": 91.0,
                "after_coverage": 84.0,
                "decline": -7.0,
                "meaningful_change": True,
                "files_declined": 2,
                "severity": "significant"
            }
        )
    
    def _generate_coverage_trivial_change_example(self) -> ExampleLog:
        """Generate coverage report showing trivial change."""
        before_content = '''Name                             Stmts   Miss  Cover
----------------------------------------------------
src/main.py                        145     12    92%
src/api.py                         203     28    86%
src/models.py                      178     19    89%
src/database.py                    156     15    90%
----------------------------------------------------
TOTAL                             682     74    89%'''

        after_content = '''Name                             Stmts   Miss  Cover
----------------------------------------------------
src/main.py                        145     12    92%
src/api.py                         203     27    87%
src/models.py                      178     19    89%
src/database.py                    156     16    90%
----------------------------------------------------
TOTAL                             682     74    89%'''

        return ExampleLog(
            name="coverage_trivial",
            description="Coverage report showing trivial change (89% stays same)",
            framework="coverage",
            log_content=f"BEFORE:\n{before_content}\n\nAFTER:\n{after_content}",
            expected_analysis={
                "before_coverage": 89.0,
                "after_coverage": 89.0,
                "change": 0.0,
                "meaningful_change": False,
                "severity": "trivial"
            }
        )
    
    def _generate_coverage_html_format_example(self) -> ExampleLog:
        """Generate HTML format coverage report."""
        html_content = '''<!DOCTYPE html>
<html>
<head>
    <title>Coverage report</title>
</head>
<body>
    <h1>Coverage report</h1>
    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Stmts</th>
                <th>Miss</th>
                <th>Cover</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>src/main.py</td>
                <td>145</td>
                <td>12</td>
                <td>92%</td>
            </tr>
            <tr>
                <td>src/api.py</td>
                <td>203</td>
                <td>28</td>
                <td>86%</td>
            </tr>
            <tr>
                <td>src/models.py</td>
                <td>178</td>
                <td>19</td>
                <td>89%</td>
            </tr>
        </tbody>
        <tfoot>
            <tr>
                <td><strong>TOTAL</strong></td>
                <td>526</td>
                <td>59</td>
                <td><strong>89%</strong></td>
            </tr>
        </tfoot>
    </table>
</body>
</html>'''

        return ExampleLog(
            name="coverage_html",
            description="HTML format coverage report",
            framework="coverage",
            log_content=html_content,
            expected_analysis={
                "coverage": 89.0,
                "format": "html",
                "files": 3
            }
        )
    
    def get_examples(self, framework: str = None) -> List[ExampleLog]:
        """Get examples filtered by framework."""
        if framework:
            return [ex for ex in self.examples if ex.framework == framework]
        return self.examples
    
    def get_example_by_name(self, name: str) -> ExampleLog:
        """Get specific example by name."""
        for example in self.examples:
            if example.name == name:
                return example
        raise ValueError(f"Example '{name}' not found")
    
    def list_examples(self) -> List[Dict[str, str]]:
        """List all available examples."""
        return [
            {
                "name": ex.name,
                "description": ex.description,
                "framework": ex.framework
            }
            for ex in self.examples
        ]


# Convenience function to get all examples
def get_all_examples() -> List[ExampleLog]:
    """Get all example logs for testing and demonstration."""
    generator = ExampleLogsGenerator()
    return generator.get_examples()


def get_examples_by_framework(framework: str) -> List[ExampleLog]:
    """Get examples filtered by framework."""
    generator = ExampleLogsGenerator()
    return generator.get_examples(framework)