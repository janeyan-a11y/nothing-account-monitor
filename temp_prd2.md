<title>Nothing Account 2.0 PRD</title>

# Revision History

| **Version** | **Brief description** | **Date** | **Revised by** |
|-|-|-|-|
| 1.0.0 | Draft PRD | 2026/1/16 | Alex Luo |
| 1.0.1 | 更新中国区2FA，补充完整Web 2FA | 2026/3/3 | Alex Luo |
| 1.0.2 | 增加3/6 FAQ章节 | 2026/3/6 | Alex Luo |



<table><colgroup><col/><col/></colgroup><tbody><tr><td>Product Manager</td><td>TBD(Alex First)</td></tr><tr><td>UI Designer</td><td>Matteo Bandi</td></tr><tr><td>R&amp;D</td><td>Grant/Editor/Bob Tao/Lucas wang</td></tr><tr><td>QA</td><td>TBD</td></tr><tr><td>Related Jira</td><td><cite src="L8cUd8Qprow9mvxG0Jzlg44xgsh" type="jira-issue"></cite></td></tr><tr><td vertical-align="middle">Figma</td><td>Web: https://www.figma.com/design/mm9BTDcEu7w8aoViKkj8Yd/Log-in---Sign-up?node-id=2147-312864&amp;p=f&amp;t=EMo1SjOiOLxVHo2b-0#1568565405<br/>App:https://www.figma.com/design/3A0Gk4lL4UygtdyBIxJSpI/Nothing-Account-2.0?node-id=142-22478&amp;m=dev</td></tr></tbody></table>

<cite doc-id="R0nywJVt3iOuqakkT1TlQl1ygHd" file-type="wiki" title="Nothing账号优化内容（与NothingX相关）" type="doc"></cite>

### 4.1:近期产品澄清：

<table><colgroup><col/><col/></colgroup><tbody><tr><td><b>问题</b></td><td><b>产品解答</b></td></tr><tr><td>退出账号后60秒内继续立马登录，是否被允许</td><td>允许，还有刚开启2FA,允许立马关闭<cite type="user" user-id="ou_d4e4a5157f62093f9d0db82e623bc191" user-name="Wanyuan Zhong_C"></cite></td></tr><tr><td>开源协议内容空白</td><td>开源协议：<a href="https://provision.nothingtech.link/account/open-source-licence.html">https://provision.nothingtech.link/account/open-source-licence.html</a></td></tr><tr><td>三方账号，还有非信任设备的概念不？</td><td>三方账号登录，目前包含谷歌和苹果，这两种方式的登录安全性较高，在使用这两个方式快捷登录时，无需进行非授信设备的二次校验；但是如果用户开启了2FA，则需要在使用三方账号时校验，这是用户的选择。</td></tr><tr><td>三方账号登录，进到账号详情页的时候，要展示2FA的设置入口吗？</td><td>客户端（含Nothing设备/出端设备）展示，三方账号与正常邮箱账号登录体验一致；<br/>web端当前在账号中心统一隐藏了2FA这个入口，并不是针对三方账号隐藏</td></tr><tr><td>验证码60秒内只能发送一次，即使上一次已经成功了，所以这个时候就会提示用户<br/>1.这个场景正常吗<br/>2.提示语当前好像没有，只有提示用户一个小时后再试的</td><td>不应该有这个场景<cite type="user" user-id="ou_d4e4a5157f62093f9d0db82e623bc191" user-name="Wanyuan Zhong_C"></cite><cite type="user" user-id="ou_4696f8bfdaddcf282d2f7df33a6a4ea7" user-name="Grant Yang"></cite></td></tr><tr><td>如果用户已开启2FA，三方账号登录是否触发2FA</td><td>关于使用三方账号登录时是否需触发二次校验的结论，请各位知悉~<cite type="user" user-id="ou_d692c91ad7225896d6098cf2af51a13d" user-name="Lucas Luo_C"></cite> <cite type="user" user-id="ou_55608a24620722166a94aca3adf11192" user-name="Editor Zhang_C"></cite> <cite type="user" user-id="ou_8526d5509f487a5464c7eb3d64ab6b4a" user-name="Albert Huang"></cite> <cite type="user" user-id="ou_599921be8cbf190467666b808ceb1585" user-name="Jiao Qi"></cite> <cite type="user" user-id="ou_4c76a69cc138d461dc5f2e711d56b907" user-name="Mars Shao_C"></cite> <br/>客户端/出端场景：如使用三方账号登录，且该账号已开启2FA，则在登录时，该账号触发2FA验证；<br/>网页端：如使用第三方账号登录，无需触发2FA，网页端账号中心也不呈现2FA入口。</td></tr><tr><td>1、进入账号--2FA设置页<br/>2、home返回桌面<br/>3、重新进入设置，右上角头像进入账号<br/>这个时候，要到账号首页，还是2FA设置页?</td><td>这个体验挺奇怪的，第三步进入到账号中心回到了2FA设置界面后，点返回是退出了账号中心来到了设置入口，而不是账号中心。<br/>体验了下Nothing设备设置入口的其他能力，无论是点到哪个功能下级页面--返回桌面--重新进入设置入口，均是来到设置入口首页。建议我们的处理逻辑：<br/>1、进入账号--2FA设置页<br/>2、home返回桌面<br/>3、重新进入设置，右上角头像进入账号，<b>进入账号中心首页</b></td></tr></tbody></table>

### 4.1：二次验证场景提示语：

如获取验证码次数已达上限则不展示“再次发送”按钮

