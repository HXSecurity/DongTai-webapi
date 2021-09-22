######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : github_contributors
# @created     : Thursday Sep 16, 2021 15:34:42 CST
#
# @description :
######################################################################

from dongtai.endpoint import R, AnonymousAndUserEndPoint
from iast.github_contributors import get_github_contributors
import threading
import asyncio
from functools import partial
import os

if os.getenv('environment', None) in ('PROD', ):

    async def delay(time):
        await asyncio.sleep(time)

    async def timer(time, function):
        while True:
            future = asyncio.ensure_future(delay(time))
            future.add_done_callback(function)
            await future

    _update = partial(get_github_contributors, update=True)

    def corotheard():
        _update()
        asyncio.run(timer(60 * 90, _update))

    t1 = threading.Thread(target=corotheard, daemon=True)
    t1.start()


class GithubContributorsView(AnonymousAndUserEndPoint):
    def get(self, request):
        dic = get_github_contributors()
        return R.success(data=dic)
