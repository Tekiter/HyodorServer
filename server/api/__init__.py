
from . import login, board, schedule, admin

def load_api(api, base):
    
    api.add_resource(login.LoginDebug, base + '/login-debug', endpoint="logindebug")

    api.add_resource(board.BoardManage, base + '/board', endpoint="boardmanage")
    api.add_resource(board.BoardPostList, base + '/board/<int:board_id>', endpoint="boardpostlist")
    api.add_resource(board.BoardPostView, base + '/board/post/<int:post_id>', endpoint="boardpost")
    api.add_resource(board.BoardComment, base + '/board/comment', endpoint="boardcomment")
    api.add_resource(board.BoardCommentAction, base + '/board/comment/<int:comment_id>', endpoint="boardcommentaction")


    api.add_resource(login.Login, base + '/login', endpoint="login")
    api.add_resource(login.LoginRefresh, base + '/login-refresh', endpoint="loginrefresh")


    api.add_resource(schedule.ScheduleAPI, base + '/schedule', endpoint="schedule")
    api.add_resource(schedule.SchedulePointAPI, base + '/schedule/<int:schedule_id>', endpoint="schedulepoint")

    api.add_resource(admin.AdminManage, base + '/admin', endpoint="adminmanage")
    api.add_resource(admin.UserManageList, base + '/admin/user', endpoint="adminuserlist")
    api.add_resource(admin.UserManage, base + '/admin/user/<string:username>', endpoint="adminusermanage")
    


