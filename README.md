# sing-box-rule-set

通过 GitHub Actions 自动下载上游规则，转换为 sing-box 的 `.srs` 二进制规则集。
支持 **OISD big**、**OISD small**、**AWAvenue 秋风广告规则的全部四种变体**及 **HaGeZi TIF Full**。

| 规则集 | 上游 | 输出 | 用途 |
| --- | --- | --- | --- |
| OISD big | <https://big.oisd.nl/> | `oisd-big.srs` | 广告、跟踪、恶意域名等 |
| OISD small | <https://small.oisd.nl/> | `oisd-small.srs` | 以广告拦截为主的较小版本 |
| AWAvenue 完整防护 | [官方 JSON](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Singbox.json) | `awavenue.srs` | 广告＋隐私＋不受欢迎 |
| AWAvenue 仅广告 | [官方 JSON](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Singbox-Only.Ads.json) | `awavenue-only-ads.srs` | 仅广告 |
| AWAvenue 不含隐私 | [官方 JSON](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Singbox-No.Privacy.json) | `awavenue-no-privacy.srs` | 广告＋不受欢迎 |
| AWAvenue 不含不受欢迎 | [官方 JSON](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Singbox-No.Unwelcome.json) | `awavenue-no-unwelcome.srs` | 广告＋隐私 |
| HaGeZi TIF Full | [官方 Adblock 列表](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/tif.txt) | `hagezi-tif-full.srs` | 恶意软件、钓鱼、诈骗、挖矿等威胁域名 |

