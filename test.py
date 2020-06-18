import requests
import json
import execjs
import time
# 执行本地的js
def getJsCode():
    f = open("test.js", 'r', encoding='UTF-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr



def crawl(searchName,startTime,endTime):
    url = 'http://www.cebpubservice.com/ctpsp_iiss/searchbusinesstypebeforedooraction/getStringMethod.do'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
    }

    pageNo = 1
    crawlList = []
    while True:

        try:
            data = {
                'searchName': searchName,
                'searchArea': '',
                'searchIndustry': '',
                'centerPlat': '',
                'businessType': '招标公告',
                'searchTimeStart': '',
                'searchTimeStop': '',
                'timeTypeParam': '',
                'bulletinIssnTime': '',
                'bulletinIssnTimeStart':startTime ,
                'bulletinIssnTimeStop': endTime,
                'pageNo': pageNo,
                'row': 15,
            }

            r = requests.post(url, headers=header, data=data)



            if r.text.find("频繁访问") != -1:
                break
            refer = r.url
            r = json.loads(r.text)
            if r.get("success") == True:
                object = r.get("object")
                returnlist = object.get("returnlist")
                for returnData in returnlist:
                    dataDict = {}
                    businessObjectName = returnData.get("businessObjectName")  # 招标项目名称
                    if businessObjectName is None:
                        businessObjectName = "--"
                    industriesType = returnData.get("industriesType")
                    if industriesType is None:
                        industriesType = "--"
                    transactionPlatfName = returnData.get("transactionPlatfName")  # 招标平台/单位
                    if transactionPlatfName is None:
                        transactionPlatfName = "--"
                    regionName = returnData.get("regionName")  # 所属区域
                    if regionName is None:
                        regionName = "--"
                    receiveTime = returnData.get("receiveTime")  # 发布时间
                    if receiveTime is None:
                        receiveTime = "--"
                    bulletinEndTime = returnData.get("bulletinEndTime")  # 结束时间
                    if bulletinEndTime is None:
                        bulletinEndTime = "--"
                    tenderProjectCode = returnData.get("tenderProjectCode")
                    transactionPlatfCode = returnData.get("transactionPlatfCode")
                    schemaVersion = returnData.get("schemaVersion")
                    businessId = returnData.get("businessId")
                    dataDict["businessObjectName"] = businessObjectName
                    dataDict["industriesType"] = industriesType
                    if industriesType is None:
                        dataDict["industriesType"] = "--"
                    dataDict["regionName"] = regionName
                    dataDict["transactionPlatfName"] = transactionPlatfName
                    dataDict["receiveTime"] = receiveTime
                    dataDict["bulletinEndTime"] = bulletinEndTime

                    tenderProjectCode = ctx.call('strEnc',tenderProjectCode,ctx.call('CurentTime'),"cebpubservice","iiss")
                    businessId = ctx.call('strEnc',businessId,ctx.call('CurentTime'),"cebpubservice","iiss")
                    
                    # 详情页数据
                    url = "http://www.cebpubservice.com/ctpsp_iiss/SecondaryAction/findDetails.do"

                    data = {
                        'schemaVersion': schemaVersion,
                        'businessKeyWord': 'tenderProject',
                        'tenderProjectCode': tenderProjectCode,
                        'businessObjectName': businessObjectName,
                        'businessId': businessId
                    }
                    r = requests.post(url, headers=header, data=data)
                    dataDict["details"] = r.text

                    crawlList.append(dataDict)

                page = object.get("page")
                totalPage = page.get("totalPage")
                pageNo = page.get("pageNo")


                if pageNo >= totalPage:
                    break
                pageNo = pageNo + 1
            else:
                print(r.text)


        except Exception as e:
            print(e)

    return crawlList

if __name__=='__main__':
    # 读取js文件
    js_content = getJsCode()
    # 编译js文件
    ctx = execjs.compile(js_content)
    crawlList = crawl("互联网","2020-05-05","2020-05-10")
    for c in crawlList:
        print(c)

