"""Compile repository-owned rules without fetching any upstream list."""

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from test_build import ROOT, builder
from formats import sing_box

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
            raw.write_text('{\n// Source: https://example.com/\n"version": 2,\n'
                           '"rules": [/* repository-owned */ {"domain_suffix": ["example.com"]}]}')
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
                self.assertEqual(record["rule_object_count"], 1)
                self.assertEqual(record["match_entry_count"], 1)
                self.assertNotIn("download_url", record)
                verifier.verify(output, root / "sources")
                original = (output / "example.srs").read_bytes()
                raw.write_text(raw.read_text() + "\n// Reviewed source reference\n")
                with self.assertRaisesRegex(ValueError, "rebuild required"):
                    verifier.verify(output, root / "sources")
                builder.build(root / "sources", output, str(COMPILER))
                self.assertEqual((output / "example.srs").read_bytes(), original)
                self.assertEqual((output / "sources/example.json").read_bytes(), raw.read_bytes())
                verifier.verify(output, root / "sources")
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
            config = sing_box.load_config((ROOT / "rules/geosite-finance-us.json").read_text())
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
                "api.robinhood.com",
                "api-m.paypal.com", "www.paypalobjects.com",
                "cash-f.squarecdn.com",
                "navyfederal.lendkey.com", "creditkarmacdn-a.akamaihd.net",
                "onlinebanking.tdbank.com", "login.openbank.us", "my.equifax.com",
                "members.transunion.com", "firstcitizens.netxinvestor.com",
                "api-v2.chimebank.com", "secure.chasecdn.com", "www.wellsfargoadvisors.com",
                "www.wfafinet.com", "boa-api.arkoselabs.com", "fp.robinhood.net",
                "cash-images-f.squarecdn.com",
                "synchronybank-us.gw-dv.io",
                "vanguard.okta.com", "chaseretcalculator.moneyguidepro.com",
                "client.osaicinstitutions.com", "clientpoint.fisglobal.com",
                "www.centresuite.com", "secure.newportgroup.com",
                "app.rollovercentral.com", "finapp.synchrony.yodlee.com",
                "finapp.synchronyiav.yodlee.com",
                "www.citibankonline.com", "www.thankyou.com", "login.fidelityrewards.com",
                "online1.elancard.com", "www.myaccountaccess.com", "ccc.vgcontent.info",
                "finapp.wealthfront.yodlee.com",
                "firstcitizens.wealthaccess.com", "www.subarumotorsfinance.com",
                "money.x.com", "money-support.x.com", "sdn.money.x.com",
                "id.kraken.com", "app.kraken.com", "pro.kraken.com",
                "api.kraken.com", "ws-auth.kraken.com", "futures.kraken.com",
            ))
            # Explicitly excluded services must stay out of US egress routing,
            # including their account, trading and dedicated resource subdomains.
            for domain in (
                "csimfunds.com", "ibkr.com", "interactivebrokers.com",
                "schwab.com", "schwab529plan.com", "schwabcdn.com",
                "schwabfunds.com", "schwabinstitutional.com", "schwabplan.com",
                "schwabworkplaceservices.com", "thinkorswim.com", "transferwise.com", "wise.com",
            ):
                cases.extend(((domain, False), ("login." + domain, False)))
            cases.extend((host, False) for host in (
                "client.schwab.com", "client.schwabcdn.com", "trade.thinkorswim.com",
                "portal.interactivebrokers.com", "api.ibkr.com",
                "api.wise.com", "api.transferwise.com",
            ))
            # General-purpose shared hosts must not be routed as finance, even
            # when a financial login page references them. Consumer wallets and
            # card-network checkout pages, public financial SDKs, aggregators,
            # market-data feeds and unverified shared endpoints are excluded.
            cases.extend((host, False) for host in (
                "x-money-prod-safe-sensitive-documents.s3.us-west-2.amazonaws.com",
                "x-money-prod-sensitive-documents.s3.us-west-2.amazonaws.com",
                "x-money-transaction-documents-prod.s3.us-west-2.amazonaws.com",
                "x.com", "www.x.com", "api.x.com", "help.x.com", "twitter.com",
                "ton.twimg.com", "pbs.twimg.com", "abs.twimg.com", "xmoney.com",
                "notmoney.x.com", "money.x.com.example.org", "money-support-other.x.com",
                "amazonaws.com", "s3.us-west-2.amazonaws.com",
                "other-account-documents.s3.us-west-2.amazonaws.com",
                "aggapi.wealthaccess.com", "api.moscwise.com",
                "app.quovo.com", "billdetail.getbills.com",
                "cdn.plaid.com", "cdn.yodlee.com",
                "cdn1.onlineaccess1.com", "cds-sdkcfg.onlineaccess1.com",
                "content.mx.com", "fin02.finicity.com",
                "frontgate-us.factset.com", "log-d0b2efe1.us.v2.we-stats.com",
                "login.awardcenter.com", "partnerauth.platform.intuit.com",
                "production.plaid.com", "q2smart.q2ebanking.com",
                "sdk-cdn.onlineaccess1.com", "widgets.moneydesktop.com",
                "wup-d0b2efe1.us.v2.we-stats.com", "www.login.awardcenter.com",
                "0geo.cardinalcommerce.com", "1geo.cardinalcommerce.com", "api.braintreegateway.com",
                "api.stripe.com", "b.stripecdn.com", "braintree-api.com",
                "braintreegateway.com", "centinelapi.cardinalcommerce.com", "checkout.com",
                "geo.cardinalcommerce.com", "hostedfields.cardinalcommerce.com", "js.checkout.com",
                "payments.braintree-api.com", "pci-connect.squareup.com", "secure.paymentech.com",
                "songbird.cardinalcommerce.com", "static.client.cardinaltrusted.com", "stripe-camo.global.ssl.fastly.net",
                "stripe.com", "writer.cardinalcommerce.com",
                "applepay.cdn-apple.com", "pay.google.com",
                "secure.checkout.visa.com", "assets.secure.checkout.visa.com",
                "pay.discovernetwork.com",
                "aa.online-metrix.net", "accounts.google.com", "analytics.dv.socure.io",
                "api-js.datadome.co", "api.ipdata.co", "api.sardine.ai",
                "api.sjpf.io", "api.transmitsecurity.io", "appleid.apple.com",
                "appleid.cdn-apple.com", "att-device.proveapis.com", "auth.svcs.verizon.com",
                "challenges.cloudflare.com", "device.proveapis.com", "ds-aksb-a.akamaihd.net",
                "iframe.arkoselabs.com", "ingestion.dv.socure.io", "js.datadome.co",
                "mpsnare.iesnare.com", "network.dv.socure.io", "p11.techlab-cdn.com",
                "recaptcha.google.com", "snap.att.com", "snap.mobile.att.com",
                "snap.mobile.att.net", "tls-eun1.fpapi.io", "www.cdn-path.com",
                "www.google.com", "www.gstatic.com", "www.prod-cde.net",
                "www.wf-box.net",
                "cloudfront.net", "unrelated.cloudfront.net", "squarecdn.com",
                "other.squarecdn.com", "akamaihd.net", "other.akamaihd.net",
                "images.ctfassets.net", "google.com", "other.google.com", "example.okta.com",
                "lendkey.com", "other.lendkey.com", "netxinvestor.com", "other.netxinvestor.com",
                "other.oflows.net", "creditkarma.com.example.org", "notpaypal.com",
                "arkoselabs.com", "other-api.arkoselabs.com",
                "squareup.com", "pci-connect.squareupstaging.com", "cashstaging.app",
                "cardinalcommerce.com", "songbirdstag.cardinalcommerce.com",
                "cas.static.client.cardinaltrusted.com", "other.cardinaltrusted.com",
                "h.online-metrix.net", "transmitsecurity.io", "other.transmitsecurity.io",
                "datadome.co", "other.datadome.co", "other.cdn-path.com",
                "socure.io", "other.dv.socure.io", "synchronybankdev-us.gw-dv.io",
                "device.uat.proveapis.com", "sandbox.plaid.com", "www.test-cde.net",
                "qa-b.stripecdn.com", "rsn30-uat.ssnc-corp.cloud", "vanguardesf.oktapreview.com",
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
