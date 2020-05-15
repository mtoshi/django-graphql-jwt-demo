# -*- coding: utf-8 -*-
"""users.schema"""

from django.contrib.auth import get_user_model
import graphene
from graphene_django.types import DjangoObjectType


class UserType(DjangoObjectType):

    """UserType"""

    class Meta:
        """Meta"""
        model = get_user_model()


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
