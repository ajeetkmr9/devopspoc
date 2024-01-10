from src.models.proxy_model import ProxyRequest


class ProxyService:

    def get_converted_code(self, request: ProxyRequest):
        """
        Get converted code from azure open ai using llm models

        :param request: Using pydentic model as request
        :return: Text format of code
        """
        request_dict = request.model_dump(mode='dict')
        return {'converted_code':'_'.join(list(request_dict.values()))}
        
