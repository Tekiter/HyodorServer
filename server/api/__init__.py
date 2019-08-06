
from . import login, board

def load_api(api, base):
    
    api.add_resource(login.LoginDebug, base + '/login-debug', endpoint="logindebug")

    api.add_resource(board.BoardManage, base + '/board', endpoint="boardmanage")
    api.add_resource(board.BoardPostList, base + '/board/<int:board_id>', endpoint="boardpostlist")
    api.add_resource(board.BoardPostView, base + '/board/post/<int:post_id>', endpoint="boardpost")
    api.add_resource(board.BoardComment, base + '/board/comment', endpoint="boardcomment")


    api.add_resource(login.Login, base + '/login', endpoint="login")
    api.add_resource(login.LoginRefresh, base + '/login-refresh', endpoint="loginrefresh")
    


