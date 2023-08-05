import json
from datetime import datetime as dt
from ....config.test_configuration import TestConfiguration as config
import platform

# TODO bad OO, should have base class and subclass twice

class SGScreenShot(object):
    # A SkyGrid Screenshot object, for sending to artefact service

    def __init__(self, session_id, path, datetime):
        self.session_id = session_id
        self.path = path
        self.datetime = datetime

    def to_json(self):
        data = dict(session_id=self.session_id, path=self.path, datetime=self.datetime)
        return json.dumps(data)

    def to_dict(self):
        return dict(session_id=self.session_id, path=self.path, datetime=self.datetime)


class SGVideo(object):
    def __init__(self, session_id, path, datetime):
        self.session_id = session_id
        self.path = path
        self.datetime = datetime

    def to_json(self):
        data = dict(session_id=self.session_id, path=self.path, datetime=self.datetime)
        return json.dumps(data)


class TestData(object):
    def __init__(self, session_id, error, test_run_id, test_name, node, duration, browser_version):
        self.session_id = session_id
        self.error = error
        self.test_run_id = test_run_id
        self.test_name = test_name
        self.datetime = str(dt.now())
        self.node = node
        self.hub = config.get_hub_url()
        self.browser = config.get_browser()
        self.browser_version = browser_version
        self.operating_system = platform.platform()
        self.environment = config.get_user_id()
        self.duration = duration

    def to_json(self):
        data = dict(session_id=self.session_id, error=self.error, test_run_id=self.test_run_id,
                    test_name=self.test_name, datetime=self.datetime, node=self.node,
                    hub=self.hub, browser=self.browser, browser_version=self.browser_version,
                    operating_system=self.operating_system, environment=self.environment, duration=self.duration)
        return json.dumps(data)


class Log(object):
    def __init__(self, session_id, log):
        self.session_id = session_id
        self.log = log

    def to_json(self):
        data = dict(session_id=self.session_id, log=self.log)
        return json.dumps(data)
