/*
* 所有表结构和SQL语句均采用小写字母
* 设计默认采用mysql数据库
*/
drop database yimeizhi ;

create database if not exists yimeizhiyi default character set utf8 collate utf8_general_ci ;  -- 设置数据库字符集和校验字符集

use yimeizhiyi ;

-- 业务配置配置表
create table if not exists business_cfg (
	id        varchar(32) , -- 配置标识
	name      varchar(64) , -- 配置名称
	type      varchar(32) , -- 配置类型
	flag      int , -- 配置有效性标识
	priority  int , -- 配置优先级
	datetime  datetime , -- 配置时间
	value     varchar(128) , -- 配置值
	primary key (id)
)engine=innodb default charset=utf8 ;

-- 员工信息表
create table if not exists employee(
       id            varchar(32) , -- 员工标识
       name          varchar(32) , -- 员工名称
       nickname      varchar(32) , -- 员工昵称
       birthday      datetime   , -- 员工出生日期
       contact1      varchar(32) , -- 联系方式1
       contact2      varchar(32) , -- 联系方式2
       homeaddress   varchar(64) , -- 家庭住址
       workaddress   varchar(64) , -- 工作住址
       jobtype       varchar(64) , -- 工作类型
       salarytype    varchar(64) , -- 工资类型
       primary key (id)
)engine=innodb default charset=utf8 ;
