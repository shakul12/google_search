from flask import Flask, render_template, request
from youtube_search import YoutubeSearch
import requests
import json
import pathlib
app = Flask(__name__)



def youtube(term):
	results = json.loads(YoutubeSearch(term, max_results=10).to_json())
	return results['videos']

def stackoverflow(term):
	url="https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=relevance&q={}&site=stackoverflow&pagesize=10".format(term)
	res=requests.get(url)
	res= res.json()
	return res['items']



@app.route("/", methods=['GET'])
def home():
	return render_template("index.html")

@app.route("/out")
def out():
	return render_template("template.html")

@app.route("/search", methods=['POST'])
def search():
	request_json = request.get_json()
	term= request_json['search']
	#term="key error python"
	youtube_result=youtube(term)
	stack_result= stackoverflow(term)
	to_be_written=""
	#print(pathlib.Path().absolute())
	f= open("techwithshakul/google-search/templates/template.html","w")
	start= '''<table id="output" style="height: 317px; width: 100%;">
				<tbody>
				<tr style="height: 109px;">
				<td style="width: 258px; height: 109px;"><img style="display: block; margin-left: auto; margin-right: auto;" src="https://www.onmsft.com/wp-content/uploads/2019/09/stackoverflow.png" alt="" width="254" height="184" /></td>
				<td style="width: 335px; text-align: center; height: 109px;"><img style="display: block; margin-left: auto; margin-right: auto;" src="https://logos-world.net/wp-content/uploads/2020/04/YouTube-Logo.png" alt="" width="162" height="91" /></td>
				</tr>'''
	end= '''</tbody>
			</table>'''
	f.write(start)
	for i in range(0,10):
		sr=stack_result[i]
		temp=''
		temp+='<tr style="height: 108px;">'
		temp+='<td style="width: 50%; height: 108px;">'
		temp+='<p style="text-align: center;"><a href="{}" target="_blank" rel="noopener">{}</a></p>'.format(sr['link'], sr['title'].encode('utf8'))
		temp+='<p style="text-align: center;"><strong>Views</strong>-&nbsp;{}<br /><strong>Score</strong>-&nbsp;{}</p>'.format(sr['view_count'], sr['score'])
		temp+='</td>'
		yr=youtube_result[i]
		temp+='<td style="width: 50%; height: 108px;">'
		temp+='<p><a href="http://www.youtube.com{}" target="_blank" rel="noopener"><img style="float: left;" src="{}" alt="" width="168" height="94" /></a>{}</p>'.format(yr['url_suffix'], yr['thumbnails'][0],yr['title'].encode('utf8'))
		temp+='<p><strong>Views</strong>- {}<br /><strong>Duration</strong>-{}</p>'.format(yr['views'],yr['duration'])
		temp+='</td></tr>'
		#print(temp)
		f.write(temp)
	f.write(end)
	f.close()
	return "done"


if __name__ == "__main__":
	app.run()