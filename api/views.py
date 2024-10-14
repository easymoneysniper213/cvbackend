from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.utils.system_comp import get_system_composition
from api.utils.pinecone import retrieve_from_pinecone
from api.utils.process_image import image_summary
from api.utils.process_response import produce_response
from api.utils.process_claim import make_system_description
from api.utils.process_claim import make_img_description
from api.utils.find_matches import find_match_composition
from api.utils.find_matches import find_match_description
import time

@api_view(['POST'])
def search_view(request):
    """
    Handles the search query and returns system compositions and search results.
    """
    start_time = time.time()

    query = request.data.get('query', '')
    if not query:
        return Response({'error': 'No query provided'}, status=400)
    
    system_compositions = get_system_composition(query)
    search_results = retrieve_from_pinecone(system_compositions)
    match_results = find_match_composition(system_compositions, search_results)

    execution_time = time.time() - start_time

    response_data = {
        'match_results': match_results,
        'search_query': query,
        'system_compositions': system_compositions,
        'search_results': search_results,
        'exec_time': execution_time
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
    my_system_components = request.data.get('my_system_components')
    pic = request.data.get('pic')

    if not patent_id or not system_components or not system_indp_claims_val:
        return Response({'error': 'Missing required fields'}, status=400)
    
    pic_list = make_system_description(system_indp_claims_val, pic)
    img_sum = ''
    if images != []:
        img_sum = image_summary(images[0], system_components)
    patent_list = make_img_description(system_components, img_sum)
    new_pic_list, new_patent_list = find_match_description(pic_list, patent_list)

    response = produce_response(patent_id, pic_list, patent_list, my_system_components, system_components, system_indp_claims_val)

    return Response({
        'status': 'success', 
        'response': response, 
        'patent_sum': patent_list, 
        'pic_sum': pic_list,
        'patent_sum_2': new_patent_list,
        'pic_sum_2': new_pic_list
    })

