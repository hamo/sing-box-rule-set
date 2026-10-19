# 仓库内自定义规则

`rules/` 保存手工维护的原文，由 [sources/custom.json](../sources/custom.json) 注册。
构建读取当前 Git checkout，保留原文和注释后编译；这些规则采用 [GPL-3.0](../LICENSE)。

## geosite-finance-us

面向美国个人用户的银行、信用卡、投资与退休、加密资产交易、支付汇款、个人信用和消费金融域名分类，用于 `route.rules` 分流。
配置示例见 [主 README](../README.md#在-sing-box-中使用)。

### 收录范围

- 金融机构的账户、业务域名及专属资源，通常使用 `domain_suffix` 覆盖根域和子域名。
- 第三方仅保留机构专属租户，或有官方来源确认用途的金融账户门户，使用 `domain` 精确匹配主机。
- 按分流需求排除 Schwab（含 thinkorswim）、IBKR 和 Wise，不将其账户及业务域名纳入美国出口分流。
- 排除公共 SDK、聚合 / 授权 API、行情 / 采集 / 营销组件、通用登录 / 验证 / CDN、S3 存储桶，以及钱包、Checkout、3DS 等通用支付组件。

机构租户须结合机构标识和官方配置核实；账户门户须有官网直链、官方业务文档或发行方披露。
仅出现在页面、CSP 白名单或 SDK 配置中不足以收录，不添加 IP、域名关键词或猜测的正则。

逐条域名、用途及来源 URL 统一维护在 [geosite-finance-us.json](geosite-finance-us.json) 的相邻注释中；
排除项的匹配回归样例见 [tests/test_custom.py](../tests/test_custom.py)。

部分金融账户门户服务多家机构或其他地区业务，域名规则无法进一步区分；该集合也未经过所有机构 App 的完整抓包验证，
无法保证覆盖全部请求或保证机构判定访问者位于美国。

## 维护方式

1. 修改规则文件，保持小写、排序和唯一；已被第一方后缀覆盖的子域名不重复添加。
2. 同时维护每条域名前的机构、用途和来源注释。支持 `//`、`/* ... */`，其余使用标准 JSON，不加尾随逗号。
3. 构建并校验，确认 SRS 可实际加载：

```sh
python3 scripts/build.py --source custom --output build-custom
python3 scripts/verify-build.py build-custom --source custom
python3 scripts/check-srs-load.py build-custom
```

注释不参与匹配，但原文校验和覆盖注释，修改后必须重建。
新增自定义集合时增加 `rules/<name>.json` 并注册来源，字段和路径限制见 [添加其他来源](../README.md#添加其他来源)。
自动更新及发布流程见 [启用自动更新](../README.md#启用自动更新)。
