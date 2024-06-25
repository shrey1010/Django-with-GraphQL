import graphene
from graphene_django import DjangoObjectType
from graphql_api import models

class User(DjangoObjectType):
    class Meta:
        model = models.User
        
class Post(DjangoObjectType):
    class Meta:
        model = models.Post
        
class UserInput(graphene.InputObjectType):
    name = graphene.string()
    
class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)
        
    ok = graphene.BooleanField()
    user = graphene.Field(User)
    
    @staticmethod
    def mutate(root,info,input):
        instance = models.User.objects.get(name=input.name)
        
        try:
            instance.followers.set([])
            instance.save()
        except:
            CreateUser(ok=False,user = None)
        
class PostInput(graphene.InputObjectType):
    content = graphene.String()
    user_id = graphene.Int()
    
class CreatePost(graphene.Mutation):
    class Arguments:
        input = PostInput(required=True)
        
    ok = graphene.Boolean()
    post = graphene.Field(Post)
    
    @staticmethod
    def mutate(root,info,input):
        user = models.User.objects.get(pk=input.user_id)
        if not user :
            return CreatePost(ok=False,user=None)   
        instance = models.Post(conteny = input.content,created_by=input.user_id)
        
        try:
            instance.save()
            CreatePost(ok=True,post=instance)
        except:
            CreatePost(ok=False,user = None)

class Query(graphene.ObjectType):
    user = graphene.Field(User,id=graphene.Int())
    
    def resolve_user(self, info,**kwargs):
        id = kwargs.get("id")
        if id is not None:
            return models.User.objects.get(pk=id)
        return None
    
    def resolve_post(self, info,**kwargs):
        return models.User.objects.all()
    
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_post = CreatePost.Field()
        
    
schema = graphene.Schema(query=Query,mutation = Mutation)
