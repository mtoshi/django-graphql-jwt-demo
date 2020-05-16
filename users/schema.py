# -*- coding: utf-8 -*-
"""users.schema"""

from django.contrib.auth import get_user_model
import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required


class UserType(DjangoObjectType):

    """UserType"""

    class Meta:
        """Meta"""
        model = get_user_model()
        exclude = ('password',)


class CreateUser(graphene.Mutation):

    """UserType"""

    user = graphene.Field(UserType)

    class Arguments:
        """Arguments"""
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
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

    users = graphene.List(UserType)

    @login_required
    def resolve_users(self, info):
        """Resolve"""
        return get_user_model().objects.all()