<table><colgroup><col/><col/><col/><col/><col/><col/><col/><col/><col/><col/><col/></colgroup><tbody><tr><td rowspan="2">触发二次验证场景</td><td colspan="3">2.0版本 涉及的端</td><td rowspan="2">正常情况提示</td><td rowspan="2">错误1-10次</td><td rowspan="2">错误次数达上限（当前界面继续点击）</td><td rowspan="2">错误上限后再触发（返回后再触发）</td><td rowspan="2">获取验证码次数到上限<br/>（当前界面继续点击）---同“错误次数达上限”提示）</td><td rowspan="2">获取验证码次数达到上限后点击<br/>（返回后再触发）</td><td rowspan="2">请求过于频繁？</td></tr><tr><td>Nothing客户端</td><td>非Nothing客户端</td><td>web端</td></tr><tr><td>邮箱登录时，非授信设备(全屏）</td><td vertical-align="middle">✔</td><td vertical-align="middle">✔</td><td vertical-align="middle">✔</td><td><img name="image.png" alt="The image shows a verification interface. At the top, it says &#34;Verification&#34; and instructs to enter the 6-digit code sent to ke****@nothing.tech to verify identity. Below, there are six numbered squares with the numbers 1, 9, 2, and three empty squares. At the bottom, it states &#34;Didn&#39;t receive the code? Send again (XXs)&#34;. This interface is related to the &#34;Verification&#34; section in the document, which discusses the二次验证场景提示语, such as when the证码次数已达上限则不展示“再次发送”按钮, and the 2.0版本涉及的端等情况." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=Mjg4ZDBiNDM1MDMxYWUyY2M2ZjNkY2M3MWEzMTdlNDJfZDljN2EyZDg2YTY5YjZhOWVlNjFhY2Y5MjJlNjllODdfSUQ6NzYyMzcyODA1NjkwNTE1ODM3MF8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="A0gwbsMEWoUhh6xb6splaJpugEc"/></td><td><img name="image.png" alt="The image shows a verification interface. At the top, it prompts to enter a 6-digit code sent to the email &#34;ke***@nothing.tech&#34;. Below, there are six numbered squares: 1, 9, 2, 2, 2, 2. At the bottom, a red text &#34;Incorrect verification code&#34; is displayed, and there is a link &#34;Didn&#39;t receive the code? Send again (XXs)&#34; in black. This image corresponds to the &#34;Verification&#34; section in the document, which discusses the二次验证场景提示语, such as when the证码次数已达上限则不展示“再次发送”按钮, and the error message &#34;Incorrect verification code&#34; is a key part of the context." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=Y2E2MDE5Y2NhZWM3MzE3NDUzYmFiNmY3OWFhN2E5YjVfYjYyZDE4ZjgyNDg0ODk2ZDdhZDVhYWY2NzM1MTg3ZThfSUQ6NzYyMzcyOTE0ODkwOTA2MzkwMF8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="PmzqbgQ6Po1QWkxi7FslWeejged"/></td><td><img name="image.png" alt="The image shows a verification interface. At the top, it prompts to enter a 6-digit code sent to &#34;ke****@nothing.tech&#34; for identity verification. Below, there are six numbered buttons: 1, 9, 2, 2, 2, 2. At the bottom, a message states &#34;Too many failed attempts. Verification is suspended temporarily. Please try again in one hour.&#34; This corresponds to the &#34;Verification&#34; scenario in the document, where the user has exceeded the error limit, causing the verification to be suspended temporarily." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=ZTYxYWVhZTIyMmQ5YWM2MGY5YzZkNjQzZThjZGZjOTJfMWQxN2UwOWI5NzYxZTI0YTAzZjIyNGJlYzAzMTBkMmVfSUQ6NzYyNzAxNzY3Nzk5OTM5NDUyN18xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="ZyAGbMJ2mopJUJxVNIDlMwesgk7"/></td><td><img name="image.png" alt="The image shows a mobile sign-in interface with a red-highlighted pop-up message. The message states &#34;For security reasons, login is temporarily suspended due to too many failed attempts. Please try again in one hour.&#34; Below the message is a &#34;Understand&#34; button. This corresponds to the &#34;delete account (popup)&#34; scenario in the revision history, where users are prompted with a similar message when attempting to delete the account, and the pop-up does not send a verification code." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=Mzc5ZjUzMDA1OWE0MDkzNTBlNTBlNzlhOWFjNTk2ODlfNWJhODRjY2ZmNDNjNDgxYWE2ZTkxM2RlY2E3NWI3ZThfSUQ6NzYyMzczNTQ3MjE1MzUzMDA3OF8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="Kxk0bDHXQoMuu0xjIwXlruNdgmc"/><br/>在输入密码完成验证点下一步时即触发该弹窗，不进入验证码界面</td><td><img name="image.png" alt="The image shows a mobile interface pop-up window with a light gray background. At the top, there is a message in black text: &#34;Requested too many times, please try again later&#34;. Below the message, there is a button labeled &#34;Understand&#34; in black text. This pop-up is related to the &#34;Nothing Account 2.0 PRD&#34; document&#39;s &#34;4.1二次验证场景提示语&#34; section, which mentions that when the number of requests exceeds the limit, the &#34;再次发送&#34; button is not displayed, and there is a prompt like &#34;验证码错误次数过多，请稍后重试--需补齐&#34;." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=ZDY1Nzg4OTFmMTk0MGMzODI5ODgyNmQ2NTE4OTEwNmVfNGYxMGI2YzA1YzdiZTVhM2RmMTNiOTM1YjAxMTc4OTlfSUQ6NzYyNzAxNjA4NDU5OTczODA3NV8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="WymqbLxgboRqVvxIrl8lAfYAguh"/></td><td>触发了账号锁，用户如果重新进入登录，则无法进入获取验证码界面，直接停留在登录界面<img name="image.png" alt="The image shows a mobile login interface with a &#34;Sign in&#34; title at the top. Below the email input field, there is a password input field with a visible password icon. A red-highlighted pop-up window displays the message &#34;For security reasons, login is temporarily suspended due to too many failed attempts. Please try again in one hour.&#34; with an &#34;Understand&#34; button below. This corresponds to the &#34;delete account (popup)&#34; scenario in the revision history, where users see a popup when clicking to delete an account, even if they trigger二次验证, and the popup does not send a verification code, which is blank and cannot be entered." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=YzJiOGEwYjY1NWUyMWM5NDI1NDVmYTllYzFmN2E1YWNfYjkwZTVmZGEwYzk0Mzg5OTE4NGFkMGY5ZTI1OWVlMTNfSUQ6NzYyNzAxNjg1MzgyNjY3MDMwMl8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="MGJlbTngpoOgAixc7tPlnwTJgwh"/></td><td></td></tr><tr><td>登录时，已开启2FA，触发2FA二次验证（全屏）</td><td vertical-align="middle">✔</td><td vertical-align="middle">✔</td><td vertical-align="middle">×</td><td><img name="image.png" alt="The image shows a verification interface for two-factor authentication. At the top, &#34;Verification&#34; is highlighted in red, with &#34;Two factor authentication&#34; below. It instructs to enter the 6-digit code sent to &#34;ma****@nothing.tech&#34; to verify identity. There are six input boxes for the code, and below them is a &#34;Didn&#39;t receive a code? Send again (XXs)&#34; prompt. At the bottom, there is a &#34;Continue&#34; button. This interface is related to the context discussing the二次验证场景提示语, such as when the证码次数已达上限则不展示“再次发送”按钮等。" href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=MjI2ZjI1NjExZjJlYWNkYmUyN2RlY2NjOWQ2Y2MyYThfZTFkY2E4ZTJiZTI4OGM2N2FlMGJiMzcyNDU5MDU1MGVfSUQ6NzYyMzcyODkxNTY1NTYxMDA3OF8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="PAxHbTTUKoNlu7xEHqhl1CSigcg"/></td><td><img name="image.png" alt="The image shows a verification interface. At the top, &#34;Verification&#34; is displayed with &#34;2FA&#34; marked in red. Below, it instructs to enter a 6-digit code sent to the email &#34;ke****@nothing.tech&#34;. The code is shown as &#34;192222&#34;. At the bottom, &#34;Incorrect verification code&#34; is highlighted in red, and there&#39;s a prompt &#34;Didn&#39;t receive the code? Send again (XXs)&#34;. This relates to the context about the &#34;Verification&#34; page in the Nothing Account 2.0 PRD, likely illustrating a scenario where the verification code is incorrect." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=OTkzM2QwN2E3ZjljYTYwMWY3YWY2NzE5NTMyNjc4NmRfMjI2OTZhZTYwM2JmYjRkNjc4MWJjZjhmNWQwYjgwMTJfSUQ6NzYyMzcyOTQwNzY1NTY5NDA0NV8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="IuiMbAAbyoRQ9MxPUNtlO2bKghb"/></td><td><img name="image.png" alt="The image shows a verification interface. At the top, it prompts to enter a 6-digit code sent to &#34;ke****@nothing.tech&#34; for identity verification. Below, there are six numbered buttons: 1, 9, 2, 2, 2, 2. At the bottom, a message states &#34;Too many failed attempts. Verification is suspended temporarily. Please try again in one hour.&#34; This corresponds to the &#34;Verification&#34; scenario in the document, where the user has exceeded the error limit, causing the verification to be suspended temporarily." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=ZWEyZjk0OGMwYTYwM2M4MTJkZTk2YWNiZjA1M2NkNmFfMzg1MzVmNzdiNDgzZmRiMTUwNGFhY2ZmMzkzMTI0YzlfSUQ6NzYyNzAxNzcyMDk4MjQ1ODA4MF8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="B87Jb6gNvoSVBOxkwxdlxCLeg6e"/></td><td><img name="image.png" alt="The image shows a mobile login interface with a &#34;Sign in&#34; title at the top. The username &#34;keith.chan@nothing.tech&#34; is displayed, and the password field is partially filled. A red-highlighted pop-up window in the center states &#34;For security reasons, login is temporarily suspended due to too many failed attempts. Please try again in one hour.&#34; with an &#34;Understand&#34; button below. This corresponds to the &#34;delete account (popup)&#34; scenario in the revision history, where users see a popup with the same message when deleting an account and triggering二次验证, but the popup does not send a verification code." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=NTJiNjQ2OWU3MWUyOGUwMzkyYThlNDRjMjJkNTg0ZmVfZDBmNjczNGEzNmUwODA2MjE3M2NhYTkyYjQxMzJkZDhfSUQ6NzYyMzczNTQ4NjM2Mzg0ODQxNl8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="EO9Jbor7Qo6HIuxdJ1GlAEPigxb"/></td><td><img name="image.png" alt="The image shows a mobile interface pop-up window with a light gray background. At the top, there is a message in black text: &#34;We&#39;ll send a code to your n***@mediaholy.com when you log in to Nothing Account&#34;. Below that, a larger message in black text reads: &#34;Requested too many times, please try again later&#34;. At the bottom center of the window, there is a button labeled &#34;Understand&#34; in black text. This pop-up is related to the &#34;Nothing Account 2.0 PRD&#34; document&#39;s context about二次验证场景提示语, specifically the &#34;验证码错误次数过多，请稍后重试--需补齐&#34; prompt when the user clicks the &#34;再次发送&#34; button after multiple failed attempts." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=MDEzMDlhYzA5YTIwNzg4NDg2ZjkwYTc1Y2Q1MDQ3ZGVfNDgyNmZmYWNjYWIwOGMwNDY3ZTQ3NTU1YzJiNmZmNjVfSUQ6NzYyNzAxODA0NjAxOTkzMTg3NF8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="WHzFboPG9oWDdEx08SJlAWspgTc"/></td><td><img name="image.png" alt="The image shows a mobile login interface with a &#34;Sign in&#34; title at the top. Below the email input field, there is a password input field with a visible password icon. A red-highlighted pop-up window displays the message &#34;For security reasons, login is temporarily suspended due to too many failed attempts. Please try again in one hour.&#34; with an &#34;Understand&#34; button below. This corresponds to the &#34;delete account (popup)&#34; scenario in the revision history, where users see a popup with the same message when attempting to delete the account, even if they have triggered the secondary verification." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=NWZiNWFhZDg2N2Q2OGQ2MTYzZWE0MTBlZjU4YjUyMzJfOTFjN2I5NWQ4ZTExNzkzZDcyYzA2OThkYWIxNzJhNjVfSUQ6NzYyNzAxODEyMDgyNTI2MTc4N18xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="SABubbPDAoJ1EHxQDB3leZ5ggBb"/></td><td></td></tr><tr><td>退出账号时，未启用设备指纹，触发二次验证（弹窗）</td><td vertical-align="middle">✔</td><td vertical-align="middle">✔</td><td vertical-align="middle">×</td><td><img name="image.png" alt="The image shows a verification interface. At the top, it says &#34;Verification&#34; and instructs to enter the 6-digit code sent to ke****@nothing.tech to verify identity. Below, there are six numbered squares with the numbers 1, 9, 2, and an empty square. At the bottom, there is a prompt &#34;Didn&#39;t receive the code? Send again (XXs)&#34;. This interface is related to the &#34;Verification&#34; section in the document, which discusses the二次验证场景提示语, such as when the证码次数已达上限则不展示“再次发送”按钮, and the 2.0版本涉及的端等情况." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=ODNmYzViYmZiOGYxYmIwZDNmOGU1MjYxNjIxZmNhMTZfNDZjZmY4MjBhZTA2ZjVhMWRiNDgwM2Q0YmU1ZDM2MDJfSUQ6NzYyMzcyODEyNzY1NTAyMjMwNl8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="ZwyebOtCmoW2nYxAZSklj1FggPh"/></td><td><img name="image.png" alt="The image shows a verification interface. At the top, it prompts to enter a 6-digit code sent to the email &#34;ke***@nothing.tech&#34;. Below, there are six numbered squares: 1, 9, 2, 2, 2, 2. At the bottom, a red text &#34;Incorrect verification code&#34; is displayed, and there is a prompt &#34;Didn&#39;t receive the code? Send again (XXs)&#34; in black. This image corresponds to the &#34;Verification&#34; section in the document, which discusses the二次验证场景提示语, such as when the证码次数已达上限则不展示“再次发送”按钮, and the error message &#34;Incorrect verification code&#34; is a key part of the context." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=ZGI2YzI3YTIwZGQwOTg4NDk5ODM4YzZmNDBiYTg3MWVfODUyYjg5MzRkM2I0NDlhNGE5MWMyODYwNTFlNGIwZGRfSUQ6NzYyMzcyOTE4NDIxNjc2NDEyN18xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="XN2Vb0soIotKrlxRBlGlLdZHgCc"/></td><td><img name="image.png" alt="The image shows a verification interface. At the top, it prompts to enter a 6-digit code sent to &#34;ke****@nothing.tech&#34; for identity verification. Below, there are six numbered buttons: 1, 9, 2, 2, 2, 2. At the bottom, a message states &#34;Too many failed attempts. Verification is suspended temporarily. Please try again in one hour.&#34; This corresponds to the &#34;Verification&#34; scenario in the document, where the user has exceeded the error limit, causing the verification to be suspended temporarily." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=NzQ1NGExNDUxM2UzODEyNGM3MGQ4NjEyZTUyYWJhZTRfZTdiZDkwZjlkZjliY2JhN2ViZGEyMWRhZTljNmVhMDRfSUQ6NzYyMzk3NTQzMzEzNzMxMTQ1NF8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="PnF7btyq2o7PycxLUSwlLxLog6g"/></td><td>用户点退出账号时继续触发二次验证弹窗，但是不下发验证码：验证码内容为空白不可输入：<br/>验证码错误次数过多，请稍后重试--需补齐<br/>The number of incorrect verification codes entered is too high. Please try again later.<br/>Understand</td><td><img name="image.png" alt="The image shows a mobile interface pop-up window with a light gray background. At the top, there is a message in black text: &#34;We&#39;ll send a code to your n****@mediaholy.com when you log in to Nothing Account&#34;. Below that, a larger message in black text reads: &#34;Requested too many times, please try again later&#34;. At the bottom center of the window, there is a button labeled &#34;Understand&#34; in black text. This pop-up is related to the &#34;Nothing Account 2.0 PRD&#34; document&#39;s context about二次验证场景提示语, specifically the &#34;验证码错误次数过多，请稍后重试--需补齐&#34; prompt when the user clicks the &#34;再次发送&#34; button too many times." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=OTYwNjJlOWMxYTY1NmU3YzYwNDRkMzUxNWZhMTRkODJfNjNlMTk4ZDE0NjMwZjVhYzBlYTBiZGZhM2JjYjI4NmNfSUQ6NzYyNzAxODIxNTMxNTAzMzgyOV8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="J6SQb9WrMoOwaLxTOXcl03mJgef"/><br/>点击”understand"关闭所有弹窗，回到账号中心首页底部</td><td>点击退出账号-退出账号确认-弹出此框<img name="image.png" alt="The image shows a mobile interface with a &#34;Privacy centre&#34; title at the top. Below are options like &#34;Privacy Policy&#34;, &#34;User Agreement&#34;, and &#34;Open Source Licences&#34;. A prominent pop-up message in the center states &#34;The number of attempts to obtain a verification code has exceeded the limit. Please try again after one hour.&#34; with a &#34;Understand&#34; button below. This corresponds to the context describing the &#34;获取验证码次数到上限（当前界面继续点击）&#34; scenario in the 2.0 version&#39;s二次验证场景提示语, where the user sees a pop-up after exceeding the verification code attempt limit." crop="[0.000000,0.418000,1.000000,0.692000]" href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=NGMwMGU3NTZkNTMzNDFkZjg3OTJjZDVlYzcyYjEzNjJfNThkNmMyMTc3MDgxNGMzNjEwNWQ1NzBkNjZmZWQyZjBfSUQ6NzYyNzAxOTE1NjU5MzQ5NTc3MV8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="0.240521" src="BPWhbSDvbo8nNXxXTxOl2Qrggcg"/></td><td></td></tr><tr><td>注册账号时触发的验证（全屏）</td><td vertical-align="middle">✔</td><td vertical-align="middle">✔</td><td vertical-align="middle">×</td><td><img name="image.png" alt="The image shows a verification interface on a mobile device. At the top, there is a &#34;Verification&#34; title and a prompt to enter a 6-digit code sent to &#34;ke****@nothing.tech&#34;. Below that, there is a code input box with six empty slots. Under the input box, there is a message &#34;Didn&#39;t receive the code? Send again (XXs)&#34;. At the bottom, there is a numeric keypad with numbers 0-9, a decimal point, a backspace button, and a checkmark button. This interface is related to the &#34;Verification&#34; section in the document, which discusses the 2.0 version&#39;s verification process." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=YThmZjUwN2Q3N2ZmYTI0OWNhYjQ4NzU5ZjVhZDUwYzlfZGJjYmQwNTg3NjU3ODM0ZjQ2Njk4MGE3YWVlMmJmMzZfSUQ6NzYyMzcyODMxMDU1NTUxMjU0OV8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="HtIibVt0OoPyK6xJbKqlUjDwgYc"/></td><td><img name="image.png" alt="The image shows a verification interface where a user is prompted to enter a 6-digit code sent to their email. The email address ends with &#34;@nothing.tech&#34;. The code entered is &#34;192222&#34;, and below it, there is a red text &#34;Incorrect verification code&#34;. At the bottom, there is a prompt &#34;Didn&#39;t receive the code? Send again (XXs)&#34;. This image corresponds to the &#34;Verification&#34; section in the document, which discusses the二次验证场景提示语, such as when the证码次数已达上限则不展示“再次发送”按钮, and the normal situation, error 1-10 times, and error limit scenarios." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=NGQwZjJkZDM4NWI4NzFiZWI1NjU2NDIwMzAzNGFkNWFfZTc3N2U0YmRhM2U1ZTk1Mzg1NWZhMzEzNjM4MDhiNmVfSUQ6NzYyMzcyOTIyMTc4MDkzNDM3M18xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="HZRgbZQKeoN3vQxtG03l8d75g2g"/></td><td><img name="image.png" alt="The image shows a verification interface. At the top, it prompts to enter a 6-digit code sent to &#34;ke****@nothing.tech&#34; for identity verification. Below, there are six numbered buttons: 1, 9, 2, 2, 2, 2. At the bottom, a message states &#34;Too many failed attempts. Verification is suspended temporarily. Please try again in one hour.&#34; This corresponds to the &#34;Verification&#34; scenario in the document, where the user has exceeded the error limit, causing the verification to be suspended temporarily." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=OTYzZjM5ZWNjMDc5NDEzZTg2MTQwYzYwZTQ0OWE5MWZfYjJiN2JlYjFjNzI1YTc5ZDU4YzU5OThmMTU2MDQ5MGRfSUQ6NzYyMzczMDM1NTUzNDcyODkzMF8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="UBTKbK7eBoMwoDxAwXDl1Mgwggf"/></td><td>输入邮箱号点击“继续/下一步”获取验证码前就弹窗：<br/>验证码错误次数过多，请稍后重试--需补齐</td><td><img name="image.png" alt="The image shows a mobile interface pop-up window with a light gray background. At the top, there is a message in black text: &#34;We&#39;ll send a code to your n****@mediaholy.com when you log in to Nothing Account&#34;. Below that, a larger message in black text reads: &#34;Requested too many times, please try again later&#34;. At the bottom center of the window, there is a button labeled &#34;Understand&#34; in black text. This pop-up is related to the &#34;Nothing Account 2.0 PRD&#34; document&#39;s context about二次验证场景提示语, specifically the &#34;验证码错误次数过多，请稍后重试--需补齐&#34; prompt when the user clicks the &#34;再次发送&#34; button too many times." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=ZjEwZWFhYTM2NWIzNDE3MTY1NDQ1MWE5ZTc0NzNkM2RfYWEyYzA3MjMzYjcwMmQ2ZTU0YWY1MjQ2Zjc4OGJhNmRfSUQ6NzYyNzAyMDc5NDM2NzI2NjUzM18xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="RIJvbl9zMoiwhdxd9k7lqql7gVf"/></td><td><img name="image.png" alt="The image shows a mobile interface with a &#34;Privacy centre&#34; title at the top. Below are options like &#34;Privacy Policy&#34;, &#34;User Agreement&#34;, and &#34;Open Source Licences&#34;. A prominent pop-up message in the center states &#34;The number of attempts to obtain a verification code has exceeded the limit. Please try again after one hour.&#34; with a &#34;Understand&#34; button below. This corresponds to the context describing the &#34;获取验证码次数到上限（当前界面继续点击）&#34; scenario in the 2.0 version&#39;s二次验证场景提示语, where the user sees a pop-up after exceeding the verification code attempt limit." crop="[0.000000,0.418000,1.000000,0.692000]" href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=ODk1MTJmZWM5MjFlODMxNDlhMDM3NzE0NzIwZjBiNzhfYTU2YThkMjU3NGM3NDMxN2Q1NDBlZTlhOTUxYzI5NjlfSUQ6NzYyNzAyMDg3MjMyNjY4MDI5MF8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="0.240521" src="VeWQbjqcmo361RxIEtqlkixXghd"/></td><td></td></tr><tr><td>开启2FA（弹窗）</td><td vertical-align="middle">✔</td><td vertical-align="middle">✔</td><td vertical-align="middle">×</td><td><img name="image.png" alt="The image shows a verification interface. At the top, there is a &#34;New code sent&#34; notification. Below, it prompts to enter a 6-digit code sent to &#34;ke****@nothing.tech&#34; to verify identity. There are four blank input boxes for the code. At the bottom, there is a &#34;Didn&#39;t receive the code? Send again (XXs)&#34; option. This interface is related to the &#34;Verification&#34; section in the document, which discusses the二次验证场景提示语, such as when the证码次数已达上限则不展示“再次发送”按钮, and the normal situation, error 1-10 times, and error limit scenarios." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=NTc4NmI3YWUxYzA1Yzk3MTRmODI4ODcwYjZhOTA2NWNfYjM5ZDljNmE3OGVhYWQxZTEwY2ExMmMwZGQ3MTAwZTRfSUQ6NzYyMzcyODU0ODI3NjM5MTY0M18xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="VXZXbhDKzo6RZSx7Wa4lIYNHgqe"/></td><td><img name="image.png" alt="The image shows a verification interface where a user is prompted to enter a 6-digit code sent to their email, with the email address partially obscured. The code entered is &#34;192222&#34;, and below it, there is a red text &#34;Incorrect verification code&#34;. At the bottom, there is a prompt &#34;Didn&#39;t receive the code? Send again (XXs)&#34;. This image corresponds to the &#34;Verification&#34; section in the document, which discusses the二次验证场景提示语, such as when the证码次数已达上限则不展示“再次发送”按钮, and the error message &#34;Incorrect verification code&#34; is a key part of the context." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=MGI1NjJhNjc3NjY4NDNhZTYyNmJmODVlMDczNDk2ODZfNzYzZGJlMDRlZWEyYzYxYjdkZWM3YjgxMDE4NTlkMjRfSUQ6NzYyMzcyOTIzMzk1NjgzNTAzOV8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="CXc7bjf8eo6xHMxJueJlUNIQgHc"/></td><td><img name="image.png" alt="The image shows a verification interface. At the top, it prompts to enter a 6-digit code sent to &#34;ke****@nothing.tech&#34; for identity verification. Below, there are six numbered buttons: 1, 9, 2, 2, 2, 2. At the bottom, a message states &#34;Too many failed attempts. Verification is suspended temporarily. Please try again in one hour.&#34; This corresponds to the &#34;Verification&#34; scenario in the document, where the user has exceeded the error limit, causing the verification to be suspended temporarily." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=MDVjMGJlZTk1NzllNzBjMDgxNDQ0M2FiZjE0ZWVjNjVfODVkZmM0ZTljNThiZGY3OWI4NGExOTczZDE0NDE3YzFfSUQ6NzYyMzczMTQzNjQ4MjQ4MTg4Nl8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="CUwLbDPUrowZJ7xTdH8lcghLghg"/></td><td>用户点邮箱开启2FA时即弹窗：<br/>验证码错误次数过多，请稍后重试--需补齐</td><td><img name="image.png" alt="The image shows a mobile interface pop-up window with a light gray background. At the top, there is a message in black text: &#34;We&#39;ll send a code to your n****@mediaholy.com when you log in to Nothing Account&#34;. Below that, a larger message in black text reads: &#34;Requested too many times, please try again later&#34;. At the bottom center of the window, there is a button labeled &#34;Understand&#34; in black text. This pop-up is related to the &#34;delete account (popup)&#34; scenario in the revision history, where users are prompted with a message when they attempt to delete their account, and the interface continues to trigger the secondary verification pop-up without sending a code." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=YmU0MjZkZTcwMjgzZjU3NWVlODM2MzNmNzllMTkxOTBfMDgyYTVmNTQyYWQ4Mzk3ODU2ZTRiYzkyNjRmYjRiZjNfSUQ6NzYyNzAyMDgwMDg0NzMxODc1NF8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="OxhcbkWv4oFe5nxaarclhgfwgoe"/></td><td><img name="image.png" alt="The image shows a mobile interface with a &#34;Privacy centre&#34; title at the top. Below are options like &#34;Privacy Policy&#34;, &#34;User Agreement&#34;, and &#34;Open Source Licences&#34;. A prominent pop-up message in the center states &#34;The number of attempts to obtain a verification code has exceeded the limit. Please try again after one hour.&#34; with a &#34;Understand&#34; button below. This corresponds to the context describing the &#34;获取验证码次数到上限&#34; (Verification Code Attempt Limit Reached) scenario in the 2.0 version&#39;s二次验证场景提示语 (Secondary Verification Prompting) section, where the &#34;再次发送&#34; (Resend) button is not displayed when the attempt limit is reached." crop="[0.000000,0.418000,1.000000,0.692000]" href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=NzA2MzZlMmIyY2IxZGYwZmNiZjlmZGM2Y2E1ZTMxOGVfMzgyNzcxMmUxODc0YzFmMzQ4YWQwNTQ1ODgzZWNiNmNfSUQ6NzYyNzAyMDg4MTYxMjYzOTk3MF8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="0.240521" src="Dd2nb7wVsoISb1xpjqWltCDxgRd"/></td><td></td></tr><tr><td>关闭2FA（弹窗）</td><td vertical-align="middle">✔</td><td vertical-align="middle">✔</td><td vertical-align="middle">×</td><td><img name="image.png" alt="The image shows a verification interface. At the top, there is a &#34;New code sent&#34; notification. Below, it prompts to enter a 6-digit code sent to &#34;ke****@nothing.tech&#34; to verify identity. There are four blank input boxes for the code. At the bottom, there is a &#34;Didn&#39;t receive the code? Send again (XXs)&#34; option. This interface is related to the context discussing the二次验证场景提示语, such as when the证码次数已达上限则不展示“再次发送”按钮等触发二次验证场景的情况。" href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=YjVlMWI3ZmE3ZThhNzZhNGE4Njg4MTMwZTNmNjZjNmNfNTIxZTY0NjU1ZTQ5OWQ1NDMxYjkwZTg4ZmY4ZWE4MGZfSUQ6NzYyMzcyODU2NTg0NjI4MTk1MF8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="Bz8zbXSsXoDNS2xTpxgluStOgWg"/></td><td><img name="image.png" alt="The image shows a verification interface where a user is prompted to enter a 6-digit code sent to their email, with the email address partially obscured. The code entered is &#34;192222&#34;, and below it, a red text &#34;Incorrect verification code&#34; is displayed, indicating the code is incorrect. There is also a prompt &#34;Didn&#39;t receive the code? Send again (XXs)&#34; at the bottom. This image is related to the context discussing the &#34;Verification&#34; section, likely illustrating a scenario where the verification code is entered incorrectly." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=ZmJkMzhkZmRkOTVmYzE3NDBkNjc1NDk2ZTZiNThjMDVfMTNjMGI0OWJmYTk4MGUwMjdkYTdlNDE5ZTg1OGU4MTNfSUQ6NzYyMzcyOTIzODAxNjk1NDA4NV8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="UVQtbK4igoX7DLxmHXJl5eDagud"/></td><td><img name="image.png" alt="The image shows a verification interface. At the top, it prompts to enter a 6-digit code sent to &#34;ke****@nothing.tech&#34; for identity verification. Below, there are six numbered buttons: 1, 9, 2, 2, 2, 2. At the bottom, a message states &#34;Too many failed attempts. Verification is suspended temporarily. Please try again in one hour.&#34; This corresponds to the context describing the &#34;Verification Suspended&#34; scenario in the 2.0 version, where the user receives a verification code but fails too many times, causing the verification to be temporarily suspended." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=MzUxMTlhN2I0ODQ4NGE0ZDc3NzM2MDJjNzhiYzY1NTlfNzI2MmZiY2MzMjI3ZjhiNTk5NzQ3YjYwY2Q0NjRhOTVfSUQ6NzYyMzczMTQ0MTU4Mjc3MTkzM18xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="WPSHbFWmrouSwcxfNB9lHXapgFc"/></td><td>用户点邮箱关闭2FA时即弹窗：<br/>验证码错误次数过多，请稍后重试--需补齐</td><td><img name="image.png" alt="The image shows a pop-up window with the text &#34;Requested too many times, please try again later&#34; and a &#34;Understand&#34; button below. This corresponds to the &#34;delete account (popup)&#34; scenario in the revision history of the Nothing Account 2.0 PRD, where users are prompted with a similar message when deleting an account and still triggering the secondary verification popup, but without sending a verification code." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=Y2VmMTAwZDA4Mjg3OGVhMzRiMzFjNDI1YjA2Y2MwM2FfZmMwMmE1ODQ5YjAwOTZlMzZhZDQ5ZTI1ZmE0MTg3OGFfSUQ6NzYyNzAyMDgwNjM1NDE0NDk5MF8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="WdnnbiKMOohswgxc5kllfFjhgBd"/></td><td><img name="image.png" alt="The image shows a mobile interface with a &#34;Privacy centre&#34; title at the top. Below, there are options like &#34;Privacy Policy&#34;, &#34;User Agreement&#34;, and &#34;Open Source Licences&#34;. A prominent pop-up message in the center states &#34;The number of attempts to obtain a verification code has exceeded the limit. Please try again after one hour.&#34; with a &#34;Understand&#34; button below. This corresponds to the context describing the &#34;获取验证码次数到上限（当前界面继续点击）&#34; scenario in the 2.0 version&#39;s二次验证场景提示语, where the user sees a pop-up when reaching the limit and needs to wait an hour to retry." crop="[0.000000,0.418000,1.000000,0.692000]" href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=YTUzOTNhZWJjMWMzOGI0Y2JkNmU1MWY1MjU1M2MyMDBfOWFmZTU3ZTZkZTExNWMxYWZhNDI1ZGJkMTRhYTUyMzJfSUQ6NzYyNzAyMDg4OTUwNjQ4MzkzM18xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="0.240521" src="MrIIbYrSSohEGix8WOZl6gqJgug"/></td><td></td></tr><tr><td>删除账号（弹窗）</td><td vertical-align="middle">✔</td><td vertical-align="middle">✔</td><td vertical-align="middle">✔</td><td><img name="image.png" alt="The image shows a verification interface. At the top, there is a &#34;New code sent&#34; notification. Below, it prompts to enter a 6-digit code sent to &#34;ke****@nothing.tech&#34; to verify identity. There are four blank input boxes for the code. At the bottom, there is a &#34;Didn&#39;t receive the code? Send again (XXs)&#34; option. This interface is related to the &#34;Verification&#34; section in the document, which discusses the二次验证场景提示语, such as when the证码次数已达上限则不展示“再次发送”按钮, and the normal situation, error 1-10 times, and error limit scenarios." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=ZGZlYTU2NzIzZDFlMjVjZjI5YTI4MWMwNDAzYjM0MWJfNWE2MDc0NjI2MTEzZjAwOTY3M2FiOGIxNzliOTQwOTVfSUQ6NzYyMzcyODU4NjkyNjY5MDAxM18xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="SAQ5bZQDAojP8JxDSwFlTmA8g1f"/></td><td><img name="image.png" alt="The image shows a verification interface. It prompts the user to enter a 6-digit code sent to the email &#34;ke***@nothing.tech&#34;. The code displayed is &#34;192222&#34;, and below it is a red warning &#34;Incorrect verification code&#34;. There is also a &#34;Didn&#39;t receive the code? Send again (XXs)&#34; option at the bottom. This image corresponds to the &#34;Verification&#34; section in the document, which discusses the二次验证场景提示语, such as when the证码次数已达上限则不展示“再次发送”按钮, and the error message &#34;验证码错误次数过多，请稍后重试--需补齐&#34; when the user clicks the &#34;再次发送&#34; button." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=MTg0ZThlYWE5OTA0ZGY2OWVhN2MxY2I0NjNmYzk4MmRfYTAzMzdiZDE1MzIzZWIwMjVkMDhhNmFhZTg3YjdkNzFfSUQ6NzYyMzcyOTI0NzY5NzI3NjY0Ml8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="ALI3bVNtnosEaSxVGygldvmfgtb"/></td><td><img name="image.png" alt="The image shows a verification interface. At the top, it prompts to enter a 6-digit code sent to &#34;ke****@nothing.tech&#34; for identity verification. Below, there are six numbered buttons: 1, 9, 2, 2, 2, 2. At the bottom, a message states &#34;Too many failed attempts. Verification is suspended temporarily. Please try again in one hour.&#34; This corresponds to the context describing the &#34;Verification&#34; scene in the Nothing Account 2.0 PRD, where the user encounters a verification suspension after multiple failed attempts." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=M2Y4Mzg1MWZjODg3OGUxZTkwMWEyMjdjMTUzODhmN2FfZmQ0MTViZjI1MDA5NTgzZjczY2FlZjVhOWZlN2YwYTlfSUQ6NzYyMzczMTQ1Mjk3NDQxOTY4Ml8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="N9uPbh1Beo4HqgxZHOIlKbavgzg"/></td><td>用户点删除账号时仍触发二次验证弹窗，但不下发验证码，验证码内容为空白不可输入<br/>验证码错误次数过多，请稍后重试--需补齐</td><td><img name="image.png" alt="The image shows a pop-up window with the text &#34;Requested too many times, please try again later&#34; displayed in the center, and a &#34;Understand&#34; button at the bottom. This pop-up is related to the &#34;delete account (popup)&#34; scenario in the 2.0 version&#39;s二次验证场景提示语, where users are prompted with this message when they click to delete the account and still trigger the secondary verification pop-up, but the verification code content is blank and cannot be entered." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=ZGYwMjg5NzVmMjRiNWMxMzZhNjAzZTEwZTJhNDYwZDFfNWQ2YzNhZDUwZjQyMjE4ZWZiODA4YWM3OTcyYTk4YjRfSUQ6NzYyNzAyMDgxMzUxODM0Mzg5OV8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="R8j5bg1CnoCNM2xw8prlUn5Rgwg"/></td><td><img name="image.png" alt="The image shows a mobile interface with a &#34;Privacy centre&#34; title at the top. Below are options like &#34;Privacy Policy&#34;, &#34;User Agreement&#34;, and &#34;Open Source Licences&#34;. A prominent pop-up message in the center states &#34;The number of attempts to obtain a verification code has exceeded the limit. Please try again after one hour.&#34; with a &#34;Understand&#34; button below. This corresponds to the context describing the &#34;获取验证码次数到上限（当前界面继续点击）&#34; scenario in the 2.0 version&#39;s二次验证场景提示语, where the user sees a pop-up after exceeding the verification code attempt limit." crop="[0.000000,0.418000,1.000000,0.692000]" href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=ODQwMjZjZjY5NDIzZmUzNzJiYTFmZDBhZDYxOTFkYjdfY2YyMmVjNTNkYzA1NDdlYTRhZTQ3ZjUyYjQwZTZlOTJfSUQ6NzYyNzAyMDg5Mzg4MTE3NTc3OF8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="0.240521" src="D2mKbupg6o7v76xxGvTlkZwAg6e"/></td><td></td></tr></tbody></table>

### 3.25：NothingX接入SSO后账号与系统账号不一致处理方案

![The image is a flowchart showing the process of handling the inconsistency between Nothing Account and system account when NothingX is connected to SSO. It starts with NothingX updating to the system account, then checks if the system account is already logged in. If not, it checks if NothingX needs to log in the system account. If the system account is not new, it checks if NothingX needs to log in the system account. If the system account is new, it checks if the NothingX version is the latest. If not, it prompts the user to update the NothingX version. If the NothingX version is the latest, it checks if the system account is the same as the NothingX account. If not, it prompts the user to choose a synchronization strategy. If the system account is the same as the NothingX account, it updates the system account to the NothingX account.](https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=MzNlM2MzYmUxZDU2NDY4ZWEzOTM4YjBiYjMzMDFjZDZfMDVmYjU5YzFmYzUwZjE4YmYwMTM3M2ZmMTNiZWNjYTFfSUQ6NzYyMTM4ODA3NzU3OTQzOTg0Ml8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM)

### 3.18：

<table><colgroup><col/><col/><col/></colgroup><thead><tr><th>议题</th><th>结论</th><th>方案</th></tr></thead><tbody><tr><td>登录注册接口中的 location 字段。</td><td>Nothing X 提供account server一个调用接口，签发token后account server会调用该接口获取location，并返回到客户端。客户端将该字段用于原代码的Location Header。</td><td>Header:<pre caption="&#xA;" lang="Plain Text"><code>X-Aud-Nothing-X-Location: Paris</code></pre><ol><li seq="1">请求nac登录接口；</li><li>Nac 签发token之后，执行后处理操作，判断clientId（source）为nothing x(app)，执行： <ol><li seq="1">请求nothing x后端服务，获取location信息；</li><li>设置到response header中，如 <code>X-Aud-Nothing-X-Location: Paris</code>（可选header，未来某版本会去掉，改为通过token判断location信息）</li><li>如果有 <code>X-Aud-Nothing-X-Location</code> header，则 nothing x app 设置该header值设置到nothing x request 的header location中。</li></ol></li></ol><br/>NAC 更新：<ul><li><code>POST api/auth/login_v2</code> response header增加 <code>X-Aud-Nothing-X-Location</code> 。</li><li><code>POST api/auth/register_v2</code> esponse header增加 <code>X-Aud-Nothing-X-Location</code> 。</li></ul><br/>Nothing X Server:<ul><li>增加获取用户location的接口，该接口会从mongodb中获取用户的locaiton，如果是新用户，则应该生成该用户的location。<ul><li>Request 参数：country</li><li>Request Header: Authentication Bearer $Token</li><li>处理：按照country映射到location。</li></ul></li></ul></td></tr><tr><td>接口认证偶发401问题。</td><td>旧代码遗留问题，修改代码，在同步token到kafka后，旧的refresh token 延迟失效。</td><td>同 结论。</td></tr></tbody></table>

### 3.16：账号V2.0需求各端/各业务入口升级不同时处理策略：<cite type="user" user-id="ou_c8fd3ed8428281b417f37b009cde9443" user-name="Bob Tao"></cite><cite type="user" user-id="ou_d692c91ad7225896d6098cf2af51a13d" user-name="Lucas Luo_C"></cite><cite type="user" user-id="ou_55608a24620722166a94aca3adf11192" user-name="Editor Zhang_C"></cite><cite type="user" user-id="ou_d4e4a5157f62093f9d0db82e623bc191" user-name="Wanyuan Zhong_C"></cite><cite type="user" user-id="ou_4696f8bfdaddcf282d2f7df33a6a4ea7" user-name="Grant Yang"></cite>



统一原则：先升级先用，未升级不触发。如果实现了SSO的，只要账号升级了就能使用

| 功能 | 功能说明 | web端 | Nothing客户端 | 非Nothing客户端 | **web端与客户端OTA不同时策略** | **账号与业务升级不同时策略** |
|-|-|-|-|-|-|-|
| 退出账号 | 退出账号前需二次校验（设备验证or二次验证弹窗） | 不涉及 | 涉及 | 不涉及/保留业务逻辑 | 已升级的端先触发，未升级保持旧版本体验 | 一，Nothing设备：  <br/>1，业务已升级，账号未升级---跟随该设备该业务入口现有体验  <br/>2，账号已升级，业务（暂未实现SSO）未升级---跟随该设备该业务入口现有体验  <br/>3，账号已升级，业务（已实现SSO）未升级---该设备该业务入口进入账号中心为最新版本的账号中心，可查看最新内容  <br/>二，非Nothing设备：（本次需求不涉及非nothing设备上退出账号的二次验证）  <br/>1，业务已携带最新版本账号发布--展示最新的账号中心内容，退出不触发二次校验  <br/>2，业务未携带最新版本账号发布--跟随该设备该业务入口现有体验 |
| 登录时增加二次验证 | 非受信任设备上登录时需触发二次验证弹窗 | 涉及 | 涉及 | 涉及 | 已升级的端先触发，未升级的端不触发二次验证 | 一，Nothing设备：  <br/>1，业务已升级，账号未升级---对该设备该业务入口不触发二次验证  <br/>2，账号已升级，业务（暂未实现SSO）未升级---对该设备该业务入口不触发二次验证  <br/>3，账号已升级，业务（已实现SSO）未升级---对该设备该业务入口触发二次验证  <br/>二，非Nothing设备：  <br/>1，业务已携带最新版本账号发布--对该设备该业务入口触发二次验证  <br/>2，业务未携带最新版本账号发布--对该设备该业务入口不触发二次验证 |
| 2FA管理态 | 支持开启/关闭2FA | 涉及 | 涉及 | 涉及 | web端已升级，客户端未升级---用户如在web端开启了2FA，在客户端无法关闭 | 一，Nothing设备：  <br/>1，业务已升级，账号未升级---该设备该业务入口进入账号中心无法管理2FA  <br/>2，账号已升级，业务（暂未实现SSO）未升级---该设备该业务入口进入账号中心无法管理2FA（不展示）  <br/>3，账号已升级，业务（已实现SSO）未升级---该设备该业务入口进入账号中心为最新版本的账号中心，可管理2FA  <br/>二，非Nothing设备：  <br/>1，业务已携带最新版本账号发布--该设备该业务入口进入账号中心可管理2FA  <br/>2，业务未携带最新版本账号发布--该设备该业务入口进入账号中心无法展示最新内容，不可管理2FA |
| 2FA运行态 | 在登录时支持触发2FA验证弹窗 | 涉及 | 涉及 | 涉及 | web端已升级，客户端未升级--用户如已在网页端打开了2FA，网页端登录时触发2FA二次校验；在客户端登录时不触发2FA二次校验。提示识别到新版本，需升级，否则不允许登录（前期账号业务没那么多时可无需这么强制）。客户端升级后，登录时需触发2FA。 | 一，Nothing设备：  <br/>1，业务已升级，账号未升级---该设备的业务入口无法触发2FA二次校验  <br/>2，账号已升级，业务（暂未实现SSO）未升级---该设备该业务入口登录时无法触发2FA二次校验  <br/>3，账号已升级，业务（已实现SSO）未升级---该设备该业务入口登录时可触发2FA二次校验  <br/>二，非Nothing设备：  <br/>1，业务已携带最新版本账号发布--该设备该业务入口登录时可触发2FA二次校验  <br/>2，业务未携带最新版本账号发布--该设备该业务入口登录时，不可触发2FA二次校验 |
| 独立的二次验证能力 | 业务入口判断用户使用某些能力时可增加一个二次校验弹窗 | 涉及 | 涉及 | 涉及 | 已升级的端先触发，未升级的端不触发二次验证 | 一，Nothing设备：  <br/>1，业务已升级，账号未升级---该设备的业务入口无法触发二次校验弹窗  <br/>2，账号已升级，业务（暂未实现SSO）未升级---该设备该业务入口登录时无法触发二次校验弹窗  <br/>3，账号已升级，业务（已实现SSO）未升级---该设备该业务入口登录时不可触发2FA二次校验  <br/>二，非Nothing设备：  <br/>1，业务已携带最新版本账号发布--该设备该业务入口登录时可触发二次校验弹窗  <br/>2，业务未携带最新版本账号发布--该设备该业务入口登录时，不可触发二次校验弹窗 |
| 隐私中心 | 支持展示隐私协议和删除账号 | 涉及 | 涉及 | 涉及 | 先升级先支持查看，未升级保持旧版本体验 | 一，Nothing设备：  <br/>1，业务已升级，账号未升级---跟随该设备该业务入口现有体验  <br/>2，账号已升级，业务（暂未实现SSO）未升级---跟随该设备该业务入口现有体验  <br/>3，账号已升级，业务（已实现SSO）未升级---该设备该业务入口进入账号中心为最新版本的账号中心，可查看最新内容  <br/>二，非Nothing设备：  <br/>1，业务未携带最新版本账号发布--跟随该设备该业务入口现有体验  <br/>2，业务已携带最新版本账号发布--该设备该业务入口进入账号中心为最新版本的账号中心，可查看最新内容 |
| SSO | 支持Nothing设备上的所有Nothing应用统登统退 | 不涉及 | 涉及 | 不涉及 | / | **Nothing设备：**  <br/>如业务已升级，账号未升级，则业务调用系统的账号能力，账号未升级就使用旧版本账号，账号已升级则使用新版本账号。  <br/>非Nothing设备：不涉及 |

后续策略：NothingAccount将上架谷歌商店，可静默更新，无需等待OTA版本。

### 3.12：2FA需求优化

2FA需求优化澄清：<cite doc-id="YqwNwm7Bei0D7WkHHvfluVV1gpc" file-type="wiki" title="2FA需求优化" type="doc"></cite>

**国内的账号中心不支持2FA功能（不支持开启关闭，也不支持登录时触发）**

**国内邮箱用户登录时，有非授信设备的二次验证兜底即可。国内手机号用户登录保持现状，手机号+验证码登录。**

### 3/11：埋点

<cite doc-id="wikuszcwVOSKXj0OsBQkW1cpdOz" file-type="wiki" title="NothingOS ET System" type="doc"></cite>  -Account

\*忘记密码/登录/注册/个人信息等信息下版本统一需求补充

### 3/10：2FA需求补充：



1.验证码验证错误次数过多：

<whiteboard token="DWw7w77m7hOyphbMUValBZIAgNg"></whiteboard>

2.相关文案：

<sheet sheet-id="7dL76l" token="FYfvsVSLGh0SM2tBAtklZ19CgNc"></sheet>



### 3/9：补充隐私协议相关内容<cite type="user" user-id="ou_b7e608f48617ee986d06128039652d4d" user-name="Keith Chan"></cite>（请帮助补充UI）

竞品体验：<cite doc-id="VJC8wAuC5h1TQfbGOL2lcq2tgQ1" type="doc"></cite>

*关于业务和账号的隐私展示结论--已与业务/隐私/法务对齐：*

***1.在Nothing Phone~~设备~~上****，Nothing账号作为独立的应用，所有Nothing手机上的APP通过SSO进入Account APP，设计采用intl版本。*

- 需显示：《Privacy Policy》《User Agreement》《Open source licenses》，Delete Account

![The image shows two mobile app screens related to Nothing Account privacy display. On the left screen, under "My Nothing account", there is a profile section with a photo, name "Keith", and email "keith.chang@nothing.tech". Below, "Explore more" lists items like "Playground (Beta)", "Nothing Community", "Privacy centre", "Two factor authentication", and "Sign out". On the right screen, "Privacy centre" displays links to "Privacy Policy", "User Agreement", "Open source licences", and a red "Delete account" button. This corresponds to the context about displaying privacy-related content in the Nothing Account app.](https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=OGM1M2I3NjRhZDRhNmFiNzcwNTdiN2UwYWFiOGNkNjNfMTg0NDMwYmIxMjY3ZmY4MjEwMTQ2ZTIxNTYxMTJlYjhfSUQ6NzYxNTgxOTc3NzA0Njc0NDc5Nl8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM)

***2.非Nothing Phone ~~设备~~（Apple ，vivo，etc.)上****，Nothing账号作为业务的附属能力整体打包发布（如Nothing X，未来的Essential Space），帐号中心Privacy Centre策略：*

