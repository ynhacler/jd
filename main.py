#!/usr/bin/python
# _*_ coding:utf-8 _*_
import json
import requests
import re
import time
import pymysql.cursors
import traceback
import random

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

head = {
        'method': 'GET',
        'scheme': 'http',
        'referer': 'https://search.jd.com/',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Mobile Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'Referrer Policy': 'no-referrer-when-downgrade',
        'Cookie': 'qrsc=3; pinId=RAGa4xMoVrs; xtest=1210.cf6b6759; ipLocation=%u5E7F%u4E1C; _jrda=5; TrackID=1aUdbc9HHS2MdEzabuYEyED1iDJaLWwBAfGBfyIHJZCLWKfWaB_KHKIMX9Vj9_2wUakxuSLAO9AFtB2U0SsAD-mXIh5rIfuDiSHSNhZcsJvg; shshshfpa=17943c91-d534-104f-a035-6e1719740bb6-1525571955; shshshfpb=2f200f7c5265e4af999b95b20d90e6618559f7251020a80ea1aee61500; cn=0; 3AB9D23F7A4B3C9B=QFOFIDQSIC7TZDQ7U4RPNYNFQN7S26SFCQQGTC3YU5UZQJZUBNPEXMX7O3R7SIRBTTJ72AXC4S3IJ46ESBLTNHD37U; ipLoc-djd=19-1607-3638-3638.608841570; __jdu=930036140; user-key=31a7628c-a9b2-44b0-8147-f10a9e597d6f; areaId=19; __jdv=122270672|direct|-|none|-|1529893590075; PCSYCityID=25; mt_xid=V2_52007VwsQU1xaVVoaSClUA2YLEAdbWk5YSk9MQAA0BBZOVQ0ADwNLGlUAZwQXVQpaAlkvShhcDHsCFU5eXENaGkIZWg5nAyJQbVhiWR9BGlUNZwoWYl1dVF0%3D; __jdc=122270672; shshshfp=72ec41b59960ea9a26956307465948f6; rkv=V0700; __jda=122270672.930036140.-.1529979524.1529984840.85; __jdb=122270672.1.930036140|85.1529984840; shshshsID=f797fbad20f4e576e9c30d1c381ecbb1_1_1529984840145'
}

head_pc = {
        'method': 'GET',
        'scheme': 'http',
        'referer': 'https://search.jd.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.37 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'Referrer Policy': 'no-referrer-when-downgrade'
}

def crow_item_lists(shopID,page = 1,pagesize = 40):
    url =  'http://wqsou.jd.com/search/searchjson?datatype=1&page='+str(page)+'&pagesize='+str(pagesize)+'&merge_sku=yes&qp_disable=yes&key=ids%2C%2C' + \
            str(shopID) +  '&source=omz&_=1543823646627&sceneval=2&g_login_type=1&callback=jsonpCBKH&g_ty=ls'+'&_='+str(int(time.time()*1000))
    r = requests.get(url, headers=head)
    time.sleep(0.1)
    r_o = json.loads(r.text[10:-2])
    items =  r_o['data']['searchm']['Paragraph']
    itemID = []
    for id in items:
        zzh = {}
        pro_id = id['wareid']
        zzh[pro_id] = {}
        zzh[pro_id]['warename'] = id['Content']['warename']
        zzh[pro_id]['commentcount'] = id['commentcount']
        zzh[pro_id]['productext'] = id['productext']
        zzh[pro_id]['shopid'] = id['shop_id']
        zzh[pro_id]['venderid'] = id['vender_id']
        zzh[pro_id]['dredisprice'] = id['dredisprice']
        zzh[pro_id]['wareid'] = pro_id
        itemID.append(zzh)
    return itemID

def crow_item_prices(itemID):
    url = 'http://p.3.cn/prices/mgets?skuIds=J_' + str(itemID)+'&_='+str(int(time.time()*1000))
    r = requests.get(url, headers=head)
    time.sleep(0.1)
    r.encoding = 'utf-8'
    r_o = r.json()
    return (r_o[0]['p'], r_o[0]['m']) #really_price,original_price

