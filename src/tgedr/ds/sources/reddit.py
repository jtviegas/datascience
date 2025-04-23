from datetime import datetime, timezone
from typing import Any, Dict, Optional

from praw import Reddit

from tgedr.ds.sources.source import Source


class RedditSrc(Source):
    """source implementing class retrieving posts from reddit"""

    __USER_AGENT = "tgedr:datascience by u/USER"
    ENVVAR_API_CLIENTID = "API_CLIENTID"
    ENVVAR_API_SECRET = "API_SECRET"
    CONTEXT_USER = "REDDIT_USER"
    CONTEXT_PSWD = "REDDIT_PSWD"
    CONTEXT_QUERY = "QUERY_STRING"
    CONTEXT_SORT = "QUERY_SORT"
    CONTEXT_FILTER = "QUERY_FILTER"
    CONTEXT_TEXT = "RETRIEVE_TEXT"
    __DEFAULT_SORT = "new"
    __DEFAULT_FILTER = "month"

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self._client_id = self._get_param(self.ENVVAR_API_CLIENTID, config)
        self._client_secret = self._get_param(self.ENVVAR_API_SECRET, config)

    def _format_submission(self, submission, context) -> dict:
        result = {
            "title": submission.title,
            "created": datetime.fromtimestamp(
                submission.created_utc, tz=timezone.utc
            ).strftime("%Y-%m-%d %H:%M:%S"),
            "url": submission.url,
        }
        if "true" == context.get(self.CONTEXT_TEXT):
            result["text"] = submission.selftext

        return result

    def get(self, context: Optional[Dict[str, Any]] = None) -> Any:
        user = self._get_param(self.CONTEXT_USER, context)
        pswd = self._get_param(self.CONTEXT_PSWD, context)
        query_string = self._get_param(self.CONTEXT_QUERY, context)

        sort = self._get_param(
            self.CONTEXT_SORT, map=context, default=self.__DEFAULT_SORT
        )
        filter = self._get_param(
            self.CONTEXT_FILTER, map=context, default=self.__DEFAULT_FILTER
        )

        reddit = Reddit(
            client_id=self._client_id,
            client_secret=self._client_secret,
            password=pswd,
            user_agent=self.__USER_AGENT,
            username=user,
        )

        result = []
        submissions = reddit.subreddit("all").search(
            query_string, sort=sort, time_filter=filter
        )
        for submission in submissions:
            if submission.is_self:
                result.append(
                    self._format_submission(submission=submission, context=context)
                )

        return result
