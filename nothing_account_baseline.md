# Nothing Account 账号基线

## 中国区 (CN)

### Nothing 客户端 (Nothing Phone)

#### 注册
- 邮箱注册
  - 流程: 输入邮箱 → 发送验证码 → 输入6位验证码 → 设置密码 → 完成注册
  - 验证码规格: 6位数字, 60秒有效
  - 发送限制: 同Email 60分钟内12次, 同IP 1分钟内10次
  - 异常: 验证码错误→"Incorrect verification code"
  - 异常: 错误达上限→"Too many failed attempts. Verification is suspended temporarily. Please try again in one hour." (暂停1小时)
  - 异常: 获取次数上限→点击获取验证码前弹窗拦截, "The number of attempts to obtain a verification code has exceeded the limit. Please try again after one hour."
  - 异常: 请求过于频繁→"Requested too many times, please try again later"
- 手机号注册
  - 流程: 输入手机号 → 发送短信验证码 → 输入验证码 → 设置密码
  - 仅中国区支持

#### 登录
- 邮箱+密码登录
  - 信任设备: 密码正确→直接登录; 密码错误≥3次(服务端计算)→触发二次验证
  - 非信任设备: 输入密码正确→触发二次验证(全屏验证码弹窗)
  - 非信任设备定义: 旧设备已登录+新设备登录(本地/异地)
  - 异常处理
    - 验证码错误1-10次: "Incorrect verification code", 可继续尝试
    - 错误达上限: "Too many failed attempts. Verification is suspended temporarily. Please try again in one hour." (仍在验证码界面)
    - 触发账号锁: 返回登录页重新登录→直接弹窗拦截→"For security reasons, login is temporarily suspended due to too many failed attempts. Please try again in one hour." →不进入验证码界面
    - 获取验证码次数达上限: 同界面继续点击→"The number of attempts to obtain a verification code has exceeded the limit. Please try again after one hour."
    - 请求过于频繁: "Requested too many times, please try again later"
- 手机号+验证码登录
  - 仅中国区, 保持现状
  - 有非授信设备二次验证兜底
- 第三方账号登录 (Google / Apple)
  - 安全性高, 跳过非授信设备二次校验
  - 但如开启2FA则需校验 (国内不支持2FA, 实际不涉及)
  - APP端展示2FA设置入口, 体验与邮箱登录一致

#### SSO (统登统退)
- Nothing设备上所有Nothing应用统一登录/退出
- 涉及模块: Settings / Nothing X / Essential Space / Share Widget
- 升级策略: 先升级先用, 未升级不触发
- 实现SSO后: 账号升级即可使用
- NothingAccount将上架谷歌商店, 可静默更新, 无需等OTA

#### 2FA (二次验证) — ❌ 中国区不支持
- 国内账号中心不支持2FA功能
  - 不支持开启/关闭(管理态)
  - 不支持登录时触发(运行态)
- 手机号用户: 手机号+验证码登录保持现状
- 邮箱用户: 有非授信设备二次验证兜底即可

#### 非授信设备二次验证
- 触发场景
  - 邮箱登录时检测到非信任设备→全屏验证码弹窗
  - 信任设备密码错误≥3次→全屏验证码弹窗
- 验证方式: 发送6位验证码到注册邮箱
- 涉及的端: Nothing客户端 ✅ | 出端APP ✅ | Web端 ✅
- 正常提示: "Verification — Enter the 6-digit code sent to xx****@nothing.tech to verify identity. Didn't receive the code? Send again (XXs)"
- 错误1-10次: "Incorrect verification code", 可继续尝试重发
- 错误达上限(界面内继续点): "Too many failed attempts. Verification is suspended temporarily. Please try again in one hour."
- 错误上限后返回再触发: 重新登录→直接弹窗拦截→不进入验证码界面
- 获取验证码次数达上限(界面内继续点): 同"错误次数达上限"提示
- 获取次数上限后返回再触发: 返回到登录页点下一步→弹出"Too many failed attempts"→点Understand回到登录页
- 请求过于频繁: 弹出"Requested too many times, please try again later"→点Understand后关闭弹窗回到上一步

