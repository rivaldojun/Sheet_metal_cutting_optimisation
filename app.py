from flask import Flask, render_template,request,jsonify,session,redirect,url_for,make_response,send_file
from api.optimisation import optimize,Item,Panel,Params
import time
app = Flask(__name__)
app.secret_key = '123'

valuesList = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        data = request.get_json()
        session['data']=data['data']
        session['pan']=data['pan']
        session['valeur']=data['valeur']
    return render_template('index.html')

@app.route('/coupe')
def plandecoupe():
    start_time=time.time()

    pan=session.get('pan')
    cut=float(session.get('valeur'))
    item=[]
    panel=[]
    k=1
    l=1
    p=Panel(l,float(pan[0]),float(pan[1]))
    l=l+1
    panel.append(p)
    data=session.get('data')
    
    
    for d in data:
        nom_produit=d[0]
        total_quantite=int(d[1])
        height=float(d[2])
        width=float(d[3])
        rotate=float(d[4])
        color=d[5]
        if (width!=0 and height!=0):
            for j in range(total_quantite):
                item.append(Item(k,width,height,rotate,nom_produit,color=color))
                k=k+1
    params=Params(panel,item,cut,True)
    sorti,r=optimize(params)
    
    if sorti=="vide":
        return redirect(url_for('erreur'))
    while sorti=="pas possible":  
        p=Panel(l,float(pan[0]),float(pan[1]))
        l=l+1
        panel.append(p)
        params=Params(panel,item,cut,True)
        sorti,r=optimize(params)
    print(r)
    end_time=time.time()-start_time
    print("temps d'execution= ",end_time)
    return send_file('static/output.pdf', as_attachment=False)

@app.route('/erreur')
def erreur():
    return render_template("erreur.html")

if __name__ == '__main__':
     app.run(debug=True)