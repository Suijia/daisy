### 获取当前时间戳
```
now =int(time.time()) # 这是时间戳
```
### 时间戳到字符串

```
timestamp=int(time.time())  # 当前时间戳，也是一个整数
time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
```
### 字符串到时间戳
```
time_struct = time.strptime("2013-10-10 23:40:00", "%Y-%m-%d %H:%M:%S")
timestamp = int(time.mktime(time_struct))
```

### time模块提供各种操作时间的函数
说明：一般有两种表示时间的方式:

    第一种 是时间戳的方式(相对于1970.1.1 00:00:00以秒计算的偏移量),时间戳是惟一的
    第二种 以数组的形式表示即(struct_time),共有九个元素，分别表示，同一个时间戳的struct_time会因为时区不同而不同
        year (four digits, e.g. 1998)
        month (1-12)
        day (1-31)
        hours (0-23)
        minutes (0-59)
        seconds (0-59)
        weekday (0-6, Monday is 0)
        Julian day (day in the year, 1-366)
        
### 主要函数

#### gmtime(...)
```
gmtime([seconds]) -> timestamp -> struct_time
```
将一个时间戳转换成一个UTC时区(0时区)的struct_time，如果seconds参数未输入，则以当前时间为转换标准
 
#### localtime(...)
```
localtime([seconds]) timestamp -> struct_time
```
将一个时间戳转换成一个当前时区的struct_time，如果`seconds`参数未输入，则以当前时间为转换标准

#### mktime(...)
```
mktime(tuple) -> struct_time -> timestamp (float)
```
将一个以struct_time转换为时间戳

#### strftime(...)
```
strftime(format[, tuple]) struct_time -> string
```
将指定的struct_time(默认为当前时间)，根据指定的格式化字符串输出
```
time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
time.strftime("%Y-%m-%d %H:%M:%S")  # 默认当前时间
```

python中时间日期格式化符号：
```
%y 两位数的年份表示（00-99）
%Y 四位数的年份表示（000-9999）
%m 月份（01-12）
%d 月内中的一天（0-31）
%H 24小时制小时数（0-23）
%I 12小时制小时数（01-12）
%M 分钟数（00=59）
%S 秒（00-59）

%a 本地简化星期名称
%A 本地完整星期名称
%b 本地简化的月份名称
%B 本地完整的月份名称
%c 本地相应的日期表示和时间表示
%j 年内的一天（001-366）
%p 本地A.M.或P.M.的等价符
%U 一年中的星期数（00-53）星期天为星期的开始
%w 星期（0-6），星期天为星期的开始
%W 一年中的星期数（00-53）星期一为星期的开始
%x 本地相应的日期表示
%X 本地相应的时间表示
%Z 当前时区的名称
%% %号本身
```

#### strptime(...)
```
strptime(string, format) string -> struct_time
```
将时间字符串根据指定的格式化符转换成数组形式的时间
``` 
time_struct = time.strptime("2013-10-10 23:40:00", "%Y-%m-%d %H:%M:%S")
timestamp = int(time.mktime(time_struct))
```

#### time(...)
```
time() -> timestamp
```
返回当前时间的时间戳

#### asctime()
```
asctime([tuple]) struct_time -> string
```
将一个struct_time(默认为当时时间)，转换成字符串

#### ctime(...)
```
ctime(seconds) timestamp -> string
```
将一个时间戳(默认为当前时间)转换成一个时间字符串
例如：
```
time.ctime()
```
输出为：
```
'Sat Mar 28 22:24:24 2009'
```

#### clock()
```
clock() -> floating point number
```
该函数有两个功能，
在第一次调用的时候，返回的是程序运行的实际时间；
以第二次之后的调用，返回的是自第一次调用后,到这次调用的时间间隔

#### sleep(...)
```
sleep(seconds)
```

### 常见用法
#### 字符串格式更改
如a = "2013-10-10 23:40:00",想改为 a = "2013/10/10 23:40:00"
方法:先转换为时间数组,然后转换为其他格式
```
timeArray = time.strptime(a, "%Y-%m-%d %H:%M:%S")
otherStyleTime = time.strftime("%Y/%m/%d %H:%M:%S", timeArray)
```

#### 时间戳转换为指定格式日期:
方法一:

    利用localtime()转换为时间数组,然后格式化为需要的格式,如
    ```
    timestamp = 1381419600
    time_struct = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", time_struct)
    otherStyletime == "2013-10-10 23:40:00"
    ```

方法二:
```
import datetime
timeStamp = 1381419600
dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
otherStyletime == "2013-10-10 23:40:00"
```


#### 获取当前时间并转换为指定日期格式
方法一:
```
import time
now = int(time.time()) 
timeArray = time.localtime(timeStamp)
otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
```
方法二:
```
import datetime
now = datetime.datetime.now()
otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
```