#### 退出账号
- 触发二次校验 (仅Nothing客户端)
- 设备锁屏密码校验 (v1.0): 有锁屏密码→需输入密码(指纹/图案/数字/人脸); 无密码→直接退出
- 出端场景/Web端退出时无需二次校验
- 确认弹窗文案模板: "Are you sure you want to sign out? You'll need to sign in again to use xxx" (xxx由入口业务方可配)
- Settings入口退出文案: "以下应用将退出账号: NothingX: 退出后, 本设备将无法使用手表和健身等功能"
- 未绑定设备通用提示: "You'll be logged out of all Nothing services and apps signed in with this account on this device."
- 二次验证弹窗: 发送6位邮箱验证码, 验证通过后退出
- 验证码错误→"Incorrect verification code"
- 错误达上限→退出弹窗仍触发, 但验证码空白不可输入, 提示"验证码错误次数过多, 请稍后重试"
- 获取次数上限→点Understand关闭所有弹窗回到账号中心首页
- 点退出→确认弹窗→二次验证弹窗→验证通过→退出到登录页

#### 删除账号
- 入口: 隐私中心 → Delete Account
- 触发二次验证弹窗 (所有端: Nothing客户端 ✅ | 出端APP ✅ | Web端 ✅)
- 验证通过→调用浏览器跳转删除请求表单
- 中国区表单: https://www.wenjuan.com/s/UZBZJvooJIb/
- 异常: 错误达上限→仍触发弹窗但不下发验证码(空白不可输入)
- 错误上限后再触发→返回再点时弹窗提示1小时后再试

#### 隐私中心
- Nothing Phone上完整版
  - 需显示: Privacy Policy, User Agreement, Open Source Licenses, Delete Account
- Privacy Policy: 调用浏览器跳转 https://nothing.tech/pages/privacy-policy
- User Agreement: Nothing X沿用已有版本; 其他App(如Playground上国区)再制定对应条款
- Open Source License: 新页面加载, App库锁定后Gradle库清单再梳理
- Delete Account: 二次验证→浏览器打开删除表单

#### 设备信任管理
- 设备置信度: 区分信任设备/非信任设备
- 信任设备标记: 已成功登录过的设备
- 非信任设备: 新设备首次登录, 异地登录

#### 忘记密码
- 沿用当前Email方式: 发送重置密码邮件
- 第三方登录忘记密码: 🔄二期规划修改密码功能, 第一期走FAQ

#### 独立验证码UI
- 布局四区域
  - 红色区域: 标题固定
  - 蓝色区域: 验证码功能说明(业务调用方可配置, Account读取)
  - 绿色区域: 验证码输入区, 功能逻辑与当前一致
  - 黄色区域: 倒计时或重发操作区
- 页面返回逻辑
  - 返回键: 返回业务方调用页面
  - 多任务: 进程显示为Account, 杀进程=验证UI及Account APP退出(进程常驻)
  - 验证Pass: 返回业务方调用页面

#### 🔄二期: 归属地修改
#### 🔄二期: 手机验证码 (Only for China)
#### 🔄二期: WhatsApp验证码接入
#### 🔄二期: 第三方登录忘记&修改密码友好提示

---

### 出端 APP (非Nothing手机)

#### 适用App
- Nothing X / Playground / Essential Space / Community 等
- 账号作为业务附属能力整体打包发布

#### 登录
- 触发二次验证条件: 业务已携带最新版本账号发布 ✅
- 未携带最新版本: 不触发二次验证

#### 2FA — ❌ 中国区不支持
- 同Nothing客户端, 不支持

#### 退出账号
- ❌ 不触发二次校验 (本次需求不涉及出端退出二次验证)

#### 删除账号
- 触发二次验证弹窗 → 跳转问卷网表单

#### 隐私中心 — 精简版
- 需显示: Privacy Policy, User Agreement, Delete Account
- 无需显示: 已收集个人信息清单, 第三方共享个人信息清单, 第三方SDK, 开源许可证, 版本信息
- 原因: 业务隐私协议已包含账号相关内容, 账号中心无需重复展示

#### SDK 切换逻辑
- account SDK可用 → 走account SDK
- account SDK不可用(非Nothing手机) → 切换至flutter SDK
- if/else判断放在NothingX本体(非flutter SDK内部)

#### 升级策略
- 业务已升级+账号未升级 → 跟随该设备该业务入口现有体验
- 账号已升级+业务未升级(未实现SSO) → 跟随现有体验
- 账号已升级+业务未升级(已实现SSO) → 进入最新版本账号中心, 可查看最新内容

---

### Web 端

#### 全局规则: 不区分CN和Intl

#### 登录
- 邮箱登录: 非授信设备二次验证 ✅
- 2FA运行态: 邮箱登录如已开启2FA→触发2FA验证 ✅
- 第三方账号登录: 不触发2FA (Web端账号中心不呈现2FA入口)

