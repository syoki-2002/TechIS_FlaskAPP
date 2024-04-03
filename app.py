from flask import Flask, render_template, request, session, url_for, redirect
from flask.views import MethodView
import random
import pickle
app = Flask(__name__)
@app.route('/sample', methods=['GET'])
def index():
  n = random.randrange(5,10)
  data = []
  for n in range(n):
    data.append(random.randrange(0,100))
  return render_template('index.html', title='Template Sample', message='これはサンプルのページです',data=data)

@app.route('/', methods=['GET','POST'])
def predict():
  if request.method == 'GET':
   msg = 'コロナの感染確率を予測したい地域と情報を入力してください'
   return render_template('predict.html', title='ようこそ', message=msg)
  if request.method == 'POST':
    reg = pickle.load(open('./model/s_data_model.pkl', 'rb'))
    x1 = request.form.get('人口')
    x2 = request.form.get('飲食店の数')
    x3 = request.form.get('バス停の数')
    x4 = request.form.get('駅数')
    x5 = request.form.get('観光スポット')
    x6 = request.form.get('宿泊施設')
    x7=request.form.get('土地面積')
    x = [[int(x1), int(x2), int(x3), int(x4), int(x5), int(x6),float(x7)]]
    corona = reg.predict(x)
    corona = round(corona[0], 2)
    corona_rate = 0 if int(x1)==0 else max(min(round(corona/int(x1),2),100),0)
    corona = f'コロナの感染確率：コロナの感染確率は{corona_rate}%です。'
    return render_template('predict.html', title='Predict Page', message=corona, 人口=x1, 飲食店の数=x2, バス停の数=x3, 駅数=x4, 観光スポット=x5, 宿泊施設=x6, 土地面積=x7)

@app.route('/next', methods=['GET'])
def next():
  return render_template('next.html', title='Next Page', message='これは次のページのサンプルです', data=['A','B','C'])

@app.template_filter('sum')
def sum_filter(data):
  total = 0
  for item in data:
    total += item
  return total
app.jinja_env.filters['list_sum'] = sum_filter

@app.context_processor
def sample_processor():
  def total(n):
    total = 0
    for i in range(n + 1):
      total += i
    return total
  return dict( total = total )

app.secret_key = b'asdfghjkl'
class HelloAPI( MethodView ):
  send = ''
  def get(self):
    if 'send' in session:
      msg = 'send：' + session['send']
      send = session['send']
    else:
      msg = 'メッセージを書いてください'
      send = ''
    return render_template('next.html', title='Next Page', message=msg, send=send)
  def post(self):
    session['send'] = request.form['send']
    return redirect('/hello/')
app.add_url_rule('/hello/', view_func=HelloAPI.as_view('hello'))

if __name__ == '__main__':
  app.run(host='localhost',port=5555, debug=True)