*CN：无需展示~~最全的~~隐私内容，且业务的隐私协议包含了使用的账号相关内容，所以帐号中心无需重复展示。*

- 无需显示：《已收集个人信息清单》《第三方共享个人信息清单》《第三方SDK》《开源许可证》，版本信息
- **需显示：《Privacy Policy》《User Agreement》，Delete Account**

*Intl：海外场景的帐号中心需标注Nothing账号的用户协议和隐私政策。*

- 需显示：《Privacy Policy》《User Agreement》，Delete Account

![The image shows two mobile app screens related to the Nothing Account 2.0 Privacy Centre. The left screen displays a user profile with options like "Personal Information", "Privacy centre", and "Sign out". The right screen, labeled "Privacy centre - CN version - EN", has a red-highlighted section containing "Open source licenses", "Personal data", "Personal information collected", "Third-party data sharing", "Connected services", "Third-party SDKs", and "Version v0.0.0". At the bottom, there is a "Delete account" button. This image corresponds to the context discussing the display of privacy-related content in the web and mobile Nothing Account Center, with the red box indicating the content to be removed.](https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=NmU4MzMwNWU0MDI5Zjc1YmRjNjZlYTNlMzAyOWY3NTRfYmY0MjNhNDQwMjI3NjU4ZjI3NDA4ZmJhNzI4ZDJlZWRfSUQ6NzYxNTgxMjg5MjIwOTgxMTE2M18xNzgyODk3NTE4OjE3ODI5MDExMThfVjM)

