from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = "secret"

API_PECAS = "http://backend:8000/api/v1/pecas"
API_SERVICOS = "http://backend:8000/api/v1/servicos"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# ----- Pecas -----
@app.route('/pecas')
def pecas():
    resp = requests.get(f"{API_PECAS}/")
    lista = resp.json() if resp.ok else []
    return render_template('pecas.html', pecas=lista)

@app.route('/pecas/cadastro', methods=['GET', 'POST'])
def cadastrar_peca():
    if request.method == 'POST':
        data = {
            'nome': request.form['nome'],
            'descricao': request.form['descricao'],
            'preco': float(request.form['preco'])
        }
        r = requests.post(f"{API_PECAS}/", json=data)
        if r.status_code == 201:
            flash('Peça cadastrada!', 'success')
            return redirect(url_for('pecas'))
        else:
            flash(r.json().get('detail', 'Erro ao cadastrar peça'), 'danger')
    return render_template('cadastro_peca.html')

@app.route('/pecas/editar/<int:pid>', methods=['GET', 'POST'])
def editar_peca(pid):
    if request.method == 'POST':
        data = {
            'nome': request.form['nome'],
            'descricao': request.form['descricao'],
            'preco': float(request.form['preco'])
        }
        payload = {k: v for k, v in data.items() if str(v).strip() != ''}
        r = requests.patch(f"{API_PECAS}/{pid}", json=payload)
        if r.ok:
            flash('Peça atualizada', 'success')
        else:
            flash(r.json().get('detail', 'Erro ao atualizar'), 'danger')
        return redirect(url_for('pecas'))
    else:
        r = requests.get(f"{API_PECAS}/{pid}")
        if r.ok:
            return render_template('editar_peca.html', peca=r.json())
        flash('Peça não encontrada', 'warning')
        return redirect(url_for('pecas'))

@app.route('/pecas/excluir/<int:pid>')
def excluir_peca(pid):
    r = requests.delete(f"{API_PECAS}/{pid}")
    if r.ok:
        flash('Peça removida', 'success')
    else:
        flash(r.json().get('detail', 'Erro ao remover'), 'danger')
    return redirect(url_for('pecas'))

# ----- Servicos -----
@app.route('/servicos')
def servicos():
    resp = requests.get(f"{API_SERVICOS}/")
    lista = resp.json() if resp.ok else []
    return render_template('servicos.html', servicos=lista)

@app.route('/servicos/cadastro', methods=['GET', 'POST'])
def cadastrar_servico():
    if request.method == 'POST':
        data = {
            'nome': request.form['nome'],
            'preco': float(request.form['preco'])
        }
        r = requests.post(f"{API_SERVICOS}/", json=data)
        if r.status_code == 201:
            flash('Serviço cadastrado!', 'success')
            return redirect(url_for('servicos'))
        else:
            flash(r.json().get('detail', 'Erro ao cadastrar serviço'), 'danger')
    return render_template('cadastro_servico.html')

@app.route('/servicos/editar/<int:sid>', methods=['GET', 'POST'])
def editar_servico(sid):
    if request.method == 'POST':
        data = {
            'nome': request.form['nome'],
            'preco': float(request.form['preco'])
        }
        payload = {k: v for k, v in data.items() if str(v).strip() != ''}
        r = requests.patch(f"{API_SERVICOS}/{sid}", json=payload)
        if r.ok:
            flash('Serviço atualizado', 'success')
        else:
            flash(r.json().get('detail', 'Erro ao atualizar'), 'danger')
        return redirect(url_for('servicos'))
    else:
        r = requests.get(f"{API_SERVICOS}/{sid}")
        if r.ok:
            return render_template('editar_servico.html', servico=r.json())
        flash('Serviço não encontrado', 'warning')
        return redirect(url_for('servicos'))

@app.route('/servicos/excluir/<int:sid>')
def excluir_servico(sid):
    r = requests.delete(f"{API_SERVICOS}/{sid}")
    if r.ok:
        flash('Serviço removido', 'success')
    else:
        flash(r.json().get('detail', 'Erro ao remover'), 'danger')
    return redirect(url_for('servicos'))

@app.route('/reset')
def reset():
    r = requests.delete("http://backend:8000/api/v1/reset")
    if r.ok:
        flash('Banco restaurado', 'info')
    else:
        flash('Erro ao resetar banco', 'danger')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port=3000, host='0.0.0.0')