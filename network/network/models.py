from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# Representa uma postagem feita por um usuário, contendo o conteúdo, o autor e a data de criação.
class Post(models.Model):
    content = models.CharField(max_length=191)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post {self.id} made by {self.user} on {self.date.strftime('%d %b %Y %H:%M:%S')}"

# Representa os seguidores
class Follow(models.Model):
    user = models.ForeignKey(User, related_name="seguido", on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name="seguindo", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.follower} segue {self.user}"

# Para Curtir e Descurtir Posts
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

class Meta:
    unique_together = ('user', 'post')