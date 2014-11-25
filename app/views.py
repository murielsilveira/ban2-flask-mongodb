from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from app.models import Filme
from flask.ext.mongoengine.wtf import model_form
from mongoengine import Q


filmes = Blueprint('filmes', __name__, template_folder='templates')


class FilmeListView(MethodView):

    def get_context(self):
        busca = request.args.get('busca', '')
        if busca:
            filmes = Filme.objects(Q(titulo__icontains=busca) | Q(diretor__icontains=busca) | Q(categoria__icontains=busca))
        else:
            filmes = Filme.objects.all()

        context = {
            "filmes": filmes,
            "busca": busca
        }
        return context

    def get(self):
        context = self.get_context()
        return render_template('filmes/list.html', **context)


class FilmeDetailView(MethodView):

    def get_context(self, titulo=None):
        filme = Filme.objects.get_or_404(titulo=titulo)
        context = {
            "filme": filme
        }
        return context

    def get(self, titulo):
        context = self.get_context(titulo)
        return render_template('filmes/detail.html', **context)


class FilmeEditView(MethodView):

    def get_context(self, titulo=None):
        form_cls = model_form(Filme, exclude=('created_at',))

        if titulo:
            filme = Filme.objects.get_or_404(titulo=titulo)
            if request.method == 'POST':
                form = form_cls(request.form, inital=filme._data)
            else:
                form = form_cls(obj=filme)
        else:
            filme = Filme()
            form = form_cls(request.form)

        context = {
            "filme": filme,
            "form": form,
            "create": titulo is None
        }
        return context

    def get(self, titulo):
        context = self.get_context(titulo)
        return render_template('filmes/edit.html', **context)

    def post(self, titulo):
        context = self.get_context(titulo)
        form = context.get('form')

        if form.validate():
            filme = context.get('filme')

            form.populate_obj(filme)
            filme.save()

            return redirect(url_for('filmes.list'))
        return render_template('filmes/edit.html', **context)


# Registrar URLs
filmes.add_url_rule('/', view_func=FilmeListView.as_view('list'))
filmes.add_url_rule('/criar/', view_func=FilmeEditView.as_view('create'), defaults={'titulo': None})
filmes.add_url_rule('/<titulo>/', view_func=FilmeDetailView.as_view('detail'))
filmes.add_url_rule('/<titulo>/editar/', view_func=FilmeEditView.as_view('edit'))
