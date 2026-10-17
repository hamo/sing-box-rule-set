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

按机构的官方站点、登录入口、页面资源引用及官方开发文档手工维护，覆盖官网之外的账户登录、业务 API、交易平台、退休账户、支付和静态资源。
`domain_suffix` 同时匹配根域名和全部子域名，因此 `secure.chase.com`、`api.robinhood.com` 等无需逐条列出。
共享服务仅在能明确关联到金融业务时收录具体主机，使用 `domain` 精确匹配；不会将整个 CDN 或通用身份验证平台加入集合。

当前有 96 条域名后缀和 12 条精确主机规则。不添加 IP、域名关键词或按名称猜测的正则。
这些是公开资料中已核实的业务入口和依赖，并未经过所有机构登录后的浏览器及手机 App 全链路抓包验证。
未知的 App 端点、直连 IP 和无法按域名区分租户的共享服务仍可能遗漏；仅靠此集合无法保证所有请求均被匹配，或保证机构判定访问者位于美国。

官方来源核对日期：2026-10-17。下面前五组为 `domain_suffix`，最后一组为 `domain`，与 JSON 中的 `rules` 顺序一致。

## 银行与综合个人金融

| 机构 / 服务 | 收录域名 | 官方站点依据 |
| --- | --- | --- |
| Fifth Third Bank | `53.com` | [官方站点](https://www.53.com/) |
| Ally | `ally.com` | [官方站点](https://www.ally.com/) |
| Bank of America | `bankofamerica.com`, `bac-assets.com`, `bofa.com` | [官网及页面中的 API、脚本、图片资源引用](https://www.bankofamerica.com/) |
| BMO US | `bmo.com` | [美国个人银行及登录入口](https://www.bmo.com/en-us/main/personal/) |
| Capital One | `capitalone.com` | [官方站点](https://www.capitalone.com/) |
| Chase / J.P. Morgan | `chase.com`, `jpmorgan.com` | [Chase 官网及 J.P. Morgan 业务链接](https://www.chase.com/) |
| Chime | `chime.com` | [官方站点](https://www.chime.com/) |
| Citi | `citi.com`, `citibank.com` | [官方站点](https://www.citi.com/) |
| Citizens Bank | `citizensbank.com`, `citizensbankonline.com` | [官网的 Pay My Loan / 网银登录入口](https://www.citizensbank.com/) |
| First Citizens | `firstcitizens.com` | [个人银行及数字银行登录入口](https://www.firstcitizens.com/personal) |
| Huntington | `huntington.com`, `huntingtonbank.com` | [官网、网银入口及独立资源域名](https://www.huntington.com/) |
| KeyBank | `key.com` | [个人银行](https://www.key.com/personal/index.html) |
| Marcus by Goldman Sachs | `marcus.com` | [储蓄及账户登录](https://www.marcus.com/us/en) |
| Navy Federal Credit Union | `navyfederal.org` | [官方站点](https://www.navyfederal.org/) |
| PNC | `pnc.com` | [官方站点](https://www.pnc.com/) |
| Regions | `regions.com` | [个人银行](https://www.regions.com/personal-banking) |
| Santander / Openbank US | `santanderbank.com`, `santanderconsumerusa.com`, `santandermedia.com`, `openbank.us` | [Santander 官网及消费金融链接](https://www.santanderbank.com/)、[Openbank 登录及资源引用](https://www.openbank.us/) |
| SoFi | `sofi.com` | [官方站点](https://www.sofi.com/) |
| TD Bank US | `td.com`, `tdbank.com`, `tdfitloan.com` | [美国个人银行、网银及贷款入口](https://www.td.com/us/en/personal-banking) |
| Truist | `truist.com` | [官方站点](https://www.truist.com/) |
| USAA | `usaa.com` | [官方站点](https://www.usaa.com/) |
| U.S. Bank | `usbank.com` | [官方站点](https://www.usbank.com/) |
| Wells Fargo | `wellsfargo.com`, `wellsfargomedia.com`, `wf.com`, `wfinterface.com` | [官网及独立资源、接口引用](https://www.wellsfargo.com/) |

## 信用卡与零售融资

| 机构 / 服务 | 收录域名 | 官方站点依据 |
| --- | --- | --- |
| American Express | `americanexpress.com`, `aexp.com`, `aexp-static.com` | [官网的接口及脚本资源引用](https://www.americanexpress.com/en-us/) |
| Discover | `discover.com`, `discovercard.com` | [官网及信用卡账户入口](https://www.discover.com/) |
| Synchrony / CareCredit | `synchrony.com`, `synchronybank.com`, `mysynchrony.com`, `syf.com`, `carecredit.com`, `synchronycredit.com`, `synchronybankterms.com` | [Synchrony 登录、信用卡及 CareCredit 入口](https://www.synchrony.com/)、[PayPal 信用产品入口及条款](https://www.paypal.com/us/home) |

## 券商与退休投资

| 机构 / 服务 | 收录域名 | 官方站点依据 |
| --- | --- | --- |
| Betterment | `betterment.com` | [官网及账户入口](https://www.betterment.com/) |
| E*TRADE / Morgan Stanley | `etrade.com`, `etrade.net`, `morganstanley.com`, `morganstanleyclientserv.com` | [E*TRADE 官网资源及 Morgan Stanley Online 链接](https://us.etrade.com/) |
| Fidelity / NetBenefits | `fidelity.com`, `netbenefits.com`, `wealthscape.com`, `fidelityinvestments.com`, `mystreetscape.com`, `wealthscapeinvestor.com` | [登录帮助](https://www.fidelity.com/customer-service/need-help-logging-in)、[年度业务说明](https://about.fidelity.com/data-and-insights/2025-annual-report)、[官方活动资料](https://www.fidelity.com/bin-public/060_www_fidelity_com/documents/learning-center/Market_Sense_Slides_03_28.pdf)、[Citizens 券商入口](https://www.citizensbank.com/)、[Santander 投资入口](https://www.santanderbank.com/) |
| Interactive Brokers | `ibkr.com`, `interactivebrokers.com` | [官方站点](https://www.interactivebrokers.com/) |
| Merrill | `merrilledge.com`, `ml.com`, `merrill.com` | [Merrill Edge 官网](https://www.merrilledge.com/)、[美国银行的 Merrill 链接](https://www.bankofamerica.com/) |
| Robinhood | `robinhood.com` | [官方站点](https://robinhood.com/us/en/) |
| Charles Schwab / thinkorswim | `schwab.com`, `schwabcdn.com`, `schwabinstitutional.com`, `schwabplan.com`, `schwabworkplaceservices.com`, `schwab529plan.com`, `thinkorswim.com` | [官网的退休、529 及工作福利入口](https://www.schwab.com/)、[登录页面资源](https://client.schwab.com/Areas/Access/Login)、[thinkorswim 官方说明](https://workplace.schwab.com/story/introduction-to-thinkorswim-web) |
| Vanguard | `vanguard.com` | [官方站点](https://investor.vanguard.com/) |
| Wealthfront | `wealthfront.com` | [官网、账户及资源入口](https://www.wealthfront.com/) |

## 支付与汇款

| 机构 / 服务 | 收录域名 | 官方站点依据 |
| --- | --- | --- |
| Cash App | `cash.app`, `cash.me` | [官方站点](https://cash.app/) |
| PayPal / Braintree | `paypal.com`, `paypal.me`, `paypalobjects.com`, `braintreegateway.com`, `braintree-api.com` | [PayPal.Me 官方说明](https://www.paypal.com/us/cshelp/article/paypalme-frequently-asked-questions-help432)、[官方 SDK / API 所需域名](https://developer.paypal.com/platforms/checkout/fastlane/getstarted/) |
| Venmo | `venmo.com` | [官方站点](https://venmo.com/) |
| Wise | `wise.com`, `transferwise.com` | [官方站点](https://wise.com/us/)、[官方旧域名链接资料](https://wise.com/documents/TW-Widgets-Price%2BComparison.pdf) |
| Zelle | `zelle.com`, `zellepay.com` | [官方站点](https://www.zelle.com/) |

## 个人信用与消费金融

| 机构 / 服务 | 收录域名 | 官方站点依据 |
| --- | --- | --- |
| Affirm | `affirm.com` | [官方站点](https://www.affirm.com/) |
| Credit Karma | `creditkarma.com` | [官方站点](https://www.creditkarma.com/) |
| Equifax | `equifax.com` | [个人信用及账户入口](https://www.equifax.com/personal/) |
| Experian | `experian.com` | [官方站点](https://www.experian.com/) |
| Happen Bank（原 LendingClub） | `happen.com`, `lendingclub.com` | [官方更名说明](https://www.happen.com/company/media-center) |
| TransUnion | `transunion.com` | [个人信用、冻结及会员登录入口](https://www.transunion.com/) |
| 信用报告及预筛选退出服务 | `annualcreditreport.com`, `optoutprescreen.com` | [Equifax 官网的消费者服务链接](https://www.equifax.com/personal/)、[TransUnion 官网](https://www.transunion.com/) |

## 共享平台上的金融业务主机（精确匹配）

下面仅匹配列出的主机本身，不匹配平台根域、其他租户或任意下级子域名。

| 机构 / 服务 | 精确主机 | 官方依据与用途 |
| --- | --- | --- |
| Cash App | `cash-f.squarecdn.com` | [官网](https://cash.app/) 引用的字体、图片及前端资源 |
| Credit Karma | `creditkarmacdn-a.akamaihd.net` | [官网](https://www.creditkarma.com/) 引用的 CSS / JS 资源 |
| Citizens Bank | `www.accessmycardonline.com`, `login.bdreporting.com` | [官网](https://www.citizensbank.com/) 的信用卡及 Clarfeld Client Access 登录入口 |
| Navy Federal | `navyfederal.lendkey.com`, `navyfederal-mba.lendkey.com`, `navyfederal-refi-med.lendkey.com`, `client.osaicinstitutions.com` | [官网](https://www.navyfederal.org/) 的学生贷款、贷款再融资及投资账户入口 / 官方域名配置 |
| First Citizens | `firstcitizens.netxinvestor.com` | [官网](https://www.firstcitizens.com/personal) 的投资账户入口 |
| TD Bank | `tdinvestmentservices.netxinvestor.com`, `tdwealth.netxinvestor.com` | [美国官网](https://www.td.com/us/en/personal-banking) 的投资及财富账户入口 |
| Santander | `santandercards-web.oflows.net` | [官网](https://www.santanderbank.com/) 的 `connect-src` 业务端点 |

`cloudfront.net`、`akamaihd.net`、`squarecdn.com`、`ctfassets.net`、`google.com`、`gstatic.com`、`okta.com` 等共享平台不会整域收录。
例如某些 Contentful 图片使用相同主机、通过 URL 路径区分租户，域名规则无法仅选中金融机构的资源。
共享验证码、广告和分析 SDK 也不会仅因出现在金融页面中就整域纳入；机构自有域名下的相关请求仍按域名后缀匹配。

## 维护方式

修改 `geosite-finance-us.json` 的对应 `domain_suffix` 或 `domain` 数组，保持小写、排序且不重复。
添加服务或独立域名时同步更新上面的官方来源依据，记录其登录、API、静态资源或账户服务用途，避免根据名称猜测域名。
第一方根域名已覆盖的子域名不重复加入；第三方共享平台优先使用精确主机。
实际使用发现漏匹配时，可提供脱敏后的请求域名、对应机构和业务场景，核实关联后补充；不要提交账户信息、令牌或完整交易 URL。

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
