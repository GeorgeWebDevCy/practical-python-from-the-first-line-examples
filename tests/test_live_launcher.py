from contextlib import redirect_stdout
from io import StringIO
import getpass
import unittest
from unittest.mock import patch

from examples.ch21 import live_launcher


class LiveLauncherTests(unittest.TestCase):
    def test_key_is_passed_only_in_child_environment(self):
        output = StringIO()
        with patch.object(live_launcher.getpass, 'getpass', return_value='fake-test-secret'), \
             patch('builtins.input', return_value='fixture-model'), \
             patch.object(live_launcher.subprocess, 'run') as run, redirect_stdout(output):
            run.return_value.returncode = 0
            self.assertEqual(live_launcher.main(), 0)
        args, kwargs = run.call_args
        self.assertNotIn('fake-test-secret', repr(args))
        self.assertEqual(kwargs['env']['OPENAI_API_KEY'], 'fake-test-secret')
        self.assertEqual(kwargs['env']['OPENAI_MODEL'], 'fixture-model')
        self.assertNotIn('fake-test-secret', output.getvalue())

    def test_missing_or_visible_input_never_starts_child(self):
        with patch.object(live_launcher.getpass, 'getpass', side_effect=getpass.GetPassWarning), \
             patch.object(live_launcher.subprocess, 'run') as run, redirect_stdout(StringIO()):
            self.assertEqual(live_launcher.main(), 1)
            run.assert_not_called()
        with patch.object(live_launcher.getpass, 'getpass', return_value=''), \
             patch('builtins.input', return_value='fixture-model'), \
             patch.object(live_launcher.subprocess, 'run') as run, redirect_stdout(StringIO()):
            self.assertEqual(live_launcher.main(), 1)
            run.assert_not_called()