Tips : 删除红色框中的内容即可



**3. web端Nothing账号中心**，【不区分CN和Intl 】

web端账号中心增加“Nothing账号用户协议/Nothing账号隐私声明“协议的展示入口，UI参考如下：

![The image shows a web端账号中心界面，顶部有头像，下方依次为Profile、Security、Privacy板块。Profile板块显示姓名Matteo Bandi、邮箱matteo.bandi@nothing.tech；Security板块有Two factor authentication开关；Privacy板块有Privacy Policy和User Agreement两个展示入口，右侧有箭头指向。该图是web端账号中心增加“Nothing账号用户协议/Nothing账号隐私声明”协议展示入口的UI参考示例。](https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=ZjIyZjVlMjZlMzI5ZTMwNjgwNzQ1YTVkNjRjNzllZjFfZWM0YjU2YjEyYzM4ZDZlMGNiMjg5NWNkMjllZGJjZWNfSUQ6NzYxNTUzMzk1OTg1ODE0NzA0Ml8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM)

### 3/6：FAQ答疑

补充埋点<cite type="user" user-id="ou_6749d09678d2be0a4da59186e4c48116" user-name="Jane Yan"></cite>

<table><colgroup><col/><col/></colgroup><tbody><tr><td><b>问题</b></td><td><b>产品解答</b></td></tr><tr><td>多台设备，相同账号，可以同时在登录做2FA吗？可以同时操作2FA设置吗?</td><td>逻辑上不行，Server端需要做原子化操作 <cite type="user" user-id="ou_d4e4a5157f62093f9d0db82e623bc191" user-name="Wanyuan Zhong_C"></cite><br/>周一对齐Server排队逻辑</td></tr><tr><td>之前没有2FA这个功能，用户在多台设备登录，但是一直不操作2FA的设置，是否后续会因为规则（新旧设备、密码错误次数），而导致自动触发2FA的逻辑？</td><td><b>已经登录的设备：</b>在业务场景触发并引导用户打开2FA，例如在Essential Space触发订阅。引导逻辑放到业务App中，Account提供SDK<br/><b>新设备登录：</b>即使没有打开2FA，新设备登录时触发二次校验</td></tr><tr><td>做验证码验证的时候，先用错误的验证码，弹出提示之后，再使用正确的验证码验证，是否可以走完验证流程？</td><td>是，正确的验证码没有超时都可以用</td></tr><tr><td>多端的状态是同步的吗？在设备A上面开启或关闭，在另外的设备上的开关状态是？</td><td>是，2FA开关跟账号走，不跟设备走<br/>提供2FA打开、关闭的API <cite type="user" user-id="ou_d4e4a5157f62093f9d0db82e623bc191" user-name="Wanyuan Zhong_C"></cite></td></tr><tr><td>今天写测试大纲的时候遇到一个问题想请教下：如果登录的时候，触发2FA流程，1分钟内验证码错误超过10次，弹出提示之后，再回到登录页重新登录，这个时候还会继续触发2FA吗？还是说登录的时候会给什么提示？<img name="image.png" alt="The image shows five screenshots of a mobile phone interface in the verification process. Each screenshot displays a verification code input field with the number &#34;192222&#34; and a numeric keypad below. Some screenshots show a message indicating the number of attempts to obtain a verification code and a &#34;Understand&#34; button. The interface also includes a loading circle in one screenshot, and the time &#34;2023-03-04 17:14:14&#34; is visible in the bottom right corner of the last screenshot." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=ZDAyZTIwY2M2MzVmNDFhZTVhZGU5ZTkyYmExMTBjYWJfNTMxMTgxMmVhM2YzMWUyMDY5YWM2MmMyMmQyYzAwM2ZfSUQ6NzYxNDAyMjMzMDY0NTYxNDMwMF8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="L9XFb1HZYotU5UxGjQFlqHqWgyM"/></td><td>产品更新策略：<cite type="user" user-id="ou_6749d09678d2be0a4da59186e4c48116" user-name="Jane Yan"></cite>评估看看--见3.10更新<br/>登录情况验证码超限制存在被盗或恶意登录情况，处理逻辑：<br/>1、1小时内无法登录<br/>2、一小时后可触发 60分钟内12次的请求<br/>3、提示弹框中增加用户重置密码的提示--无需提醒<br/>Cc <cite type="user" user-id="ou_b7e608f48617ee986d06128039652d4d" user-name="Keith Chan"></cite></td></tr><tr><td>验证码获取限制是什么？</td><td><ul><li>验证码：6位数字</li><li>验证码有效时长：60秒</li><li>验证码发送限制：<ul><li>相同Email：60分钟内12次请求</li><li>相同IP：一分钟内请求10次</li></ul></li></ul></td></tr><tr><td>2FA接口什么时候给出，还有红点也需要服务端新增接口，红点是按照账号维度管理的，无法本地存储。删除头像单独使用NothingAccount后端的api合适吗？</td><td>接口：指部署测试环境App可以调试 <cite type="user" user-id="ou_d4e4a5157f62093f9d0db82e623bc191" user-name="Wanyuan Zhong_C"></cite><br/>红点：增加API接口提供状态逻辑 <cite type="user" user-id="ou_d4e4a5157f62093f9d0db82e623bc191" user-name="Wanyuan Zhong_C"></cite><br/>删除头像API：沿用当前API，后端做处理 <cite type="user" user-id="ou_4696f8bfdaddcf282d2f7df33a6a4ea7" user-name="Grant Yang"></cite><br/>Account中的API全部转成Account的，与Nothing X的解耦 <cite type="user" user-id="ou_d692c91ad7225896d6098cf2af51a13d" user-name="Lucas Luo_C"></cite><cite type="user" user-id="ou_c8fd3ed8428281b417f37b009cde9443" user-name="Bob Tao"></cite></td></tr><tr><td>nothing x app目前有版权信息, 看最新的设计是去掉了吗?<img name="image.png" alt="The image shows two screenshots related to account privacy center and copyright information. On the left, the &#34;Privacy centre - CN version - SC&#34; screen displays a menu with options like &#34;用户协议&#34; (User Agreement), &#34;隐私政策&#34; (Privacy Policy), and a prominent &#34;删除账号&#34; (Delete Account) button. On the right, the &#34;About&#34; screen has sections such as &#34;服务条款&#34; (Service Terms), &#34;开源许可证&#34; (Open Source License), and a copyright notice at the bottom reading &#34;© 2025 - 2026 Nothing Technology Limited 版权所有&#34; (© 2025 - 2026 Nothing Technology Limited All Rights Reserved). This corresponds to the FAQ content about accessing privacy center and copyright information from different entry points." href="https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=ZTEzMGI3ODc4NGYwNmY3MmU4ZDYzN2Y0N2I1ZTg3ZDlfMjZjYzk2NzZkYzYxMTU1OTUzMTNiMjViYjhiZmY0MzFfSUQ6NzYxNDAzNjU0NTQ2ODc5NjYzOF8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM" mime="image/png" scale="1.000000" src="N1y6bO6c8oyuWpxZDgqlC6DFgKf"/></td><td>1、从Account里面跳进来叫做【隐私中心】，有【删除账号】按钮，没有版权信息<br/>2、从Nothing X的About进来，有【版权信息】，没有【删除账号】</td></tr><tr><td>sdk调用逻辑：<br/>nothingx <br/>1.account sdk 获取user信息，跳转到账号中心<br/>2.自己集成flutter sdk, flutter sdk 可以自己通过服务端api请求user<br/>这两者是if else的逻辑<br/>nothingx本体要同时集成这两个sdk<br/>当account sdk不可用时(不在nothing手机上)，切换至flutter sdk<br/>现状：if else的判断放在了flutter sdk里面，实际应该放在nothingx本体</td><td></td></tr></tbody></table>

