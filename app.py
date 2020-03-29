import os, sys
import requests


api_key='enter your api key here'
url='https://newsapi.org/v2/top-headlines' 


welcome= ''' 

	Welcome to JB's news app

	Usage: python app.py -country [country code] -category [category] -results [number of results]

	Options:

	-country	:	ae ar at au be bg br ca ch cn co cu cz de eg 
				fr gb gr hk hu id ie il in it jp kr lt lv ma 
				mx my ng nl no nz ph pl pt ro rs ru sa se sg 
				si sk th tr tw ua us ve za


	-category   :	Business, Entertainment, General, Health, Science, Sports, Technology

	-results    :	Number of Results (1-30). Default is 5.

	-help		:	Shows this usage info

'''

def news_api(country, category, results=5):
	params= {
		'country': f'{country}',
		'apikey': 'your api key here',
		'category': f'{category}', 
		'pageSize': '50'
	}

	response=requests.get(url,params=params)
	headlines=response.json()
	total_results=headlines['totalResults']

	
	try:
		if response.status_code==200:
			print('Total Results:',total_results)

			filename=f'{country}_{category}_news.txt'
			news=open(filename,'w')

			for article_number in range(results):
				try:
					# printing article title with description
					title=headlines['articles'][article_number]['title']
					description=headlines['articles'][article_number]['description']
					print(article_number,':\n',title, '\n\n', description,'\n\n\n')

					#making short urls of article links
					article_url=headlines['articles'][article_number]['url']
					url2=f'https://api.shrtco.de/v2/shorten?url={article_url}'
					response=requests.get(url2)
					response_json=response.json()
					short_link=response_json['result']['full_short_link']


					news.write(f"Article Number:{article_number}\n Title:{title}\n\n Description:{description}\n\n Short Link:{short_link}\n\n\n")

				except KeyError:
					print('Error in retrieving article info', '\n\n')
		
			news.close()
			path=os.getcwd()
			print(f'Details added to: {path}\\{filename}')		
		
		else:
			print("Status code:",headlines.status_code)
			
	
	except KeyError:
		print('Error Occured in news api')


args=sys.argv[1:]


if len(args)==0:
	print(welcome)

elif len(args)==4:
	try:
		news_api(args[1],args[3])
	except:
		print('Please input correct country code & category')
		print(welcome)

elif len(args)==6:
	try:
		news_api(args[1],args[3],int(args[5]))
	except:
		print('Please input correct country code, category, & number of results (1-30)')
		print(welcome)
elif len(args)==1:
	print(welcome)
else:
	print('Please input correct country code, category, & number of results (1-30)')
	print(welcome)
