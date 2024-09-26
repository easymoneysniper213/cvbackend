from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.utils.system_comp import get_system_composition
from api.utils.pinecone import retrieve_from_pinecone
from api.utils.process_image import image_summary
from api.utils.process_response import produce_response

@api_view(['POST'])
def search_view(request):
    """
    Handles the search query and returns system compositions and search results.
    """
    query = request.data.get('query', '')
    if not query:
        return Response({'error': 'No query provided'}, status=400)
    
    system_compositions = get_system_composition(query)
    search_results = retrieve_from_pinecone(system_compositions)

    response_data = {
        'search_query': query,
        'system_compositions': system_compositions,
        'search_results': search_results,
    }

    return Response(response_data)


@api_view(['POST'])
def details_comparison(request):
    """
    Handles the submission of detailed data from the DetailsPage, such as Patent ID,
    system components, independent claims, and images, and processes/stores this information.
    """
    patent_id = request.data.get('patent_id')
    system_components = request.data.get('system_components')
    system_indp_claims_val = request.data.get('system_indp_claims_val')
    images = request.data.get('images')

    if not patent_id or not system_components or not system_indp_claims_val:
        return Response({'error': 'Missing required fields'}, status=400)

    print(images)
    img_sum = ''
    if images != []:
        img_sum = image_summary(images[0], system_components)

    response = produce_response(patent_id, img_sum, system_indp_claims_val)
    return Response({'status': 'success', 'response': response})
