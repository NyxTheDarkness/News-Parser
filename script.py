import newspaper
import time
import datetime

def CheckForMoreArticles():
    print 'Checking for more articles from CNN'
    cnn = newspaper.build(u'http://us.cnn.com/')
    print 'Found ' + str(cnn.size()) + ' new articles from CNN'
    print 'Checking for more articles from SMH'
    smh = newspaper.build(u'http://smh.com.au/')
    print 'Found ' + str(smh.size()) + ' new articles from SMH'
    print 'Checking for more articles from Slashdot'
    slashdot = newspaper.build(u'http://slashdot.org/')
    print 'Found ' + str(smh.size()) + ' new articles from SlashDot'
    return cnn.articles + smh.articles + slashdot.articles

def CompileData(article):
    title = article.title + '\r\n===================================================================\r\n'
    date = 'Date:\r\n' + str(article.publish_date) + '\r\n===================================================================\r\n'
    keywords = 'Keywords:\r\n' + str(article.keywords).encode('utf-8') + '\r\n===================================================================\r\n'
    summary = 'Generated Summary:\r\n' + article.summary + '\r\n===================================================================\r\n'
    link = 'Link:\r\n' + article.url + '\r\n===================================================================\r\n'
    data = title + date + keywords + summary + link
    return data.encode('utf-8')

def MakeValidName(title):
    win_valid = '-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(b for b in title if b in win_valid)


#Setup
interesting = False
alive = True
seperator = '==================================================================='
keys = open("keywords.txt").read().splitlines()
print '===================='
print '     News Parser'
print '       By Nyx'
print '===================='
articles = CheckForMoreArticles()
print seperator



while(alive):
    for article in articles:
        try:
            print 'Downloading new article'
            article.download()
            print 'Parsing new article'
            article.parse()
            article.nlp()
            print 'Currently doing new article: ' + article.title.encode('utf-8')
            for key in keys:
                if key in article.keywords:
                    interesting = True
                    print 'New article seems interesting'
                    print 'Saving article to storage'
                    with open('articles/' + MakeValidName(article.title) + '.txt', "w") as text_file:
                        text_file.write(CompileData(article))
                    break
            if interesting == False:
                print 'New article does not seem interesting'
            interesting = False
        except:
            print('Failed parsing new article')
        print seperator
    print 'Waitng 10 minutes before checking for more articles'
    time.sleep(600)
    articles = CheckForMoreArticles()
    print seperator
