import graphene
from graphene_django import DjangoObjectType

from apps.incomes.models import Income


class IncomeType(DjangoObjectType):
    class Meta:
        model = Income
        fields = ("id", "amount", "description", "user")


# noinspection PyArgumentList
# noinspection PyUnusedLocal
class IncomeMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        amount = graphene.Float()
        description = graphene.String()

    income = graphene.Field(IncomeType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        pk = kwargs.pop("id")
        income = Income.objects.get(pk=pk)
        income.amount = kwargs.get("amount", income.amount)
        income.description = kwargs.get("description", income.description)
        income.save(update_fields=["amount", "description"])

        return IncomeMutation(income=income)


# noinspection PyMethodMayBeStatic
# noinspection PyUnusedLocal
class Query(graphene.ObjectType):
    incomes = graphene.List(IncomeType)

    def resolve_incomes(self, info, **kwargs):
        return Income.objects.select_related("user").all()


class Mutation(graphene.ObjectType):
    update_income = IncomeMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
