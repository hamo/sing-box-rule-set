# 美国金融服务移动端域名核对

核对日期：2026-10-17。对应 `geosite-finance-us`，规则原文仍由本仓库维护，不同步第三方域名列表。

本轮读取公开 App 关联文件、官方资产清单、未登录页面及其引用的前端资源、官方 SDK 源码和文档。
没有登录账户、运行手机 App 或抓取实际交易流量。因此这里记录的是公开证据覆盖范围，不是各 App 当前版本的完整网络请求清单。

## 如何理解证据

| 证据 | 能证明什么 | 不能据此推断什么 |
| --- | --- | --- |
| AASA / Android Asset Links | 站点声明与指定 App 的链接或凭据关联 | 所有 API、风控依赖；每个列出的 App 都使用该主机发请求 |
| 机构官方安全计划的资产清单 | 机构确认资产归属 | 清单中所有资产都是生产 App 的必需端点 |
| 官方登录页及其引用的程序 | 页面引用、预连接或业务代码配置了具体地址 | 每个分支都会执行；原生 App 必然调用同一端点 |
| 官方 SDK 的 Production 配置 | 对应组件生产环境的接口和依赖 | 机构一定集成了该组件或使用同一 SDK 版本 |

第一方根域已经覆盖的子域名不重复加入。第三方服务仅补充已核实的主机，使用 `domain` 精确匹配，不自动扩展到平台其他主机。
支付组件可能也在其他机构和商户网站中使用，这些网站发往同一支付主机的请求也会匹配本规则。

## 本轮新增与依据

### 第一方金融业务域名