### **3/4：提交翻译文案**

本次新增翻译内容:H列标注"v2.0.0"

<cite doc-id="SxmDwnfIAiCu26kFUpQlxi7agIg" file-type="wiki" title="Nothing Account 页面文案" type="doc"></cite>

### 3/3：沟通问题

Account 顶部文案过长，不影响底部按钮位置，底部按钮位置固定，避免滑动底部按钮看不见

![The image shows a screenshot of a chat conversation. At 17:21, Keith Chan states "底部按键区域一定是固定的". Below the text, there is a diagram of a mobile app interface with a login screen, including "Email login", "Create account", and "Welcome to Nothing" sections. At 17:22, Lucas Luo_C agrees, saying "对，我也是这样想的，底部固定位置". This image is related to the context discussing the fixed position of the bottom buttons in the Nothing Account page, as mentioned in the "沟通问题" section.](https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=NTE3ZWFiNjg0M2VkYzI3Njg5NTQ3YWYyZWQ0Y2U3YmNfNGY0NTUyZmUyNDdlM2M5MjFmYzcyN2RiNDU5YWZmNzVfSUQ6NzYxMjk1ODc5NTg2MTQ5NTUxOF8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM)

### API接口

<sheet sheet-id="q5MOps" token="FYfvsVSLGh0SM2tBAtklZ19CgNc"></sheet>

