# -*- coding: utf-8 -*-
"""users.schema"""

from django.contrib.auth import get_user_model
import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import superuser_required
from graphql_jwt.decorators import login_required


class UserType(DjangoObjectType):

    """UserType"""

    class Meta:
        """Meta"""
        model = get_user_model()
        exclude = ('password',)


class CreateUser(graphene.Mutation):

    """UserType"""

    user = graphene.Field(UserType, token=graphene.String(required=True))

    class Arguments:
        """Arguments"""
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    @superuser_required
    def mutate(self, info, username, password, email, **kwargs):
        """mutate"""
        user = get_user_model()(username=username,
                                email=email,)
        user.set_password(password)
        user.save()
        return CreateUser(user=user)


class Mutation(graphene.ObjectType):

    """Mutation"""

    create_user = CreateUser.Field()


class Query(graphene.ObjectType):

    """Query"""

    users = graphene.List(UserType, token=graphene.String(required=True))
    user = graphene.Field(UserType, token=graphene.String(required=True))

    @superuser_required
    def resolve_users(self, info, **kwargs):
        """Resolve"""
        return get_user_model().objects.all()

    @login_required
    def resolve_user(self, info, **kwargs):
        """Resolve"""
        return info.context.user