#### 2FA
- 管理态: ❌ Web端统一隐藏2FA入口 (非针对第三方账号)
- 运行态: 如已在APP端开启2FA, Web端登录时触发; 第三方登录不触发
- Web端已升级+客户端未升级: 用户在Web开启2FA→客户端无法关闭

#### 删除账号
- 触发二次验证弹窗 → 跳转浏览器表单
- 中国区跳问卷网

#### 隐私中心
- 增加协议入口: Nothing账号用户协议, Nothing账号隐私声明
- 三大板块: Profile / Security / Privacy
- Security板块: Two factor authentication开关
- Privacy板块: Privacy Policy, User Agreement

#### 退出账号
- ❌ 无需二次校验

#### 升级策略
- 已升级的端先触发, 未升级保持旧版本体验
- Web端先升级→已升级功能可用, 未升级端不受影响

---

## 海外 (Intl)

### Nothing 客户端 (Nothing Phone)

#### 注册
- 邮箱注册 (同中国区流程)
  - 流程: 输入邮箱 → 发送验证码 → 输入6位验证码 → 设置密码
  - 验证码: 6位数字, 60秒有效
  - 发送限制: 同Email 60分钟内12次, 同IP 1分钟内10次
- ❌ 无手机号注册

#### 登录
- 邮箱+密码登录 (同中国区流程)
  - 信任设备: 密码错误≥3次→触发二次验证
  - 非信任设备: 密码正确后→触发二次验证
- 第三方账号登录 (Google / Apple)
  - 跳过非授信设备二次校验 (安全性高)
  - 但如开启2FA→触发2FA验证
  - APP端展示2FA设置入口, 体验与邮箱登录一致

#### SSO (统登统退)
- 同中国区

#### 2FA (二次验证) ✅ 完整支持
- 管理态 (开启/关闭)
  - 默认值: 关闭
  - 开启流程: 点击开启2FA → 发送验证码到邮箱 → 输入6位验证码 → 验证成功→开启; 验证失败→保持关闭
  - 关闭流程: 点击关闭2FA → 发送验证码到邮箱 → 输入6位验证码 → 验证成功→关闭; 验证失败→保持打开
  - 所有端均可管理: Nothing客户端 ✅ | 出端APP ✅ | Web端(管理态隐藏但开关同步)
  - 2FA开关跟账号走, 不跟设备走; 多端状态同步
  - 原子化操作: Server端排队逻辑, 多设备不可同时操作
  - 退出账号后60秒内重新登录→允许; 刚开启2FA→允许立即关闭
- 运行态 (登录时触发)
  - 已开启2FA的账号登录时→触发2FA二次验证(全屏)
  - 所有端均生效: Nothing客户端 ✅ | 出端APP ✅ | Web端(邮箱登录触发, 三方登录不触发)
  - 正常提示: "Verification — Two factor authentication — Enter the 6-digit code sent to xx****@nothing.tech"
  - 错误1-10次: "Incorrect verification code"
  - 错误达上限: "Too many failed attempts. Verification is suspended temporarily. Please try again in one hour."
  - 触发账号锁: 重新登录→直接弹窗拦截
- 异常处理 (同非授信设备)
  - 验证码错误→提示重试
  - 错误达上限→暂停1小时
  - 获取验证码次数上限→弹窗拦截
  - 请求过于频繁→提示稍后再试
- 验证码规格
  - 6位数字, 60秒有效
  - 发送限制: 同Email 60分钟内12次, 同IP 1分钟内10次
- 场景: 开启2FA(弹窗) / 关闭2FA(弹窗)

#### 非授信设备二次验证
- 同中国区完整流程

#### 退出账号
- 仅Nothing客户端退出触发二次校验
- 同中国区完整流程

#### 删除账号
- 触发二次验证弹窗 → 跳转浏览器表单
- 海外表单: https://docs.google.com/forms/d/e/1FAIpQLScpIGeFODh4d-SaaBrRmq5juLCQ9kQsp96a813XPAIhMaMrVg/viewform
- 异常处理同中国区

#### 隐私中心
- Nothing Phone上完整intl版本
  - 需显示: Privacy Policy, User Agreement, Open Source Licenses, Delete Account
- Privacy Policy: https://nothing.tech/pages/privacy-policy
- User Agreement: https://nothing.tech/pages/user-agreement (海外版本)
- Open Source License: 新页面加载

