from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe

from recipe import serializers

# This is the original before refactor
#
# class TagViewSet(viewsets.GenericViewSet,
#                  mixins.ListModelMixin,
#                  mixins.CreateModelMixin):
#     """Manage tags in the database"""
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     queryset = Tag.objects.all()
#     serializer_class = serializers.TagSerializer

#     def get_queryset(self):
#         """Return objects for the current authenticated user only
#            i.e. only tags that were created by the requesting user
#         """
#         return self.queryset.filter(user=self.request.user).order_by('-name')

#     def perform_create(self, serializer):
#         """Create a new tag"""
#         # save the data and also setting the user
#         # to the requesting user
#         serializer.save(user=self.request.user)


# class IngredientViewSet(viewsets.GenericViewSet,
#                         mixins.ListModelMixin,
#                         mixins.CreateModelMixin):
#     """Manage ingredients in the database"""
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     queryset = Ingredient.objects.all()
#     serializer_class = serializers.IngredientSerializer

#     def get_queryset(self):
#         """Return objects for the current authenticated user only"""
#         return self.queryset.filter(user=self.request.user).order_by('-name')

#     def perform_create(self, serializer):
#         """Create a new ingredient"""
#         serializer.save(user=self.request.user)

# After refactoring with base class
class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """Base viewset for user owned recipe attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for current user"""
        # convert the query param string into bool
        assigned_only = bool(
            # ,0 is the default value if undefined
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            # tags/ingredients that are not assigned to recipe
            # will have the recipe field null
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()

    def perform_create(self, serializer):
        """Create a new ingredient"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    
    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve the recipes for the authenticated user"""
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            # tags__id__in is django way to query in foreign table
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """
            Return appropriate serializer class
            ModelViewSet has list() and retrieve()
            in case of retrieve(), we want the serializer
            to be the one that provides detail
            retrieve is getting one object only
            e.g. /api/recipe/recipes/1
            list is getting all the recipes
            e.g. /api/recipe/recipes
        """
        # action is the name of the function
        # that gets called by the endpoint
        # this one is the default from mixin
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        # our custom action upload_image (see below)
        elif self.action == "upload_image":
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)

    # the action decorator is to add custom endpoint
    # detail=True means we can only do this for the detail url
    # url_path is the path appended at end
    # i.e. /api/recipe/recipes/1/upload-image
    # (since detail=True, we can only upload image to existing recipe)
    @action(methods=['POST'], detail=True, url_path='upload-image')
    # pk is primary key that get passed in to the view
    def upload_image(self, request, pk=None):
        """Upload an image to a recipe"""
        # will get the object based on the id in the url
        recipe = self.get_object()
        # self.get_serializer will call the
        # get_serializer_class method (see above)
        # we use this self.get_serializer instead of specifying
        # the RecipeImageSerializer directly because
        # 1. it is best practice
        # 2. we get the built in function to upload in browseable api
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
