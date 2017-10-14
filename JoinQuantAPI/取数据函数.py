'''
    get_price ­ 获取历史数据
    获取一支或者多只股票的行情数据,按天或者按分钟，这里请在使用时注意防止未来函数
    关于停牌: 因为此API可以获取多只股票的数据,可能有的股票停牌有的没有,为了保持时间轴的一致, 我们默认没有跳过停牌的日期,停牌时使用停牌前的数据填充(请看SecurityUnitData的paused属性).如想跳过,请使skip_paused=True参数,同时只取一只股票的信息

    参数
    security: 一支股票代码或者一个股票代码的list
    count:
        与start_date二选一，不可同时使用.数量,返回的结果集的行数,即表示获取end_date之前几个 frequency 的数据start_date: 与 count 二选一，不可同时使用. 字符串或者 datetime.datetime/datetime.date 对象,开始时间.如果 count 和 start_date 参数都没有, 则 start_date 生效, 值是 ‘2015­01­01’. 注意:当取分钟数据时, 时间可以精确到分钟, 比如: 传入 datetime.datetime(2015, 1, 1,10, 0, 0) 或者 '2015-01-01 10:00:00' .当取分钟数据时, 如果只传入日期, 则日内时间是当日的 00:00:00.当取天数据时, 传入的日内时间会被忽略
    end_date: 
        格式同上, 结束时间, 默认是’2015­12­31’, 包含此日期. 注意: 当取分钟数据时, 如果end_date 只有日期, 则日内时间等同于 00:00:00, 所以返回的数据是不包括 end_date 这一天的.
    frequency: 
        单位时间长度, 几天或者几分钟, 现在支持’Xd’,’Xm’, ‘daily’(等同于’1d’),‘minute’(等同于’1m’), X是一个正整数, 分别表示X天和X分钟(不论是按天还是按分钟回测都能拿到这两种单位的数据),注意,当X>1时,fields只支持[‘open’, ‘close’, ‘high’, ‘low’, ‘volume’, ‘money’]这几个标准字段.默认值是daily
    fields: 
        字符串list, 选择要获取的行情数据字段, 默认是None(表示[‘open’,‘close’,‘high’, ‘low’,‘volume’, ‘money’]这几个标准字段),支持SecurityUnitData里面的所有基本属性,包含：[‘open’,’close’,‘low’,‘high’,‘volume’,‘money’,‘factor’,‘high_limit’,’low_limit’,‘avg’,’pre_close’, ‘paused’]
    skip_paused: 
        是否跳过不交易日期(包括停牌,未上市或者退市后的日期).如果不跳过,停牌时会使用停牌前的数据填充(具体请看SecurityUnitData的paused属性),上市前或者退市后数据都为 nan,
        但要注意:默认为 False 当 skip_paused 是 True 时, 只能取一只股票的信息
    fq: 复权选项:
        'pre' : 前复权(根据’use_real_price’选项不同含义会有所不同, 参见set_option), 默认是前复权
        None : 不复权, 返回实际价格
        'post' : 后复权
    返回
        请注意,为了方便比较一只股票的多个属性,同时也满足对比多只股票的一个属性的需求, 我们在security参数是一只股票和多只股票时返回的结构完全不一样
        如果是一支股票, 则返回pandas.DataFrame对象行索引是datetime.datetime对象,列索引是行情字段名字,比如’open’/’close’.
        如果是多支股票,则返回pandas.Panel对象,里面是很多pandas.DataFrame对象,索引是行情字段(open/close/…),每个pandas.DataFrame的行索引是datetime.datetime对象,列索引是股票代号. 
'''
##
get_price(security, start_date=None, end_date=None, frequency='daily', field
s=None, skip_paused=False, fq='pre', count=None)