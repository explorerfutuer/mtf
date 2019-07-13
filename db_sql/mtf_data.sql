/*
* 所有表结构和SQL语句均采用小写字母
* 设计默认采用mysql数据库
*/
drop database yimeizhi ;

create database if not exists yimeizhiyi default character set utf8 collate utf8_general_ci ;  -- 设置数据库字符集和校验字符集

use yimeizhiyi ;

create table if not exists employee_info(
	synseq			int unsigned auto_increment unique , -- 记录编号
	empno 			varchar(32) ,	-- 员工编号
	empname			varchar(32) ,	-- 员工姓名
	empsex			tinyint(1) default 0 ,	-- 0:女 , 1: 男
	empage			tinyint default 0 ,	-- 年龄
	empseniority	tinyint default 0 ,	-- 工龄
	hiredate 		datetime default now() ,
	contact1		varchar(16) ,	-- 联系方式1
	contact2		varchar(16) ,	-- 联系方式2
	empalias		varchar(32) ,	-- 尊称
	empaddress1		varchar(64) ,	-- 住址1
	empaddress2		varchar(64) ,	-- 住址2
	primary key (empno)
)engine=innodb default charset=utf8 ;
-- 主键
-- alter table employee_info add constraint pk_employee_info employee_info(empno) ;
-- 创建员工表的索引
create index i_employee_info_name on employee_info (empname,empalias) ;



-- 客户偏好信息表
create table if not exists  conf_consumer_prefer(
synseq			int default 0 , -- 记录编号
confno 			varchar(32) , -- 配置编号
consumerno		varchar(32) , -- 客户编号
preferkey		varchar(32) , -- 偏好的简单描述
prefervalue		varchar(256) , -- 偏好详细描述
primary key (confno)
) engine=innodb default charset=utf8 ;
-- 主键
-- alter table conf_consumer_prefer add constraint pk_conf_consumer_prefer conf_consumer_prefer(confno) ;
-- 创建偏好索引
create index i_conf_prefer_no on conf_consumer_prefer(confno) ;
alter table conf_consumer_prefer add foreign key fk_consumerno_on_conf_prefer(consumerno) references consumer_info(consumerno) ;


-- 客户交易记录表
create table if not exists consumer_trade_info(
synseq			int default 0 , -- 记录编号
consumerno		varchar(32) , -- 客户编号
salesno			varchar(32) , -- 销售编号
tradedesc		varchar(256) , -- 交易描述
consumercare1	varchar(128) , -- 客户关怀1
consumercare2	varchar(128) , -- 客户关怀2
primary key(salesno)
) ;
alter  table  consumer_trade_info add foreign key fk_consumerno_on_trade_info(consumerno) references consumer_info(consumerno) ;


-- 采购信息表
create table if not exists  purchase_info(
synseq			int unsigned auto_increment unique , -- 记录编号
purchaseno		varchar(32) ,	-- 采购编号
goodsno			varchar(32) , -- 货物编号
purchasedate	datetime default now() , -- 采购日期
purchaseway		int unsigned default 0 , -- 采购方式 1:当面交易 , 2:打电话 , 3:微信 , 4:淘宝 , 5:京东
maker			varchar(128) , -- 卖家公司名称
price			decimal(8,2) , -- 单价
purchasecnt		int unsigned default 0 , -- 采购数量
totalprice		decimal(12 , 2) , -- 总价格
extraprice		decimal(10,2) , -- 额外费用
extradesc		varchar(128) , -- 额外费用描述
purcharsedesc	varchar(256) , -- 采购描述，用于回忆
primary key(purchaseno)
) engine=innodb default charset=utf8;

-- 计划表
create table if not exists plan_info(
synseq			int unsigned auto_increment unique , -- 记录编号
planno			varchar(32) , -- 规划编号
createtime		datetime default now() , -- 规划创建时间
completetime	datetime , -- 完成截止日期
completeprogress tinyint unsigned default 0 , -- 完成进度数据介于[0,100]
plandesc		varchar(128) , -- 规划描述
primary key(planno)
) ;

