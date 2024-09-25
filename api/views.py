# api/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.utils.system_comp import get_system_composition
from api.utils.pinecone import retrieve_from_pinecone

@api_view(['POST'])
def search_view(request):
    query = request.data.get('query', '')
    if not query:
        return Response({'error': 'No query provided'}, status=400)
    
    system_compositions = get_system_composition(query)
    search_results = retrieve_from_pinecone(system_compositions)

    '''
    with open('debug.txt', 'w') as f:
        f.write(str(search_results))
    '''

    response_data = {
        'search_query': query,
        'system_compositions': system_compositions,
        'search_results': search_results,
    }

    return Response(response_data)
