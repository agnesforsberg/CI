import unittest
import requests
from src.CI import app


class TestCheckCommit(unittest.TestCase):
    def test_check(self):
        with open("/tmp/auth") as f:
            auth = f.read().strip()

            sha = "976fd7f5f2024665c5363cab2b35b4efc0ea3d53"
            payload = {
                "repository": {
                    "full_name": "agnesforsberg/CI"
                },
                "after": sha
            }

            headers = {
                'Authorization': 'Bearer ' + auth
            }
            get_url = "https://api.github.com/repos/agnesforsberg/CI/commits/{sha}/status".format(sha=sha)
            
            app.update_status(payload, 'asdf', sha, status="success")
            res = requests.get(get_url, headers=headers)
            ctx = res.json()
            self.assertEqual(ctx['state'], "success")

            app.update_status(payload, 'asdf', sha, status="pending")
            res = requests.get(get_url, headers=headers)
            ctx = res.json()
            self.assertEquals(ctx['state'], "pending")