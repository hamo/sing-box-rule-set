"""Compile repository-owned rules without fetching any upstream list."""

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from test_build import ROOT, builder

COMPILER = ROOT / ".tools/sing-box"
spec = importlib.util.spec_from_file_location("custom_verify", ROOT / "scripts/verify-build.py")
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


@unittest.skipUnless(COMPILER.is_file(), "Run scripts/install-sing-box.py first")
class CustomTests(unittest.TestCase):
    def test_local_build_preserves_source_and_rejects_stale_or_invalid_updates(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "sources").mkdir()
            (root / "rules").mkdir()
            (root / "docs").mkdir()
            (root / "docs/rule-set-README.md").write_text("custom rules\n")
            (root / "LICENSE").write_text("fixture license\n")
            raw = root / "rules/example.json"
            raw.write_text(json.dumps({"version": 2, "rules": [{"domain_suffix": ["example.com"]}]}))
            config = {"name": "example", "path": "rules/example.json", "format": "sing-box"}
            (root / "sources/custom.json").write_text(json.dumps({"sources": [config]}))
            output = root / "output"
            with patch.object(builder, "ROOT", root), patch.object(builder, "download") as download:
                builder.build(root / "sources", output, str(COMPILER))
                download.assert_not_called()
                self.assertEqual((output / "sources/example.json").read_bytes(), raw.read_bytes())
                record = json.loads((output / "metadata.json").read_text())["sources"][0]
                self.assertEqual(record["source_type"], "local")
                self.assertEqual(record["path"], config["path"])
                self.assertNotIn("download_url", record)
                verifier.verify(output, root / "sources")
                original = (output / "example.srs").read_bytes()
                raw.write_text(json.dumps({"version": 2, "rules": [{"domain_suffix": ["example.net"]}]}))
                with self.assertRaisesRegex(ValueError, "rebuild required"):
                    verifier.verify(output, root / "sources")
                builder.build(root / "sources", output, str(COMPILER))
                self.assertNotEqual((output / "example.srs").read_bytes(), original)
                verifier.verify(output, root / "sources")
                previous = (output / "example.srs").read_bytes()
                raw.write_text("invalid JSON")
                with self.assertRaises(ValueError):
                    builder.build(root / "sources", output, str(COMPILER))
                self.assertEqual((output / "example.srs").read_bytes(), previous)

    def test_finance_domains_and_subdomains_match_with_strict_suffix_boundaries(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "build"
            with patch.object(builder, "download") as download:
                builder.build(ROOT / "sources", output, str(COMPILER), ["custom"])
                download.assert_not_called()
            verifier.verify(output, ROOT / "sources", ["custom"])
            config = json.loads((ROOT / "rules/geosite-finance-us.json").read_text())
            domains = [domain for rule in config["rules"] for domain in rule.get("domain_suffix", [])]
            hosts = [host for rule in config["rules"] for host in rule.get("domain", [])]
            self.assertEqual(len(domains), len(set(domains)))
            self.assertEqual(len(hosts), len(set(hosts)))
            cases = []
            for rule in config["rules"]:
                for entries in rule.values():
                    self.assertEqual(entries, sorted(entries))
            for domain in domains:
                cases.extend(((domain, True), ("login." + domain, True),
                              ("not" + domain, False), (domain + ".example.org", False)))
            for host in hosts:
                self.assertFalse(any(host == domain or host.endswith("." + domain) for domain in domains))
                cases.extend(((host, True), ("other." + host, False),
                              ("not" + host, False), (host + ".example.org", False)))
            # Real service endpoints catch missing independent domains, rather than
            # deriving every positive case from the rule file under test.
            cases.extend((host, True) for host in (
                "secure.bankofamerica.com", "api1.bac-assets.com", "secure.chase.com",
                "apix.chase.com", "online.citi.com", "www.citizensbankonline.com",
                "mobile.usaa.com", "api-a.usaa.com", "c1.wfinterface.com",
                "www17.wellsfargomedia.com", "cdaas.aexp.com", "www.aexp-static.com",
                "consumercenter.mysynchrony.com", "api.syf.com", "cdn2.etrade.net",
                "login.fidelity.com", "netbenefits.fidelity.com", "www.netbenefits.com",
                "client.schwabcdn.com", "trade.thinkorswim.com", "api.robinhood.com",
                "api-m.paypal.com", "www.paypalobjects.com", "api.braintreegateway.com",
                "payments.braintree-api.com", "cash-f.squarecdn.com",
                "navyfederal.lendkey.com", "creditkarmacdn-a.akamaihd.net",
                "onlinebanking.tdbank.com", "login.openbank.us", "my.equifax.com",
                "members.transunion.com", "firstcitizens.netxinvestor.com",
                "api-v2.chimebank.com", "secure.chasecdn.com", "www.wellsfargoadvisors.com",
                "www.wfafinet.com", "boa-api.arkoselabs.com", "fp.robinhood.net",
                "cash-images-f.squarecdn.com", "pci-connect.squareup.com",
                "centinelapi.cardinalcommerce.com", "geo.cardinalcommerce.com",
                "0geo.cardinalcommerce.com", "1geo.cardinalcommerce.com",
                "hostedfields.cardinalcommerce.com", "writer.cardinalcommerce.com",
                "songbird.cardinalcommerce.com", "static.client.cardinaltrusted.com",
                "applepay.cdn-apple.com", "pay.google.com", "secure.checkout.visa.com",
                "assets.secure.checkout.visa.com", "pay.discovernetwork.com",
            ))
            cases.extend((host, False) for host in (
                "cloudfront.net", "unrelated.cloudfront.net", "squarecdn.com",
                "other.squarecdn.com", "akamaihd.net", "other.akamaihd.net",
                "images.ctfassets.net", "www.google.com", "www.gstatic.com", "example.okta.com",
                "lendkey.com", "other.lendkey.com", "netxinvestor.com", "other.netxinvestor.com",
                "other.oflows.net", "creditkarma.com.example.org", "notpaypal.com",
                "arkoselabs.com", "other-api.arkoselabs.com", "iframe.arkoselabs.com",
                "squareup.com", "pci-connect.squareupstaging.com", "cashstaging.app",
                "cardinalcommerce.com", "songbirdstag.cardinalcommerce.com",
                "cas.static.client.cardinaltrusted.com", "other.cardinaltrusted.com",
                "www.cdn-path.com", "api.transmitsecurity.io", "api.sjpf.io",
                "h.online-metrix.net", "js.datadome.co", "api-js.datadome.co",
                "www.apple.com", "cdn-apple.com", "other.cdn-apple.com",
            ))
            for candidate, expected in cases:
                with self.subTest(domain=candidate):
                    result = subprocess.check_output([
                        str(COMPILER), "rule-set", "match", "--format", "binary",
                        str(output / "geosite-finance-us.srs"), candidate,
                    ], text=True, stderr=subprocess.STDOUT)
                    self.assertEqual("match rules." in result, expected)


if __name__ == "__main__":
    unittest.main()