### 2/28：

- 2FA校验失败次数限制，结合在安全模型里面统计处理 <cite type="user" user-id="ou_d4e4a5157f62093f9d0db82e623bc191" user-name="Wanyuan Zhong_C"></cite>
- 补充埋点信息 <cite type="user" user-id="ou_fd8046dad99856e79bcbcd44594c1a39" user-name="Alex Luo"></cite>



### 2/27： UI Review

- [x] 中国区账号交互流程及功能定义 <cite type="user" user-id="ou_fd8046dad99856e79bcbcd44594c1a39" user-name="Alex Luo"></cite>

- [ ] 第三方登录忘记&修改密码友好提示逻辑 <cite type="user" user-id="ou_fd8046dad99856e79bcbcd44594c1a39" user-name="Alex Luo"></cite>
  - [ ] 第一期走 FAQ，二期再规划增加修改密码功能

- [x] 网页2FA交互UI审计拉通 Matteo Bandi <cite type="user" user-id="ou_fd8046dad99856e79bcbcd44594c1a39" user-name="Alex Luo"></cite>

# 🗂 Background

- 当前已有账号在手机端无法满足SSO，各模块独立管理账号生命周期逻辑，导致用户体验差
- 当前账号缺少基本的安全保证机制，无法为后续软件商业化，支付等提供基础安全保障

  - 二次校验
  - 登录设备合法性检查
  - token管理能力缺失