def crow_item_cat(itemID):
    url = 'https://item.jd.com/' + str(itemID) + '.html'
    head_pc['user-agent'] = USER_AGENTS[random.randint(0,len(USER_AGENTS)-1)]
    r = requests.get(url, headers=head_pc)
    time.sleep(0.1)
    r.encoding = 'utf-8'
    findword = r"(.*)cat:\ \[([^\[\]]*)\](.*)"
    pattern = re.compile(findword)
    results = pattern.findall(r.text)
    zz = results[0][1]
    if len(zz) == 0:
        return []
    return zz

def crow_item_express(item):
    skuID = 0
    for k in item:
        skuID = k
    cat = crow_item_cat(skuID)
    venderID = item[skuID]['venderid']
    url1 = 'https://c0.3.cn/stock?callback=jQuery8487848&area=1_72_2799_0&extraParam={%22originid%22:%221%22}&skuId='+str(skuID)+'&cat='+cat+'&venderId='+venderID+'&_='+str(int(time.time()*1000))
    #print url1
    head_pc['user-agent'] = USER_AGENTS[random.randint(0,len(USER_AGENTS)-1)]
    r = requests.get(url1, headers=head_pc)
    time.sleep(0.1)
    r_o = json.loads(r.text[14:-1])
    shop_address = r_o['stock']['D']['df']
    shop_if_baoyou = r_o['stock']['dcashDesc']
    return (shop_address,shop_if_baoyou)

def crow_item_coupon(item):
    skuID = 0
    for k in item:
        skuID = k
    cat = crow_item_cat(skuID)
    venderID = item[skuID]['venderid']

    url2 = 'https://cd.jd.com/promotion/v2?callback=jQuery4749369&area=25_2235_2246_52440&isCanUseDQ=isCanUseDQ-1&isCanUseJQ=isCanUseJQ-1&platform=0&orgType=2&appid=1' \
           ''+'&skuId='+str(skuID)+'&jdPrice='+item[skuID]['dredisprice']+'&shopId='+item[skuID]['shopid']+'&venderId='+venderID+'&cat='+cat.replace(',','%2C')+'&_='+str(int(time.time()*1000))
    head_pc['user-agent'] = USER_AGENTS[random.randint(0,len(USER_AGENTS)-1)]
    r = requests.get(url2, headers=head_pc)
    time.sleep(0.1)
    r_o = json.loads(r.text[14:-1])
    dess = []
    if r_o['quan'] and r_o['quan']['title']:
        dess.append(r_o['quan']['title'])
    if r_o['skuCoupon']:
        desc1 = []
        for it in r_o['skuCoupon']:
            start_time = it['beginTime']
            end_time = it['endTime']
            fav_price = it['quota']
            fav_count = it['trueDiscount']
            dess.append(u'from %s to %s,price %s count %s' % (start_time, end_time, fav_price, fav_count))
        #return ';'.join(desc1)
    if r_o['prom'] and r_o['prom']['pickOneTag']:
        desc2 = []
        for it in r_o['prom']['pickOneTag']:
            dess.append(it['content'])
    return ';'.join(dess)

def get_shop_db():
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='1q2w3e',
        db='jd',
        charset='utf8'
    )
    cursor = connect.cursor()
    sql = "SELECT shop_id FROM shop"
    cursor.execute(sql)
    shop_list = []
    for row in cursor.fetchall():
        shop_list.append(row[0])
    cursor.close()
    connect.close()
    return shop_list

def getCommJson(productId, page=0,score=0):
        """
        score=0为全部，1为差评，2为中评，3为好评
        sortType=6为按时间排序，5为推荐排序
        isShadowSku 是否不只显示当前商品的评论，默认是 0否， 1为是
        """
        commUrl = "https://club.jd.com/comment/skuProductPageComments.action?productId="+str(productId)+"&score="+ str(score)+ "&sortType=6&pageSize=10&isShadowSku=0&page=" + str(page)+'&_='+str(int(time.time()*1000))
        head_pc['user-agent'] = USER_AGENTS[random.randint(0,len(USER_AGENTS)-1)]
        try:
            time.sleep(0.2)
            html = requests.get(commUrl,headers=head_pc).text
        except:
            print 'errUrl:'+commUrl
            return None
        time.sleep(0.1)
        try:
            json_content = None
            json_content = json.loads(html)
            #print json_content
        except Exception as e:
            print 'errHTML:'+html
            print 'errUrl1:'+commUrl
            print(traceback.format_exc())
        time.sleep(0.1)
        return json_content

