from src.models.model import UnitRequest

class UnitTestGenerationService:
    def get_unit_cases(self, request: UnitRequest):
        """
        Get converted code from azure open ai using llm models

        :param request: Using pydentic model as request
        :return: Text format of code
        """
        request_dict = request.model_dump(mode='dict')
        return {'Unit_test_case_generted': '_'.join(list(request_dict.values()))}