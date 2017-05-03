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

## 住户信息绑定

#### API
```
POST http://www.desckie.com/api/weweb/bind/
```

#### 参数说明

* 需要登录状态
* <code>name</code>: 住户姓名。
* <code>room</code>: 房间号。

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

## 活动报名

#### API
```
POST http://www.desckie.com/api/weweb/join/
```

#### 参数说明

* 需要登录状态
* <code>name</code>: 活动名称。

#### 错误类型

* 您已报名该活动

## 提交留言

#### API
```
POST http://www.desckie.com/api/weweb/message/
```

#### 参数说明

* 需要登录状态
* <code>message</code>: 用户留言。

## 获取缴费信息

#### API
```
GET http://www.desckie.com/api/weweb/payinfo/
```

#### 参数说明

* 需要登录状态

#### 返回数据
```
{
  "data": {
    "total_price": 1080,
    "park_price": 30,
    "name": "李宗航",
    "other_price": 50,
    "manage_price": 1000,
    "room": "244"
  },
  "err": 0
}
```

## 模拟支付操作

#### API
```
POST http://www.desckie.com/api/weweb/pay/
```

#### 参数说明

* 需要登录状态

#### 错误类型

* 当月没有待缴费的费用

## 待租借场地列表

#### API
```
GET http://www.desckie.com/api/weweb/list/place/
```

#### 返回数据
```
{
  "data": [
    {
      "member": 4,
      "place": "羽毛球场1号场地"
    },
    {
      "member": 4,
      "place": "羽毛球场2号场地"
    },
    {
      "member": 4,
      "place": "羽毛球场3号场地"
    },
    {
      "member": 4,
      "place": "网球场1号场地"
    },
    {
      "member": 4,
      "place": "网球场2号场地"
    },
    {
      "member": 4,
      "place": "棋牌室401"
    },
    {
      "member": 10,
      "place": "棋牌室402"
    },
    {
      "member": 15,
      "place": "棋牌室403"
    }
  ],
  "err": 0
}
```

## 场地租借

#### API
```
POST http://www.desckie.com/api/weweb/rent/
```

#### 参数说明

* 要求登录状态
* <code>place</code>: 租借场地名称。

## 饮品类型查询

#### API
```
GET http://www.desckie.com/api/weweb/list/drink/
```

#### 返回数据

```
{
  "data": [
    {
      "price": 15,
      "name": "11.5L农夫山泉"
    },
    {
      "price": 20,
      "name": "17L农夫山泉"
    }
  ],
  "err": 0
}
```