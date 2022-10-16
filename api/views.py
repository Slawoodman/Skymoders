from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializer import ModSerializer
from projects.models import Mod, Review

from api import serializer


@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def getRoutes(request):
    routes = [
        {'GET':'api/mods/'},
        {'GET':'api/mods/id'},
        {'POST':'api/mods/id/vote'},

        {'GET':'api/moders/token'},
        {'Post':'api/moders/token/refresh'},

    ]

    return Response(routes)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getMods(request):
    mods = Mod.objects.all()
    serializer = ModSerializer(mods, many=True)
    print('USER:' ,request.user)
    # print(serializer)
    # print(serializer.data)
    return Response(serializer.data)

 
@api_view(['GET'])
def getMod(request, pk):
    mod = Mod.objects.get(id=pk)
    serializer = ModSerializer(mod, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def modVote(request, pk):
    # mod = Mod.objects.get(id=pk)    
    mod = Mod.objects.get(id=pk)
    user = request.user.profile
    data = request.data

    review, created = Review.objects.get_or_create(
        owner=user,
        mod=mod,
    )

    review.value = data['value']
    review.save()
    mod.getVoteCount

    serializer = ModSerializer(mod, many=False)
    return Response(serializer.data)
  
    