big 包含 small，选择一个即可。规则说明见 [OISD 官网](https://oisd.nl/)。
OISD 官方为 [AdGuard Home](https://oisd.nl/setup/adguardhome) 提供以上订阅地址；
列表文件头虽然标记为 `[Adblock Plus]`，规则本身可交给 sing-box 的 AdGuard 转换器处理。
AWAvenue 使用 [官方仓库](https://github.com/TG-Twilight/AWAvenue-Ads-Rule) 的四种 sing-box JSON，
通过通用 `sing-box` 格式转换器编译，保留精确域名、域名后缀和关键词的原始匹配语义。
四种变体选用其中一个即可；「不受欢迎」包含强制更新、PCDN、推送等规则。
HaGeZi 使用 [Threat Intelligence Feeds 的 Full 版本](https://github.com/hagezi/dns-blocklists#tif)，
复用通用 `adguard` 转换器，校验文件头声明的 `Number of entries` 与实际规则行数。

## 启用自动更新

1. 将本项目推送到 GitHub 公开仓库，默认分支使用 `main`。
2. 在 **Actions → Update rule sets → Run workflow** 运行首次构建。
3. 成功后会自动创建 `rule-set` 分支，之后每 6 小时更新一次。

推送构建脚本、规则来源或 workflow 的变更也会自动触发构建。
workflow 已声明 `contents: write`，使用内置 `GITHUB_TOKEN`，无需额外配置 PAT 或 Secret。
构建后会检查全部配置项对应的产物、SHA-256 和 SRS 版本；发布前再次校验，
缺失或损坏的产物不会推送。Actions 运行摘要会列出完整构建结果。
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
使用 HaGeZi TIF Full 时替换为 `hagezi-tif-full`。
上面的 action 配置片段适用于 sing-box 1.11.0 及以上版本。
当前提供的 SRS 均为版本 2，要求 sing-box 1.10.0+。
秋风的原始 JSON 为版本 3；官方编译器根据实际使用的字段将其编译为版本 2。
旧版的拦截配置请参考对应版本文档。
建议启用 `experimental.cache_file.enabled`，缓存远程规则集。
以上是配置片段，需要合并到现有配置。仅添加 `rule_set` 定义不会自动拦截。

## 构建与发布

```text
sources/*.json → 下载 → 按 format 选择通用转换器 → 校验与转换 → rule-set 分支
```

- 固定官方 sing-box 编译器版本，并验证下载包的 SHA-256。
- OISD 和 HaGeZi 使用 `sing-box rule-set convert --type adguard`；AWAvenue 四种官方 JSON 使用 `rule-set compile`。
- 域名、子域名、例外、通配符等匹配语义由官方转换器处理；内容相同时不提交。
- 校验 OISD 的 `Entries`、HaGeZi 的 `Number of entries`，以及 JSON 的版本字段、规则数组和最小规则数量，
  避免把错误页、截断文件或空列表发布出去。
- sing-box 对部分不支持的规则会跳过并成功退出；构建检测其跳过日志并失败，避免发布不完整的转换结果。
- 下载支持重试、低速超时和可配置的备用地址；OISD 使用维护者的官方 GitHub 镜像作为备用。
- 全部规则集构建成功并通过完整性校验后才发布，任一来源失败时远端保留上一版。
- `rule-set` 分支保留 `.srs`、上游原文件、许可证及带哈希的 `metadata.json`。
- 发布通过普通 Git 提交和推送完成；规则更新保留分支历史。
- PR 执行转换、SRS 匹配和本地 Git 发布测试，不下载上游规则；手动选择其他分支运行时
  只构建和上传 artifact，`main` 才能发布。

OISD 和 HaGeZi 的转换命令见 [AdGuard DNS Filter 文档](https://sing-box.sagernet.org/configuration/rule-set/adguard/)。
其专门的 AdGuard 二进制规则不能反编译成普通规则集 JSON，因此保留上游 `.txt` 供审阅。
转换时移除订阅文件头并规范空白行，完整原文件保持原样。
秋风则直接保留官方 `.json` 并编译，命令见
[sing-box source format 文档](https://sing-box.sagernet.org/configuration/rule-set/source-format/)。

## 本地运行

需要 Python 3.9+、curl 和 Git。安装脚本支持 Linux/macOS 的 amd64、arm64。

```sh
python3 scripts/install-sing-box.py
python3 -m unittest discover -s tests -v
python3 scripts/build.py
```

生成结果在 `build/`。也可以使用已安装的官方编译器：

```sh
python3 scripts/build.py --sing-box /absolute/path/to/sing-box
```

只构建指定上游（可重复传入 `--upstream`）；此操作会用选中的结果替换本地输出目录：

```sh
python3 scripts/build.py --upstream oisd --output build-oisd
```

自动发布 workflow 始终构建所有上游，避免发布时缺少未选中的规则集。

## 添加其他来源

上游仅保存配置，转换工具按输入格式组织；构建入口自动读取所有上游配置：

```text
sources/
  awavenue.json             # 秋风的地址、格式和可选校验
  hagezi.json               # HaGeZi TIF Full 的地址、格式和可选校验
  oisd.json                 # OISD 的地址、格式和可选校验
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

`name` 决定输出文件名，必须全局唯一；`url` 必须使用 HTTPS；`format` 决定转换方式。
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
| 注释与订阅头 | 注释不计入规则数量；`[Adblock Plus]` / `[AdGuard]` 订阅头在转换输入中移除 |

`$dnsrewrite=0.0.0.0` 可被官方转换器接受，但改写动作会被忽略，仅保留匹配逻辑；
本项目生成的 SRS 不包含 DNS 改写动作。

浏览器专用的 CSS 元素隐藏、脚本注入，以及 URL 路径、端口、查询参数和
`$script`、`$image`、`$third-party` 等修饰符不在支持范围内。
应选择 OISD、HaGeZi 这类 DNS 域名过滤列表。sing-box 报告跳过不支持的规则时，
构建会失败，不会发布该次结果。详细兼容范围见
[官方 AdGuard DNS Filter 文档](https://sing-box.sagernet.org/configuration/rule-set/adguard/)。

JSON 编译产物的 SRS 版本由官方编译器根据源格式版本及实际使用字段决定，可能低于源 JSON 版本。
源 JSON 版本与实际 SRS 版本分别记录在 `metadata.json` 中。
当前 OISD、HaGeZi 的 AdGuard 转换产物及秋风 JSON 编译产物均为 SRS 版本 2。

`min_rules` 可选，默认 1。`adguard` / `adblock` 格式统计非注释规则行；sing-box JSON 格式统计
顶层 `rules` 数组的规则对象数量，二者都在转换前校验。

`adguard` / `adblock` 列表还支持可选的声明式校验，例如 OISD：

```json
{
  "name": "oisd-big",
  "url": "https://big.oisd.nl/",
  "format": "adguard",
  "min_rules": 10000,
  "validation": {
    "headers": ["[Adblock Plus]", "[AdGuard]"],
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

HaGeZi TIF Full 来源于 [hagezi/dns-blocklists](https://github.com/hagezi/dns-blocklists#tif)，
遵循上游的 [GNU GPL v3 许可证](https://github.com/hagezi/dns-blocklists/blob/main/LICENSE)。
原始列表及其作者、项目、许可证声明保留在 `sources/hagezi-tif-full.txt` 中。