-- 福利表
create table if not exists  welfare_info(
synseq			int unsigned auto_increment unique , -- 记录编号
welfareno		varchar(32) , -- 福利编号
holiday			date , -- 福利日期
welfaredesc		varchar(128) , -- 福利描述
welfarecost		decimal(12,2) , -- 福利花费
reserve			varchar(32) , -- 备用字段
primary key(welfareno)
) ;


create table if not exists waste_info(
synseq			int unsigned default 0 , -- 记录编号
wasteno			varchar(32) , -- 废品编号
wastename		varchar(64) , -- 废品名称
wasteamount		decimal(10,2), -- 废料数量
wasteprice		decimal(10,2), -- 废料单价
dealdate		datetime default now() , -- 出售日期
primary key(wasteno)
) ;

-- 薪水标准表
create table if not exists salarystandard_info(
synseq			int unsigned auto_increment unique , -- 记录编号
salaryno		varchar(32) , -- 薪水标准编号
createdate		datetime default now() , -- 薪水改变时间
laborvalue		decimal(10,2) , -- 薪水改变时间
salarystatus	tinyint unsigned default 0 , -- 薪资的状态0:当前正在使用
salarydesc		varchar(64) , -- 薪资描述
primary key(salaryno)
) ;


-- 工资表
create table if not exists wage_info(
synseq			int unsigned default 0 , -- 记录编号
salaryno		varchar(32) , -- 薪水标准编号
empno			varchar(32) , -- 员工编号
begdatetime		datetime default now() , -- 开始打卡时间
enddatetime		datetime , -- 结束打卡时间
effortthing		varchar(64) , -- 工作量简单描述
payoff			tinyint unsigned default 0 , -- 0:表示未结算
payoffdesc		varchar(64)  -- 工作结算简单描述
)engine=innodb default charset=utf8;
alter  table  wage_info add foreign key fk_wage_info_on_salaryno(salaryno) references salarystandard_info(salaryno) ;
alter  table  wage_info add foreign key fk_wage_info_on_empno(empno) references employee_info(empno) ;
create index i_wage_info_empno on wage_info(empno) ;



-- 收支总汇表
create table if not exists incomexpense_info(
synseq			int unsigned auto_increment unique , -- 记录编号
inoutno			varchar(32) , -- 编号
inoutkind		tinyint unsigned not null , -- 收支种类
inoutdatetime	datetime not null , -- 收支时间
payoff			tinyint default 0 , -- 是否支付
inoutdesc		varchar(128) , -- 收支描述
inoutamt		decimal(12,2) , -- 收支金额
reserve			varchar(64)  -- 备用字段
)engine=innodb default charset=utf8;


-- 同步信息表
create table if not exists  syncdata_info(
tablename		varchar(32) , -- 表名
recdsize		int unsigned default 0 , -- 表中的记录数
lastsyncpoint	int unsigned default 0 , -- 最后同步的位置
syncdatetime	datetime  default now() , -- 最后通过的时间点
willsyncnt		int unsigned default 0 , -- 待同步的记录数据
) engine=innodb default charset=utf8;




/*
	触发器
*/
CREATE  TRIGGER trigger_name [BEFORE|AFTER] [delete | insert | update] 
ON table_name
FOR EACH ROW
WHEN (SELECT col1, FROM tblname WHERE col1 = new.col1) ISNULL | NOTNULL  -- 此处就是条件变量
BEGIN
 -- Trigger logic goes here....
END;

-- 主键自增与获取当前日期
--  create table testkey(id integer primary key autoincrement , idate TIMESTAMP default (datetime('now', 'localtime') ));
-- 正常日期: Year-Month-Day Hour:Minute:Second => '%Y-%m-%d %H:%M:%S'    -- 其他: %s(从 1970-01-01 算起的秒数)，%f(当前秒SS.SSS相对精度比较高)  %%(%)
-- 修饰符 数字 [days | hours | minutes | seconds | months | years] ， start of [month | year | day ]， unixepoch(UNIX时间戳)， localtime  
-- strftime('%Y-%m-%d %H:%M:%S' , 'now' , '8 hour')  ==  datetime('now', 'localtime')
-- 方法: strftime(根据第一个参数指定的格式返回日期) , time(返回时间格式为 HH:MI:SS ) , date(返回日期 YYYY-MM-DD) , datetime(YYYY-MM-DD HH:MI:SS) , 
