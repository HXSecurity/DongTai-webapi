######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : github_contributors
# @created     : Thursday Sep 16, 2021 15:34:42 CST
#
# @description :
######################################################################



from dongtai.endpoint import R, AnonymousAndUserEndPoint
from iast.github_contributors import get_github_contributors

class GithubContributorsView(AnonymousAndUserEndPoint):
    def get(self, request):
        dic, expired = get_github_contributors()
        return R.success(data=dic)