#### 引导开启2FA
- 前提: 用户未开启2FA
- 触发场景举例
  - 非信任设备登录
  - 高危用户数据操作 (数据删除, 数据导出)
  - 业务方触发敏感操作 (订阅支付, 退订)
- 流程
  - 引导页面: 说明危险操作+打开2FA的必要性
  - 打开流程: 与用户主动进入Settings开启流程一致
  - 打开完毕: 返回正确结果给调用方, 业务方流程继续, 无需再验证一次
  - 返回按钮: 返回业务方页面(非账号页面)
- 已登录设备: 业务场景触发引导, 引导逻辑放业务App, Account提供SDK
- 新设备登录: 即使没开2FA, 新设备登录时触发二次校验

#### 小红点逻辑
- Settings Icon小红点: 新功能推出或重要功能更新时高亮提醒
- 显示逻辑
  - 标记为可增加红点的功能(新功能/有更新的功能)
  - 用户登录账号中心首次看到该功能→标注红点
  - 用户不点击→红点不消失
  - 支持展示红点的功能需可配置(随版本)
- 消失逻辑
  - 账号维度: 一个功能对一个账号显示一次, 点击即消失
  - 跨设备同步: 任意设备点击后, 该功能红点对所有设备消失
  - 清数据/恢复出厂设置后: 已点击过则不再显示
- 红点API: 服务端新增接口提供状态逻辑, 按账号维度管理, 无法本地存储

#### 🔄二期: 归属地修改
#### 🔄二期: WhatsApp验证码接入

---

### 出端 APP (非Nothing手机)

#### 适用App
- Nothing X / Playground / Essential Space 等

#### 登录
- 触发二次验证: 业务已携带最新版本账号 ✅
- 未携带最新版本: 不触发二次验证

#### 2FA ✅
- 业务已携带最新版本账号: 管理态(可管理2FA) ✅ + 运行态(登录触发2FA) ✅
- 业务未携带最新版本: 不可管理2FA, 不触发2FA

#### 退出账号
- ❌ 不触发二次校验 (本次需求不涉及)

#### 删除账号
- 触发二次验证弹窗 → 跳转Google Forms

#### 隐私中心 — intl精简版
- 需显示: Privacy Policy, User Agreement, Delete Account

#### SDK 切换逻辑
- 同中国区出端

#### 升级策略
- 业务已升级+账号未升级 → 跟随现有体验
- 账号已升级+业务未升级(已实现SSO) → 使用最新版本账号中心

---

### Web 端

#### 全局规则: 不区分CN和Intl

#### 登录
- 邮箱登录: 非授信设备二次验证 ✅ + 2FA运行态(如已开启) ✅
- 第三方账号登录: 不触发2FA

#### 2FA
- 管理态: ❌ 统一隐藏2FA入口(非针对第三方账号隐藏)
- 运行态: 已开启2FA则邮箱登录时触发; 第三方登录不触发
- Web端已升级+客户端未升级: 用户Web端开启2FA→客户端无法关闭; 客户端登录不触发2FA

#### 账号中心
- Profile板块: 姓名, 邮箱
- Security板块: Two factor authentication开关
- Privacy板块: Privacy Policy, User Agreement
- 不区分CN和Intl

#### 升级策略
- Web端已升级+客户端未升级: 已升级功能可用, 未升级端不受影响
- 用户如在Web端开启2FA, 客户端登录时提示识别到新版本需升级(前期可不强制)

---

## 通用 (跨区域)

### 密码规则 (v1.0+)
- 用户端要求: 8-30 characters, 至少1个大写字母+1个小写字母+1个数字+1个特殊符号
- 服务端限制: 加密后6-30位
- 密码错误≥3次(服务端计算)→触发二次验证
- 无账号禁用功能, 错误次数超限不会暂停账号
- 修改密码后: 其他设备token失效, 需重新登录

### 速率限制细则 (v1.0 服务端规则)
- 登录: 同Email 60分钟内最多12次; 同IP 1分钟内最多60次
- 注册: 同IP 60分钟内最多12次
- 忘记密码: 同Email 60分钟内最多12次; 同IP 1分钟内最多10次
- 邮件验证码发送&验证: 同Email 60分钟内最多12次; 同IP 1分钟内最多10次
- 账号不会因错误次数而被暂停使用

### 设备登录限制 (v1.0)
- Nothing X / CMF watch: 仅限1台设备登录
- 在新设备登录→上一台设备token自动失效
- Nothing Phone 上可多台设备登录同账号(不同业务App通过SSO)

