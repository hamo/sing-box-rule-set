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

按机构的官方站点、登录入口、页面资源引用及官方开发文档手工维护，覆盖官网之外的账户登录、业务 API、交易平台、退休账户及机构专属资源。
`domain_suffix` 同时匹配根域名和全部子域名，因此 `secure.chase.com`、`api.robinhood.com` 等无需逐条列出。
只收录金融机构的账户、业务域名及有明确依据的专属资源。第三方仅保留机构专属租户主机，
或由官方来源明确确认用途的金融账户登录 / 业务办理门户，均按 `domain` 精确匹配。
公共 SDK、聚合 API、共用授权接口、营销 / 行情 / 采集组件，以及通用支付、收单、商户结账组件均不纳入。
页面引用和 CSP 白名单只能证明关联，不能单独证明金融机构专属或金融账户入口。
仅有金融页面引用不足以收录跨行业通用的登录、验证码、指纹、身份验证、IP 查询或 CDN 主机；即使精确匹配也不纳入。

当前有 127 条域名后缀和 33 条精确主机规则。不添加 IP、域名关键词或按名称猜测的正则。
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
| Chase / J.P. Morgan | `chase.com`, `chasecdn.com`, `jpmorgan.com` | [Chase 官网及 J.P. Morgan 业务链接](https://www.chase.com/)、[登录程序的独立资源配置](https://secure.chase.com/web/auth/dashboard) |
| Chime | `chime.com`, `chimebank.com`, `chimecard.com`, `chimepayments.com` | [官方站点](https://www.chime.com/)、[官方安全计划的金融服务资产清单](https://bugcrowd.com/engagements/chime#targets)；清单证明归属，不等同于原生 App 的生产请求清单 |
| Citi | `citi.com`, `citibank.com`, `citibankonline.com` | [官方站点](https://www.citi.com/)、[官方网银使用说明](https://www.ipbus.citi.com/assets/pdf/benefits_steps/benefits-steps-en.pdf) |
| Citizens Bank | `citizensbank.com`, `citizensbankonline.com` | [官网的 Pay My Loan / 网银登录入口](https://www.citizensbank.com/) |
| First Citizens | `firstcitizens.com`, `firstcitizensrewards.com` | [个人银行及数字银行登录入口](https://www.firstcitizens.com/personal) |
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
| U.S. Bank | `usbank.com`, `usbankgomobile.com` | [官方站点](https://www.usbank.com/) |
| Wells Fargo | `wellsfargo.com`, `wellsfargomedia.com`, `wf.com`, `wfinterface.com` | [官网及独立资源、接口引用](https://www.wellsfargo.com/) |
| Chase 汽车贷款及旧账户入口 | `astonmartinfinancial.com`, `fiskerfinance.com`, `jaguarfinancialgroup.com`, `landroverfinancialgroup.com`, `maseraticapitalusa.com`, `mclarenfinancialservices.com`, `myjaguarfinancialgroup.com`, `mylandroverfinancialgroup.com`, `mymaseraticapitalusa.com`, `mymazdacapitalservices.com`, `mysubarumotorsfinance.com`, `rivianfinancialservices.com`, `subarumotorsfinance.com` | [官方网银业务配置](https://secure.chase.com/web/auth/dashboard) 中明示的消费金融域名，含存量贷款账户入口 |

## 信用卡与零售融资

| 机构 / 服务 | 收录域名 | 官方站点依据 |
| --- | --- | --- |
| Citi 信用卡及积分 | `citicards.com`, `thankyou.com`, `cititravel.com` | [信用卡入口](https://www.citicards.com/)、[Citi 官方积分说明](https://www.citi.com/credit-cards/money-management/citi-thankyou-rewards-faqs)、[官方卡片权益与 Citi Travel](https://www.citi.com/credit-cards/citi-strata-credit-card) |
| Elan / Fidelity Rewards | `elancard.com`, `fidelityrewards.com`, `myaccountaccess.com` | [Fidelity 官方信用卡页面的 Elan 链接](https://www.fidelity.com/spend-save/visa-signature-card)、[Fidelity Rewards 正式入口](https://www.fidelityrewards.com/credit/welcome.do)、[Elan 官方持卡人登录说明](https://www.elanfinancialservices.com/credit-card/news-and-community/unlimited-cash-card.html) |
| U.S. Bank / Elan 卡片权益 | `myvisacardportal.com`, `mycardbenefits.com` | [U.S. Bank 信用卡页面](https://www.usbank.com/credit-cards.html) 的卡片权益入口；Fidelity 信用卡页面也引用 myvisacardportal.com |
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
| J.P. Morgan Securities | `jpmorgansecurities.com` | [Chase 网银投资业务配置](https://secure.chase.com/web/auth/dashboard) 提供的投资账户服务入口 |
| Merrill | `merrilledge.com`, `ml.com`, `merrill.com` | [Merrill Edge 官网](https://www.merrilledge.com/)、[美国银行的 Merrill 链接](https://www.bankofamerica.com/) |
| Robinhood | `robinhood.com` | [官方站点](https://robinhood.com/us/en/) |
| Charles Schwab / thinkorswim | `schwab.com`, `schwabcdn.com`, `schwabinstitutional.com`, `schwabplan.com`, `schwabworkplaceservices.com`, `schwab529plan.com`, `schwabfunds.com`, `csimfunds.com`, `thinkorswim.com` | [官网的退休、529 及工作福利入口](https://www.schwab.com/)、[登录页面资源](https://client.schwab.com/Areas/Access/Login)、[thinkorswim 官方说明](https://workplace.schwab.com/story/introduction-to-thinkorswim-web) |
| Vanguard | `vanguard.com` | [官方站点](https://investor.vanguard.com/) |
| Wealthfront | `wealthfront.com` | [官网、账户及资源入口](https://www.wealthfront.com/) |
| Wells Fargo Advisors | `wellsfargoadvisors.com`, `wfafinet.com` | [Wells Fargo 登录页](https://connect.secure.wellsfargo.com/auth/login/present) 所加载的 [投资账户登录程序](https://connect.secure.wellsfargo.com/auth/static/ui/loginaltsignon/public/js/main.242a0e2a5ef9d2046d10.js) 配置 |

## 支付与汇款

| 机构 / 服务 | 收录域名 | 官方站点依据 |
| --- | --- | --- |
| Cash App | `cash.app`, `cash.me` | [官方站点](https://cash.app/) |
| PayPal | `paypal.com`, `paypal.me`, `paypalobjects.com` | [PayPal.Me 官方说明](https://www.paypal.com/us/cshelp/article/paypalme-frequently-asked-questions-help432)、[官方 SDK / API 所需域名](https://developer.paypal.com/platforms/checkout/fastlane/getstarted/) |
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

## 金融机构专属主机及直接账户入口（精确匹配）

下面仅匹配列出的主机本身，不匹配平台根域、其他主机或任意下级子域名。
机构专属租户主机结合机构标识和官方配置确认关联；金融账户门户则须由机构官网直链、官方业务文档或发行方资产披露确认用途，不能只有 CSP / SDK 引用。

| 机构 / 服务 | 精确主机 | 官方依据与用途 |
| --- | --- | --- |
| Cash App | `cash-f.squarecdn.com`, `cash-images-f.squarecdn.com` | [官网](https://cash.app/) 与 [登录页](https://cash.app/login) 引用的 Cash App 专属资源 |
| Credit Karma | `creditkarmacdn-a.akamaihd.net` | [官网](https://www.creditkarma.com/) 引用的 CSS / JS 资源 |
| Citizens Bank | `www.accessmycardonline.com`, `login.bdreporting.com` | [官网](https://www.citizensbank.com/) 的信用卡及 Clarfeld Client Access 登录入口 |
| Navy Federal | `navyfederal.lendkey.com`, `navyfederal-mba.lendkey.com`, `navyfederal-refi-med.lendkey.com`, `client.osaicinstitutions.com` | [官网](https://www.navyfederal.org/) 的学生贷款、贷款再融资及投资账户入口 / 官方域名配置 |
| First Citizens | `firstcitizens.netxinvestor.com` | [官网](https://www.firstcitizens.com/personal) 的投资账户入口 |
| TD Bank | `tdinvestmentservices.netxinvestor.com`, `tdwealth.netxinvestor.com` | [美国官网](https://www.td.com/us/en/personal-banking) 的投资及财富账户入口 |
| Santander | `santandercards-web.oflows.net` | [官网](https://www.santanderbank.com/) 的 `connect-src` 业务端点 |
| Bank of America | `boa-api.arkoselabs.com` | [官方登录页](https://secure.bankofamerica.com/auth/signon/) 引用的 [验证码组件](https://secure1.bac-assets.com/auth/signon/spa-assets/js/common-chunks/common-es6-components-37b4bd18d0d4b150bdbf.m.js) 配置 |
| Robinhood | `fp.robinhood.net` | [官方登录页](https://robinhood.com/login) 的预连接主机；该证据不单独证明原生 App 调用或具体采集行为 |
| Synchrony 专属登录保护 | `synchronybank-us.gw-dv.vip`, `synchronybank-us.gw-dv.io`, `synchronybank-us.gw-dv.xyz`, `synchronybank-us.cdn-gw-dv.vip`, `synchronybank-us.ck123.io` | [官方登录页](https://securelogin.synchronybank.com/) 配置中明确带 synchronybank-us 标识的租户主机；不收录公共采集服务或测试主机 |
| Vanguard 专属认证及登录资源 | `vanguard.okta.com`, `ccc.vgcontent.info` | [官方登录页](https://logon.vanguard.com/logon) 的认证租户及实际加载的 vg-vgn 样式 / 脚本；排除共用行情接口与 oktapreview 测试租户 |
| First Citizens 投资与退休账户 | `firstcitizens.wealthaccess.com`, `secure.newportgroup.com` | [官方页面或资源](https://www.firstcitizens.com/personal)；官网提供的账户入口 |
| Wealthfront 专属账户连接 | `finapp.wealthfront.yodlee.com` | [官方登录页](https://www.wealthfront.com/login) 引用的 finapp.wealthfront 租户主机；不收录 Plaid / Yodlee 公共接口与 CDN |
| Synchrony 账户服务 | `finapp.synchrony.yodlee.com`, `finapp.synchronyiav.yodlee.com`, `www.onlinecreditcenter6.com` | [当前官方登录配置](https://securelogin.synchronybank.com/) 中的 Synchrony 专属连接租户；[发行方官方资产披露](https://investors.synchrony.com/filings-regulatory/sec-filings/all-sec-filings/content/0001193125-14-228938/d680310dex101.htm) 列出 onlinecreditcenter6.com，结合当前引用及页面品牌确认账户用途；不收录公共 CDN 和账单组件 |
| TD / Citizens 信用卡、财富及账单服务 | `tdbank.billeriq.com`, `clientpoint.fisglobal.com`, `www.centresuite.com` | [官方页面或资源](https://www.td.com/us/en/personal-banking)；美国官网提供的账单、信托投资及信用卡账户入口；Citizens 官网也引用 CentreSuite |
| Robinhood 退休账户转入 | `app.rollovercentral.com` | [机构登录页](https://robinhood.com/login) CSP 证明关联；[SS&C 官方产品说明](https://www.ssctech.com/resources/form/streamlining-ira-rollovers-smarter-approach-2025) 确认 IRA 转入业务；[公开账户门户](https://app.rollovercentral.com/) 返回 RolloverCentral 退休业务页面 |
| Chase 退休测算 | `chaseretcalculator.moneyguidepro.com` | [官方网银程序配置](https://secure.chase.com/web/auth/dashboard) 中的 Chase 专属退休测算主机；不收录共用账户聚合 / 授权 API |

`clientpoint.fisglobal.com`、`secure.newportgroup.com`、`login.bdreporting.com` 等仍可能服务多家金融机构；
保留的依据是官网直接提供的信托投资、退休或财富账户入口，而不是它们出现在某个 SDK 的配置里。
这些入口承载金融账户业务；域名规则仍无法按机构或地区进一步区分。

不收录 `www.google.com`、`www.gstatic.com`、`accounts.google.com`、`appleid.apple.com` 等通用网页、资源和登录主机，
也不收录 reCAPTCHA、Cloudflare Turnstile、DataDome 等跨行业通用服务的共享主机。
跨行业共用的指纹、身份验证、风控、运营商验证及 IP 查询端点，同样不因金融页面引用就加入。
无法确认属于金融机构专属主机或直接金融账户入口的共享资源从严排除。
例如保留银行专属的 `boa-api.arkoselabs.com`、`vanguard.okta.com`，排除通用的 `iframe.arkoselabs.com` 和 Google / Apple 登录；
Apple Pay、Google Pay、卡组织的 Checkout / 钱包页面及 Stripe、Checkout.com、Cardinal 3DS 等通用支付组件均不纳入本集合。
Braintree 公共支付 API、Square PCI 连接和 Paymentech 支付网关也按此原则排除。
排除 `applepay.cdn-apple.com`、`pay.google.com`、`secure.checkout.visa.com`、`assets.secure.checkout.visa.com`、`pay.discovernetwork.com`。

`cloudfront.net`、`akamaihd.net`、`squarecdn.com`、`ctfassets.net`、`google.com`、`gstatic.com`、`okta.com` 等共享平台不会整域收录。
例如某些 Contentful 图片使用相同主机、通过 URL 路径区分租户，域名规则无法仅选中金融机构的资源。
机构自有域名下的资源仍按域名后缀匹配。
CSP 明示的主机表示官方页面允许相应业务依赖，不等同于每次访问必然发出请求；代码中的测试环境、示例及广告拦截检测域名不据此收录。

### 共享组件复查后的排除范围

以下 20 条精确主机不收录，避免把金融机构页面依赖的共用组件扩展成金融分流规则：

| 类型 | 排除主机 | 依据及排除原因 |
| --- | --- | --- |
| Plaid 公共 API / SDK | `production.plaid.com`, `cdn.plaid.com` | [官方 Link Web SDK](https://plaid.com/docs/link/web/) 与 [Hosted Link API 示例](https://plaid.com/docs/link/hosted-link/) 使用共用主机，无法按主机区分机构 |
| Yodlee 公共 SDK | `cdn.yodlee.com` | [官方 FastLink 集成说明](https://developer.yodlee.com/resources/yodlee/fastlink-3/docs/documentation) 提供的共用 JavaScript，不是机构专属账户主机 |
| Q2 / MX 共用组件 | `cdn1.onlineaccess1.com`, `sdk-cdn.onlineaccess1.com`, `cds-sdkcfg.onlineaccess1.com`, `q2smart.q2ebanking.com`, `widgets.moneydesktop.com`, `content.mx.com` | [First Citizens 网银页](https://digitalbanking.firstcitizens.com/) 引用的公共 SDK / 配置 / 财务管理组件；[Q2 SMART 文档](https://cdn1.onlineaccess1.com/cdn/base/documentation/help/smart/content/getstarted/sysrequirements.htm) 还明确涉及营销权限，页面引用不足以收录 |
| 共用账户聚合及授权 | `aggapi.wealthaccess.com`, `app.quovo.com`, `fin02.finicity.com`, `partnerauth.platform.intuit.com` | [Chase 程序配置](https://secure.chase.com/web/auth/dashboard) 中的共用聚合 / 授权依赖；[Wealth Access API 文档](https://api.wealthaccess.com/) 也说明其供外部系统集成，不作为机构专属账户入口收录 |
| 共用行情组件 | `frontgate-us.factset.com` | [Vanguard 投资者页](https://investor.vanguard.com/) CSP 允许的行情连接主机，不是 Vanguard 专属账户入口 |
| 仅配置引用、用途或专属性不足 | `api.moscwise.com`, `wup-d0b2efe1.us.v2.we-stats.com`, `log-d0b2efe1.us.v2.we-stats.com`, `billdetail.getbills.com`, `login.awardcenter.com`, `www.login.awardcenter.com` | 分别见 [Wise](https://wise.com/login)、[Synchrony](https://securelogin.synchronybank.com/)、[Truist](https://bank.truist.com/web/authentication) 和 [Santander](https://rolb.santanderbank.com/) 的公开配置；无法据此确认属于专属金融账户主机。`api.moscwise.com` 的公开 CNAME 为 `apicustomdomain.sardine.ai`；这不足以确认其属于 Wise 账户业务 API |

## 维护方式

修改 `geosite-finance-us.json` 的对应 `domain_suffix` 或 `domain` 数组，保持小写、排序且不重复。
规则文件使用带注释的 JSON；每条域名前的 `//` 注释记录机构、来源依据和直接来源 URL，供逐条人工 review。
新增或修改域名时同时维护相邻注释。构建保留带注释的原文，校验和也覆盖注释；注释不参与 SRS 匹配。
`sing-box` 转换器支持 `//` 行注释和 `/* ... */` 块注释，其余结构使用标准 JSON，不使用尾随逗号。
添加服务或独立域名时同步更新上面的官方来源依据，记录其登录、API、静态资源或账户服务用途，避免根据名称猜测域名。
第一方根域名已覆盖的子域名不重复加入；第三方服务必须核实机构专属租户，或通过官方来源明确确认金融账户门户用途，再使用精确主机；公共 SDK、聚合 / 授权 API、行情、采集及支付组件不得仅凭页面引用纳入。
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
