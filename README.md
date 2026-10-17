# sing-box-rule-set

通过 GitHub Actions 将上游列表和仓库内自定义规则编译为 sing-box `.srs`，当前提供 24 个规则集。

## 规则集

| 规则集 | 来源 | format | 订阅（SRS） | 用途 |
| --- | --- | --- | --- | --- |
| OISD big | <https://big.oisd.nl/> | `adblock` | [oisd-big.srs](https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/oisd-big.srs) | 广告、跟踪、恶意域名等 |
| OISD small | <https://small.oisd.nl/> | `adblock` | [oisd-small.srs](https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/oisd-small.srs) | 以广告拦截为主的较小版本 |
| AWAvenue 完整防护 | [官方 JSON](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Singbox.json) | `sing-box` | [awavenue.srs](https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/awavenue.srs) | 广告＋隐私＋不受欢迎 |
| AWAvenue 仅广告 | [官方 JSON](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Singbox-Only.Ads.json) | `sing-box` | [awavenue-only-ads.srs](https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/awavenue-only-ads.srs) | 仅广告 |
| AWAvenue 不含隐私 | [官方 JSON](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Singbox-No.Privacy.json) | `sing-box` | [awavenue-no-privacy.srs](https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/awavenue-no-privacy.srs) | 广告＋不受欢迎 |
| AWAvenue 不含不受欢迎 | [官方 JSON](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Singbox-No.Unwelcome.json) | `sing-box` | [awavenue-no-unwelcome.srs](https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/awavenue-no-unwelcome.srs) | 广告＋隐私 |
| HaGeZi TIF Full | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/tif.txt) | `adblock` | [hagezi-tif-full.srs](https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-tif-full.srs) | 恶意软件、钓鱼、诈骗、挖矿等威胁域名 |
| HaGeZi Pro | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt) | `adblock` | [hagezi-pro.srs](https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-pro.srs) | 综合广告、跟踪、遥测和恶意域名 |
| HaGeZi TIF Medium | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/tif.medium.txt) | `adblock` | [hagezi-tif-medium.srs](https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-tif-medium.srs) | 威胁防护中等版本 |
| HaGeZi TIF Mini | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/tif.mini.txt) | `adblock` | [hagezi-tif-mini.srs](https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-tif-mini.srs) | 威胁防护精简版本 |
| HaGeZi Native Amazon | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.amazon.txt) | `adblock` | [hagezi-native-amazon.srs](https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-native-amazon.srs) | Amazon 设备及服务的内置跟踪 |
| HaGeZi Native Apple | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.apple.txt) | `adblock` | [hagezi-native-apple.srs](https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-native-apple.srs) | iOS、macOS、tvOS 内置跟踪 |
| HaGeZi Native Huawei | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.huawei.txt) | `adblock` | [hagezi-native-huawei.srs](https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-native-huawei.srs) | 华为设备内置跟踪 |
| HaGeZi Native Microsoft | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.winoffice.txt) | `adblock` | [hagezi-native-microsoft.srs](https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-native-microsoft.srs) | Windows、Office、MSN 内置跟踪 |
| HaGeZi Native Samsung | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.samsung.txt) | `adblock` | [hagezi-native-samsung.srs](https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-native-samsung.srs) | 三星设备内置跟踪 |
| HaGeZi Native TikTok | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.tiktok.txt) | `adblock` | [hagezi-native-tiktok.srs](https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-native-tiktok.srs) | TikTok 指纹跟踪 |
| HaGeZi Native TikTok Aggressive | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.tiktok.extended.txt) | `adblock` | [hagezi-native-tiktok-aggressive.srs](https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-native-tiktok-aggressive.srs) | TikTok 指纹跟踪激进版本 |
| HaGeZi Native LG webOS | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.lgwebos.txt) | `adblock` | [hagezi-native-lgwebos.srs](https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-native-lgwebos.srs) | LG webOS 内置跟踪 |
| HaGeZi Native Roku | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.roku.txt) | `adblock` | [hagezi-native-roku.srs](https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-native-roku.srs) | Roku 内置跟踪 |
| HaGeZi Native Vivo | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.vivo.txt) | `adblock` | [hagezi-native-vivo.srs](https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-native-vivo.srs) | Vivo 设备内置跟踪 |
| HaGeZi Native OPPO/Realme | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.oppo-realme.txt) | `adblock` | [hagezi-native-oppo-realme.srs](https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-native-oppo-realme.srs) | OPPO、Realme 设备内置跟踪 |
| HaGeZi Native Xiaomi | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.xiaomi.txt) | `adblock` | [hagezi-native-xiaomi.srs](https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-native-xiaomi.srs) | 小米设备内置跟踪 |
| AdGuard DNS Filter | [官方 DNS Filter](https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt) | `adguard` | [adguard-dns-filter.srs](https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/adguard-dns-filter.srs) | 针对 DNS 优化的综合广告和跟踪拦截 |
| 美国个人金融服务 | [本仓库 JSON](https://raw.githubusercontent.com/hamo/sing-box-rule-set/main/rules/geosite-finance-us.json) | `sing-box` | [geosite-finance-us.srs](https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/geosite-finance-us.srs) | 银行、信用卡、投资、支付及消费金融域名分类，用于分流 |

### 规则选择

- 综合广告拦截：OISD、HaGeZi Pro、AdGuard DNS Filter 先选一个；秋风按需补充。
- OISD big 已包含 small；AWAvenue 四种变体选一个。「不受欢迎」包括强制更新、PCDN、推送等规则。
- 威胁防护：HaGeZi TIF Full / Medium / Mini 三选一，后两者为轻量版本。
- Native Tracker 按设备或服务选择，可能影响相关功能；TikTok 普通版与 Aggressive 版选一个。
- `geosite-finance-us` 用于金融流量分流，范围与维护方式见 [自定义规则说明](rules/README.md)。

## 在 sing-box 中使用

点击上表的 SRS 链接订阅；Fork 后将 URL 中的 `hamo/sing-box-rule-set` 换成自己的仓库名。
以下片段适用于 sing-box 1.11.0+，需合并到现有配置。当前 SRS 格式版本均为 2，可由 sing-box 1.10.0+ 加载。

在 `route.rule_set` 中注册远程规则集，替换名称即可使用其他列表：

```json
{
  "type": "remote",
  "tag": "oisd-big",
  "format": "binary",
  "url": "https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/oisd-big.srs",
  "update_interval": "6h"
}
```

广告规则在 `dns.rules` 中引用，放在兜底规则之前：

```json
{
  "rule_set": ["oisd-big"],
  "action": "reject"
}
```

金融分流先按同样方式注册 `geosite-finance-us`，再在 `route.rules` 的兜底规则之前指定已有出站：

```json
{
  "rule_set": ["geosite-finance-us"],
  "action": "route",
  "outbound": "US-FINANCE"
}
```

将 `US-FINANCE` 换成自己的出站标签。金融集合不用于广告拦截。
仅注册 `rule_set` 不会自动生效；建议启用 `experimental.cache_file.enabled` 缓存远程规则集。

## 启用自动更新

1. 将项目推送到 GitHub，默认分支为 `main`；Fork 后在 Actions 页面启用工作流。
2. 在 **Actions → Update rule sets → Run workflow** 运行首次构建。
3. 成功后订阅 `rule-set` 分支，之后每 6 小时更新一次。

计划时间为 UTC `00:23 / 06:23 / 12:23 / 18:23`，即北京时间 `02:23 / 08:23 / 14:23 / 20:23`；定时任务可能延迟。
修改规则、来源配置、构建脚本或发布模板也会触发更新。长期无活动的公开仓库若被停用定时任务，可在 Actions 页面重新启用。

工作流使用内置 `GITHUB_TOKEN`，已声明 `contents: write`，无需 PAT 或额外 Secret。
仓库 / 组织策略需允许工作流写入 `rule-set` 分支。仅 `main` 可以发布；其他分支的手动运行只构建和上传 artifact。
PR 的 CI 执行转换、匹配和本地发布测试，不下载上游列表。

### 构建与发布校验

```text
sources/*.json → 下载远端 / 复制仓库文件 → 按 format 转换 → 校验 → 实际加载 → rule-set 分支
```

- 编译器版本固定，下载包校验 SHA-256；下载支持重试、超时及配置的备用地址。
- 转换前校验格式、声明条目数和最小规则数量，转换后核对数量、文件哈希和 SRS 版本。
- 实际启动 sing-box 加载全部 SRS，初始化成功并正常退出后才能发布。
- 任一来源失败均保留上一版；本地构建也不会用半成品覆盖已有结果。
- 通过普通 Git 提交和推送保留发布历史，内容相同则不提交。

发布分支保存 `.srs`、完整来源原文件、`LICENSE` 和 `metadata.json`。
元数据记录编译器、来源版本、规则数量、实际下载地址及 SHA-256；本地来源记录 `source_type: "local"` 和仓库路径。
修改本地原文或注释后必须重建，发布校验会拒绝与当前 checkout 不一致的旧产物。

## 本地运行

需要 Python 3.9+、curl 和 Git。安装脚本支持 Linux / macOS 的 amd64、arm64。

```sh
python3 scripts/install-sing-box.py
python3 -m unittest discover -s tests -v
python3 scripts/build.py
python3 scripts/verify-build.py build
python3 scripts/check-srs-load.py build
```

产物位于 `build/`。可用 `--sing-box /absolute/path/to/sing-box` 指定已有编译器。
仅构建某个来源组时使用独立输出目录，避免替换其他来源的产物：

```sh
python3 scripts/build.py --source oisd --output build-oisd
```

`--source` 可重复传入，`--upstream` 是兼容别名；校验部分构建时，`verify-build.py` 也须传入相同的 `--source`。
仅构建仓库规则见 [rules/README.md](rules/README.md#维护方式)。
自动发布始终构建全部来源。

## 添加其他来源

在 `sources/*.json` 的 `sources` 数组中添加记录。远端列表使用 `url`，仓库规则使用 `path`，转换逻辑由 `format` 决定：

```json
{
  "sources": [
    {
      "name": "example-list",
      "url": "https://example.com/list.txt",
      "format": "adblock"
    },
    {
      "name": "geosite-finance-us",
      "path": "rules/geosite-finance-us.json",
      "format": "sing-box"
    }
  ]
}
```

| 字段 | 说明 |
| --- | --- |
| `name` | 全局唯一的输出名称 |
| `url` / `path` | 二选一；URL 必须为 HTTPS，本地路径相对仓库根目录且必须位于 `rules/` 内，不能通过符号链接越界 |
| `format` | 下表中的输入格式 |
| `fallback_urls` | 可选 HTTPS 备用地址数组，主地址下载失败时依次尝试；不适用于本地来源 |
| `min_rules` | 默认 1；文本格式统计非注释规则行，sing-box JSON 统计顶层 `rules` 对象数 |
| `validation` | AdGuard / Adblock 列表的可选声明式校验，见下文 |

| format | 输入 | 转换工具 | 来源原文 |
| --- | --- | --- | --- |
| `adguard` | AdGuard 兼容 DNS 列表 | `sing-box rule-set convert --type adguard` | `sources/<name>.txt` |
| `adblock` | `adguard` 的别名，兼容的 Adblock 风格 DNS 列表 | 同上 | `sources/<name>.txt` |
| `sing-box` | sing-box source-format JSON，支持 `//` 和 `/* ... */` 注释，不使用尾随逗号 | `sing-box rule-set compile` | `sources/<name>.json`，保留注释 |

OISD 声明 `Syntax: Adblock Plus Filter List`，HaGeZi 声明 `Syntax: AdBlock`，均配置为 `adblock`；
AdGuard DNS Filter 配置为 `adguard`。AWAvenue 直接编译官方 JSON，保留原始匹配字段；
其源格式版本 3 编译为当前 SRS 版本 2，源版本和实际 SRS 版本分别记录在元数据中。

### AdGuard / Adblock 语法范围

两种格式复用同一转换器。订阅头 `[Adblock Plus]` 不表示支持全部浏览器过滤语法。
支持范围以固定版本的 [sing-box AdGuard DNS 转换器](https://sing-box.sagernet.org/configuration/rule-set/adguard/) 为准：

| 规则类型 | 示例 / 说明 |
| --- | --- |
| 域名、子域名与例外 | `\|\|example.com^`、`@@\|\|allowed.example.com^` |
| 通配符 | `\|\|track*.example.com^` |
| 域名正则 | `/ads[0-9]+\.example\.com/`，受转换器及正则引擎限制 |
| 修饰符 | `$important`；其他修饰符须确认官方支持范围 |
| 取消规则 | DNS `$badfilter` 在编译前取消文本相同的规则，支持与 `$important` 组合；不支持 `$domain` 等部分取消语法 |
| 简单域名片段 | 无修饰符的 `\|\|countly-`、`-ad123-` 及其 `@@` 例外，编译前改写为等价域名正则 |
| 注释与订阅头 | 注释不计入规则数量；已识别的订阅头仅从转换输入移除，来源原文保持完整 |

片段改写仅适用于 `||label-`（字母 / 数字开头的标签前缀）和 `-word-`（字母、数字、连字符组成的关键词）。
例如 `||countly-` → `/(?i)(^|\.)countly-/`，`-ad123-` → `/(?i)-ad123-/`。
先处理 `$badfilter`，再改写片段，保留大小写不敏感、标签边界和例外语义；已有正则、带修饰符规则及 IP 不参与改写。

CSS 元素隐藏、脚本注入、URL 路径 / 端口 / 查询参数及 `$script`、`$image`、`$third-party` 等浏览器语法不受支持。
`$dnsrewrite=0.0.0.0` 可被官方转换器接受，但只保留匹配逻辑，SRS 不包含 DNS 改写动作。
AdGuard 二进制规则不能反编译为普通规则集 JSON，请通过发布分支的原始 `.txt` 审阅来源。

### 不兼容规则与元数据

默认 `unsupported_policy: "error"`：编译器跳过规则即构建失败。
显式配置 `"report"` 时必须提供正整数 `max_skipped_rules`，仅发布兼容部分；不支持的 `$badfilter` 组合仍然失败。
AdGuard DNS Filter 采用报告模式，上限 200 条；其原文中的少量 IP 规则和 IP / URL 正则会跳过。

`metadata.json` 的 `rule_count` 保存原始规则行数，`conversion` 记录实际编译数量、取消指令、被取消规则、
`rewritten_rules` 改写映射及 `skipped_rules` 逐条原因。计数必须与输入一致，成功数量不得低于 `min_rules`；
改写成功的规则计入编译数量。Actions 摘要展示这些信息，订阅头部元数据不会被内嵌子列表覆盖。

### 声明式校验与新格式

`validation` 可包含以下选项，未配置时不要求特定上游的文件头：

| 选项 | 示例 | 作用 |
| --- | --- | --- |
| `headers` | `["[Adblock Plus]"]` | 文件首行须为其中一个订阅头 |
| `title_prefix` | `"Example List"` | `Title` 须以该文本开头 |
| `count_field` | `"entries"` / `"Number of entries"` | 指定注释字段必须存在，且声明条目数与实际规则行数一致；字段名忽略大小写 |

新增输入格式时，在 `scripts/formats/` 实现 `validate(source)`、`convert(raw, output, compiler, source)`，
声明 `EXTENSION`，再到 `formats/__init__.py` 注册。上游名称不参与转换逻辑；新增来源或格式时同步补充测试、订阅说明和授权声明。

## 来源与许可证

本项目为独立的格式转换与分发项目，代码及仓库自定义规则采用 [GPL-3.0](LICENSE)。
上游规则及其转换产物遵循各自的 GPL v3 许可证，完整原文及作者声明保留在发布分支的 `sources/` 中。

| 上游 / 维护者 | 许可证 |
| --- | --- |
| OISD / Stephan van Ruth | [GPL v3](https://github.com/sjhgvr/oisd/blob/main/LICENSE) |
| [AWAvenue / TG-Twilight](https://github.com/TG-Twilight/AWAvenue-Ads-Rule) | [GPL v3](https://github.com/TG-Twilight/AWAvenue-Ads-Rule/blob/main/LICENSE) |
| [HaGeZi](https://github.com/hagezi/dns-blocklists) | [GPL v3](https://github.com/hagezi/dns-blocklists/blob/main/LICENSE) |
| [AdGuard DNS Filter](https://github.com/AdguardTeam/AdGuardSDNSFilter) | [GPL v3](https://github.com/AdguardTeam/AdGuardSDNSFilter/blob/master/LICENSE) |
