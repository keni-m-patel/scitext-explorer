class VectorSpaceModels(object):
    def __init__(self,config):
        pass
    
    def bag_of_words(documents):

        new_dict = {}
        for i in documents:
            if i in new_dict:
                new_dict[i] += 1
            else:
                new_dict[i] = 1
        return new_dict
        
