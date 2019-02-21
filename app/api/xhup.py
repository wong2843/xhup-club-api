# -*- coding: utf-8 -*-
import logging

from flask.views import MethodView
import marshmallow as ma
from flask_rest_api import abort, Blueprint

from app import api_rest, current_config
from app.api import api_prefix
from app.service.auth import qq_group
from app.service.xhup.characters import save_split_table, get_info
from app.utils.common import login_required

logger = logging.getLogger(__name__)

xhup_bp = Blueprint(
    'xhup', __name__, url_prefix=f'{api_prefix}/xhup',
    description="小鹤双拼相关的功能"
)


class TableCreateArgsSchema(ma.Schema):
    """请求应该带有的参数

    """
    class Meta:
        strict = True
        ordered = True

    version = ma.fields.String()
    table = ma.fields.String()


@api_rest.definition('Char')
class CharSchema(ma.Schema):
    class Meta:
        strict = True
        ordered = True

    char = ma.fields.String()
    info = ma.fields.String()
    version = ma.fields.String()


@xhup_bp.route("/chars")
class CharView(MethodView):
    """小鹤音形 拆字表查询 api"""

    @xhup_bp.arguments(TableCreateArgsSchema)
    @xhup_bp.response(code=201)
    @login_required
    def post(self, data: dict):
        """提交新的拆字表

        只允许 QQ群`小鹤双拼输入法`的管理员访问此 api
        必须要带版号，而且版号必须比之前的高。
        ---
        :return None
        """
        if not qq_group.is_admin(current_config.XHUP_GROUP_ID):
            abort(401, "you are not the admin of qq group '小鹤双拼输入法'")

        try:
            save_split_table(data['table'], data['version'])
        except RuntimeError as e:
            abort(400, e.args)

    @xhup_bp.arguments(CharSchema)
    @xhup_bp.response(CharSchema, code=200, description="成功获取到 char 的 info")
    def get(self, data: dict):
        """查字，这个是最常用的方法

        默认使用最新的拆字表
        """
        char = data['char']
        info = get_info(char)
        if not info:
            abort(404, f"no info for character {char}")

        return {
            "info": info
        }
