
TODO
- Local client
    [ ] image capture
        - yolo 定时捕捉图片帧
    [ ] voice collection
        - 中断接收语音
    [ ] client interface
        - 请求get_images接口
            - request format: { "image": image_file,  "time": 捕捉时间戳   }
            - response format: {"success" : True}
        - 请求get_voice接口
            - request format: { "voice": wav_file,  "time": 捕捉时间戳   }
            - response format: {"success" : True, "voice": wav_file}

- LapTop Server
    [ ] server interface
        - get_images
            - 定期接收图片， 时间戳
            - request format: { "image": image_file,  "time": 捕捉时间戳   }
            - response format: {"success" : True}
        - get_voice
            - 用户语音触发 发送 语音文件
            - request format: { "voice": wav_file,  "time": 捕捉时间戳   }
            - response format: {"success" : True, "voice": wav_file}
            - 触发pipeline: 
                - tts / whisper 语音转文本
                - 大模型调用
        


- windows 和WSL 端口打通命令
```shell
# window 的shell 用管理员模式设置
# 添加端口转发规则
netsh interface portproxy add v4tov4 listenport=8000 listenaddress=0.0.0.0 connectport=8000 connectaddress=172.22.61.219

# 查看现有规则
netsh interface portproxy show all

# 如果需要删除规则
# netsh interface portproxy delete v4tov4 listenport=8000 listenaddress=0.0.0.0
```

- 打开window 防火墙让外网访问
~~~powershell
New-NetFirewallRule -DisplayName "WSL2 Port 8000" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
~~~



把打开的防火墙的规则删除
~~~powershell
Remove-NetFirewallRule -DisplayName "WSL2 Port 8000"
~~~
更加详细操作
~~~powershell
# 以管理员身份打开 PowerShell

# 查看所有防火墙规则，找到您创建的规则
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "*WSL2*"} | Format-Table DisplayName, Enabled

# 删除特定的 WSL2 规则
Remove-NetFirewallRule -DisplayName "WSL2 Port 8000"

# 或者删除所有包含 WSL 的规则
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "*WSL*"} | Remove-NetFirewallRule

# 确认已删除
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "*WSL*"}
~~~