### 语言与邮件支持 (v1.0)
- 邮件类型: Verify Account(验证账号) / Welcome(欢迎) / Reset Password(重置密码)
- 支持语言: 英语, 西班牙语, 德语, 意大利语, 法语, 日语, 韩语, 繁体中文(台湾), 泰语, 阿拉伯语
- 列表没有的语言默认使用English
- 阿拉伯语邮件模板对应英文内容
- 语言代码参考: http://www.lingoes.net/zh/translator/langcode.htm

### 用户信息字段规则 (v1.0)
- 头像: 限图片类型, 不超过2MB
- first_name / last_name: 最长32个字符
- username: 数据库唯一, 仅支持a-z0-9_- (小写字母/数字/中横线/下划线), 不支持大写
- 昵称: 少于20个characters; 不符合规则→保持原昵称不变
- 昵称含无效字符→红色提示 "Nickname contains an invalid character" (简体中文: "昵称包含无效字符")
- 客户端+服务端双重校验禁用字符

### 账号信息记录 (v1.0)
- 一期: 记录当前设备所在国家/地区(用于Shared Widget判断分享图片版权)
- 后续: 设备使用语言, 登录设备信息(手机型号含非Nothing手机, PC/Mac)
- 预留通用接口: 接入App/Widget可按规范提交需记录的信息字段

### Account 被禁用处理 (v1.0)
- 用户手动禁用Nothing Account→SDK提供报错弹框
- UI标题: "Account disabled notification" / "Nothing账号提醒"
- UI内容: "Nothing account is disabled. Please enable it and try again." / "Nothing账号被禁用, 请启用后重试。"
- 按钮: Cancel(取消) / Go to settings(跳转设置页)
- 三方App自行判断弹框弹出时机

### Profile 页面配置 (v1.0)
- 各业务可配置在Profile页面的入口(参考Experimental features实验室功能)
- 配置信息: 图标, 名称, summary, 跳转入口链接
- 文案需支持多语言
- 支持修改头像和昵称
- ❌ Google Account入口已删除(原支持online config开关, 默认开启, 未登录跳Google sign in, 已登录跳Settings>Google)

### SSO 接入方 (v1.0)
- Nothing X app
- CMF watch app
- Shared widget (一期优先支持)
- Community widget
- 未登录→调起Nothing account登录; 未注册→进入注册流程

### Source 规范 (P0)
- nothing_x: Nothing X 首次注册
- playground: Playground 首次注册
- essential_space: Essential Space 首次注册
- community: Community 首次注册
- website: WebSite 首次注册
- os_Account: Account 首次注册
- share_widget: ShareWidget 首次注册
- 其他: 应用名称作为source
- 规则: 第一次注册成功时配置, 当前已有字段后续统一清洗

### Location 字段 (P0)
- 精度: 国家&区域
- Nothing X提供接口: NAC签发token→调用Nothing X获取location→返回到客户端
- Header: X-Aud-Nothing-X-Location: Paris
- 新用户: 按country映射到location并生成
- 🔄未来: 某版本去掉header, 改为通过token判断location

### 验证码策略
- 第一期: Email OTP
- 不用SMS: 触达率低, 安全性低, 成本高
- 🔄二期: WhatsApp (占有率高但接入复杂, 商业化论证ROI后再接入)
- 🔄二期: 手机验证码 (Only for China)

### 二次验证码规格 (全局)
- 验证码: 6位数字
- 有效时长: 60秒
- 发送限制
  - 相同Email: 60分钟内12次请求
  - 相同IP: 1分钟内10次请求
- 60秒内只发一次: 即使上一次成功也不重复发送
- 错误次数达上限(10次)→触发1小时锁定

### 安全模型
- 生命周期管理
  - 登录: 信任设备密码错误≥3次 / 非信任设备(本地/异地)
  - 密码修改: Email方式忘记密码
  - 🔄二期: 归属地修改
- 业务支持
  - 订阅: 体验结束/未结束启动订阅→二次验证
  - 退订/退款: 终止订阅服务→二次验证
- 合规&安全
  - 数据导出: 用户触发导出个人数据→二次验证
  - 账号注销: 最终确认注销验证→二次验证
  - 撤销隐私同意: 二次验证确认本人操作
  - 变更2FA信息: 开启/关闭2FA→二次验证

