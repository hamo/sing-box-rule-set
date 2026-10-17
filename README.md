# sing-box-rule-set

通过 GitHub Actions 自动下载上游规则或读取仓库内自定义规则，转换为 sing-box 的 `.srs` 二进制规则集。
支持 **OISD big/small**、**AWAvenue 秋风广告规则的全部四种变体**、**HaGeZi Pro**、
**HaGeZi TIF Full/Medium/Mini**、**HaGeZi Native Tracker 全部 12 个列表**、**AdGuard DNS Filter**及本仓库维护的 **geosite-finance-us**，共 24 个规则集。

| 规则集 | 来源 | format | 输出 | 用途 |
| --- | --- | --- | --- | --- |
| OISD big | <https://big.oisd.nl/> | `adblock` | `oisd-big.srs` | 广告、跟踪、恶意域名等 |
| OISD small | <https://small.oisd.nl/> | `adblock` | `oisd-small.srs` | 以广告拦截为主的较小版本 |
| AWAvenue 完整防护 | [官方 JSON](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Singbox.json) | `sing-box` | `awavenue.srs` | 广告＋隐私＋不受欢迎 |
| AWAvenue 仅广告 | [官方 JSON](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Singbox-Only.Ads.json) | `sing-box` | `awavenue-only-ads.srs` | 仅广告 |
| AWAvenue 不含隐私 | [官方 JSON](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Singbox-No.Privacy.json) | `sing-box` | `awavenue-no-privacy.srs` | 广告＋不受欢迎 |
| AWAvenue 不含不受欢迎 | [官方 JSON](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Singbox-No.Unwelcome.json) | `sing-box` | `awavenue-no-unwelcome.srs` | 广告＋隐私 |
| HaGeZi TIF Full | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/tif.txt) | `adblock` | `hagezi-tif-full.srs` | 恶意软件、钓鱼、诈骗、挖矿等威胁域名 |
| HaGeZi Pro | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt) | `adblock` | `hagezi-pro.srs` | 综合广告、跟踪、遥测和恶意域名 |
| HaGeZi TIF Medium | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/tif.medium.txt) | `adblock` | `hagezi-tif-medium.srs` | 威胁防护中等版本 |
| HaGeZi TIF Mini | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/tif.mini.txt) | `adblock` | `hagezi-tif-mini.srs` | 威胁防护精简版本 |
| HaGeZi Native Amazon | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.amazon.txt) | `adblock` | `hagezi-native-amazon.srs` | Amazon 设备及服务的内置跟踪 |
| HaGeZi Native Apple | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.apple.txt) | `adblock` | `hagezi-native-apple.srs` | iOS、macOS、tvOS 内置跟踪 |
| HaGeZi Native Huawei | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.huawei.txt) | `adblock` | `hagezi-native-huawei.srs` | 华为设备内置跟踪 |
| HaGeZi Native Microsoft | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.winoffice.txt) | `adblock` | `hagezi-native-microsoft.srs` | Windows、Office、MSN 内置跟踪 |
| HaGeZi Native Samsung | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.samsung.txt) | `adblock` | `hagezi-native-samsung.srs` | 三星设备内置跟踪 |
| HaGeZi Native TikTok | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.tiktok.txt) | `adblock` | `hagezi-native-tiktok.srs` | TikTok 指纹跟踪 |
| HaGeZi Native TikTok Aggressive | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.tiktok.extended.txt) | `adblock` | `hagezi-native-tiktok-aggressive.srs` | TikTok 指纹跟踪激进版本 |
| HaGeZi Native LG webOS | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.lgwebos.txt) | `adblock` | `hagezi-native-lgwebos.srs` | LG webOS 内置跟踪 |
| HaGeZi Native Roku | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.roku.txt) | `adblock` | `hagezi-native-roku.srs` | Roku 内置跟踪 |
| HaGeZi Native Vivo | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.vivo.txt) | `adblock` | `hagezi-native-vivo.srs` | Vivo 设备内置跟踪 |
| HaGeZi Native OPPO/Realme | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.oppo-realme.txt) | `adblock` | `hagezi-native-oppo-realme.srs` | OPPO、Realme 设备内置跟踪 |
| HaGeZi Native Xiaomi | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.xiaomi.txt) | `adblock` | `hagezi-native-xiaomi.srs` | 小米设备内置跟踪 |
| AdGuard DNS Filter | [官方 DNS Filter](https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt) | `adguard` | `adguard-dns-filter.srs` | 针对 DNS 优化的综合广告和跟踪拦截 |
| 美国个人金融服务 | [本仓库 JSON](https://raw.githubusercontent.com/hamo/sing-box-rule-set/main/rules/geosite-finance-us.json) | `sing-box` | `geosite-finance-us.srs` | 银行、信用卡、投资、支付及消费金融域名分类，用于分流 |

big 包含 small，选择一个即可。规则说明见 [OISD 官网](https://oisd.nl/)。
OISD big/small 的文件头为 `[Adblock Plus]`，声明 `Syntax: Adblock Plus Filter List`，
因此配置使用 `format: "adblock"`。官方也为 [AdGuard Home](https://oisd.nl/setup/adguardhome)
提供同一组订阅地址，表示规则可被 AdGuard 使用。
AWAvenue 使用 [官方仓库](https://github.com/TG-Twilight/AWAvenue-Ads-Rule) 的四种 sing-box JSON，
通过通用 `sing-box` 格式转换器编译，保留精确域名、域名后缀和关键词的原始匹配语义。
四种变体选用其中一个即可；「不受欢迎」包含强制更新、PCDN、推送等规则。
HaGeZi 提供 [Pro](https://github.com/hagezi/dns-blocklists#pro)、
[Threat Intelligence Feeds 的 Full/Medium/Mini](https://github.com/hagezi/dns-blocklists#tif)
及 [Native Tracker 全部设备/服务列表](https://github.com/hagezi/dns-blocklists#native)。
这些上游文件声明 `Syntax: AdBlock`，配置使用 `adblock`，并校验 `Number of entries` 与实际规则行数。
[AdGuard DNS Filter](https://github.com/AdguardTeam/AdGuardSDNSFilter) 是针对 DNS 过滤优化的综合列表，
配置使用 `adguard`，校验标题和最小规则数量；本项目发布其 sing-box 兼容部分。
转换前将 `||countly-`、`-ad123-` 等简单域名片段改写为等价的域名正则，
保留大小写不敏感、域名标签边界及例外语义；改写前后内容记录在 `conversion.rewritten_rules`。
官方原文件含少量 sing-box 不支持的 IP 规则及 IP/URL 正则，跳过条目和原因逐项记录在
`metadata.json` 的 `conversion.skipped_rules` 及 Actions 构建摘要中。
AdGuard DNS Filter 显式配置 `unsupported_policy: "report"`，最多允许跳过 200 条；超过上限即失败。
OISD、HaGeZi 和 AdGuard DNS Filter 都使用 sing-box 的 `adguard` 转换器；
配置中的格式名描述上游数据，转换命令保持 `--type adguard`。

综合广告列表可先在 OISD、HaGeZi Pro、AdGuard DNS Filter 中选择一个，秋风按需补充。
TIF Full/Medium/Mini 三选一；Medium/Mini 为轻量替代版本。
Native Tracker 按设备或服务选择，部分规则可能影响相关功能；TikTok 普通版与 Aggressive 版选一个。

`geosite-finance-us` 为本仓库手工维护的分类规则，覆盖美国面向个人的银行与金融服务，
用于 `route.rules` 分流，勿加入广告拦截列表。来源和收录范围见 [自定义规则说明](rules/README.md)。

## 启用自动更新

1. 将本项目推送到 GitHub 公开仓库，默认分支使用 `main`。
2. 在 **Actions → Update rule sets → Run workflow** 运行首次构建。
3. 成功后会自动创建 `rule-set` 分支，之后每 6 小时更新一次。

推送 `rules/**`、构建脚本、规则来源或 workflow 的变更也会自动触发构建。
workflow 已声明 `contents: write`，使用内置 `GITHUB_TOKEN`，无需额外配置 PAT 或 Secret。
构建后会检查全部配置项对应的产物、SHA-256 和 SRS 版本；发布前再次校验，
缺失或损坏的产物不会推送。Actions 运行摘要会列出完整构建结果。
发布前还会用全部本地 SRS 生成临时配置，实际启动 sing-box，要求成功初始化并正常退出。
任一 SRS 无法加载时，workflow 失败并阻止发布。
如果组织策略限制 Actions 写入，需允许该仓库的 workflow 写入；不要为 `rule-set`
分支设置禁止机器人直接推送的保护规则。

定时计划为 UTC `00:23 / 06:23 / 12:23 / 18:23`，即北京时间
`08:23 / 14:23 / 20:23 / 次日 02:23`；GitHub 定时任务可能延迟。
Fork 后需要在 Actions 页面启用工作流。公开仓库长期无活动时，GitHub 可能停用定时任务，
可在 Actions 页面重新启用。

## 在 sing-box 中使用

本仓库的固定订阅地址如下，Fork 后将 `hamo/sing-box-rule-set` 替换为自己的仓库名：

```text
https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/oisd-big.srs
https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/oisd-small.srs
https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/awavenue.srs
https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/awavenue-only-ads.srs
https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/awavenue-no-privacy.srs
https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/awavenue-no-unwelcome.srs
https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-tif-full.srs
https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-pro.srs
https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-tif-medium.srs
https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-tif-mini.srs
https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-native-amazon.srs
https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-native-apple.srs
https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-native-huawei.srs
https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-native-microsoft.srs
https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-native-samsung.srs
https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-native-tiktok.srs
https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-native-tiktok-aggressive.srs
https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-native-lgwebos.srs
https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-native-roku.srs
https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-native-vivo.srs
https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-native-oppo-realme.srs
https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/hagezi-native-xiaomi.srs
https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/adguard-dns-filter.srs
https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/geosite-finance-us.srs
```

在现有配置的 `route.rule_set` 中加入：

```json
{
  "type": "remote",
  "tag": "oisd-big",
  "format": "binary",
  "url": "https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/oisd-big.srs",
  "update_interval": "6h"
}
```

然后在现有 `dns.rules` 中，放在其他兜底规则之前：

```json
{
  "rule_set": ["oisd-big"],
  "action": "reject"
}
```

使用秋风规则时，将上面片段中的 `oisd-big` 替换为对应变体名称，如 `awavenue-only-ads`。
使用其他规则集时替换为对应输出名称，例如 `hagezi-pro`、`hagezi-tif-mini`、
`hagezi-native-apple` 或 `adguard-dns-filter`。
上面的 action 配置片段适用于 sing-box 1.11.0 及以上版本。
当前提供的 SRS 均为版本 2，要求 sing-box 1.10.0+。
秋风的原始 JSON 为版本 3；官方编译器根据实际使用的字段将其编译为版本 2。
旧版的拦截配置请参考对应版本文档。
建议启用 `experimental.cache_file.enabled`，缓存远程规则集。
以上是配置片段，需要合并到现有配置。仅添加 `rule_set` 定义不会自动拦截。

## 自定义规则的维护与使用

本仓库直接维护的源文件位于 `rules/`，由 `sources/custom.json` 注册。例如：

```json
{
  "sources": [
    {
      "name": "geosite-finance-us",
      "path": "rules/geosite-finance-us.json",
      "format": "sing-box"
    }
  ]
}
```

`path` 为仓库根目录的相对文件路径，必须指向 `rules/` 内文件，不能与 `url` 同时配置，不能通过符号链接跳出目录；
本地来源不支持 `fallback_urls`。构建复制本次 checkout 内的文件，再复用对应 `format` 转换器，
不下载第三方列表。原文保存在发布分支 `sources/<name>.json`，元数据标记 `source_type: "local"` 并记录原路径和哈希。
修改原文后必须重新构建；发布校验会拒绝与当前源文件不一致的旧产物。

第一套使用 `geosite-finance-us` 命名，范围包含个人银行、信用卡、券商与退休投资、支付汇款、个人信用与消费金融。
分类及官方依据见 [rules/README.md](rules/README.md)。该集合覆盖服务商第一方域名及子域名、已核实的独立登录 / API / 交易 / 风控 / 资源域名，
以及共享平台上的特定金融业务主机（精确匹配）。不会整域匹配通用 CDN、验证码或身份验证平台。
不表示服务器均位于美国；部分域名也承载其他地区业务。尚未验证所有机构登录后的完整 App 流量，
无法保证覆盖所有金融请求或保证机构认定访问者位于美国。
公开 App 关联记录及登录、风控、支付 SDK 的证据和限制见 [移动端核对记录](rules/finance-us-mobile-audit.md)。

可以在现有 `route.rule_set` 中添加：

```json
{
  "type": "remote",
  "tag": "geosite-finance-us",
  "format": "binary",
  "url": "https://raw.githubusercontent.com/hamo/sing-box-rule-set/rule-set/geosite-finance-us.srs",
  "update_interval": "6h"
}
```

然后在现有 `route.rules` 中、相关兜底规则之前配置目标出站（将 `US-FINANCE` 替换为你已有的出站标签）：

```json
{
  "rule_set": ["geosite-finance-us"],
  "action": "route",
  "outbound": "US-FINANCE"
}
```

这是分流集合，应按实际需求配置出站，不作为广告拦截的 `reject` 规则。
仅构建仓库内规则：

```sh
python3 scripts/build.py --source custom --output build-custom
python3 scripts/verify-build.py build-custom --source custom
python3 scripts/check-srs-load.py build-custom
```

提交 `rules/**` 或 `sources/custom.json` 的修改后，GitHub Actions 会完整构建、校验、加载并更新 `rule-set` 分支。
后续添加自定义集合只需增加 `rules/<name>.json` 和配置记录，同样可使用 `adguard` / `adblock` 格式的本地文本。

## 构建与发布

```text
sources/*.json → 下载远端 / 复制仓库文件 → 按 format 转换 → 校验及实际加载 → rule-set 分支
```

- 固定官方 sing-box 编译器版本，并验证下载包的 SHA-256。
- OISD、HaGeZi 和 AdGuard DNS Filter 使用 `sing-box rule-set convert --type adguard`；AWAvenue 四种官方 JSON 使用 `rule-set compile`。
- 域名、子域名、例外、通配符等匹配语义由官方转换器处理；内容相同时不提交。
- 校验 OISD 的 `Entries`、HaGeZi 的 `Number of entries`，以及 JSON 的版本字段、规则数组和最小规则数量，
  避免把错误页、截断文件或空列表发布出去。
- 默认检测 sing-box 跳过日志并失败；AdGuard DNS Filter 显式允许有上限的兼容转换，记录每条跳过原因。
- 转换前处理 DNS `$badfilter`，取消其对应规则，再将支持的简单域名片段改写为等价正则。
- 编译后核对输入、取消、跳过和成功转换的数量；改写规则已计入成功数量，元数据和摘要保留改写映射。
- 实际启动 sing-box 加载全部 SRS；测试同时验证损坏的 SRS 内容会导致启动检查失败。
- 下载支持重试、低速超时和可配置的备用地址；OISD 使用维护者的官方 GitHub 镜像作为备用。
- 远端和仓库内自定义规则一起构建；本地规则不进行上游下载，改动 `rules/**` 自动触发更新。
- 全部规则集按各自配置的兼容策略构建成功并通过完整性校验后才发布，任一来源失败时远端保留上一版。
- `rule-set` 分支保留 `.srs`、上游原文件、许可证及带哈希的 `metadata.json`。
- 发布通过普通 Git 提交和推送完成；规则更新保留分支历史。
- PR 执行转换、SRS 匹配和本地 Git 发布测试，不下载上游规则；手动选择其他分支运行时
  只构建和上传 artifact，`main` 才能发布。

OISD、HaGeZi 和 AdGuard DNS Filter 的转换命令见 [AdGuard DNS Filter 文档](https://sing-box.sagernet.org/configuration/rule-set/adguard/)。
其专门的 AdGuard 二进制规则不能反编译成普通规则集 JSON，因此保留上游 `.txt` 供审阅。
转换时移除订阅文件头、规范空白行，并改写支持的简单域名片段；完整原文件保持原样。
秋风则直接保留官方 `.json` 并编译，命令见
[sing-box source format 文档](https://sing-box.sagernet.org/configuration/rule-set/source-format/)。

## 本地运行

需要 Python 3.9+、curl 和 Git。安装脚本支持 Linux/macOS 的 amd64、arm64。

```sh
python3 scripts/install-sing-box.py
python3 -m unittest discover -s tests -v
python3 scripts/build.py
python3 scripts/verify-build.py build
python3 scripts/check-srs-load.py build
```

生成结果在 `build/`。也可以使用已安装的官方编译器：

```sh
python3 scripts/build.py --sing-box /absolute/path/to/sing-box
```

只构建指定来源组（可重复传入 `--source`，`--upstream` 保持兼容）；此操作会用选中的结果替换本地输出目录：

```sh
python3 scripts/build.py --upstream oisd --output build-oisd
```

自动发布 workflow 始终构建所有来源（含自定义规则），避免发布时缺少未选中的规则集。

## 添加其他来源

来源仅保存配置，转换工具按输入格式组织；构建入口自动读取所有来源配置：

```text
sources/
  adguard.json              # AdGuard DNS Filter 的地址、格式和可选校验
  awavenue.json             # 秋风的地址、格式和可选校验
  custom.json               # 仓库内自定义规则的相对路径和格式
  hagezi.json               # HaGeZi Pro、TIF 和 Native Tracker 的地址、格式和可选校验
  oisd.json                 # OISD 的地址、格式和可选校验
rules/
  geosite-finance-us.json    # 手工维护的美国个人金融服务域名
scripts/
  build.py                  # 读取上游配置、下载、按格式分发、汇总产物
  common.py                 # HTTPS 下载、哈希和 SRS 输出校验
  formats/
    __init__.py             # format → 转换器映射
    adguard.py              # 通用 AdGuard 转换
    sing_box.py             # 通用 sing-box JSON 编译
```

接入新上游只需新增 `sources/example.json`，或者在现有配置的 `sources` 数组中添加记录。
上游名称不参与转换逻辑，也不需要对应的 Python 模块。最小配置：

```json
{
  "sources": [
    {
      "name": "example-list",
      "url": "https://example.com/list.txt",
      "format": "adblock"
    }
  ]
}
```

`name` 决定输出文件名，必须全局唯一；`url`（HTTPS）和 `path`（指向 `rules/` 内文件的仓库相对路径）必须二选一；`format` 决定转换方式。
可选 `fallback_urls` 为 HTTPS 地址数组：主地址下载失败时依次尝试备用地址，
转换和完整性校验仍然执行；实际下载地址记录在 `metadata.json` 的 `download_url` 中。

| format | 输入 | 转换工具 | 原始文件保存 |
| --- | --- | --- | --- |
| `adguard` | AdGuard 兼容过滤列表 | `sing-box rule-set convert --type adguard` | `sources/<name>.txt` |
| `adblock` | `adguard` 的别名，适用于兼容的 Adblock 风格 DNS 列表 | 同上，复用同一个转换器 | `sources/<name>.txt` |
| `sing-box` | sing-box source-format JSON | `sing-box rule-set compile` | `sources/<name>.json` |

### AdGuard / Adblock 语法范围

`adblock` 与 `adguard` 的转换、校验和失败处理完全相同。支持范围由固定版本的
sing-box AdGuard DNS 转换器决定；`[Adblock Plus]` 文件头只是订阅标识，
不代表整套浏览器过滤语法都可以用于 DNS 规则集。

| 规则类型 | 示例 / 说明 |
| --- | --- |
| 域名及子域名 | `\|\|example.com^` |
| 例外规则 | `@@\|\|allowed.example.com^` |
| 通配符 | `\|\|track*.example.com^`，支持 `*` |
| 域名正则 | `/ads[0-9]+\.example\.com/`；受 sing-box 正则引擎和转换器限制 |
| 有限的修饰符 | `$important`；其他修饰符需按官方支持范围确认 |
| 取消规则 | DNS `$badfilter` 在编译前取消文本相同的目标规则，支持与 `$important` 组合；不支持浏览器 `$domain` 等部分取消语法 |
| 简单域名片段 | 无修饰符的 `\|\|countly-`、`-ad123-` 等及其 `@@` 例外，在编译前改写为等价的域名正则 |
| 注释与订阅头 | 注释不计入规则数量；`[Adblock Plus]` / `[AdGuard]` 订阅头在转换输入中移除 |

域名片段改写限于无修饰符的 `||label-`（字母/数字开头的标签前缀）及 `-word-`（字母、数字和连字符组成的关键词）。
例如 `||countly-` → `/(?i)(^|\.)countly-/`，`-ad123-` → `/(?i)-ad123-/`。
例外标记 `@@` 保留；先执行 `$badfilter` 取消，再做改写。已有正则、带修饰符规则和 IP 规则不参与此改写。

`$dnsrewrite=0.0.0.0` 可被官方转换器接受，但改写动作会被忽略，仅保留匹配逻辑；
本项目生成的 SRS 不包含 DNS 改写动作。

浏览器专用的 CSS 元素隐藏、脚本注入，以及 URL 路径、端口、查询参数和
`$script`、`$image`、`$third-party` 等修饰符不在支持范围内。
应选择 OISD、HaGeZi、AdGuard DNS Filter 这类 DNS 域名过滤列表。默认情况下，sing-box 报告
跳过不支持的规则时，构建会失败。AdGuard DNS Filter 使用下述显式报告策略发布兼容部分。
详细兼容范围见
[官方 AdGuard DNS Filter 文档](https://sing-box.sagernet.org/configuration/rule-set/adguard/)。

JSON 编译产物的 SRS 版本由官方编译器根据源格式版本及实际使用字段决定，可能低于源 JSON 版本。
源 JSON 版本与实际 SRS 版本分别记录在 `metadata.json` 中。
当前 OISD、HaGeZi、AdGuard DNS Filter 的转换产物及秋风 JSON 编译产物均为 SRS 版本 2。

`unsupported_policy` 可选，默认为 `"error"`。仅在明确接受部分转换时使用 `"report"`，
并配置正整数 `max_skipped_rules` 作为跳过上限；不能将其视为完整兼容原列表。
报告模式仍要求编译器报告的输入总数与实际输入相同，成功条数＋跳过条数必须与输入总数一致，
且成功编译的规则数量不能低于 `min_rules`。不支持的 `$badfilter` 组合始终失败。
`metadata.json` 的 `rule_count` 保留上游原始规则行数，`conversion` 记录实际编译数量、
取消指令、被取消的规则、`rewritten_rules` 中的改写映射，以及逐条跳过原因。
改写不改变规则条数，改写成功的规则计入实际编译数量；构建摘要同步展示改写和跳过详情。
原文件仍完整保留，订阅顶部元数据不会被内嵌子列表的同名字段覆盖。

`min_rules` 可选，默认 1。`adguard` / `adblock` 格式统计非注释规则行；sing-box JSON 格式统计
顶层 `rules` 数组的规则对象数量，二者都在转换前校验。

`adguard` / `adblock` 列表还支持可选的声明式校验，例如 OISD：

```json
{
  "name": "oisd-big",
  "url": "https://big.oisd.nl/",
  "format": "adblock",
  "min_rules": 10000,
  "validation": {
    "headers": ["[Adblock Plus]"],
    "count_field": "entries"
  }
}
```

| validation 选项 | 作用 |
| --- | --- |
| `headers` | 要求文件首行为配置中的某个订阅头 |
| `title_prefix` | 要求 `Title` 以指定文本开头 |
| `count_field` | 要求指定注释字段存在，且声明的条目数与实际规则行数相同；字段名忽略大小写 |

例如某个 AdGuard 上游可使用 `title_prefix: "Example List"` 和 `count_field: "total lines"`。
没有配置这些选项时，通用转换器不会要求某个上游特有的文件头。
可识别的 `[Adblock Plus]` / `[AdGuard]` 订阅头会在转换输入中自动移除，原文件完整保留。

接入新格式时，在 `scripts/formats/` 中添加转换器，实现 `validate(source)`、
`convert(raw, output, compiler, source)` 并声明原文件的 `EXTENSION`，
然后在 `formats/__init__.py` 注册 `format`。转换器只负责格式处理，下载、哈希、产物
汇总和发布由公共流程完成。
新增上游或格式时补充测试、订阅说明及来源授权声明。

## 来源与许可证

OISD 由 Stephan van Ruth 维护，本项目为独立的格式转换与分发项目。
上游规则及其转换产物使用 [GNU GPL v3](LICENSE)，
[原始许可证](https://github.com/sjhgvr/oisd/blob/main/LICENSE)和原始文件头声明均予以保留。
本仓库转换代码同样以 GPL-3.0 发布。

AWAvenue 秋风广告规则由 [TG-Twilight/AWAvenue-Ads-Rule](https://github.com/TG-Twilight/AWAvenue-Ads-Rule)
维护，其规则和转换产物遵循上游当前的 [GNU GPL v3 许可证](https://github.com/TG-Twilight/AWAvenue-Ads-Rule/blob/main/LICENSE)。
官方原始 JSON 保留在 `sources/awavenue*.json` 中，来源地址与文件哈希记录在 `metadata.json`。

HaGeZi Pro、TIF 和 Native Tracker 来源于 [hagezi/dns-blocklists](https://github.com/hagezi/dns-blocklists)，
遵循上游的 [GNU GPL v3 许可证](https://github.com/hagezi/dns-blocklists/blob/main/LICENSE)。
原始列表及其作者、项目、许可证声明保留在 `sources/hagezi-*.txt` 中。

AdGuard DNS Filter 来源于 [AdguardTeam/AdGuardSDNSFilter](https://github.com/AdguardTeam/AdGuardSDNSFilter)，
遵循上游的 [GNU GPL v3 许可证](https://github.com/AdguardTeam/AdGuardSDNSFilter/blob/master/LICENSE)。
原始列表及其来源、作者和许可证声明保留在 `sources/adguard-dns-filter.txt` 中。

本仓库手工维护的 `rules/` 分类规则同样采用 [GNU GPL v3](LICENSE)，各机构官方域名依据记录在 [rules/README.md](rules/README.md)。
