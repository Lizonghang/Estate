# API Document

## 模拟登录操作

#### API
```
GET http://www.desckie.com/api/weweb/test/login?openid=OPENID
```

#### 参数说明

* <code>openid</code>: 登录用户的openid，如<code>o26a00hNevT3Nrt2-yNk5Ln_6EPg</code>。

## 模拟登出操作

#### API
```
GET http://www.desckie.com/api/weweb/test/logout/
```

## 提交物业报修工单

#### API
```
POST http://www.desckie.com/api/weweb/repair/
```

#### 参数说明

* 需要登录状态
* <code>loc</code>: 故障地点。
* <code>desc</code>: 故障描述。