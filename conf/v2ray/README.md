# v2ray 配置

### 命令
```
生成uuid：
/usr/bin/v2ray/v2ctl uuid  
systemctl status v2ray
systemctl restart v2ray
```
### 配置文件路径
```
/etc/systemd/system/v2ray.service
/etc/v2ray/config.json

/data/v2ray.crt
/data/v2ray.key

/etc/nginx/nginx.conf add below
include conf.d/*.conf;

```