| 机构 | 新增域名后缀 | 官方依据与判断 |
| --- | --- | --- |
| Chime | `chimebank.com`, `chimecard.com`, `chimepayments.com` | [官方安全计划的 Primary Targets](https://bugcrowd.com/engagements/chime#targets) 同时列出这三个金融服务资产范围、Chime Android / iOS 正式版及 `app.chime.com`。这是资产归属证据，未据此断言某个生产 App 的 API 地址；未把清单中的全部内部、其他产品或测试资产复制进规则。 |
| Chase | `chasecdn.com` | [官方登录程序](https://secure.chase.com/web/auth/dashboard) 的配置引用 `secure.chasecdn.com`，用于登录相关内容、资源及故障页面。 |
| Wells Fargo Advisors | `wellsfargoadvisors.com`, `wfafinet.com` | [官方登录页](https://connect.secure.wellsfargo.com/auth/login/present) 所引用的 [版本化登录程序](https://connect.secure.wellsfargo.com/auth/static/ui/loginaltsignon/public/js/main.242a0e2a5ef9d2046d10.js) 中配置了独立的投资账户入口。 |

### 登录、验证码和支付依赖

| 主机（精确匹配） | 依据 | 证据范围 |
| --- | --- | --- |
| `boa-api.arkoselabs.com` | [BofA 官方登录页](https://secure.bankofamerica.com/auth/signon/) 引用的 [验证码公共组件](https://secure1.bac-assets.com/auth/signon/spa-assets/js/common-chunks/common-es6-components-37b4bd18d0d4b150bdbf.m.js) 配置该主机的 `/v2/` 脚本接口及验证码成功、失败事件 | 可确定是 BofA 登录验证码租户；不收录整个 `arkoselabs.com`。 |
| `cash-images-f.squarecdn.com` | [Cash App 登录页](https://cash.app/login) 的 `cdn.imageUrl` 配置 | 登录图片资源，精确到该主机。 |
| `pci-connect.squareup.com` | Cash App 登录页引用的 [版本化程序](https://cash-f.squarecdn.com/web/login/c088f93f5bbb609e19c2851a3d4baabfe0ac9160/main.e42a62cc19c77425.js) 的 `production` 支付配置 | 包含 Google Pay 令牌接口；排除同段代码中的 `squareupstaging.com` 测试地址。 |
| `fp.robinhood.net` | [Robinhood 官方登录页](https://robinhood.com/login) 的 `preconnect` 配置；同页还引用已被现有规则覆盖的 `fp.robinhood.com` | 仅据此确认登录页面指定了独立预连接主机，不凭 `fp` 命名断言采集内容或原生 App 调用。 |

### 支付 SDK 和 3DS 认证

[Braintree 官方 Web SDK 文档](https://braintree.github.io/braintree-web/current/#content-security-policy) 分别列出了 Apple Pay、Google Pay 和 3D Secure 的生产域名。
本次同时核对了 [官方文档源码固定版本](https://github.com/braintree/braintree-web/blob/9672fcf9dcd6100b74ca863e8691bb7bfc019dc6/jsdoc/Home.md)。
这里的 Web SDK 证据适用于对应支付组件和浏览器流程，不自动视为每家银行原生 App 的依赖证明。

官方配置引用 [Songbird 生产加载器](https://songbird.cardinalcommerce.com/edge/v1/songbird.js)，其引用的
[版本化生产配置](https://songbird.cardinalcommerce.com/edge/v1/597f4104d311c33d4189/1.597f4104d311c33d4189.songbird.js)
进一步列出了下面的接口、消息来源、日志及可选支付组件地址。仅按明示主机添加，不按 SDK 允许的通配域名或 ACS 的任意来源扩大匹配。

| 主机（精确匹配） | 官方配置中的用途 |
| --- | --- |
| `songbird.cardinalcommerce.com`, `static.client.cardinaltrusted.com` | 官方 SDK 文档的 Production 脚本来源 |
| `centinelapi.cardinalcommerce.com` | 生产认证 API、订单接口和消息来源 |
| `hostedfields.cardinalcommerce.com`, `geo.cardinalcommerce.com`, `0geo.cardinalcommerce.com`, `1geo.cardinalcommerce.com` | 生产配置明确列出的 `postMessageDomains`；该配置本身不证明每个会话都会连接全部主机 |
| `writer.cardinalcommerce.com` | SDK 的生产 `s3Writer` 日志接口 |
| `applepay.cdn-apple.com`, `pay.google.com` | Braintree 文档的 Apple Pay / Google Pay Production 组件依赖；不扩大到 `apple.com`、`cdn-apple.com` 或 `google.com` 整域 |
| `secure.checkout.visa.com`, `assets.secure.checkout.visa.com`, `pay.discovernetwork.com` | Songbird 生产配置中的可选 Visa Checkout / Discover Wallet 组件；存在配置不等同于这些组件在当前 App 中启用 |

固定版本 Songbird 配置的 SHA-256：`49f44b77dcf6c6d78e309bdea55a83ff9fcd20f461aa08c11416126d1b3663c8`。
外部前端版本更新后 URL 可能失效，维护时需要从官方入口重新核实引用关系，不能仅根据旧主机名称继续扩展。

## 已覆盖，无需增加重复规则

| 机构 / 服务 | 本轮核对的已有域名示例 | 官方依据 |
| --- | --- | --- |
| Capital One | `verified.capitalone.com`, `tms.capitalone.com`, `bfp.capitalone.com`, `deviceinfo.capitalone.com` | [登录页](https://verified.capitalone.com/auth/signin) 的生产 Bootstrap 资源及 [官网](https://www.capitalone.com/) 的浏览器指纹脚本引用，均由 `capitalone.com` 覆盖 |
| Venmo / PayPal | `id.venmo.com`, `api.venmo.com`, `c.paypal.com`, `b.stats.paypal.com`, `ddbm2.paypal.com`, `www.paypalobjects.com` | [Venmo 登录入口](https://venmo.com/account/sign-in) 的跳转和资源引用，已被 `venmo.com`、`paypal.com`、`paypalobjects.com` 覆盖 |
| PayPal / Braintree Android | `api.braintreegateway.com`, `api-m.paypal.com` | 官方 Android SDK 的 [生产 API 配置](https://github.com/braintree/braintree_android/blob/84e9886561f990edf5f24a3b610a21eaffdd6d99/BraintreeCore/src/main/java/com/braintreepayments/api/core/TokenizationKey.kt) 和 [事件上报地址](https://github.com/braintree/braintree_android/blob/84e9886561f990edf5f24a3b610a21eaffdd6d99/BraintreeCore/src/main/java/com/braintreepayments/api/core/AnalyticsApi.kt)；[Magnes 集成代码](https://github.com/braintree/braintree_android/blob/84e9886561f990edf5f24a3b610a21eaffdd6d99/DataCollector/src/main/java/com/braintreepayments/api/datacollector/MagnesInternalClient.kt) 另可确认原生风控采集集成，但不据此臆测 SDK 内部所有网络地址 |
| American Express | `acs-safekey.americanexpress.com`, `bdaas.americanexpress.com`, `sso.americanexpress.com`, `global.americanexpress.com`, `icm.aexp-static.com` | [官方登录页](https://www.americanexpress.com/en-us/account/login) 的登录、SafeKey 和资源配置 |
| Wells Fargo | `c1.wfinterface.com`, `connect.secure.wellsfargo.com`, `www10.wellsfargomedia.com`, `www15.wellsfargomedia.com` | [官方登录页](https://connect.secure.wellsfargo.com/auth/login/present) 的资源引用 |
| E*TRADE | `mobiletrade.etrade.com`, `federation.etrade.com`, `trading.etrade.com`, `cdn2.etrade.net` | [官方登录入口](https://us.etrade.com/e/t/user/login) 的业务配置 |
| USAA | `api-a.usaa.com`, `mobile.usaa.com`, `secure.usaa.com` | [官方登录入口](https://www.usaa.com/inet/ent_logon/Logon) 的资源及接口引用 |

其他机构的 App 关联核对结果见下一节；没有新增独立域名不表示其 App 没有 API。

## App 关联文件核对范围

对规则说明中 47 个主要服务域查询了 Apple 的 AASA 缓存，其中 30 个返回含 App 标识的关联记录。
所有查询的主域本来就已被后缀规则覆盖，本轮不重复添加这些域名。
缓存可能滞后，源站可在不同子域部署不同文件；某个根域查询返回 404，不能据此判断 App 不存在或没有关联域名。
关联记录也可能包含其他地区、企业签名或测试包，不能把所有标识都当作美国正式版。

| 服务 | 查询主域 | 结果 |
| --- | --- | --- |
| Fifth Third Bank | [`53.com`](https://app-site-association.cdn-apple.com/a/v1/53.com) | 本次根域查询未取得关联文件 |
| Ally | [`ally.com`](https://app-site-association.cdn-apple.com/a/v1/ally.com) | 返回含 App 标识的关联记录 |
| Bank of America | [`bankofamerica.com`](https://app-site-association.cdn-apple.com/a/v1/bankofamerica.com) | 返回含 App 标识的关联记录 |
| BMO US | [`bmo.com`](https://app-site-association.cdn-apple.com/a/v1/bmo.com) | 本次根域查询未取得关联文件 |
| Capital One | [`capitalone.com`](https://app-site-association.cdn-apple.com/a/v1/capitalone.com) | 返回含 App 标识的关联记录 |
| Chase / J.P. Morgan | [`chase.com`](https://app-site-association.cdn-apple.com/a/v1/chase.com) | 返回含 App 标识的关联记录 |
| Chime | [`chime.com`](https://app-site-association.cdn-apple.com/a/v1/chime.com) | 返回含 App 标识的关联记录 |
| Citi | [`citi.com`](https://app-site-association.cdn-apple.com/a/v1/citi.com) | 返回含 App 标识的关联记录 |
| Citizens Bank | [`citizensbank.com`](https://app-site-association.cdn-apple.com/a/v1/citizensbank.com) | 本次根域查询未取得关联文件 |
| First Citizens | [`firstcitizens.com`](https://app-site-association.cdn-apple.com/a/v1/firstcitizens.com) | 本次根域查询未取得关联文件 |
| Huntington | [`huntington.com`](https://app-site-association.cdn-apple.com/a/v1/huntington.com) | 返回含 App 标识的关联记录 |
| KeyBank | [`key.com`](https://app-site-association.cdn-apple.com/a/v1/key.com) | 返回含 App 标识的关联记录 |
| Marcus by Goldman Sachs | [`marcus.com`](https://app-site-association.cdn-apple.com/a/v1/marcus.com) | 本次根域查询未取得关联文件 |
| Navy Federal Credit Union | [`navyfederal.org`](https://app-site-association.cdn-apple.com/a/v1/navyfederal.org) | 返回含 App 标识的关联记录 |
| PNC | [`pnc.com`](https://app-site-association.cdn-apple.com/a/v1/pnc.com) | 本次根域查询未取得关联文件 |
| Regions | [`regions.com`](https://app-site-association.cdn-apple.com/a/v1/regions.com) | 本次根域查询未取得关联文件 |
| Santander / Openbank US | [`santanderbank.com`](https://app-site-association.cdn-apple.com/a/v1/santanderbank.com) | 返回含 App 标识的关联记录 |
| SoFi | [`sofi.com`](https://app-site-association.cdn-apple.com/a/v1/sofi.com) | 返回含 App 标识的关联记录 |
| TD Bank US | [`td.com`](https://app-site-association.cdn-apple.com/a/v1/td.com) | 返回含 App 标识的关联记录 |
| Truist | [`truist.com`](https://app-site-association.cdn-apple.com/a/v1/truist.com) | 本次根域查询未取得关联文件 |
| USAA | [`usaa.com`](https://app-site-association.cdn-apple.com/a/v1/usaa.com) | 返回含 App 标识的关联记录 |
| U.S. Bank | [`usbank.com`](https://app-site-association.cdn-apple.com/a/v1/usbank.com) | 返回含 App 标识的关联记录 |
| Wells Fargo | [`wellsfargo.com`](https://app-site-association.cdn-apple.com/a/v1/wellsfargo.com) | 本次根域查询未取得关联文件 |
| American Express | [`americanexpress.com`](https://app-site-association.cdn-apple.com/a/v1/americanexpress.com) | 返回含 App 标识的关联记录 |
| Discover | [`discover.com`](https://app-site-association.cdn-apple.com/a/v1/discover.com) | 返回含 App 标识的关联记录 |
| Synchrony / CareCredit | [`synchrony.com`](https://app-site-association.cdn-apple.com/a/v1/synchrony.com) | 返回含 App 标识的关联记录 |
| Betterment | [`betterment.com`](https://app-site-association.cdn-apple.com/a/v1/betterment.com) | 本次根域查询未取得关联文件 |
| E*TRADE / Morgan Stanley | [`etrade.com`](https://app-site-association.cdn-apple.com/a/v1/etrade.com) | 本次根域查询未取得关联文件 |
| Fidelity / NetBenefits | [`fidelity.com`](https://app-site-association.cdn-apple.com/a/v1/fidelity.com) | 返回含 App 标识的关联记录 |
| Interactive Brokers | [`ibkr.com`](https://app-site-association.cdn-apple.com/a/v1/ibkr.com) | 返回含 App 标识的关联记录 |
| Merrill | [`merrilledge.com`](https://app-site-association.cdn-apple.com/a/v1/merrilledge.com) | 本次根域查询未取得关联文件 |
| Robinhood | [`robinhood.com`](https://app-site-association.cdn-apple.com/a/v1/robinhood.com) | 返回含 App 标识的关联记录 |
| Charles Schwab / thinkorswim | [`schwab.com`](https://app-site-association.cdn-apple.com/a/v1/schwab.com) | 返回含 App 标识的关联记录 |
| Vanguard | [`vanguard.com`](https://app-site-association.cdn-apple.com/a/v1/vanguard.com) | 返回含 App 标识的关联记录 |
| Wealthfront | [`wealthfront.com`](https://app-site-association.cdn-apple.com/a/v1/wealthfront.com) | 返回含 App 标识的关联记录 |
| Cash App | [`cash.app`](https://app-site-association.cdn-apple.com/a/v1/cash.app) | 返回含 App 标识的关联记录 |
| PayPal / Braintree | [`paypal.com`](https://app-site-association.cdn-apple.com/a/v1/paypal.com) | 返回含 App 标识的关联记录 |
| Venmo | [`venmo.com`](https://app-site-association.cdn-apple.com/a/v1/venmo.com) | 返回含 App 标识的关联记录 |
| Wise | [`wise.com`](https://app-site-association.cdn-apple.com/a/v1/wise.com) | 返回含 App 标识的关联记录 |
| Zelle | [`zelle.com`](https://app-site-association.cdn-apple.com/a/v1/zelle.com) | 本次根域查询未取得关联文件 |
| Affirm | [`affirm.com`](https://app-site-association.cdn-apple.com/a/v1/affirm.com) | 返回含 App 标识的关联记录 |
| Credit Karma | [`creditkarma.com`](https://app-site-association.cdn-apple.com/a/v1/creditkarma.com) | 返回含 App 标识的关联记录 |
| Equifax | [`equifax.com`](https://app-site-association.cdn-apple.com/a/v1/equifax.com) | 本次根域查询未取得关联文件 |
| Experian | [`experian.com`](https://app-site-association.cdn-apple.com/a/v1/experian.com) | 本次根域查询未取得关联文件 |
| Happen Bank（原 LendingClub） | [`happen.com`](https://app-site-association.cdn-apple.com/a/v1/happen.com) | 返回含 App 标识的关联记录 |
| TransUnion | [`transunion.com`](https://app-site-association.cdn-apple.com/a/v1/transunion.com) | 本次根域查询未取得关联文件 |
| 信用报告及预筛选退出服务 | [`annualcreditreport.com`](https://app-site-association.cdn-apple.com/a/v1/annualcreditreport.com) | 本次根域查询未取得关联文件 |

## 未纳入与后续核实边界

- `api.transmitsecurity.io`：Affirm [公开登录页面](https://www.affirm.com/user/signin) 引用了该服务；这是跨行业共享接口，尚未确认机构专用端点或原生 App 的实际调用，暂不加入。
- `api.sjpf.io`：Robinhood 登录资源包含共享指纹 SDK 的该地址，未据此收录整个共享指纹平台；机构自有的 `fp.robinhood.com` 已覆盖，页面明示的独立 `fp.robinhood.net` 本轮精确补充。
- `www.cdn-path.com`：American Express 登录页配置了 `inauthScriptDomain`，但尚未确认该共享主机的租户边界及原生 App 依赖，暂不加入。
- `api-js.datadome.co`、`js.datadome.co`：PayPal 的公开脚本包含共享防机器人组件地址，当前金融域下的代理入口 `ddbm2.paypal.com` 已覆盖，不把共享平台整域加入。
- 通用 CAPTCHA、内容、分析或错误上报平台，以及依赖 URL 路径区分租户的主机，不因某个 SDK 中出现过就整域收录。库中注释、示例、拦截检测用的广告域名也不作为业务依赖。
- Chime 官方资产清单还包含 `1debit.com`、`chmfin.com` 等范围，但本轮未确认其具体生产金融业务用途，不批量复制全部资产。没有把测试环境域名作为独立新增条目；现有第一方后缀本身仍可能匹配其测试子域名。
- 本地公开访问 IBKR 登录入口发生了地区跳转，该现象不作为美国 App 所需独立地区域名的依据。

后续可用实际 App 请求的脱敏域名与版本信息补证。只有域名无法区分共享平台上的不同租户时，应明确记录限制，不能用关键词、全平台域名或 IP 段代替精确证据。
