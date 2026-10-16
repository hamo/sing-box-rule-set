# sing-box rule sets

此分支由 GitHub Actions 自动生成。转换代码和使用说明见本仓库的 `main` 分支。

| 规则集 | 二进制订阅 | 上游原文件 | 上游 |
| --- | --- | --- | --- |
| OISD big | [oisd-big.srs](oisd-big.srs) | [oisd-big.txt](sources/oisd-big.txt) | <https://big.oisd.nl/> |
| OISD small | [oisd-small.srs](oisd-small.srs) | [oisd-small.txt](sources/oisd-small.txt) | <https://small.oisd.nl/> |
| AWAvenue 完整防护 | [awavenue.srs](awavenue.srs) | [awavenue.json](sources/awavenue.json) | [官方 JSON](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Singbox.json) |
| AWAvenue 仅广告 | [awavenue-only-ads.srs](awavenue-only-ads.srs) | [awavenue-only-ads.json](sources/awavenue-only-ads.json) | [官方 JSON](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Singbox-Only.Ads.json) |
| AWAvenue 不含隐私 | [awavenue-no-privacy.srs](awavenue-no-privacy.srs) | [awavenue-no-privacy.json](sources/awavenue-no-privacy.json) | [官方 JSON](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Singbox-No.Privacy.json) |
| AWAvenue 不含不受欢迎 | [awavenue-no-unwelcome.srs](awavenue-no-unwelcome.srs) | [awavenue-no-unwelcome.json](sources/awavenue-no-unwelcome.json) | [官方 JSON](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Singbox-No.Unwelcome.json) |
| HaGeZi TIF Full | [hagezi-tif-full.srs](hagezi-tif-full.srs) | [hagezi-tif-full.txt](sources/hagezi-tif-full.txt) | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/tif.txt) |

当前提供的 SRS 格式版本均为 2，要求 sing-box 1.10.0+。
AWAvenue 原始 JSON 为版本 3，官方编译器根据实际字段生成版本 2 的 SRS。
big 已包含 small，选用其中一个即可。
AWAvenue 四种变体选用其中一个：完整防护为广告＋隐私＋不受欢迎；仅广告为最小集合；
不含隐私为广告＋不受欢迎；不含不受欢迎为广告＋隐私。

[metadata.json](metadata.json) 记录上游版本、规则数量、编译器版本和 SHA-256。
`sources/` 保存本次构建使用的完整上游原文件。OISD 和 HaGeZi TIF Full 使用 sing-box 官方
`rule-set convert --type adguard` 直接生成 `.srs`，保留原生 AdGuard 匹配语义。
这两组订阅的上游文件均声明为 Adblock 格式，构建配置和 `metadata.json` 使用
`format: "adblock"`；它是 `adguard` 转换器的别名。
AdGuard 二进制规则无法反编译成普通规则集 JSON，请通过原始 `.txt` 审阅来源。
AWAvenue 四种变体直接编译官方 sing-box JSON，保留原始匹配字段及语义，可通过 `.json` 审阅来源。

本项目不是 OISD 官方项目。OISD 由 Stephan van Ruth 维护，来源：<https://oisd.nl/>。
OISD 规则及衍生文件遵循 [GNU GPL v3](LICENSE)，原始声明保留在 `sources/` 中。

AWAvenue 秋风广告规则由 [TG-Twilight/AWAvenue-Ads-Rule](https://github.com/TG-Twilight/AWAvenue-Ads-Rule)
维护，规则及衍生文件遵循 [GNU GPL v3](LICENSE)，
[上游许可证](https://github.com/TG-Twilight/AWAvenue-Ads-Rule/blob/main/LICENSE)及原始 JSON 来源可供查阅。

HaGeZi TIF Full 由 [hagezi/dns-blocklists](https://github.com/hagezi/dns-blocklists#tif) 维护，
规则及衍生文件遵循 [GNU GPL v3](LICENSE)，
[上游许可证](https://github.com/hagezi/dns-blocklists/blob/main/LICENSE)及作者声明保留在原始列表中。
