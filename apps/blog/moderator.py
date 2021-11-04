from moderation import moderation
from moderation.moderator import GenericModerator

from apps.blog.models import Post


# Add your moderator settings for AnotherModel here
# class PostModerator(GenericModerator):
#     pass


moderation.register(Post)  # Uses default moderation settings
# moderation.register(Post, PostModerator)  # Uses custom moderation settings