- 当前账号用户归属信息缺失，无法统计分析用户来源，用户归属
- 当前账号系统无法满足EO 14177要求，匹配数据隔离约束

# 🎯 Requirement Goals and values

## **For users**

- 提供统一无缝用户账号管理体验

  - Nothing手机：一只App登录，其他App同步状态
  - Nothing网站：统一刷新SSO设计风格，匹配官网和社区等网站设计样式
- 提供安全可信赖的账号系统生态

  - 二次校验：确保用户执行关键操作是保证用户资产安全
  - 设备信任管理：管理账号登录设备可信度，确保用户账号正常、异常登录第一时间被告知并做出安全保护操作
  - Token精细化管理：确保业务资产

## **For business**

- 支持公司未来更好的商业化布局，包含但不限于AI订阅，云服务，积分，优惠券。
- 支持更好的进行用户精细化运营

# 📋️ Requirement Scope

<table><colgroup><col/><col/></colgroup><tbody><tr><td><b>需求点 Requirements</b></td><td><b>模块 Modules</b></td></tr><tr><td>SSO</td><td>Settings/Nothing X/Essential Space/Share widget</td></tr><tr><td rowspan="2" vertical-align="middle">安全策略</td><td><b>Web：</b>Nothing Account Center</td></tr><tr><td><b>Mobile</b>：<ul><li>Settings</li><li>外发的Nothing X</li><li>Nothing Account App</li><li>其他与账号关联的 App</li></ul></td></tr></tbody></table>

# 📱 Competitor



# 🖌 Requirement Description

## 1、第一期核心功能：SSO

<whiteboard token="R2yUwqJnPhuxrvbG3kyluhAogFf"></whiteboard>

## 2、第一期核心功能：2FA

- **安全模型**

<sheet sheet-id="suTHNo" token="FYfvsVSLGh0SM2tBAtklZ19CgNc"></sheet>

- **工作流程**

<whiteboard token="DKU3wIVYrh36kdbJr4zlJlUeg1e"></whiteboard>

- **触发模型（Scope）**

<table><colgroup><col/><col/><col/><col/></colgroup><tbody><tr><td><b> 场景</b></td><td><b>子场景</b></td><td><b>说明</b></td><td><b>是否触发</b></td></tr><tr><td colspan="4">生命周期管理</td></tr><tr><td rowspan="3" vertical-align="middle"><b>登录</b></td><td vertical-align="middle"> 信任设备二次登录</td><td>密码错误&gt;=3（服务端计算）</td><td vertical-align="middle"> YES</td></tr><tr><td rowspan="2" vertical-align="middle">非信任设备登录</td><td>旧设备已经登录，又在新设备触发登录 - 本地登录</td><td vertical-align="middle"> YES</td></tr><tr><td>旧设备已经登录，又在新设备触发登录 - 异地登录</td><td>YES</td></tr><tr><td rowspan="3" vertical-align="middle"><b>账号信息修改</b></td><td>密码</td><td>沿用当前忘记密码功能 - Email</td><td> YES</td></tr><tr><td> 忘记密码</td><td>沿用当前忘记密码功能- Email</td><td>YES</td></tr><tr><td>归属地 - 本期不做</td><td>用户修改归属地</td><td>YES</td></tr><tr><td colspan="4">业务支持</td></tr><tr><td rowspan="2" vertical-align="middle"><b>订阅</b></td><td vertical-align="middle"> 套餐/服务订阅</td><td><ul><li>体验结束启动订阅流程进入付款流程</li><li>体验未结束启动订阅流程进入付款流程</li></ul></td><td vertical-align="middle">YES</td></tr><tr><td vertical-align="middle">退订/退款</td><td><ul><li>订阅服务使用过程中终止订阅服务</li></ul></td><td vertical-align="middle"> YES</td></tr><tr><td rowspan="4" vertical-align="middle"><b>合规&amp;安全</b></td><td vertical-align="middle">数据导出</td><td>用户触发导出个人数据</td><td vertical-align="middle">YES</td></tr><tr><td vertical-align="middle"> 账号注销</td><td>用户触发账号注销流程，完成注销条款/说明后，最终确认注销验证是否本人触发</td><td vertical-align="middle">YES</td></tr><tr><td vertical-align="middle"> 撤销隐私同意</td><td>用户选择撤销隐私同意权，触发二次验证确认是否用户本人触发</td><td vertical-align="middle">YES</td></tr><tr><td vertical-align="middle">变更2FA 信息</td><td><ul><li>更新 2FA 信息（打开-&gt;关闭）</li><li>更新 2FA 验证信息（更新2FA方式）</li></ul></td><td vertical-align="middle">YES</td></tr></tbody></table>

- **模型演变**

<whiteboard token="C92ewryuEhrb76b5bLPlk1bFgTe"></whiteboard>

### **2.1、直接上流程 - 验证码：mobile Phone**

**方向：第一期**Email  OTP

**为什么不用SMS：**触达率低，安全性低，成本高

**为什么不用Whatsapp：**Whatsapp占有率高，但一期接入较复杂，会新增成本，商业化论证ROI后再接入

<sheet sheet-id="mL9yYF" token="FYfvsVSLGh0SM2tBAtklZ19CgNc"></sheet>

<sheet sheet-id="9C1CA3" token="FYfvsVSLGh0SM2tBAtklZ19CgNc"></sheet>



<whiteboard token="FAYjwtYPIhGcv5bIDAXlGcIagth"></whiteboard>

#### 2.1.1、小红点逻辑

**Settings Icon小红点：**

- 定义：此小红点在账户设置有新功能推出或有重要功能更新时会需要显示，高亮提醒用户有重要的更新
- 红点显示逻辑：

  - 如某些功能被标记为可增加红点的功能（新功能或有更新的功能），在用户登录账号中心首次看到该功能时，该功能标注红点。如用户不点击该功能，该功能红点不消失。
  - 支持展示红点的功能需可配置（随版本），如新增的功能或有重要更新的功能均有可能配置红点。
- 红点消失逻辑：

  - 账号维度，一个新功能仅对一个账号显示一次，点击则消失。用户在任意一台设备上点击了某红点功能，则该功能的红点对该用户消失，且该功能的红点不再出现该用户的其他设备。
  - 无论用户清理APP数据还是恢复出厂设置后，只要用户通过点击进入过指向的功能页面，小红点则消失。

#### 2.1.2、二次校验开关逻辑 <cite type="user" user-id="ou_8526d5509f487a5464c7eb3d64ab6b4a" user-name="Albert Huang"></cite>

- 默认值：关闭
- 打开2FA：用户点击开启2FA按钮会发送验证码到邮箱，触发验证码二次验证

验证成功：2FA打开

验证失败：2FA保持关闭

- 关闭2FA：在2FA开启状态下，用户可点击关闭2FA，点击后，会发送验证码到邮箱，触发验证码二次验证

验证成功：2FA关闭

验证失败：2FA保持打开

- 二次校验渠道：注册了当前账号的邮箱
- 验证码：6位
- 验证码有效时长：60秒
- 验证码发送限制：

  - 相同Email：60分钟内12次请求
  - 相同IP：一分钟内请求10次
- **二次校验管理态：**所有端（客户端/web端）均可管理。
- **二次校验运行态：**所有端（客户端/web端）均生效。



#### 2.1.3、关于页面逻辑 <cite type="user" user-id="ou_d692c91ad7225896d6098cf2af51a13d" user-name="Lucas Luo_C"></cite>

