#!/usr/bin/env python3
"""
当股票在当日收盘30分钟内涨幅到达9.5%~9.9%时间段的时候，我们进行买入，在第二天开盘卖出。注意：请按照分钟进行回测该策略。
"""
# 初始化程序, 整个回测只运行一次
def initialize(context):
    # 每天买入股票数量
    g.daily_buy_count = 5
    # 设置我们要操作的股票池,这里我们操作多只股票，下列股票选自计算机信息技术相关板块
    g.stocks = get_industry_stocks('I64') + get_industry_stocks('I65')
    # 防止板块之间重复包含某只股票, 排除掉重复的, g.stocks 现在是一个集合(set)
    g.stocks = set(g.stocks)
    # 让每天早上开盘时执行 morning_sell_all
    run_daily(morning_sell_all, 'open')
    set_option('use_real_price', True)

#参数 func 必须是一个全局的函数, 不能是类的成员函数
def morning_sell_all(context):
    # 将目前所有的股票卖出
    for security in context.portfolio.positions:
        # 全部卖出
        order_target(security, 0)
        # 记录这次卖出
        log.info("Selling %s" % (security))

def before_trading_start(context):
    # 今天已经买入的股票
    g.today_bought_stocks = set()
    # 得到所有股票昨日收盘价, 每天只需要取一次, 所以放在 before_trading_start 中
    g.last_df = history(1,'1d','close',g.stocks)

# 在每分钟的第一秒运行, data 是上一分钟的切片数据
def handle_data(context, data):
    # 判断是否在当日最后的2小时，我们只追涨最后2小时满足追涨条件的股票
    if context.current_dt.hour < 3 and context.current_dt.minute < 30:
        return
    # 每天只买这么多个
    if len(g.today_bought_stocks) >= g.daily_buy_count:
        return
    # 只遍历今天还没有买入的股票
    for security in (g.stocks - g.today_bought_stocks):
        # 得到当前价格
        price = data[security].close
        # 获取这只股票昨天收盘价
        last_close = g.last_df[security][0]
        # 如果上一时间点价格已经涨了9.5%~9.9%
        # 今天的涨停价格区间大于1元，今天没有买入该支股票
        if price/last_close > 1.095 \
            and price/last_close < 1.099 \
            and data[security].high_limit - last_close >= 1.0:
            # 得到当前资金余额
            cash = context.portfolio.cash
            # 计算今天还需要买入的股票数量
            need_count = g.daily_buy_count - len(g.today_bought_stocks)
            # 把现金分成几份,
            buy_cash = context.portfolio.cash / need_count
            # 买入这么多现金的股票
            order_value(security, buy_cash)
            # 放入今日已买股票的集合
            g.today_bought_stocks.add(security)
            # 记录这次买入
            log.info("Buying %s" % (security))
        # 买够5个之后就不买了
        if len(g.today_bought_stocks) >= g.daily_buy_count:
            break