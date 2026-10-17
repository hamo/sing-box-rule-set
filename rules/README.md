# 仓库内维护的自定义规则

`rules/` 保存本仓库直接维护的规则原文，`sources/custom.json` 注册名称、路径和输入格式。
构建时从本次 Git checkout 复制文件并编译，不下载或同步第三方规则列表。
本目录的规则采用仓库的 GPL-3.0 许可证。配置中的本地路径必须位于 `rules/` 下，不能通过路径或符号链接跳出该目录。

## geosite-finance-us

面向美国个人用户的银行及金融服务域名分类，涵盖银行、信用卡、券商与退休投资、支付汇款、个人信用与消费金融。
`finance-us` 描述收录对象和用途，不代表所有服务仅限美国、公司均注册在美国或服务器 IP 均在美国。
部分服务使用全球共享域名，因此该集合也可能匹配其其他地区业务。

这是分流分类集合，应在 `route.rules` 中配合你选择的出站使用。
该集合不应加入广告拦截的 `reject` 列表；不会自动为你选择直连或代理。

当前按下面各机构的官方站点手工整理第一方域名。`domain_suffix` 同时匹配根域名和子域名。
首批为主要服务的起始集合，应用依赖的独立认证、静态资源和第三方服务域名仍可能需要继续补充。

官方站点核对日期：2026-10-17。以下分组与 JSON 中的 `rules` 顺序一致。

## 银行与综合个人金融

| 机构 / 服务 | 收录域名 | 官方站点依据 |
| --- | --- | --- |
| Fifth Third Bank | `53.com` | [官方站点](https://www.53.com/) |
| Ally | `ally.com` | [官方站点](https://www.ally.com/) |
| Bank of America | `bankofamerica.com` | [官方站点](https://www.bankofamerica.com/) |
| Capital One | `capitalone.com` | [官方站点](https://www.capitalone.com/) |
| Chase | `chase.com` | [官方站点](https://www.chase.com/) |
| Chime | `chime.com` | [官方站点](https://www.chime.com/) |
| Citi | `citi.com`, `citibank.com` | [官方站点](https://www.citi.com/) |
| Citizens Bank | `citizensbank.com` | [官方站点](https://www.citizensbank.com/) |
| Navy Federal Credit Union | `navyfederal.org` | [官方站点](https://www.navyfederal.org/) |
| PNC | `pnc.com` | [官方站点](https://www.pnc.com/) |
| SoFi | `sofi.com` | [官方站点](https://www.sofi.com/) |
| Truist | `truist.com` | [官方站点](https://www.truist.com/) |
| USAA | `usaa.com` | [官方站点](https://www.usaa.com/) |
| U.S. Bank | `usbank.com` | [官方站点](https://www.usbank.com/) |
| Wells Fargo | `wellsfargo.com` | [官方站点](https://www.wellsfargo.com/) |

## 信用卡与零售融资

| 机构 / 服务 | 收录域名 | 官方站点依据 |
| --- | --- | --- |
| American Express | `americanexpress.com` | [官方站点](https://www.americanexpress.com/en-us/) |
| Discover | `discover.com` | [官方站点](https://www.discover.com/) |
| Synchrony | `synchrony.com`, `synchronybank.com` | [官方站点](https://www.synchrony.com/) |

## 券商与退休投资

| 机构 / 服务 | 收录域名 | 官方站点依据 |
| --- | --- | --- |
| E*TRADE | `etrade.com` | [官方站点](https://us.etrade.com/) |
| Fidelity | `fidelity.com` | [官方站点](https://www.fidelity.com/) |
| Interactive Brokers | `ibkr.com`, `interactivebrokers.com` | [官方站点](https://www.interactivebrokers.com/) |
| Merrill | `merrilledge.com`, `ml.com` | [官方站点](https://www.merrilledge.com/) |
| Robinhood | `robinhood.com` | [官方站点](https://robinhood.com/us/en/) |
| Charles Schwab | `schwab.com` | [官方站点](https://www.schwab.com/) |
| Vanguard | `vanguard.com` | [官方站点](https://investor.vanguard.com/) |

## 支付与汇款

| 机构 / 服务 | 收录域名 | 官方站点依据 |
| --- | --- | --- |
| Cash App | `cash.app`, `cash.me` | [官方站点](https://cash.app/) |
| PayPal | `paypal.com` | [官方站点](https://www.paypal.com/us/home) |
| Venmo | `venmo.com` | [官方站点](https://venmo.com/) |
| Wise | `wise.com` | [官方站点](https://wise.com/us/) |
| Zelle | `zelle.com`, `zellepay.com` | [官方站点](https://www.zelle.com/) |

## 个人信用与消费金融

| 机构 / 服务 | 收录域名 | 官方站点依据 |
| --- | --- | --- |
| Affirm | `affirm.com` | [官方站点](https://www.affirm.com/) |
| Credit Karma | `creditkarma.com` | [官方站点](https://www.creditkarma.com/) |
| Experian | `experian.com` | [官方站点](https://www.experian.com/) |
| Happen Bank（原 LendingClub） | `happen.com`, `lendingclub.com` | [官方更名说明](https://www.happen.com/company/media-center) |

## 维护方式

修改 `geosite-finance-us.json` 的对应 `domain_suffix` 数组，保持小写、排序且不重复；单条精确匹配可使用 sing-box 的 `domain` 字段。
添加服务或独立域名时同步更新上面的官方来源依据，避免根据名称猜测域名。

只构建自定义规则并检查完整性和实际加载：

```sh
python3 scripts/build.py --source custom --output build-custom
python3 scripts/verify-build.py build-custom --source custom
python3 scripts/check-srs-load.py build-custom
```

全量构建、校验及发布前加载检查：

```sh
python3 scripts/build.py
python3 scripts/verify-build.py build
python3 scripts/check-srs-load.py build
```

提交 `rules/**` 或 `sources/**` 的修改会触发 GitHub Actions，成功后更新 `rule-set` 分支的 SRS、原文及 metadata。
自定义来源原文的哈希必须与当前 checkout 中的原文一致，修改原文后需要重新构建才能发布。
新增集合时，添加 `rules/<name>.json`，并在 `sources/custom.json` 的 `sources` 数组中新增 `name`、`path`、`format` 记录即可。