- Policy Management：管理与合规，隐私政策相关的功能，功能清单

  - Privacy Policy：点击后调用浏览器跳转到官网Privacy Policy
  
    - Link：https://nothing.tech/pages/privacy-policy
  - User Agreement：点击后调用浏览器跳转到官网User Agreement
  
    - 海外版本：https://nothing.tech/pages/user-agreement
    - 中国版本：
    
      - Nothing X: 沿用当前Nothing X已有版本
      - 其他App：例如后续如果Playground要上国区，再制定对应条款
  - Open Source License：点击后打开新页面加载并显示【开源许可证】申明
  
    - App库锁定后开发提供gradle库的清单再梳理 <cite type="user" user-id="ou_fd8046dad99856e79bcbcd44594c1a39" user-name="Alex Luo"></cite>
  - Delete Account：当前版本点击后调用浏览器打开在线【删除账号请求表单】
  
    - 中国区：[https://www.wenjuan.com/s/UZBZJvooJIb/](https://www.wenjuan.com/s/UZBZJvooJIb/)
    - 海外区：https://docs.google.com/forms/d/e/1FAIpQLScpIGeFODh4d-SaaBrRmq5juLCQ9kQsp96a813XPAIhMaMrVg/viewform

2.1.4、独立验证码UI逻辑

- **布局定义**

  - 红色区域：标题，固定显示同样文案
  - 蓝色区域：验证码功能说明，支持文案自定义（业务调用方配置，Account读取）
  - 绿色区域：验证码输入区域，功能逻辑与当前保持一致
  - 黄色区域：倒计时或重发操作区域 - 功能逻辑与当前保持一致
- **页面返回逻辑**

  - 从哪里来回哪里去：业务交互页面调用起验证界面后的操作行为
  
    - 返回键：返回业务方调用的页面
    - 多任务：
    
      - 进入多任务，进程显示为Account
      - 杀进程：验证UI及Account APP退出，但Account进程常驻（除非用户到Account APP详情中disable，或点击force stop）
    - 验证Pass：返回业务方调用的页面
- **文案模板：**

<sheet sheet-id="g6ufnj" token="FYfvsVSLGh0SM2tBAtklZ19CgNc"></sheet>

#### 2.1.4、退出登录逻辑

- 退出登录确认UI：用户点击退出登录后，显示退出登录UI

  - Confirm：点击此按钮后，调用手机解锁逻辑（该功能当前版本已经实现），身份验证Pass后退出登录，回到登录页面
  - Cancel：点击此按钮后，直接回到Profile页面
  - 提醒文案：支持调用方可配置，但需按统一模板进行微调
  
    - 模板：
    
      - Are you sure you want to sign out? You’ll need to sign in again to use **xxx**
      - 其中xxx可由入口业务方自行配置：例如发起退出的是Nothing X，则Nothing X自行配置此信息
      - 注意：用户进入系统Settings触发的退出登录文案为以下应用将退出账号：NothingX:退出后，本设备将无法使用手表和健身等功能。   
      
        - 如用户未在NothingX绑定设备，则通用提示：Are you sure you want to sign out? You’ll need to sign in again to use Account-Associated Service such as Nothing X, Essential space, etc.
        - 如用户在NothingX绑定了设备，则提示：
      
        <grid>
        <column width-ratio="0.507900">
        ![The image shows a mobile phone screen with a user profile at the top, including a circular profile picture, the name "Keith", and the email "keith.chan@nothing.tech". Below the profile, there are options like "Personal information", "Share widgets", "Privacy centre", and "Two factor authentication". A prominent pop-up window in the center displays the "Sign out" option, with the message "You’ll be logged out of all Nothing services and apps signed in with this account on this device." and two buttons: "Cancel" and "Confirm". This image corresponds to the context about the exit login logic in the 2FA feature of the Nothing Account 2.0, specifically when the user is not bound to NothingX devices.](https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=MWJjNTAxMjNkZTY0NzdhYWIyNDg2YWQwNjYyN2IzNzJfNDg2MTRiNmQwZGU5ZWM3OGFhOWY3NjllNTVhMTQ4ODZfSUQ6NzYxNzc0Mzk4NDY1OTU4MjY4NF8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM)
        </column>
        <column width-ratio="0.492100">
        ![The image shows the "Huawei Account" settings page on a mobile device. At the top, there is a profile section with "未设置昵称" and an email address. Below, there are options like "个人信息", "帐号安全", "付款与账单", "云空间", "查找设备", and "设置家人共享". A prominent "退出帐号" pop-up window is displayed, listing "云空间" and "华为分享" as applications that will log out the current account, with details that the device can't access cloud space services or perform positioning, locking, and data erasure operations after logging out. It also states that logging out won't delete history messages, with "取消" (Cancel) and "退出帐号" (Log out) buttons at the bottom.](https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=NTE0NTJiNTc1ZDEwNDYxMmU1NzZmNzZhYWE0Yzg1ODZfZGZhYmRlMGZhZmYwODY0NzVmNmQ5MmY2N2VkYWYzMzZfSUQ6NzYxNzc0NDExNjgzMTEyOTMxMl8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM)
        </column>
        </grid>

  <whiteboard token="DB8awz1uRhwJFGbQDNdlhEXGg8c"></whiteboard>

二次验证弹窗：

![The image shows a verification interface for the 2FA (Two-Factor Authentication) process in the Nothing Account 2.0 PRD. It prompts the user to enter a 6-digit code sent to ma****@nothing.tech to verify their identity. There are six blank input boxes for the code, with a "Didn't receive a code? Send again (XXs)" message below, and a "Change" link in red. At the bottom, there is a "Continue" button. This interface is part of the direct 2FA process using mobile phone, as mentioned in the context about the first phase core function.](https://internal-api-drive-stream-sg.larksuite.com/space/api/box/stream/download/authcode/?code=MzZkMGMyYWYyNzRhYzBhM2EyMTUzZGM5ZjM5OTM3ZWVfOWNiMjk1NGRlYThkOGQyYzUwM2E0YzIwOGJjOGNlMGFfSUQ6NzYxNjY4NjUyMjIxNzI3MTAwNF8xNzgyODk3NTE4OjE3ODI5MDExMThfVjM)

注意：仅Nothing客户端退出账号才涉及校验，其他端（web端/出端场景）退出时无需二次校验。

#### 2.1.5、引导开启2FA逻辑

**核心需求：前提是未开启2FA**

- **场景举例** - 业务方调用Account能力先判断是否打开了2FA，没有则走引导流程

  - 场景1：非信任设备登录或高危用户数据操作（高危定义：数据删除、数据导出）
  - 场景2：业务方触发了敏感操作，如用户触发了订阅支付流程，触发了退订流程等
- **流程说明：**

  - 引导打开：引导打开页面增加对危险操作的说明和打开2FA的必要性
  - 打开流程：打开流程与用户主动进入账号Settings中的保持一致
  - 打开完毕：此流程在用户打开2FA并完成验证码输入后，返回正确的结果给到调用方，则业务方的流程可以继续往下走，无需再验证一次
  - 返回按钮：点击返回按钮后，返回到业务方页面，而非账号页面



#### 2.1.6 设备置信度



### 2.2、**直接上流程 - 验证码：Web site**

**第一期目标：**网页端支持安全配置中心，应用端账号页面暂时不调整

安全配置中心支持功能参考 手机端UI，需要支持跳转到安全配置页面 <cite type="user" user-id="ou_d803e4b0a78e73e62357bcbbcb36a4a0" user-name="Matteo Bandi"></cite>

<whiteboard token="SzLQw9Mr8h03KBbZ01ol4LKlgFh"></whiteboard>

### 2.3、 数据更新规则

#### 2.3.1、Source 规范 - P0

**目的：**规范统一用户来源，对 source 进行统一规范

| **App** | **source 名称** | **说明** | **配置条件** |
|-|-|-|-|
| Nothing X | nothing_x | 专门统计从 此 App中转化的用户数 | 第一次注册成功 |
|  Playground | playground | 专门统计从 此 App中转化的用户数 | 第一次注册成功 |
| Essential Space | essential_space | 专门统计从 此 App中转化的用户数 | 第一次注册成功 |
| Community | community | 专门统计从 此 App中转化的用户数 | 第一次注册成功 |
| WebSite | website | 专门统计从 此 App中转化的用户数 | 第一次注册成功 |
| Account | os_Account | 专门统计从 此 App中转化的用户数 | 第一次注册成功 |
| ShareWidget | share_widget | 专门统计从 此 App中转化的用户数 | 第一次注册成功 |
| 其他 | 应用名称作为 source | 专门统计从 此 App中转化的用户数 | 第一次注册成功 |

**说明：**当前已有字段，后续统一做切换清洗

#### 2.3.2、Location- P0

**目的：**提高用户区域分布状况

**精度：**国家&区域





### 2.4、新旧Feature差异

<cite doc-id="U4NUwb7RoiD0rVkCKkFlgdPygxb" file-type="wiki" title="Old Feature list vs new feature list" type="doc"></cite>



### 2.5、需求Jira拆分及优先级

总单：<cite src="S0Nod6ZS3oUfD0xJvZWlObrtgMg" type="jira-issue"></cite>

<table><colgroup><col/><col/><col/><col/></colgroup><tbody><tr><td><b>领域</b></td><td><b>Jira单</b></td><td><b>优先级</b></td><td><b>其他说明</b></td></tr><tr><td rowspan="6" vertical-align="middle">APP</td><td><cite src="LAgRdK4oEoSRohxTbyqlhd2sgCd" type="jira-issue"></cite></td><td>P0</td><td></td></tr><tr><td><cite src="N4cOdbakKoABQFxYotxlkCu0gnc" type="jira-issue"></cite></td><td>P0</td><td></td></tr><tr><td><cite src="LY9EdfEUWo8uC4xfGOJllXwSgOd" type="jira-issue"></cite></td><td>P0</td><td></td></tr><tr><td><cite src="U5TPdTqJIowC7TxtPPElZJD6gtc" type="jira-issue"></cite></td><td>P0</td><td></td></tr><tr><td><cite src="B8ptdYDJkoa6F0xUcZclWa4fgGn" type="jira-issue"></cite></td><td>P0</td><td></td></tr><tr><td><cite src="QvmBdJC8EoCeQfxTpyFlXCzZgGg" type="jira-issue"></cite></td><td>P0</td><td></td></tr><tr><td rowspan="4" vertical-align="middle">Server</td><td><cite src="Gw1tdS1UDohG5oxVJHYlLo95g3g" type="jira-issue"></cite></td><td>P0</td><td></td></tr><tr><td><cite src="X8ztdm1F4oxsrBxEmJFlN8kUg0b" type="jira-issue"></cite></td><td>P0</td><td></td></tr><tr><td><cite src="KWP8dHW5qotN9axnQdZlC6tVgjf" type="jira-issue"></cite></td><td>P0</td><td></td></tr><tr><td><cite src="Syh4dlfDLoHs8lxw3bEleFYNgBc" type="jira-issue"></cite></td><td>P0</td><td></td></tr></tbody></table>

### 2.6、验证码资费参考 

- 邮箱验证码收费情况及成本模拟





- 手机验证码收费情况及成本模拟 - Only for China

# 📊 MDM Event Tracking

（持续更新中 Updating）

<sheet sheet-id="uusxOK" token="FYfvsVSLGh0SM2tBAtklZ19CgNc"></sheet>

---

# Q & A

---