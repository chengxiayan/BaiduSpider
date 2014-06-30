BaiduSpider
===========

爬取百度贴吧，从中获取所有提到的流行小说名字，根据出现次数判断小说流行度


​先说说需求：我想做的一个爬虫，它通过爬取百度“小说推荐吧”里面的所有帖子，从中找到被提到最多的小说，为什么会有这种需求呢，因为我书荒的时候就会去这个贴吧，看哪本小说被推荐的多，我就看哪本了。

    ​要实现这个功能，我碰到的问题主要有以下几个：

    ​    ​1）如果判断一个词组表示的是一本小说；

    ​    ​2）采用什么搜索算法；

    ​    ​3）百度贴吧浏览10页以后的内容需要登录，如何在爬虫里面登录贴吧；

    ​对于第一个问题，我是这样解决的，从一个包含很多流行小说的网站上爬取部分小说名字，我是在豆瓣读书上找的，找了几个标签总共2000~3000本小说的名字，然后将这些小说名字与网页中的文字进行比对，如果有匹配的就表示是一本小说了，虽说无法判断所有小说，但能提取出流行小说就够了。最后匹配了部分网页发现这种有些问题，比如有小说名叫《战士》或《毒》，这种词出现的太多了，而且大部分时候想表达的意思不是小说名，我最终的处理方案是这些匹配的词后必须跟特定的符号或词语，比如别人提到“毒写的不错”或“《毒》”，抑或是“毒，战士，活着 都可以”，我才认定别人提到的应该是小说名了，当然，这样判断不一定准确，但应该有80%左右是对的。

    ​对于第二个问题，我搜多模式匹配，有两种比较流行的算法，AC多模匹配和Wu-Manber算法，前一种似乎不太适合非ascii字符的情形，所有我最终主要采用的是Wu-Manber算法，这种算法的实现思路大概是这样的(因为这不是主要，所以写的比较简单，可以自行百度)：

    ​比如有abcdef,ijkhlsd 这两个模式串需要在一段文字中进行匹配，我可以设定一个值k=4(该值应该小于最小模式串的长度),和block=2（该值应该小于k值），有两个表，ShiftTable和HashTable，在ShiftTable中放的是偏移值，对于串abcdef，分别计算ab,bc,cd,的Hash值，然后在ShiftTable中Hash值对应的地方放上偏移值，比如cd的偏移值是0,bd是1，ab是2，然后HashTable对应偏移为0的地方存放最开始block大小字符串的哈希值和相应模式串的索引。匹配过程是这样的：字符串从开头中每一个block长度求hash值，找到ShiftTable中相应地方的偏移值，如果不是0，则将指针前移偏移值个位置，如果是0，则和HashTable中相应地方存放的前缀Hash值进行比对，如果比对相等，再进行全字匹配。

    ​对于第三个问题，根据前人总结的，百度登陆有三个步骤：

    ​    ​1.Get方式连接https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=false，得到cookie

    ​    ​2.Get方式连接https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=false，得到的内容中包含一个tocken，解析出这个tocken的值

    ​    ​3.Post以下内容：
1
2
3
4
5
6
7
8
9
10
11
12
13
14
	
post_data = {'username':self.usrname,
                        'password':self.passwd,
                        'token':self.token,
                        'charset':'UTF-8',
                        'callback':'parent.bd12Pass.api.login._postCallback',
                        'index':'0',
                        'isPhone':'false',
                        'mem_pass':'on',
                        'loginType':'1',
                        'safeflg':'0',
                        'staticpage':'https://passport.baidu.com/v2Jump.html',
                        'tpl':'mn',
                        'u':'http://www.baidu.com',
                        'verifycode':'',}

​可以通过在最终连接的页面中查找用户名来判断登陆是否成功。
