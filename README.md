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

## 获取小区活动列表

#### API
```
GET http://www.desckie.com/api/weweb/list/activity/
```

#### 返回数据
```
{
  "data": [
    {
      "date": "2017-05-04",
      "loc": "上海市杨浦区政学路77号INNOSPACE+一楼 IPOclub",
      "name": "INNOSPACE + 基础服务公开课",
      "detail": "随着政府对双创的支持，越来越多的科技企业开始关注各类创业扶持政策。但每年各委办局推出的针对多种行业多种业态的政策就有上千项，哪些适合自己企业、需要达到什么条件、什么时间申报等问题都需要花时间研究。可谓多如牛毛，浩如瀚海，此类犹如排列组合的复杂难题，让专业的人来教会你“一招鲜”，从此不错过任何政府的扶持资金。"
    },
    {
      "date": "2017-05-03",
      "loc": "北京海淀",
      "name": "读书日活动特辑",
      "detail": "还记得上一次看书是什么时候吗？ 在这全民读书月的四月，你读书了吗？ 这世上最有趣的事，第一是人，第二是书。2017世界读书日即将来临，除了认真读一本书之外，参加一场读书有关的活动，也可以是读书日正确的打开方式喔！"
    }
  ],
  "err": 0
}
```