def getCommMeta(item_id):
        #获取相对属性，买家印象，评论总结
        commentJson = getCommJson(item_id)

        commentMetas = {}
        commentMetas['goodRateShow'] = str(commentJson["productCommentSummary"]["goodRateShow"]) # 好评率
        commentMetas['poorRateShow'] = str(commentJson["productCommentSummary"]["poorRateShow"]) # 差评率
        commentMetas['commentCount'] = str(commentJson["productCommentSummary"]["commentCount"])    #评论数
        commentMetas['goodCount'] = str(commentJson["productCommentSummary"]["goodCount"])      #好评数
        commentMetas['generalCount'] = str(commentJson["productCommentSummary"]["generalCount"])    #中评数
        commentMetas['poorCount'] = str(commentJson["productCommentSummary"]["poorCount"])      #差评数

        # 买家印象
        commentMetas['hotCommentTags'] = commentJson["hotCommentTagStatistics"]
        return commentMetas

def splitComments(commentJson):
        comments = []
        for comm in commentJson['comments']:
            comment = {}
            comment["cmid"] = str(comm.get('id',""))    # 该评论的id
            comment["guid"] = str(comm.get('guid',""))
            try:
                comment["content"] = str(comm.get('content',"")).replace(',',"，").replace(' ',"").replace('\n',"").strip()
            except:
                comment["content"] = comm.get('content',"")

            comment["creationTime"] = str(comm.get('creationTime',""))
            comment["referenceId"] = str(comm.get('referenceId',""))  # 该评论所属的商品
            comment["replyCount"] = str(comm.get('replyCount',""))
            comment["score"] = str(comm.get('score',""))
            try:
                comment["nickname"] = str(comm.get('nickname',""))
            except:
                comment["nickname"] = comm.get('nickname',"")
            comment["productColor"] = str(comm.get('productColor',""))
            comment["productSize"] = str(comm.get('productSize',""))
            comments.append(comment)
        return comments

def getComments(item_id):
        #获取该产品的好评，中评，差评各100页评论数据
        comments = {}
        comments['goodComments'] = []
        comments['geneComments'] = []
        comments['badComments'] = []

        # 好评
        for i in range(100):
            commentJson = getCommJson(item_id, i,score=3)
            if commentJson == None:
                continue
            if len(commentJson['comments']) == 0:
                break
            comments['goodComments'].extend(splitComments(commentJson))

        time.sleep(1)
        # 中评
        for i in range(100):
            commentJson = getCommJson(item_id, i,score=2)
            if commentJson == None:
                continue
            if len(commentJson['comments']) == 0:
                break
            comments['geneComments'].extend(splitComments(commentJson))
        time.sleep(1)
        # 差评
        for i in range(100):
            commentJson = getCommJson(item_id, i,score=1)
            if commentJson == None:
                continue
            if len(commentJson['comments']) == 0:
                break
            comments['badComments'].extend(splitComments(commentJson))
        time.sleep(1)
        return comments


