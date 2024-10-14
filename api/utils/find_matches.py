from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F

tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

def calculate_similarity(sentence1, sentence2):
    def mean_pooling(model_output, attention_mask):
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def cosine_similarity(emb1, emb2):
        return F.cosine_similarity(emb1, emb2, dim=1)
    
    encoded_input = tokenizer([sentence1, sentence2], padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**encoded_input)

    sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
    sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)
    similarity_score = cosine_similarity(sentence_embeddings[0].unsqueeze(0), sentence_embeddings[1].unsqueeze(0))

    return similarity_score.item()

def find_match_composition(system_compositions, search_results, similarity_threshold=0.4):
    final_results = []
    
    for result in search_results:
        matches = []  
        used_components = set()  

        for system_component in system_compositions:
            best_match = ""
            best_similarity = 0
            
            for component in result['metadata']['all_system_components']:
                if component in used_components:
                    continue  
                
                similarity = calculate_similarity(system_component, component)
                if similarity > best_similarity and similarity >= similarity_threshold:
                    best_similarity = similarity
                    best_match = component

            if best_match:
                used_components.add(best_match)
            
            matches.append(best_match if best_match else "")
        final_results.append(matches)
    
    return final_results


def find_match_description(pic_list, patent_list, similarity_threshold=0.4):
    matches = {}
    used_items = set()  
    
    if len(pic_list) <= len(patent_list):
        shorter_list = pic_list
        longer_list = patent_list
        is_pic_shorter = True  
    else:
        shorter_list = patent_list
        longer_list = pic_list
        is_pic_shorter = False

    while len(shorter_list) < len(longer_list):
        shorter_list.append("")  
    
    for short_item in shorter_list:
        best_match = ""
        best_similarity = 0
        
        for long_item in longer_list:
            if long_item in used_items:
                continue 
            
            similarity = calculate_similarity(short_item, long_item)
            
            if similarity > best_similarity and similarity >= similarity_threshold:
                best_similarity = similarity
                best_match = long_item

        if best_match:
            matches[short_item] = best_match
            used_items.add(best_match)  
        else:
            matches[short_item] = ""  
    
    if is_pic_shorter:
        pic_list = shorter_list
    else:
        patent_list = shorter_list
    
    return pic_list, patent_list