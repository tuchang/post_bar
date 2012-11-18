# -- coding: utf8 --
__metaclass__ = type
import web
session = web.config._session
from config.config import *
from models.node_model import *
from models.cat_model import *
from models.post_model import *
from models.user_model import *
from models.comment_model import *
from libraries.crumb import Crumb

class admin:
    def __init__(self):
        if session.user_id != 1:
            raise web.SeeOther('/')

class index(admin):
    
    crumb = Crumb()
    
    def GET(self):
        
        cat_result = cat_model().get_all()
        cats = []
        for cat in cat_result:
            node_total = node_model().count_table({'category_id':cat.id})
            cats.append({'cat':cat, 'node_total':node_total})
        self.crumb.append('后台')
        return admin_render.index('后台', cats, self.crumb.output())

class cat(admin):
    
    crumb = Crumb()
    form = cat_model().form

    def GET(self, cat_name):
        cat = cat_model().get_one({'name':cat_name})
        if cat is None:
            self.crumb.append('分类不存在')
            return admin_render.index('分类不存在', self.crumb.output())
        else:
            self.crumb.append('/admin', '后台')
            nodes = node_model().get_all({'category_id':cat.id})
            return admin_render.cat_view(cat.display_name, self.crumb.output(), cat, self.form, nodes)

    def POST(self, cat_name):
