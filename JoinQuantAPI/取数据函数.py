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

'''
    history ♠ ­ 获取历史数据
    查看历史的行情数据

    关于停牌:因为获取了多只股票的数据,可能有的股票停牌有的没有,为了保持时间轴的一致, 我们默认没有跳过停牌的日期, 停牌时使用停牌前的数据填充(请看SecurityUnitData的paused属性).如想跳过,请使用skip_paused=True参数当取天数据时, 不包括当天的, 即使是在收盘后

    参数
    见文档
    返回
        见文档
'''
##
history(count, unit='1d', field='avg', security_list=None, df=True, skip_pause
d=False, fq='pre')

'''
    attribute_history ♠ ­ 获取历史数据
    查看历史的行情数据

    查看某一支股票的历史数据,可以选这只股票的多个属性,默认跳过停牌日期.当取天数据时, 不包括当天的, 即使是在收盘后

    参数
    见文档
    返回
    见文档
'''
##
attribute_history(security, count, unit='1d',fields=['open', 'close', 'high', 'low', 'volume', 'money'],skip_paused=True, df=True, fq='pre')

'''
    get_current_data ♠ ­ 获取当前时间数据
    获取当前单位时间（当天/当前分钟）的涨跌停价,是否停牌，当天的开盘价等。回测时,通过API获取到的是前一个单位时间(天/分钟)的数据,而有些数据,我们在这个单位时间是知道的,比如涨跌停价,是否停牌,当天的开盘价. 我们添加了这个API用来获取这些数据

    参数
    见文档
    返回
    见文档
'''
##
get_current_data()

'''
    get_fundamentals ­ 查询财务数据
    查询财务数据，详细的数据字段描述请点击财务数据文档查看
    参数
    见文档
    返回
    见文档
'''
##
get_fundamentals(query_object, date=None, statDate=None)

'''
    get_index_stocks ­ 获取指数成份股
    获取一个指数给定日期在平台可交易的成分股列表，请点击指数列表查看指数信息
    参数
    见文档
    返回
    返回股票代码的list
'''
##
get_index_stocks(index_symbol, date=None)

'''
    get_industry_stocks ­ 获取行业成份股
    获取在给定日期一个行业的所有股票，行业分类列表见数据页面­行业概念数据。
    参数
    见文档
    返回
    返回股票代码的list
'''
##
get_industry_stocks(industry_code, date=None)

'''
    get_concept_stocks ­ 获取概念成份股
    获取在给定日期一个概念板块的所有股票，概念板块分类列表见数据页面­行业概念数据。
    参数
    见文档
    返回
    返回股票代码的list
'''
##
get_concept_stocks(concept_code, date=None)

#jqdata模块
#jqdata 模块用来提供更多数据
from jqdata import *

'''
    get_all_trade_days ­ 获取所有交易日
    获取所有交易日, 不需要传入参数, 返回一个包含所有交易日的 numpy.ndarray, 每个元素为一个datetime.date 类型.
    参数
    见文档
    返回
    返回股票代码的list
'''
##
get_all_trade_days()

'''
    get_trade_days ­ 获取指定范围交易日
    获取指定日期范围内的所有交易日, 返回 numpy.ndarray, 包含指定的 start_date 和 end_date, 默认返回至datatime.date.today() 的所有交易日
    参数
    见文档
    返回
    返回股票代码的list
'''
##
get_trade_days(start_date=None, end_date=None, count=None)

'''
    get_money_flow ­ 获取资金流信息
    获取一只或者多只股票在一个时间段内的资金流向数据
    参数
    见文档
    返回
    返回股票代码的list
'''
##
get_money_flow(security_list, start_date=None, end_date=None, fields=None, cou
nt=None)

'''
    gta.run_query ­ 查询国泰安数据
    查询国泰安数据，详细的数据字段描述请点击国泰安数据查看，注意未来函数，建议使用filter进行过滤
    
    1. 为了防止返回数据量过大, 我们每次最多返回3000行
    2. 不能进行连表查询，即同时查询多张表内数据
    参数
    见文档
    返回
    返回股票代码的list
'''
##
get_money_flow(security_list, start_date=None, end_date=None, fields=None, cou
nt=None)