def insert_comment(item_id):
    comments = getComments(item_id) # 获取100页评价

    zz_list = []
    try:
        # 存好评
        for comm in comments['goodComments']:
            try:
                level = 'good'
                i_id = item_id
                cm_id = str(comm['cmid'])
                score = comm['score']
                content = comm['content']
                user = comm['nickname']
                comment_time = comm['creationTime']
                up_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                zz_list.append((i_id,cm_id,level,score,user,comment_time,content,up_time))
            except Exception as e:
                print("exception: " + str(e))
    except:
        print('comment error save good comm' + str(item_id))
        traceback.print_exc()

    try:
        # 存中评
        for comm in comments['geneComments']:
            try:
                level = 'gene'
                i_id = item_id
                cm_id = str(comm['cmid'])
                score = comm['score']
                content = comm['content']
                user = comm['nickname']
                comment_time = comm['creationTime']
                up_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                zz_list.append((i_id,cm_id,level,score,user,comment_time,content,up_time))
            except Exception as e:
                print("exception: " + str(e))
    except:
        print('comment error save good comm' + str(item_id))
        traceback.print_exc()

    try:
        # 存差评
        for comm in comments['badComments']:
            try:
                level = 'bad'
                i_id = item_id
                cm_id = str(comm['cmid'])
                score = comm['score']
                content = comm['content']
                user = comm['nickname']
                comment_time = comm['creationTime']
                up_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                zz_list.append((i_id,cm_id,level,score,user,comment_time,content,up_time))
            except Exception as e:
                print("exception: " + str(e))
    except:
        print('comment error save good comm' + str(item_id))
        traceback.print_exc()
    return zz_list

def test():
    print '1、获取店铺列表'
    shop_list = get_shop_db()

    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='1q2w3e',
        db='jd',
        charset='utf8'
    )
    item_id_list = []
    for shop_id in shop_list:
        print '2、获取商品列表'
        items = crow_item_lists(shop_id)
        #print "商品数：" + str(len(items))
        print '3、获取商品包邮和优惠信息'
        for item in items:
            iidd = 0
            for kk in item:
                iidd = kk
                item_id_list.append(iidd)
            coupons = crow_item_coupon(item)
            express = crow_item_express(item)
            prices = crow_item_prices(iidd)
            title = item[iidd]['warename']
            comment_count = int(item[iidd]['commentcount'])
            really_price = prices[0]
            original_price = prices[1]
            address = express[0]
            if_express = express[1]
            up_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            #加入数据库
            cursor = connect.cursor()
            sql = "INSERT INTO item(item_id,title,comment_count,really_price,original_price,address,if_express,coupon,update_time) " \
                  "VALUES ( '%s', '%s','%d',  '%s' ,  '%s','%s','%s','%s','%s')"
            data = (iidd,title,comment_count,really_price,original_price,address,if_express,coupons,up_time)
            cursor.execute(sql % data)
            connect.commit()
            cursor.close()
            #break

    print "4、获取评论列表"
    for ii in item_id_list:
        commentMetas = getCommMeta(ii) # 获取评价的相对属性
        #加入数据库
        cursor = connect.cursor()
        sql = "UPDATE ITEM SET good_rateshow = '%s',poor_rateshow" \
                    " = '%s',comment_count = '%d',good_count = '%d',general_count = '%d',poor_count = '%d'WHERE ITEM_ID = '%s'"
        data = (commentMetas['goodRateShow'],commentMetas['poorRateShow'],int(commentMetas['commentCount']),int(commentMetas['goodCount']),int(commentMetas['generalCount']),int(commentMetas['poorCount']),ii)
        try:
           cursor.execute(sql % data)
           connect.commit()
           cursor.close()
        except:
           connect.rollback()
        #好中差评论,只存100页的
        zb = insert_comment(ii)#(i_id,cm_id,level,score,user,comment_time,content,up_time)
        for zz in zb:
            try:
                cursor = connect.cursor()
                sql = "INSERT INTO COMMENT(ITEM_ID,CM_ID,LEVEL,SCORE,USER,COMMENT_TIME,CONTENT,UPDATE_TIME)" \
                      " VALUES('%s', '%s','%s', '%s' , '%s','%s','%s','%s')"
                data = (zz[0],zz[1],zz[2],zz[3],zz[4],zz[5],zz[6],zz[7])
                cursor.execute(sql % data)
                connect.commit()
                cursor.close()
            except Exception as e:
                print("exception: " + str(e))
        #break
    connect.close()

if __name__ == '__main__':
    #item_id = '11157435967'
    #commentMetas = getCommMeta(item_id) # 获取评价的相对属性
    #print commentMetas
    #comments = getComments(item_id) # 获取100页评价
    #print comments
    test()
    #print str(int(time.time()*1000))
    #head_pc['user-agent'] = USER_AGENTS[random.randint(0,len(USER_AGENTS)-1)]
    #print head_pc
    print '======end======='