import pandas as pd                                   
from bs4 import BeautifulSoup                          
import requests  
from time import sleep
import gspread       
import json
from oauth2client.service_account import ServiceAccountCredentials
from discord_webhook import DiscordWebhook, DiscordEmbed
webhook = DiscordWebhook(
    url='https://discord.com/api/webhooks/885738210028834837/1sgVSbCizBNn9U5xApl2cLxoeb2XuTCUlCbA1ziqPKUMltzrDZJCJSvmVYHry3kLd4Bm', username="Flippa Scraped File")
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86 Safari/537.36'
}
def flippa_scrape():
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive.file']
    creds = ServiceAccountCredentials.from_json_keyfile_name('sheets-automation-lovefromvlogger.json', scope)
    client = gspread.authorize(creds)
    
    import datetime
    x = datetime.datetime.now()
    hour = x.hour
    minute = x.minute
    date_1= x.day
    month = x.month
    year = x.year
    date_time1 = f'{date_1}-{month}-{year}_{hour}-{minute}'
    
    login_data = {
        'utf8': '✓',
        'session[email]': 'banglabokbok420@gmail.com',
        'session[password]': '5rVQ&FSR',
        'commit': 'Sign in'

    }
    
    prac_sheet_api = client.open("flippa_all_listings").sheet1
    all_links = prac_sheet_api.col_values(1)[1:]
    print(len(all_links))
    
    data_list = []                                         
    item = {}
    with requests.Session() as s:
        url = 'https://www.flippa.com/sign-in'
        r = s.get(url, headers = headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        login_data['authenticity_token'] = soup.find('input', attrs = {'name':'authenticity_token'})['value']

        r = s.post(url, data = login_data, headers = headers)
        link = 'https://flippa.com/search?filter%5Bproperty_type%5D=website,established_website,starter_site&page%5Bsize%5D=7000'
        rs = s.get(link, headers= headers)
        soup = BeautifulSoup(rs.content, 'html5lib')
        print(soup)
        links1 = soup.find("div",attrs={'id':'bootstrap-scope'}).find('script',attrs= {'type':'text/javascript'}).get_text().split('const DEFAULT_SEARCH_PARAMS')[0].split('const FILTER_OPTIONS')[1][2:].split('const STATE = ')[1]
        links1 = links1[:-4]
        print(links1)
        m = json.loads(links1)


        with open(f'{date_time1}.json', 'w') as outfile:
            json.dump(m, outfile)
        with open(f'{date_time1}.json','r') as file:
            data = json.load(file)

        reviews_json = data.get('listings')
        for time,domains,nickname,review_1,review_2,rating1,siteages,profitpmonths,unique_traffics,bid_prices,num_bids,abouts in zip(reviews_json,reviews_json,reviews_json,reviews_json,reviews_json,reviews_json,reviews_json,reviews_json,reviews_json,reviews_json,reviews_json,reviews_json):
            link3 = time.get('listing_url')
            if link3 in all_links:
                pass
            else:
                print(link3)

                property_name = domains.get('property_name')

                title = nickname.get('title')
                country_name = review_1.get('country_name')
                category = review_2.get('category')

                monetization = rating1.get('monetization')
                siteage = siteages.get('formatted_age_in_years')
                profitpmonth = profitpmonths.get('profit_average')
                unique_traffic = unique_traffics.get('uniques_per_month')
                bid_price1 = bid_prices.get('price')
                bid_price = f'${bid_price1} USD'
                num_bid = num_bids.get('bid_count')
                about = abouts.get('summary')
                item = {
                    'Listing_url': link3,
                    'Domain': property_name,
                    'Type': category,
                    'Country': country_name,
                    'Category': title,
                    'Monetization': monetization,
                    'Site Age': siteage,
                    'Avg net profit per month $': profitpmonth,
                    'Avg monthly traffic unique': unique_traffic,
                    'Bid price $': bid_price,
                    'Number of bids': num_bid,
                    'About': about
                }
                data_list.append(item)

    df = pd.DataFrame(data_list)
    done = df.drop_duplicates(subset=['Domain','About','Bid price $'],keep='first') 
    dn = done.reset_index(drop=True)
    
    all_links2 = dn['Listing_url'].tolist()
    kn = len(all_links2)
    
    lin = []
    for li in all_links2:
        lin.append([li])

    length = len(all_links)+2
    prac_sheet_api.update(f'{length}:100000', lin)
    leng = length - 1
    
    all_links_collected_to_csv = dn['Listing_url'].tolist()
    domain = dn['Domain'].tolist()
    types = dn['Type'].tolist()
    country_a = dn['Country'].tolist()
    category = dn['Category'].tolist()
    monetization = dn['Monetization'].tolist()
    site_age = dn['Site Age'].tolist()
    avg_net_profit_per_month = dn['Avg net profit per month $'].tolist()
    avg_monthly_traffic_unique = dn['Avg monthly traffic unique'].tolist()
    bid_price = dn['Bid price $'].tolist()
    number_of_bids = dn['Number of bids'].tolist()
    
    
    data = []
    lists = {}
    

    with requests.Session() as s:
        url = 'https://www.flippa.com/sign-in'
        r = s.get(url, headers = headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        login_data['authenticity_token'] = soup.find('input', attrs = {'name':'authenticity_token'})['value']

        r = s.post(url, data = login_data, headers = headers)
        counts = 0
        name = 'Flippa'
        for link,a1,b1,c1,d1,e1,f1,g1,h1,i1,j1 in zip(all_links_collected_to_csv,domain,types,country_a,category,monetization,site_age,avg_net_profit_per_month,avg_monthly_traffic_unique,bid_price,number_of_bids):
            counts += 1
            ids = link.split('/')[3]
            print(counts)
            print(link)
            try:
                rs = s.get(link, headers= headers, timeout = 10)
                soup = BeautifulSoup(rs.content, 'html.parser')
    #----------------------------------------------------------------------------------------------
                try:
                    platform = soup.find('div',attrs= {'id':'platform'}).get_text().strip()    
                except:
                    platform = '-'

        #----------------------------------------------------------------------------------------------
                try:
                    avg_rev_per_month = soup.find('div',attrs= {'id':'gross_revenue'}).get_text().strip()[1:-4]
                except:
                    avg_rev_per_month = '-'

        #----------------------------------------------------------------------------------------------
                try:
                    prof_box = soup.find('div',attrs={'class':'Chart Chart--snapshot Chart--snapshotMd'})
                except:
                    pass
        #----------------------------------------------------------------------------------------------
                try:
                    traffic_box = soup.find('div',attrs= {'class':'Chart Chart--snapshot'})
                except:
                    pass
        #----------------------------------------------------------------------------------------------
                try:
                    profit = prof_box['profit-data'].split(',')
                except:
                    pass
        #----------------------------------------------------------------------------------------------
                try:
                    revenue = prof_box['gross-data'].split(',')
                except:
                    pass
        #----------------------------------------------------------------------------------------------
                try:
                    traffic = traffic_box['line-two'].split(',')
                except:
                    pass
        #----------------------------------------------------------------------------------------------
                traffic_date = []
                try:
                    traffic_date1 = traffic_box['months'].split(',')
                    for n in traffic_date1:
                        an = n[1:-1].replace('"','')
                        bn = an[:-2] + '20' + an[-2:]
                        traffic_date.append(bn)
        #             print(traffic_date)
                except:
                    pass
        #----------------------------------------------------------------------------------------------
                date = []
                try:
                    prof_rev_date1 = prof_box['months'].split(',')
                    for n in prof_rev_date1:
                        ans = n[1:-1].replace('"','')
                        bns = ans[:-2] + '20' + ans[-2:]
                        date.append(bns)
        #             print(date)
                except:
                    pass
        
        #----------------------------------------------------------------------------------------------
                try:
                    profits = '-'
                except:
                    pass
                try:
                    profits = f"{date[0][:]} : ${profit[0][1:].replace(']','').replace('null','0')}"
                except:
                    pass
                try:
                    profits = f"{date[0][:]} : ${profit[0][1:].replace('null','0')}\n{date[1]} : ${profit[1].replace(']','').replace('null','0')}"
                except:
                    pass
                try:
                    profits = f"{date[0][:]} : ${profit[0][1:].replace('null','0')}\n{date[1]} : ${profit[1].replace('null','0')}\n{date[2]} : ${profit[2].replace(']','').replace('null','0')}"
                except:
                    pass
                try:
                    profits = f"{date[0][:]} : ${profit[0][1:].replace('null','0')}\n{date[1]} : ${profit[1].replace('null','0')}\n{date[2]} : ${profit[2].replace('null','0')}\n{date[3]} : ${profit[3].replace(']','').replace('null','0')}"
                except:
                    pass
                try:
                    profits = f"{date[0][:]} : ${profit[0][1:].replace('null','0')}\n{date[1]} : ${profit[1].replace('null','0')}\n{date[2]} : ${profit[2].replace('null','0')}\n{date[3]} : ${profit[3].replace('null','0')}\n{date[4]} : ${profit[4].replace(']','').replace('null','0')}"
                except:
                    pass
                try:
                    profits = f"{date[0][:]} : ${profit[0][1:].replace('null','0')}\n{date[1]} : ${profit[1].replace('null','0')}\n{date[2]} : ${profit[2].replace('null','0')}\n{date[3]} : ${profit[3].replace('null','0')}\n{date[4]} : ${profit[4].replace('null','0')}\n{date[5]} : ${profit[5].replace(']','').replace('null','0')}"
                except:
                    pass 
                try:
                    profits = f"{date[0][:]} : ${profit[0][1:].replace('null','0')}\n{date[1]} : ${profit[1].replace('null','0')}\n{date[2]} : ${profit[2].replace('null','0')}\n{date[3]} : ${profit[3].replace('null','0')}\n{date[4]} : ${profit[4].replace('null','0')}\n{date[5]} : ${profit[5].replace('null','0')}\n{date[6]} : ${profit[6].replace(']','').replace('null','0')}" 
                except:
                    pass
                try:
                    profits = f"{date[0][:]} : ${profit[0][1:].replace('null','0')}\n{date[1]} : ${profit[1].replace('null','0')}\n{date[2]} : ${profit[2].replace('null','0')}\n{date[3]} : ${profit[3].replace('null','0')}\n{date[4]} : ${profit[4].replace('null','0')}\n{date[5]} : ${profit[5].replace('null','0')}\n{date[6]} : ${profit[6].replace('null','0')}\n{date[7]} : ${profit[7].replace(']','').replace('null','0')}"
                except:
                    pass
                try:
                    profits = f"{date[0][:]} : ${profit[0][1:].replace('null','0')}\n{date[1]} : ${profit[1].replace('null','0')}\n{date[2]} : ${profit[2].replace('null','0')}\n{date[3]} : ${profit[3].replace('null','0')}\n{date[4]} : ${profit[4].replace('null','0')}\n{date[5]} : ${profit[5].replace('null','0')}\n{date[6]} : ${profit[6].replace('null','0')}\n{date[7]} : ${profit[7].replace('null','0')}\n{date[8]} : ${profit[8].replace(']','').replace('null','0')}"
                except:
                    pass
                try:
                    profits = f"{date[0][:]} : ${profit[0][1:].replace('null','0')}\n{date[1]} : ${profit[1].replace('null','0')}\n{date[2]} : ${profit[2].replace('null','0')}\n{date[3]} : ${profit[3].replace('null','0')}\n{date[4]} : ${profit[4].replace('null','0')}\n{date[5]} : ${profit[5].replace('null','0')}\n{date[6]} : ${profit[6].replace('null','0')}\n{date[7]} : ${profit[7].replace('null','0')}\n{date[8]} : ${profit[8].replace('null','0')}\n{date[9]} : ${profit[9].replace(']','').replace('null','0')}"
                except:
                    pass
                try:
                    profits = f"{date[0][:]} : ${profit[0][1:].replace('null','0')}\n{date[1]} : ${profit[1].replace('null','0')}\n{date[2]} : ${profit[2].replace('null','0')}\n{date[3]} : ${profit[3].replace('null','0')}\n{date[4]} : ${profit[4].replace('null','0')}\n{date[5]} : ${profit[5].replace('null','0')}\n{date[6]} : ${profit[6].replace('null','0')}\n{date[7]} : ${profit[7].replace('null','0')}\n{date[8]} : ${profit[8].replace('null','0')}\n{date[9]} : ${profit[9].replace('null','0')}\n{date[10]} : ${profit[10].replace(']','').replace('null','0')}"
                except:
                    pass
                try:
                    profits = f"{date[0][:]} : ${profit[0][1:].replace('null','0')}\n{date[1]} : ${profit[1].replace('null','0')}\n{date[2]} : ${profit[2].replace('null','0')}\n{date[3]} : ${profit[3].replace('null','0')}\n{date[4]} : ${profit[4].replace('null','0')}\n{date[5]} : ${profit[5].replace('null','0')}\n{date[6]} : ${profit[6].replace('null','0')}\n{date[7]} : ${profit[7].replace('null','0')}\n{date[8]} : ${profit[8].replace('null','0')}\n{date[9]} : ${profit[9].replace('null','0')}\n{date[10]} : ${profit[10].replace('null','0')}\n{date[11]} : ${profit[11].replace(']','').replace('null','0')}" 
                except:
                    pass
        #----------------------------------------------------------------------------------------------
                try:
                    revenues = '-'
                except:
                    pass
                try:
                    revenues = f"{date[0][:]} : ${revenue[0][1:].replace(']','').replace('null','0')}"
                except:
                    pass
                try:
                    revenues = f"{date[0][:]} : ${revenue[0][1:].replace('null','0')}\n{date[1]} : ${revenue[1].replace(']','').replace('null','0')}"
                except:
                    pass
                try:
                    revenues = f"{date[0][:]} : ${revenue[0][1:].replace('null','0')}\n{date[1]} : ${revenue[1].replace('null','0')}\n{date[2]} : ${revenue[2].replace(']','').replace('null','0')}"
                except:
                    pass
                try:
                    revenues = f"{date[0][:]} : ${revenue[0][1:].replace('null','0')}\n{date[1]} : ${revenue[1].replace('null','0')}\n{date[2]} : ${revenue[2].replace('null','0')}\n{date[3]} : ${revenue[3].replace(']','').replace('null','0')}"
                except:
                    pass
                try:
                    revenues = f"{date[0][:]} : ${revenue[0][1:].replace('null','0')}\n{date[1]} : ${revenue[1].replace('null','0')}\n{date[2]} : ${revenue[2].replace('null','0')}\n{date[3]} : ${revenue[3].replace('null','0')}\n{date[4]} : ${revenue[4].replace(']','').replace('null','0')}"
                except:
                    pass
                try:
                    revenues = f"{date[0][:]} : ${revenue[0][1:].replace('null','0')}\n{date[1]} : ${revenue[1].replace('null','0')}\n{date[2]} : ${revenue[2].replace('null','0')}\n{date[3]} : ${revenue[3].replace('null','0')}\n{date[4]} : ${revenue[4].replace('null','0')}\n{date[5]} : ${revenue[5].replace(']','').replace('null','0')}"
                except:
                    pass 
                try:
                    revenues = f"{date[0][:]} : ${revenue[0][1:].replace('null','0')}\n{date[1]} : ${revenue[1].replace('null','0')}\n{date[2]} : ${revenue[2].replace('null','0')}\n{date[3]} : ${revenue[3].replace('null','0')}\n{date[4]} : ${revenue[4].replace('null','0')}\n{date[5]} : ${revenue[5].replace('null','0')}\n{date[6]} : ${revenue[6].replace(']','').replace('null','0')}" 
                except:
                    pass
                try:
                    revenues = f"{date[0][:]} : ${revenue[0][1:].replace('null','0')}\n{date[1]} : ${revenue[1].replace('null','0')}\n{date[2]} : ${revenue[2].replace('null','0')}\n{date[3]} : ${revenue[3].replace('null','0')}\n{date[4]} : ${revenue[4].replace('null','0')}\n{date[5]} : ${revenue[5].replace('null','0')}\n{date[6]} : ${revenue[6].replace('null','0')}\n{date[7]} : ${revenue[7].replace(']','').replace('null','0')}"
                except:
                    pass
                try:
                    revenues = f"{date[0][:]} : ${revenue[0][1:].replace('null','0')}\n{date[1]} : ${revenue[1].replace('null','0')}\n{date[2]} : ${revenue[2].replace('null','0')}\n{date[3]} : ${revenue[3].replace('null','0')}\n{date[4]} : ${revenue[4].replace('null','0')}\n{date[5]} : ${revenue[5].replace('null','0')}\n{date[6]} : ${revenue[6].replace('null','0')}\n{date[7]} : ${revenue[7].replace('null','0')}\n{date[8]} : ${revenue[8].replace(']','').replace('null','0')}"
                except:
                    pass
                try:
                    revenues = f"{date[0][:]} : ${revenue[0][1:].replace('null','0')}\n{date[1]} : ${revenue[1].replace('null','0')}\n{date[2]} : ${revenue[2].replace('null','0')}\n{date[3]} : ${revenue[3].replace('null','0')}\n{date[4]} : ${revenue[4].replace('null','0')}\n{date[5]} : ${revenue[5].replace('null','0')}\n{date[6]} : ${revenue[6].replace('null','0')}\n{date[7]} : ${revenue[7].replace('null','0')}\n{date[8]} : ${revenue[8].replace('null','0')}\n{date[9]} : ${revenue[9].replace(']','').replace('null','0')}"
                except:
                    pass
                try:
                    revenues = f"{date[0][:]} : ${revenue[0][1:].replace('null','0')}\n{date[1]} : ${revenue[1].replace('null','0')}\n{date[2]} : ${revenue[2].replace('null','0')}\n{date[3]} : ${revenue[3].replace('null','0')}\n{date[4]} : ${revenue[4].replace('null','0')}\n{date[5]} : ${revenue[5].replace('null','0')}\n{date[6]} : ${revenue[6].replace('null','0')}\n{date[7]} : ${revenue[7].replace('null','0')}\n{date[8]} : ${revenue[8].replace('null','0')}\n{date[9]} : ${revenue[9].replace('null','0')}\n{date[10]} : ${revenue[10].replace(']','').replace('null','0')}"
                except:
                    pass
                try:
                    revenues = f"{date[0][:]} : ${revenue[0][1:].replace('null','0')}\n{date[1]} : ${revenue[1].replace('null','0')}\n{date[2]} : ${revenue[2].replace('null','0')}\n{date[3]} : ${revenue[3].replace('null','0')}\n{date[4]} : ${revenue[4].replace('null','0')}\n{date[5]} : ${revenue[5].replace('null','0')}\n{date[6]} : ${revenue[6].replace('null','0')}\n{date[7]} : ${revenue[7].replace('null','0')}\n{date[8]} : ${revenue[8].replace('null','0')}\n{date[9]} : ${revenue[9].replace('null','0')}\n{date[10]} : ${revenue[10].replace('null','0')}\n{date[11]} : ${revenue[11].replace(']','').replace('null','0')}" 
                except:
                    pass
        #----------------------------------------------------------------------------------------------
                try:
                    traffics = '-'
                except:
                    pass
                try:
                    traffics = f"{traffic_date[0][:]} : {traffic[0][1:].replace(']','')}"
                except:
                    pass
                try:
                    traffics = f"{traffic_date[0][:]} : {traffic[0][1:]}\n{traffic_date[1]} : {traffic[1].replace(']','')}"
                except:
                    pass
                try:
                    traffics = f"{traffic_date[0][:]} : {traffic[0][1:]}\n{traffic_date[1]} : {traffic[1]}\n{traffic_date[2]} : {traffic[2].replace(']','')}"
                except:
                    pass
                try:
                    traffics = f"{traffic_date[0][:]} : {traffic[0][1:]}\n{traffic_date[1]} : {traffic[1]}\n{traffic_date[2]} : {traffic[2]}\n{traffic_date[3]} : {traffic[3].replace(']','')}"
                except:
                    pass
                try:
                    traffics = f"{traffic_date[0][:]} : {traffic[0][1:]}\n{traffic_date[1]} : {traffic[1]}\n{traffic_date[2]} : {traffic[2]}\n{traffic_date[3]} : {traffic[3]}\n{traffic_date[4]} : {traffic[4].replace(']','')}"
                except:
                    pass
                try:
                    traffics = f"{traffic_date[0][:]} : {traffic[0][1:]}\n{traffic_date[1]} : {traffic[1]}\n{traffic_date[2]} : {traffic[2]}\n{traffic_date[3]} : {traffic[3]}\n{traffic_date[4]} : {traffic[4]}\n{traffic_date[5]} : {traffic[5].replace(']','')}"
                except:
                    pass 
                try:
                    traffics = f"{traffic_date[0][:]} : {traffic[0][1:]}\n{traffic_date[1]} : {traffic[1]}\n{traffic_date[2]} : {traffic[2]}\n{traffic_date[3]} : {traffic[3]}\n{traffic_date[4]} : {traffic[4]}\n{traffic_date[5]} : {traffic[5]}\n{traffic_date[6]} : {traffic[6].replace(']','')}" 
                except:
                    pass
                try:
                    traffics = f"{traffic_date[0][:]} : {traffic[0][1:]}\n{traffic_date[1]} : {traffic[1]}\n{traffic_date[2]} : {traffic[2]}\n{traffic_date[3]} : {traffic[3]}\n{traffic_date[4]} : {traffic[4]}\n{traffic_date[5]} : {traffic[5]}\n{traffic_date[6]} : {traffic[6]}\n{traffic_date[7]} : {traffic[7].replace(']','')}"
                except:
                    pass
                try:
                    traffics = f"{traffic_date[0][:]} : {traffic[0][1:]}\n{traffic_date[1]} : {traffic[1]}\n{traffic_date[2]} : {traffic[2]}\n{traffic_date[3]} : {traffic[3]}\n{traffic_date[4]} : {traffic[4]}\n{traffic_date[5]} : {traffic[5]}\n{traffic_date[6]} : {traffic[6]}\n{traffic_date[7]} : {traffic[7]}\n{traffic_date[8]} : {traffic[8].replace(']','')}"
                except:
                    pass
                try:
                    traffics = f"{traffic_date[0][:]} : {traffic[0][1:]}\n{traffic_date[1]} : {traffic[1]}\n{traffic_date[2]} : {traffic[2]}\n{traffic_date[3]} : {traffic[3]}\n{traffic_date[4]} : {traffic[4]}\n{traffic_date[5]} : {traffic[5]}\n{traffic_date[6]} : {traffic[6]}\n{traffic_date[7]} : {traffic[7]}\n{traffic_date[8]} : {traffic[8]}\n{traffic_date[9]} : {traffic[9].replace(']','')}"
                except:
                    pass
                try:
                    traffics = f"{traffic_date[0][:]} : {traffic[0][1:]}\n{traffic_date[1]} : {traffic[1]}\n{traffic_date[2]} : {traffic[2]}\n{traffic_date[3]} : {traffic[3]}\n{traffic_date[4]} : {traffic[4]}\n{traffic_date[5]} : {traffic[5]}\n{traffic_date[6]} : {traffic[6]}\n{traffic_date[7]} : {traffic[7]}\n{traffic_date[8]} : {traffic[8]}\n{traffic_date[9]} : {traffic[9]}\n{traffic_date[10]} : {traffic[10].replace(']','')}"
                except:
                    pass
                try:
                    traffics = f"{traffic_date[0][:]} : {traffic[0][1:]}\n{traffic_date[1]} : {traffic[1]}\n{traffic_date[2]} : {traffic[2]}\n{traffic_date[3]} : {traffic[3]}\n{traffic_date[4]} : {traffic[4]}\n{traffic_date[5]} : {traffic[5]}\n{traffic_date[6]} : {traffic[6]}\n{traffic_date[7]} : {traffic[7]}\n{traffic_date[8]} : {traffic[8]}\n{traffic_date[9]} : {traffic[9]}\n{traffic_date[10]} : {traffic[10]}\n{traffic_date[11]} : {traffic[11].replace(']','')}" 
                except:
                    pass

            #------------------------------------------------------------------------------------------------------------------------------------------
                try:
                    description = soup.find('div',attrs= {'class':'Listing-siteDescription'}).get_text()
                except:
                    description = '-'
        #         print(description)

        #----------------------------------------------------------------------------------------------
        #----------------------------------------------------------------------------------------------   

                try:
                    buy_now_price = soup.find('span',attrs= {'class':'Listing-buyItNowPrice'}).get_text().strip()
                except:
                    buy_now_price = '-'

        #----------------------------------------------------------------------------------------------       
                try:
                    backlinks = soup.findAll('h3',attrs= {'class':'Semrush__attribute-value u-mgn-top-15'})[1].get_text()
                except:
                    backlinks = '-'
                print(backlinks)

        #----------------------------------------------------------------------------------------------       
                try:
                    reffering_domains = soup.findAll('h3',attrs= {'class':'Semrush__attribute-value u-mgn-top-15'})[0].get_text()
                except:
                    reffering_domains = '-'

        #----------------------------------------------------------------------------------------------
                channels = []
                try:
                    channel = soup.findAll('table',attrs={'class':'Table Table--bordered'})[1].find('tbody').find_all('tr')
                    for n in channel:
                        date1 = n.find('td').get_text()
                        channels.insert(0,date1)
                    try:
                        channel_1 = channels[-1].strip()
                    except:
                        channel_1 = '-'
                    try:
                        channel_2 = channels[-2].strip()
                    except:
                        channel_2 = '-'
                    try:
                        channel_3 = channels[-3].strip()
                    except:
                        channel_3 = '-'
                    try:
                        channel_4 = channels[-4].strip()
                    except:
                        channel_4 = '-'
                    try:
                        channel_5 = channels[-5].strip()
                    except:
                        channel_5 = '-'

                except:
                    channel_1 = '-'
                    channel_2 = '-'
                    channel_3 = '-'
                    channel_4 = '-'
                    channel_5 = '-'

        #----------------------------------------------------------------------------------------------
                countries = []
                try:
                    country = soup.findAll('table',attrs={'class':'Table Table--bordered'})[2].find('tbody').find_all('tr')
                    for n in country:
                        date1 = n.find('td').get_text()
                        countries.insert(0,date1)

                    try:
                        country_1 = countries[-1].strip()
                    except:
                        country_1 = '-'
                    try:
                        country_2 = countries[-2].strip()
                    except:
                        country_2 = '-'
                    try:
                        country_3 = countries[-3].strip()
                    except:
                        country_3 = '-'
                    try:
                        country_4 = countries[-4].strip()
                    except:
                        country_4 = '-'
                    try:
                        country_5 = countries[-5].strip()
                    except:
                        country_5 = '-'


                except:
                    country_1 = '-'
                    country_2 = '-'
                    country_3 = '-'
                    country_4 = '-'
                    country_5 = '-'
        #----------------------------------------------------------------------------------------------
                try:
                    seller_name = soup.find('div',attrs= {'class':'about-the-seller__name'}).get_text().strip()
                except:
                    seller_name = '-'
                print(seller_name)
                try:
                    total_keywords = soup.findAll('h3',attrs= {'class':'Semrush__attribute-value u-mgn-top-15'})[2].get_text()
                except:
                    total_keywords = '-' 
            except:
                a1 = '-'
                b1 = '-'
                c1 = '-'
                d1 = '-'
                e1 = '-'
                f1 = '-'
                g1 = '-'
                h1 = '-'
                i1 = '-'
                j1 = '-'
                seller_name = '-'
                backlinks = '-'



            lists = {
                'Website': name,
                'Id': ids,
                'Url': link,
                'Domain': a1,
                'Platform': platform,
                'Industry':b1,
                'Country':c1,
                'Category':d1,
                'Monetization':e1,
                'Site Age': f1,
                'Avg net profit per Month $': g1,
                'Avg revenue per month': avg_rev_per_month,
                'Avg monthly traffic unique': h1,
                'Profit Months': profits,
                'Revenue Months': revenues,
                'Traffic Months': traffics,
                'Buy Now Price': buy_now_price,
                'Bid Price':i1,
                'Number of bids': j1,
                'About':description,
                'Backlinks Number': backlinks,
                'Reffering Domains': reffering_domains,
                'Total Keywords': total_keywords,
                'Top 1 channel': channel_1,
                'Top 2 channel': channel_2,
                'Top 3 channel': channel_3,
                'Top 4 channel': channel_4,
                'Top 5 channel': channel_5,
                'Top 1 Countries': country_1,
                'Top 2 countries': country_2,
                'Top 3 countries': country_3,
                'Top 4 countries': country_4,
                'Top 5 countries': country_5,
                'Seller Name': seller_name,
                'Country of Seller':c1,
                'Date/Time Scraped': date_time1
            }
            data.append(lists)
    #         print(data)
    df1 = pd.DataFrame(data)
    df = df1.drop_duplicates(subset=['Domain', 'Bid Price', 'Seller Name','Backlinks Number'], keep=False).reset_index(drop=True)
    df.to_csv(f'{date_time1}.csv',encoding='utf-8-sig', index=False)
    sleep(3)
    
    import boto3
    from botocore.client import Config
    import os
    import datetime

    ACCESS_KEY_ID = 'HYSNOFX366HFL5SNDO2U'
    ACCESS_SECRET_KEY = 'I0KyriBKEjM6v8pD7CxNjUDDzVUdsmWofTxxJrMTzX0'
    bucket_name = 'flippa-exchange'

    session = boto3.session.Session()
    client = session.client('s3',
                            region_name='fra1',
                            endpoint_url='https://fra1.digitaloceanspaces.com',
                            aws_access_key_id=ACCESS_KEY_ID,
                            aws_secret_access_key=ACCESS_SECRET_KEY)

    file_dir = 'Flippa'
    for file in os.listdir():
        if f'{date_time1}.csv' in file:
            print(f'file name: {file}\n')
            upload_file_bucket = bucket_name
            upload_file_key = 'Flippa/' + str(file)
            client.upload_file(file, bucket_name,upload_file_key)
    print('Bot sent files')
    
    embed = DiscordEmbed(title='Flippa', description=f'''Urls Yesterday: {leng}
    Total New Urls Today: {kn}''')
    with open(f'{date_time1}.csv', "rb") as f:
        webhook.add_file(file=f.read(), filename=f'{date_time1}.csv')
    webhook.add_embed(embed)
    response = webhook.execute()
    webhook.remove_embeds()
    webhook.remove_files()
    sleep(601)
    
while True:
    r = requests.get('https://www.timeanddate.com/worldclock/bangladesh/dhaka',headers= headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    time1 = soup.find('span',attrs= {'id':'ct'}).get_text().lower()
    print(time1)
    time = time1[:5]
    
    if 'am' in str(time1):
        if '10:23' in str(time):
            flippa_scrape()
        if '10:24' in str(time):
            flippa_scrape()
        if '10:25' in str(time):
            flippa_scrape()
        if '10:26' in str(time):
            flippa_scrape()
        if '10:27' in str(time):
            flippa_scrape()
        
    sleep(179)