### 升级策略 (统一原则: 先升级先用)
- Nothing设备
  - 业务已升级+账号未升级 → 跟随该业务入口现有体验
  - 账号已升级+业务未升级(未实现SSO) → 跟随现有体验
  - 账号已升级+业务未升级(已实现SSO) → 最新账号中心, 查看最新内容
- 非Nothing设备
  - 业务已携带最新账号 → 最新账号中心内容
  - 业务未携带最新 → 跟随现有体验
- 各功能差异
  - 退出账号: 已升级端先触发, 未升级保持旧版
  - 登录二次验证: 已升级端触发, 未升级不触发
  - 2FA管理态: 已升级可用, 未升级不展示
  - 2FA运行态: 已升级端触发, 未升级不触发
  - 独立二次验证: 已升级端触发, 未升级不触发
  - 隐私中心: 先升级先查看新版
- NothingAccount上架谷歌商店后可静默更新, 无需等OTA

### API 接口
- POST api/auth/login_v2
- POST api/auth/register_v2
- Response Header: X-Aud-Nothing-X-Location
- 2FA开关 API: 提供打开/关闭接口
- 红点 API: 服务端新增接口, 按账号维度管理
- 接口认证偶发401: 旧代码问题, 同步token到kafka后旧refresh token延迟失效

### 其他规则
- 退出账号后60秒内重新登录: 允许
- 刚开启2FA允许立即关闭
- 多端同时2FA操作: 逻辑上不允许, Server端原子化操作
- 2FA开关: 同步跟账号走, 不跟设备走
- 底部按钮位置: 固定不随内容滑动
- 正确验证码未超时: 即使之前输错过也可以用

### 🔄二期: 第三方登录忘记&修改密码友好提示
### 🔄二期: 归属地修改 (触发二次验证)
### 🔄二期: 手机验证码 (Only for China, 成本模拟中)
### 🔄二期: WhatsApp验证码 (ROI论证后接入)
### 🔄二期: 修改密码功能 (第一期走FAQ)

---

## 验证码异常场景速查表

### 登录时非授信设备二次验证
- 正常: "Enter the 6-digit code sent to xx****@nothing.tech" + 60s倒计时重发
- 错误1-10次: "Incorrect verification code"
- 错误达上限(界面内): "Too many failed attempts. Verification is suspended temporarily. Please try again in one hour."
- 错误上限后返回再触发: 重新登录→弹窗→"For security reasons, login is temporarily suspended due to too many failed attempts. Please try again in one hour." →不进入验证码界面
- 获取上限(界面内): 同错误达上限
- 获取上限后返回再触发: 回到登录页点下一步→弹窗拦截
- 请求过于频繁: "Requested too many times, please try again later" →点Understand消失

### 2FA二次验证 (仅海外)
- 正常: "Two factor authentication — Enter the 6-digit code sent to xx****@nothing.tech"
- 错误1-10次: "Incorrect verification code"
- 错误达上限: "Too many failed attempts. Verification is suspended temporarily. Please try again in one hour."
- 触发账号锁: 重新登录→弹窗拦截

### 退出账号二次验证 (仅Nothing客户端)
- 正常: 同登录非授信设备验证码
- 错误1-10次: "Incorrect verification code"
- 错误达上限: 仍弹窗但不下发验证码(空白不可输入) + "验证码错误次数过多, 请稍后重试" + Understand→关闭回首页
- 获取上限后: "The number of attempts to obtain a verification code has exceeded the limit. Please try again after one hour." + Understand→关闭回首页

### 注册验证码
- 正常: 同登录验证码流程
- 错误1-10次: "Incorrect verification code"
- 错误达上限: 输入邮箱号点继续前就弹窗拦截: "验证码错误次数过多, 请稍后重试"
- 获取上限后: 点继续前弹窗: "The number of attempts to obtain a verification code has exceeded the limit. Please try again after one hour."

### 开启/关闭2FA验证码 (仅海外)
- 正常: "New code sent" → 输入验证码
- 错误1-10次: "Incorrect verification code"
- 错误达上限: 点击开启/关闭时即弹窗→"验证码错误次数过多, 请稍后重试"
- 获取上限后: 弹窗: "The number of attempts to obtain a verification code has exceeded the limit. Please try again after one hour."

### 删除账号验证码 (所有端)
- 正常: "New code sent" → 输入验证码
- 错误1-10次: "Incorrect verification code"
- 错误达上限: 仍弹窗但不下发验证码(空白不可输入) + "验证码错误次数过多, 请稍后重试" + Understand→关闭
- 获取上限后: Understand→关闭弹窗
