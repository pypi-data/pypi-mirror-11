from datetime import datetime, time
import uuid
import os

from pscore.clients.saucelabs.saucelabs_client import SauceLabsClient
from pscore.config.test_configuration import TestConfiguration


class WebDriverFinalizer:
    # TODO: Move to config
    SCREENSHOT_PATH = TestConfiguration.get_screenshot_dir()

    @staticmethod
    def create_screenshot_filename():
        return str(uuid.uuid4()) + '.png'

    @staticmethod
    def finalize(driver, test_failed, logger, test_context=None):
        """
        :type driver: selenium.webdriver.remote.webdriver.WebDriver
        """

        desired_execution_environment = TestConfiguration.get_execution_environment()
        using_skygrid = TestConfiguration.get_skygrid_enabled()

        if desired_execution_environment == 'grid':
            if using_skygrid:
                WebDriverFinalizer.finalize_skygrid(driver, test_failed, test_context)
            else:
                WebDriverFinalizer.finalise_grid_driver(driver, test_failed, logger)

            return

        elif desired_execution_environment == 'local':
            WebDriverFinalizer.finalise_grid_driver(driver, test_failed, logger)
            return

        elif desired_execution_environment in ['saucelabs', 'sauce']:
            WebDriverFinalizer.finalise_saucelabs_driver(driver, test_failed, test_context)
            return

        else:
            logger.error(
                "Could not teardown driver properly as the specified execution environment was not recognised: %s "
                % desired_execution_environment)

        # Catch-all driver teardown.  This shouldn't be needed, but just in case something crazy happens we don't want
        # to leave any orphaned sessions open
        if driver is not None:
            logger.info(
                "Could not parse driver to finalize in any specific fashion.  Quitting driver to prevent orphan session.")
            driver.quit()

        return

    @staticmethod
    def finalise_saucelabs_driver(driver, test_failed, test_context):
        test_context.logger.info("Finalizing driver for Saucelabs")
        try:
            job_id = driver.session_id
            test_context.logger.debug("Quitting driver instance.")
            driver.quit()

            test_context.logger.debug("Creating Saucelabs client.")
            client = SauceLabsClient(sauce_username=TestConfiguration.get_sauce_username(),
                                     sauce_access_key=TestConfiguration.get_sauce_key())

            test_context.logger.debug("Waiting for job to complete.")
            WebDriverFinalizer.wait_until_sauce_job_completes(client, job_id, test_context.logger)

            test_context.logger.debug("Setting job public.")
            client.set_job_public(job_id, True)

            if test_failed:
                test_context.logger.debug("Setting job pass status to False.")
                client.set_job_pass_status(job_id, False)
                error = test_context.error_message
                print 'error message: {}'.format(error)
                test_context.logger.debug("Setting job error text.")
                client.set_error(job_id, error)
            else:
                test_context.logger.debug("Setting job pass status to True.")
                client.set_job_pass_status(job_id, True)

            report_url = 'https://saucelabs.com/jobs/{}'.format(str(job_id))
            test_context.logger.info("SauceLabs report: <a href=\"{}\" target=\"_blank\">link</a>".format(report_url))
        except TypeError as e:
            test_context.logger.error(
                "TypeError caught when finalizing for SauceLabs.  This signifies a problem in the finalization code: %s" % str(
                    e))
            raise

        except Exception as e:
            test_context.logger.error("Exception caught when finalizing for SauceLabs: %s" % str(e))
            raise

    @staticmethod
    def wait_until_sauce_job_completes(client, job_id, logger):
        polling_delay_sec = 1
        max_attempts = 10
        job_completed = False

        for x in range(1, max_attempts):
            job_completed = client.job_is_complete(job_id)
            if job_completed:
                break
            else:
                time().sleep(polling_delay_sec)

        if not job_completed:
            logger.error("Saucelabs job %s did not complete within %s seconds during finalization"
                         % (job_id, str(max_attempts * polling_delay_sec)))

    @staticmethod
    def finalise_grid_driver(driver, test_failed, logger):
        if driver is not None:
            if test_failed:
                filename = WebDriverFinalizer.create_screenshot_filename()
                logger.info('Test Finalizer: Detected test failure, attempting screenshot: ' + filename)

                try:
                    file_path = os.path.join(WebDriverFinalizer.SCREENSHOT_PATH, filename)
                    driver.save_screenshot(file_path)
                except:
                    logger.error('Test Finalizer: Exception thrown when attempting screenshot: ' + filename)

                try:
                    final_url = driver.current_url
                    logger.info('Test Finalizer: Final url: ' + final_url)
                except:
                    logger.error('Test Finalizer: Exception thrown when attempting to get the drivers final url')

            else:
                logger.info('Test Finalizer: Detected test passed.')

            logger.info('Test Finalizer: Ending browser session.')
            driver.quit()

        else:
            logger.warning('Test Finalizer: Attempted to finalise test but the session had already terminated.')

    @staticmethod
    def finalize_skygrid(driver, test_failed, test_context):
        if driver is not None:
            if test_failed:
                WebDriverFinalizer.finalise_skygrid_driver_failure(driver, test_context)
            else:
                test_context.logger.info('Test Finalizer: Detected test passed.')
                driver.quit()
            test_context.logger.info('Test Finalizer: Ending browser session.')
        else:
            test_context.logger.warning(
                'Test Finalizer: Attempted to finalise test but the session had already terminated.')

    @staticmethod
    def finalise_skygrid_driver_failure(driver, test_context):
        from pscore.clients.skygrid.api.skygridapiclient import SkyGridApiClient as ApiClient
        from pscore.clients.skygrid.metadata.skygridmetadataclient import SkyGridMetaDataClient as ArtefactsClient
        from pscore.clients.skygrid.dao.data import TestData, Log
        import time as t

        final_url = driver.current_url
        test_context.logger.info('Test Finalizer: Final url: ' + final_url)

        skygrid_hub_node = driver.wrapped_driver.active_node_ip()
        session_id = driver.session_id
        node_browser_version = driver.desired_capabilities['version']

        artefacts_client = ArtefactsClient(test_context.logger)
        grid_api_client = ApiClient(driver=driver)

        # upload screenshots taken by user
        artefacts_client.upload_screenshots(test_context.skygrid_screenshots)

        # upload final screenshot and kill driver
        screenshot = grid_api_client.take_screenshot()
        artefacts_client.upload_screenshot(screenshot.to_json())
        # MUST quit driver before uploading video, so video is finalized and ready to be copied
        driver.quit()

        # upload video
        video = grid_api_client.get_video()
        artefacts_client.upload_video(video.to_json())

        # upload test details
        with open('guid.txt') as f:
            guid = f.readline()

        test_session_guid = guid.strip()
        duration = int(t.time()) - test_context.start_time_seconds
        test_data = TestData(session_id, test_context.error_message, test_session_guid, test_context.test_name,
                             skygrid_hub_node, duration, browser_version=node_browser_version)
        artefacts_client.upload_test_details(test_data.to_json())

        # upload log
        log = Log(session_id, test_context.log_text)
        artefacts_client.upload_log(log.to_json())

        # output report URL
        test_report = artefacts_client.get_test_report_uri(session_id)
        session_report = artefacts_client.get_test_run_report_uri(test_session_guid)
        test_context.logger.info("This test report: <a href=\"{}\" target=\"_blank\">test</a>".format(test_report))
        test_context.logger.info(
            "This test session: <a href=\"{}\" target=\"_blank\">session</a>".format(session_report))
